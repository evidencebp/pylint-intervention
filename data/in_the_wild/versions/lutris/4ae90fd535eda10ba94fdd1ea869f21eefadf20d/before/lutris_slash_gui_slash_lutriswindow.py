"""Main window for the Lutris interface."""
import os
from collections import namedtuple
from gettext import gettext as _

from gi.repository import Gdk, Gio, GLib, GObject, Gtk

from lutris import services, settings
from lutris.database import categories as categories_db
from lutris.database import games as games_db
from lutris.database.services import ServiceGameCollection
from lutris.game import Game
from lutris.game_actions import GameActions
from lutris.gui import dialogs
from lutris.gui.addgameswindow import AddGamesWindow
from lutris.gui.config.preferences_dialog import PreferencesDialog
from lutris.gui.views import COL_ID, COL_NAME
from lutris.gui.views.grid import GameGridView
from lutris.gui.views.list import GameListView
from lutris.gui.views.store import GameStore
from lutris.gui.widgets.contextual_menu import ContextualMenu
from lutris.gui.widgets.game_bar import GameBar
from lutris.gui.widgets.gi_composites import GtkTemplate
from lutris.gui.widgets.sidebar import LutrisSidebar
from lutris.gui.widgets.utils import load_icon_theme, open_uri
# pylint: disable=no-member
from lutris.services.base import BaseService
from lutris.services.lutris import LutrisService
from lutris.util import datapath
from lutris.util.jobs import AsyncCall
from lutris.util.log import logger
from lutris.util.system import update_desktop_icons


@GtkTemplate(ui=os.path.join(datapath.get(), "ui", "lutris-window.ui"))
class LutrisWindow(Gtk.ApplicationWindow):  # pylint: disable=too-many-public-methods
    """Handler class for main window signals."""

    default_view_type = "grid"
    default_width = 800
    default_height = 600

    __gtype_name__ = "LutrisWindow"
    __gsignals__ = {
        "view-updated": (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    games_scrollwindow = GtkTemplate.Child()
    sidebar_revealer = GtkTemplate.Child()
    sidebar_scrolled = GtkTemplate.Child()
    game_revealer = GtkTemplate.Child()
    search_entry = GtkTemplate.Child()
    zoom_adjustment = GtkTemplate.Child()
    blank_overlay = GtkTemplate.Child()
    viewtype_icon = GtkTemplate.Child()

    def __init__(self, application, **kwargs):
        width = int(settings.read_setting("width") or self.default_width)
        height = int(settings.read_setting("height") or self.default_height)
        super().__init__(
            default_width=width,
            default_height=height,
            window_position=Gtk.WindowPosition.NONE,
            name="lutris",
            icon_name="lutris",
            application=application,
            **kwargs
        )
        update_desktop_icons()
        load_icon_theme()
        self.application = application
        self.window_x = settings.read_setting("window_x")
        self.window_y = settings.read_setting("window_y")
        if self.window_x and self.window_y:
            self.move(int(self.window_x), int(self.window_y))
        self.threads_stoppers = []
        self.window_size = (width, height)
        self.maximized = settings.read_setting("maximized") == "True"
        self.service = None
        self.game_actions = GameActions(application=application, window=self)
        self.search_timer_id = None
        self.selected_category = settings.read_setting("selected_category", default="runner:all")
        self.filters = self.load_filters()
        self.set_service(self.filters.get("service"))
        self.icon_type = self.load_icon_type()
        self.game_store = GameStore(self.service, self.service_media)
        self.view = Gtk.Box()

        self.connect("delete-event", self.on_window_delete)
        self.connect("configure-event", self.on_window_configure)
        self.connect("realize", self.on_load)
        if self.maximized:
            self.maximize()

        self.init_template()
        self._init_actions()

        self.set_dark_theme()

        self.set_viewtype_icon(self.view_type)

        lutris_icon = Gtk.Image.new_from_icon_name("lutris", Gtk.IconSize.MENU)
        lutris_icon.set_margin_right(3)

        self.sidebar = LutrisSidebar(self.application, selected=self.selected_category)
        self.sidebar.connect("selected-rows-changed", self.on_sidebar_changed)
        # "realize" is order sensitive- must connect after sidebar itself connects the same signal
        self.sidebar.connect("realize", self.on_sidebar_realize)
        self.sidebar_scrolled.add(self.sidebar)

        # This must wait until the selected-rows-changed signal is connected
        self.sidebar.initialize_rows()

        self.sidebar_revealer.set_reveal_child(self.side_panel_visible)
        self.sidebar_revealer.set_transition_duration(300)

        self.game_bar = None
        self.revealer_box = Gtk.HBox(visible=True)
        self.game_revealer.add(self.revealer_box)

        self.connect("view-updated", self.update_store)
        GObject.add_emission_hook(BaseService, "service-login", self.on_service_login)
        GObject.add_emission_hook(BaseService, "service-logout", self.on_service_logout)
        GObject.add_emission_hook(BaseService, "service-games-loaded", self.on_service_games_updated)
        GObject.add_emission_hook(Game, "game-updated", self.on_game_updated)
        GObject.add_emission_hook(Game, "game-stopped", self.on_game_stopped)
        GObject.add_emission_hook(Game, "game-removed", self.on_game_collection_changed)

    def _init_actions(self):
        Action = namedtuple("Action", ("callback", "type", "enabled", "default", "accel"))
        Action.__new__.__defaults__ = (None, None, True, None, None)

        actions = {
            "add-game": Action(self.on_add_game_button_clicked),
            "preferences": Action(self.on_preferences_activate),
            "about": Action(self.on_about_clicked),
            "show-installed-only": Action(  # delete?
                self.on_show_installed_state_change,
                type="b",
                default=self.filter_installed,
                accel="<Primary>h",
            ),
            "toggle-viewtype": Action(self.on_toggle_viewtype),
            "icon-type": Action(self.on_icontype_state_change, type="s", default=self.icon_type),
            "view-sorting": Action(self.on_view_sorting_state_change, type="s", default=self.view_sorting),
            "view-sorting-ascending": Action(
                self.on_view_sorting_direction_change,
                type="b",
                default=self.view_sorting_ascending,
            ),
            "show-side-panel": Action(
                self.on_side_panel_state_change,
                type="b",
                default=self.side_panel_visible,
                accel="F9",
            ),
            "show-hidden-games": Action(
                self.hidden_state_change,
                type="b",
                default=self.show_hidden_games,
            ),
            "open-forums": Action(lambda *x: open_uri("https://forums.lutris.net/")),
            "open-discord": Action(lambda *x: open_uri("https://discord.gg/Pnt5CuY")),
            "donate": Action(lambda *x: open_uri("https://lutris.net/donate")),
        }

        self.actions = {}
        app = self.props.application
        for name, value in actions.items():
            if not value.type:
                action = Gio.SimpleAction.new(name)
                action.connect("activate", value.callback)
            else:
                default_value = None
                param_type = None
                if value.default is not None:
                    default_value = GLib.Variant(value.type, value.default)
                if value.type != "b":
                    param_type = default_value.get_type()
                action = Gio.SimpleAction.new_stateful(name, param_type, default_value)
                action.connect("change-state", value.callback)
            self.actions[name] = action
            if value.enabled is False:
                action.props.enabled = False
            self.add_action(action)
            if value.accel:
                app.add_accelerator(value.accel, "win." + name)

    @property
    def service_media(self):
        return self.get_service_media(self.load_icon_type())

    def on_load(self, widget, data=None):
        """Finish initializing the view"""
        self._bind_zoom_adjustment()
        self.view.grab_focus()
        self.view.contextual_menu = ContextualMenu(self.game_actions.get_game_actions())

    def on_sidebar_realize(self, widget, data=None):
        """Grab the initial focus after the sidebar is initialized - so the view is ready."""
        self.view.grab_focus()

    def load_filters(self):
        """Load the initial filters when creating the view"""
        category, value = self.selected_category.split(":")
        filters = {
            category: value
        }  # Type of filter corresponding to the selected sidebar element
        filters["hidden"] = settings.read_setting("show_hidden_games").lower() == "true"
        filters["installed"] = settings.read_setting("filter_installed").lower() == "true"
        return filters

    def hidden_state_change(self, action, value):
        """Hides or shows the hidden games"""
        action.set_state(value)
        settings.write_setting("show_hidden_games", str(value).lower(), section="lutris")
        self.filters["hidden"] = value
        self.emit("view-updated")

    @property
    def current_view_type(self):
        """Returns which kind of view is currently presented (grid or list)"""
        return settings.read_setting("view_type") or "grid"

    @property
    def filter_installed(self):
        return settings.read_setting("filter_installed").lower() == "true"

    @property
    def side_panel_visible(self):
        return settings.read_setting("side_panel_visible").lower() != "false"

    @property
    def show_tray_icon(self):
        """Setting to hide or show status icon"""
        return settings.read_setting("show_tray_icon", default="false").lower() == "true"

    @property
    def view_sorting(self):
        value = settings.read_setting("view_sorting") or "name"
        if value.endswith("_text"):
            value = value[:-5]
        return value

    @property
    def view_sorting_ascending(self):
        return settings.read_setting("view_sorting_ascending").lower() != "false"

    @property
    def show_hidden_games(self):
        return settings.read_setting("show_hidden_games").lower() == "true"

    @property
    def sort_params(self):
        _sort_params = [("installed", "COLLATE NOCASE DESC")]
        _sort_params.append((
            self.view_sorting,
            "COLLATE NOCASE ASC"
            if self.view_sorting_ascending
            else "COLLATE NOCASE DESC"
        ))
        return _sort_params

    def get_running_games(self):
        """Return a list of currently running games"""
        return games_db.get_games_by_ids([game.id for game in self.application.running_games])

    def get_recent_games(self):
        """Return a list of currently running games"""
        searches, _filters, excludes = self.get_sql_filters()
        games = games_db.get_games(searches=searches, filters={'installed': '1'}, excludes=excludes)
        return sorted(
            games,
            key=lambda game: max(game["installed_at"] or 0, game["lastplayed"] or 0),
            reverse=True
        )

    def game_matches(self, game):
        if self.filters.get("installed"):
            if game["appid"] not in games_db.get_service_games(self.service.id):
                return False
        if not self.filters.get("text"):
            return True
        return self.filters["text"] in game["name"].lower()

    def set_service(self, service_name):
        if self.service and self.service.id == service_name:
            return self.service
        if not service_name:
            self.service = None
            return
        try:
            self.service = services.SERVICES[service_name]()
        except KeyError:
            logger.error("Non existent service '%s'", service_name)
            self.service = None
        return self.service

    @staticmethod
    def combine_games(service_game, lutris_game):
        """Inject lutris game information into a service game"""
        if lutris_game and service_game["appid"] == lutris_game["service_id"]:
            for field in ("platform", "runner", "year", "installed_at", "lastplayed", "playtime", "installed"):
                service_game[field] = lutris_game[field]
        return service_game

    def get_service_games(self, service_name):
        """Switch the current service to service_name and return games if available"""
        service_games = ServiceGameCollection.get_for_service(service_name)
        if service_name == "lutris":
            lutris_games = {g["slug"]: g for g in games_db.get_games()}
        else:
            lutris_games = {g["service_id"]: g for g in games_db.get_games(filters={"service": self.service.id})}

        def get_sort_value(game):
            sort_defaults = {
                "name": "",
                "year": 0,
                "lastplayed": 0.0,
                "installed_at": 0.0,
                "playtime": 0.0,
            }
            view_sorting = self.view_sorting
            lutris_game = lutris_games.get(game["appid"])
            if not lutris_game:
                return sort_defaults.get(view_sorting, "")
            value = lutris_game.get(view_sorting)
            if value:
                return value
            # Users may have obsolete view_sorting settings, so
            # we must tolerate them. We treat them all as blank.
            return sort_defaults.get(view_sorting, "")

        return [
            self.combine_games(game, lutris_games.get(game["appid"])) for game in sorted(
                service_games,
                key=get_sort_value,
                reverse=not self.view_sorting_ascending
            ) if self.game_matches(game)
        ]

    def get_games_from_filters(self):
        service_name = self.filters.get("service")
        if service_name in services.SERVICES:
            if self.service.online and not self.service.is_authenticated():
                self.show_label(_("Connect your %s account to access your games") % self.service.name)
                return []
            return self.get_service_games(service_name)
        dynamic_categories = {
            "recent": self.get_recent_games,
            "running": self.get_running_games,
        }
        if self.filters.get("dynamic_category") in dynamic_categories:
            return dynamic_categories[self.filters["dynamic_category"]]()
        if self.filters.get("category") and self.filters["category"] != "all":
            game_ids = categories_db.get_game_ids_for_category(self.filters["category"])
        else:
            game_ids = None
        searches, filters, excludes = self.get_sql_filters()
        games = games_db.get_games(
            searches=searches,
            filters=filters,
            excludes=excludes,
            sorts=self.sort_params
        )
        if game_ids is not None:
            return [game for game in games if game["id"] in game_ids]
        return games

    def get_sql_filters(self):
        """Return the current filters for the view"""
        sql_filters = {}
        sql_excludes = {}
        if self.filters.get("runner"):
            sql_filters["runner"] = self.filters["runner"]
        if self.filters.get("platform"):
            sql_filters["platform"] = self.filters["platform"]
        if self.filters.get("installed"):
            sql_filters["installed"] = "1"
        if self.filters.get("text"):
            searches = {"name": self.filters["text"]}
        else:
            searches = None
        if not self.filters.get("hidden"):
            sql_excludes["hidden"] = 1
        return searches, sql_filters, sql_excludes

    def get_service_media(self, icon_type):
        """Return the ServiceMedia class used for this view"""
        service = self.service if self.service else LutrisService
        medias = service.medias
        if icon_type in medias:
            return medias[icon_type]()
        return medias[service.default_format]()

    def update_revealer(self, game=None):
        if game:
            if self.game_bar:
                self.game_bar.destroy()
            self.game_bar = GameBar(game, self.game_actions, self.application)
            self.revealer_box.pack_start(self.game_bar, True, True, 0)
        elif self.game_bar:
            # The game bar can't be destroyed here because the game gets unselected on Wayland
            # whenever the game bar is interacted with. Instead, we keep the current game bar open
            # when the game gets unselected, which is somewhat closer to what the intended behavior
            # should be anyway. Might require closing the game bar manually in some cases.
            pass
            # self.game_bar.destroy()
        if self.revealer_box.get_children():
            self.game_revealer.set_reveal_child(True)
        else:
            self.game_revealer.set_reveal_child(False)

    def show_empty_label(self):
        """Display a label when the view is empty"""
        if self.filters.get("text"):
            self.show_label(_("No games matching '%s' found ") % self.filters["text"])
        else:
            if self.filters.get("category") == "favorite":
                self.show_label(_("Add games to your favorites to see them here."))
            elif self.filters.get("installed"):
                self.show_label(_("No installed games found. Press Ctrl+H so show all games."))
            else:
                self.show_splash()
                # self.show_label(_("No games found"))

    def update_store(self, *_args, **_kwargs):
        self.game_store.store.clear()
        for child in self.blank_overlay.get_children():
            child.destroy()
        games = self.get_games_from_filters()
        logger.debug("Showing %d games", len(games))
        self.view.service = self.service.id if self.service else None
        GLib.idle_add(self.update_revealer)
        for game in games:
            self.game_store.add_game(game)
        if not games:
            self.show_empty_label()
        self.search_timer_id = None
        return False

    def set_dark_theme(self):
        """Enables or disables dark theme"""
        gtksettings = Gtk.Settings.get_default()
        gtksettings.set_property(
            "gtk-application-prefer-dark-theme",
            settings.read_setting("dark_theme", default="false").lower() == "true"
        )

    def _bind_zoom_adjustment(self):
        """Bind the zoom slider to the supported banner sizes"""
        service = self.service if self.service else LutrisService
        media_services = list(service.medias.keys())
        self.load_icon_type()
        self.zoom_adjustment.set_lower(0)
        self.zoom_adjustment.set_upper(len(media_services) - 1)
        if self.icon_type in media_services:
            value = media_services.index(self.icon_type)
        else:
            value = 0
        self.zoom_adjustment.props.value = value
        self.zoom_adjustment.connect("value-changed", self.on_zoom_changed)

    def on_zoom_changed(self, adjustment):
        """Handler for zoom modification"""
        media_index = round(adjustment.props.value)
        adjustment.props.value = media_index
        service = self.service if self.service else LutrisService
        media_services = list(service.medias.keys())
        if len(media_services) <= media_index:
            media_index = media_services.index(service.default_format)
        icon_type = media_services[media_index]
        if icon_type != self.icon_type:
            self.save_icon_type(icon_type)
            self.show_spinner()

    def show_overlay(self, widget):
        """Display a widget in the blank overlay"""
        for child in self.blank_overlay.get_children():
            child.destroy()
        self.blank_overlay.add(widget)
        self.blank_overlay.props.visible = True

    def show_label(self, message):
        """Display a label in the middle of the UI"""
        self.show_overlay(Gtk.Label(message, visible=True))

    def show_splash(self):
        image = Gtk.Image(visible=True)
        image.set_from_file(os.path.join(datapath.get(), "media/splash.svg"))
        self.show_overlay(image)

    def show_spinner(self):
        spinner = Gtk.Spinner(visible=True)
        spinner.start()
        for child in self.blank_overlay.get_children():
            child.destroy()
        self.blank_overlay.add(spinner)
        self.blank_overlay.props.visible = True

    def hide_overlay(self):
        self.blank_overlay.props.visible = False
        for child in self.blank_overlay.get_children():
            child.destroy()

    @property
    def view_type(self):
        """Return the type of view saved by the user"""
        view_type = settings.read_setting("view_type")
        if view_type in ["grid", "list"]:
            return view_type
        return self.default_view_type

    def do_key_press_event(self, event):  # pylint: disable=arguments-differ
        # XXX: This block of code below is to enable searching on type.
        # Enabling this feature steals focus from other entries so it needs
        # some kind of focus detection before enabling library search.

        # Probably not ideal for non-english, but we want to limit
        # which keys actually start searching
        if event.keyval == Gdk.KEY_Escape:
            self.search_entry.set_text("")
            self.view.grab_focus()
            return Gtk.ApplicationWindow.do_key_press_event(self, event)

        if (  # pylint: disable=too-many-boolean-expressions
            not Gdk.KEY_0 <= event.keyval <= Gdk.KEY_z or event.state & Gdk.ModifierType.CONTROL_MASK
            or event.state & Gdk.ModifierType.SHIFT_MASK or event.state & Gdk.ModifierType.META_MASK
            or event.state & Gdk.ModifierType.MOD1_MASK or self.search_entry.has_focus()
        ):
            return Gtk.ApplicationWindow.do_key_press_event(self, event)
        self.search_entry.grab_focus()
        return self.search_entry.do_key_press_event(self.search_entry, event)

    def load_icon_type(self):
        """Return the icon style depending on the type of view."""
        setting_key = "icon_type_%sview" % self.current_view_type
        if self.service and self.service.id != "lutris":
            setting_key += "_%s" % self.service.id
        self.icon_type = settings.read_setting(setting_key)
        return self.icon_type

    def save_icon_type(self, icon_type):
        """Save icon type to settings"""
        self.icon_type = icon_type
        setting_key = "icon_type_%sview" % self.current_view_type
        if self.service and self.service.id != "lutris":
            setting_key += "_%s" % self.service.id
        settings.write_setting(setting_key, self.icon_type)
        self.redraw_view()

    def redraw_view(self):
        """Completely reconstruct the main view"""
        if not self.game_store:
            logger.error("No game store yet")
            return
        if self.view:
            self.view.destroy()
        self.game_store = GameStore(self.service, self.service_media)
        if self.view_type == "grid":
            self.view = GameGridView(
                self.game_store,
                self.game_store.service_media,
                hide_text=settings.read_setting("hide_text_under_icons") == "True"
            )
        else:
            self.view = GameListView(self.game_store, self.game_store.service_media)

        self.view.connect("game-selected", self.on_game_selection_changed)
        self.view.connect("game-activated", self.on_game_activated)
        self.view.contextual_menu = ContextualMenu(self.game_actions.get_game_actions())
        for child in self.games_scrollwindow.get_children():
            child.destroy()
        self.games_scrollwindow.add(self.view)

        self.view.show_all()
        GLib.idle_add(self.update_store)

    def set_viewtype_icon(self, view_type):
        self.viewtype_icon.set_from_icon_name("view-%s-symbolic" % view_type, Gtk.IconSize.BUTTON)

    def set_show_installed_state(self, filter_installed):
        """Shows or hide uninstalled games"""
        settings.write_setting("filter_installed", bool(filter_installed))
        self.filters["installed"] = filter_installed

    def on_service_games_updated(self, service):
        """Request a view update when service games are loaded"""
        if self.service and service.id == self.service.id:
            self.emit("view-updated")
        return True

    def on_service_login(self, service):
        AsyncCall(service.reload, None)
        return True

    def on_service_logout(self, service):
        if self.service and service.id == self.service.id:
            self.emit("view-updated")
        return True

    def on_dark_theme_state_change(self, action, value):
        """Callback for theme switching action"""
        action.set_state(value)
        settings.write_setting("dark_theme", value.get_boolean())
        self.set_dark_theme()

    @GtkTemplate.Callback
    def on_resize(self, widget, *_args):
        """Size-allocate signal.
        Updates stored window size and maximized state.
        """
        if not widget.get_window():
            return
        self.maximized = widget.is_maximized()
        size = widget.get_size()
        if not self.maximized:
            self.window_size = size
        self.search_entry.set_size_request(min(max(50, size[0] - 470), 800), -1)

    def on_window_delete(self, *_args):
        if self.application.running_games.get_n_items():
            self.hide()
            return True

    def on_window_configure(self, *_args):
        """Callback triggered when the window is moved, resized..."""
        self.window_x, self.window_y = self.get_position()

    @GtkTemplate.Callback
    def on_destroy(self, *_args):
        """Signal for window close."""
        # Stop cancellable running threads
        for stopper in self.threads_stoppers:
            stopper()

        # Save settings
        width, height = self.window_size
        settings.write_setting("width", width)
        settings.write_setting("height", height)
        if self.window_x and self.window_y:
            settings.write_setting("window_x", self.window_x)
            settings.write_setting("window_y", self.window_y)
        settings.write_setting("maximized", self.maximized)

    @GtkTemplate.Callback
    def on_preferences_activate(self, *_args):
        """Callback when preferences is activated."""
        self.application.show_window(PreferencesDialog)

    def on_show_installed_state_change(self, action, value):
        """Callback to handle uninstalled game filter switch"""
        action.set_state(value)
        self.set_show_installed_state(value.get_boolean())
        self.emit("view-updated")

    @GtkTemplate.Callback
    def on_search_entry_changed(self, entry):
        """Callback for the search input keypresses"""
        if self.search_timer_id:
            GLib.source_remove(self.search_timer_id)
        self.filters["text"] = entry.get_text().lower().strip()
        self.search_timer_id = GLib.timeout_add(150, self.update_store)

    @GtkTemplate.Callback
    def on_search_entry_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Down:
            if self.current_view_type == 'grid':
                self.view.select_path(Gtk.TreePath('0'))  # needed for gridview only
                # if game_bar is alive at this point it can mess grid item selection up
                # for some unknown reason,
                # it is safe to close it here, it will be reopened automatically.
                if self.game_bar:
                    self.game_bar.destroy()  # for gridview only
            self.view.set_cursor(Gtk.TreePath('0'), None, False)  # needed for both view types
            self.view.grab_focus()

    @GtkTemplate.Callback
    def on_about_clicked(self, *_args):
        """Open the about dialog."""
        dialogs.AboutDialog(parent=self)

    def on_game_error(self, game, error):
        """Called when a game has sent the 'game-error' signal"""
        logger.error("%s crashed", game)
        dialogs.ErrorDialog(error, parent=self)

    @GtkTemplate.Callback
    def on_add_game_button_clicked(self, *_args):
        """Add a new game manually with the AddGameDialog."""
        self.application.show_window(AddGamesWindow)
        return True

    def on_toggle_viewtype(self, *args):
        view_type = "list" if self.current_view_type == "grid" else "grid"
        logger.debug("View type changed to %s", view_type)
        self.set_viewtype_icon(view_type)
        settings.write_setting("view_type", view_type)
        self.redraw_view()
        self._bind_zoom_adjustment()

    def on_icontype_state_change(self, action, value):
        action.set_state(value)
        self._set_icon_type(value.get_string())

    def on_view_sorting_state_change(self, action, value):
        self.actions["view-sorting"].set_state(value)
        value = str(value).strip("'")
        settings.write_setting("view_sorting", value)
        self.emit("view-updated")

    def on_view_sorting_direction_change(self, action, value):
        self.actions["view-sorting-ascending"].set_state(value)
        settings.write_setting("view_sorting_ascending", bool(value))
        self.emit("view-updated")

    def on_side_panel_state_change(self, action, value):
        """Callback to handle side panel toggle"""
        action.set_state(value)
        side_panel_visible = value.get_boolean()
        settings.write_setting("side_panel_visible", bool(side_panel_visible))
        self.sidebar_revealer.set_reveal_child(side_panel_visible)

    def on_sidebar_changed(self, widget):
        """Handler called when the selected element of the sidebar changes"""
        for filter_type in ("category", "dynamic_category", "service", "runner", "platform"):
            if filter_type in self.filters:
                self.filters.pop(filter_type)

        row = widget.get_selected_row()
        if row:
            self.selected_category = "%s:%s" % (row.type, row.id)
            self.filters[row.type] = row.id

        service_name = self.filters.get("service")
        self.set_service(service_name)
        self._bind_zoom_adjustment()
        self.redraw_view()

    def on_game_selection_changed(self, view, selection):
        if not selection:
            GLib.idle_add(self.update_revealer)
            return False
        game_id = view.get_model().get_value(selection, COL_ID)
        if not game_id:
            GLib.idle_add(self.update_revealer)
            return False
        if self.service:
            game = ServiceGameCollection.get_game(self.service.id, game_id)
        else:
            game = games_db.get_game_by_field(int(game_id), "id")
        if not game:
            game = {
                "id": game_id,
                "appid": game_id,
                "name": view.get_model().get_value(selection, COL_NAME),
                "slug": game_id,
                "service": self.service.id if self.service else None,
            }
            logger.warning("No game found. Replacing with placeholder %s", game)

        GLib.idle_add(self.update_revealer, game)
        return False

    def is_game_displayed(self, game):
        """Return whether a game should be displayed on the view"""
        if game.is_hidden and not self.show_hidden_games:
            return False

        # Stopped games do not get displayed on the running page
        if game.state == game.STATE_STOPPED:
            selected_row = self.sidebar.get_selected_row()
            if selected_row and selected_row.id == "running":
                return False
        return True

    def on_game_updated(self, game):
        """Updates an individual entry in the view when a game is updated"""
        if game.appid and self.service:
            db_game = ServiceGameCollection.get_game(self.service.id, game.appid)
        else:
            db_game = games_db.get_game_by_field(game.id, "id")
        if not self.is_game_displayed(game):
            self.game_store.remove_game(db_game["id"])
            return True
        updated = self.game_store.update(db_game)
        if not updated:
            self.update_store()
        return True

    def on_game_stopped(self, game):
        """Updates the game list when a game stops; this keeps the 'running' page updated."""
        selected_row = self.sidebar.get_selected_row()
        # Only update the running page- we lose the selected row when we do this,
        # but on the running page this is okay.
        if selected_row is not None and selected_row.id == "running":
            self.game_store.remove_game(game.id)
        return True

    def on_game_collection_changed(self, _sender):
        """Simple method used to refresh the view"""
        self.emit("view-updated")
        return True

    def on_game_activated(self, view, game_id):
        """Handles view activations (double click, enter press)"""
        if self.service:
            logger.debug("Looking up %s game %s", self.service.id, game_id)
            db_game = games_db.get_game_for_service(self.service.id, game_id)
            if self.service.id == "lutris":
                if not db_game or not db_game["installed"]:
                    self.service.install(game_id)
                    return
                game_id = db_game["id"]
            else:
                if db_game and db_game["installed"]:
                    game_id = db_game["id"]
                else:
                    service_game = ServiceGameCollection.get_game(self.service.id, game_id)
                    if not service_game:
                        logger.error("No game %s found for %s", game_id, self.service.id)
                        return
                    game_id = self.service.install(service_game)
        if game_id:
            game = Game(game_id)
            if game.is_installed:
                game.emit("game-launch")
            else:
                game.emit("game-install")
