"""Main window for the Lutris interface."""
# pylint: disable=no-member
import os
from collections import namedtuple

from gi.repository import Gtk, Gdk, GLib, Gio

from lutris import api, pga, settings
from lutris.game import Game
from lutris.game_actions import GameActions
from lutris.sync import sync_from_remote
from lutris.runtime import RuntimeUpdater

from lutris.util import resources
from lutris.util.log import logger
from lutris.util.jobs import AsyncCall

from lutris.util import http
from lutris.util import datapath
# from lutris.util.steam.watcher import SteamWatcher

from lutris.services import get_services_synced_at_startup, steam

from lutris.vendor.gi_composites import GtkTemplate

from lutris.gui.util import open_uri
from lutris.gui import dialogs
from lutris.gui.sidebar import SidebarListBox
from lutris.gui.widgets.services import SyncServiceWindow
from lutris.gui.runnersdialog import RunnersDialog
from lutris.gui.config.add_game import AddGameDialog
from lutris.gui.config.system import SystemConfigDialog
from lutris.gui.views.list import GameListView
from lutris.gui.views.grid import GameGridView
from lutris.gui.views.menu import ContextualMenu
from lutris.gui.views.store import GameStore
from lutris.gui.widgets.utils import IMAGE_SIZES
from lutris.gui.game_panel import GamePanel


@GtkTemplate(ui=os.path.join(datapath.get(), "ui", "lutris-window.ui"))
class LutrisWindow(Gtk.ApplicationWindow):
    """Handler class for main window signals."""

    default_view_type = "grid"
    default_width = 800
    default_height = 600

    __gtype_name__ = "LutrisWindow"

    main_box = GtkTemplate.Child()
    games_scrollwindow = GtkTemplate.Child()
    sidebar_revealer = GtkTemplate.Child()
    sidebar_scrolled = GtkTemplate.Child()
    connection_label = GtkTemplate.Child()
    search_revealer = GtkTemplate.Child()
    search_entry = GtkTemplate.Child()
    search_toggle = GtkTemplate.Child()
    zoom_adjustment = GtkTemplate.Child()
    no_results_overlay = GtkTemplate.Child()
    connect_button = GtkTemplate.Child()
    disconnect_button = GtkTemplate.Child()
    register_button = GtkTemplate.Child()
    sync_button = GtkTemplate.Child()
    sync_label = GtkTemplate.Child()
    sync_spinner = GtkTemplate.Child()
    add_popover = GtkTemplate.Child()
    viewtype_icon = GtkTemplate.Child()

    def __init__(self, application, **kwargs):
        self.application = application
        self.runtime_updater = RuntimeUpdater()
        self.threads_stoppers = []
        self.selected_runner = None
        self.selected_platform = None
        self.icon_type = None

        # Load settings
        width = int(settings.read_setting("width") or self.default_width)
        height = int(settings.read_setting("height") or self.default_height)
        self.window_size = (width, height)
        self.maximized = settings.read_setting("maximized") == "True"

        view_type = self.get_view_type()
        self.load_icon_type_from_settings(view_type)

        # Window initialization
        self.game_actions = GameActions(application=application, window=self)
        self.game_store = GameStore(
            self.icon_type,
            self.filter_installed,
            self.view_sorting,
            self.view_sorting_ascending,
            self.show_installed_first,
        )
        self.view = self.get_view(view_type)
        self.game_store.connect("sorting-changed", self.on_game_store_sorting_changed)
        super().__init__(
            default_width=width,
            default_height=height,
            icon_name="lutris",
            application=application,
            **kwargs
        )
        if self.maximized:
            self.maximize()
        self.init_template()
        self._init_actions()
        self._bind_zoom_adjustment()

        # Load view
        self.games_scrollwindow.add(self.view)
        self._connect_signals()
        # Set theme to dark if set in the settings
        self.set_dark_theme()
        self.set_viewtype_icon(view_type)

        # Add additional widgets
        self.sidebar_listbox = SidebarListBox()
        self.sidebar_listbox.set_size_request(250, -1)
        self.sidebar_listbox.connect("selected-rows-changed", self.on_sidebar_changed)
        self.sidebar_scrolled.add(self.sidebar_listbox)

        self.game_scrolled = Gtk.ScrolledWindow(visible=True)
        self.game_scrolled.set_size_request(320, -1)
        self.game_scrolled.get_style_context().add_class("game-scrolled")
        self.game_scrolled.set_policy(Gtk.PolicyType.EXTERNAL, Gtk.PolicyType.EXTERNAL)

        self.game_panel = Gtk.Box()
        self.main_box.pack_end(self.game_scrolled, False, False, 0)

        self.view.show()

        # Contextual menu
        self.view.contextual_menu = ContextualMenu(self.game_actions.get_game_actions())

        self.game_store.load()

        # Sidebar
        self.sidebar_revealer.set_reveal_child(self.sidebar_visible)
        self.update_runtime()

        # Connect account and/or sync
        credentials = api.read_api_key()
        if credentials:
            self.on_connect_success(None, credentials["username"])
        else:
            self.toggle_connection(False)
            self.sync_library()

        self.sync_services()

        # steamapps_paths = steam.get_steamapps_paths(flat=True)
        # self.steam_watcher = SteamWatcher(steamapps_paths, self.on_steam_game_changed)

    def _init_actions(self):
        Action = namedtuple(
            "Action", ("callback", "type", "enabled", "default", "accel")
        )
        Action.__new__.__defaults__ = (None, None, True, None, None)

        actions = {
            "browse-games": Action(lambda *x: open_uri("https://lutris.net/games/")),
            "register-account": Action(
                lambda *x: open_uri("https://lutris.net/user/register/")
            ),
            "disconnect": Action(self.on_disconnect),
            "connect": Action(self.on_connect),
            "synchronize": Action(lambda *x: self.sync_library()),
            "sync-local": Action(lambda *x: self.open_sync_dialog()),
            "add-game": Action(self.on_add_game_button_clicked),
            "preferences": Action(self.on_preferences_activate),
            "manage-runners": Action(self.on_manage_runners),
            "about": Action(self.on_about_clicked),
            "show-installed-only": Action(
                self.on_show_installed_state_change,
                type="b",
                default=self.filter_installed,
                accel="<Primary>h",
            ),
            "show-installed-first": Action(
                self.on_show_installed_first_state_change,
                type="b",
                default=self.show_installed_first,
            ),
            "toggle-viewtype": Action(self.on_toggle_viewtype),
            "icon-type": Action(
                self.on_icontype_state_change, type="s", default=self.icon_type
            ),
            "view-sorting": Action(
                self.on_view_sorting_state_change, type="s", default=self.view_sorting
            ),
            "view-sorting-ascending": Action(
                self.on_view_sorting_direction_change,
                type="b",
                default=self.view_sorting_ascending,
            ),
            "use-dark-theme": Action(
                self.on_dark_theme_state_change, type="b", default=self.use_dark_theme
            ),
            "show-tray-icon": Action(
                self.on_tray_icon_toggle, type="b", default=self.show_tray_icon
            ),
            "show-side-bar": Action(
                self.on_sidebar_state_change,
                type="b",
                default=self.sidebar_visible,
                accel="F9",
            ),
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
    def current_view_type(self):
        """Returns which kind of view is currently presented (grid or list)"""
        return "grid" if isinstance(self.view, GameGridView) else "list"

    @property
    def filter_installed(self):
        return settings.read_setting("filter_installed") == "true"

    @property
    def sidebar_visible(self):
        return settings.read_setting("sidebar_visible") in [
            "true",
            None,
        ]

    @property
    def use_dark_theme(self):
        """Return whether to use the dark theme variant (if the theme provides one)"""
        return settings.read_setting("dark_theme", default="false").lower() == "true"

    @property
    def show_installed_first(self):
        return settings.read_setting("show_installed_first") == "true"

    @property
    def show_tray_icon(self):
        return settings.read_setting("show_tray_icon", default="false").lower() == "true"

    @property
    def view_sorting(self):
        return settings.read_setting("view_sorting") or "name"

    @property
    def view_sorting_ascending(self):
        return settings.read_setting("view_sorting_ascending") != "false"

    def sync_services(self):
        """Sync local lutris library with current Steam games and desktop games"""
        def full_sync(syncer_cls):
            syncer = syncer_cls()
            games = syncer.load()
            return syncer.sync(games, full=True)

        def on_sync_complete(response, errors):
            """Callback to update the view on sync complete"""
            if errors:
                logger.error("Sync failed: %s", errors)
            added_games, removed_games = response

            for game_id in added_games:
                self.game_store.add_or_update(game_id)

            for game_id in removed_games:
                self.remove_game_from_view(game_id)

        for service in get_services_synced_at_startup():
            AsyncCall(full_sync, on_sync_complete, service.SYNCER)

    def on_steam_game_changed(self, operation, path):
        """Action taken when a Steam AppManifest file is updated"""
        appmanifest = steam.AppManifest(path)
        # if self.running_game and "steam" in self.running_game.runner_name:
        #     self.running_game.notify_steam_game_changed(appmanifest)

        runner_name = appmanifest.get_runner_name()
        games = pga.get_games_where(steamid=appmanifest.steamid)
        if operation == Gio.FileMonitorEvent.DELETED:
            for game in games:
                if game["runner"] == runner_name:
                    steam.mark_as_uninstalled(game)
                    self.game_store.set_uninstalled(Game(game["id"]))
                    break
        elif operation in (Gio.FileMonitorEvent.CHANGED, Gio.FileMonitorEvent.CREATED):
            if not appmanifest.is_installed():
                return
            if runner_name == "winesteam":
                return
            game_info = None
            for game in games:
                if game["installed"] == 0:
                    game_info = game
                else:
                    # Game is already installed, don't do anything
                    return
            if not game_info:
                game_info = {"name": appmanifest.name, "slug": appmanifest.slug}
            if steam in get_services_synced_at_startup():
                game_id = steam.mark_as_installed(
                    appmanifest.steamid, runner_name, game_info
                )
                self.game_store.update_game_by_id(game_id)

    def set_dark_theme(self):
        """Enables or disbales dark theme"""
        gtksettings = Gtk.Settings.get_default()
        gtksettings.set_property("gtk-application-prefer-dark-theme", self.use_dark_theme)

    def get_view(self, view_type):
        """Return the appropriate widget for the current view"""
        if view_type == "grid":
            return GameGridView(self.game_store)
        return GameListView(self.game_store)

    def _connect_signals(self):
        """Connect signals from the view with the main window.

        This must be called each time the view is rebuilt.
        """
        self.view.connect("game-installed", self.on_game_installed)
        self.view.connect("game-selected", self.game_selection_changed)

    def _bind_zoom_adjustment(self):
        """Bind the zoom slider to the supported banner sizes"""
        image_sizes = list(IMAGE_SIZES.keys())
        self.zoom_adjustment.props.value = image_sizes.index(self.icon_type)
        self.zoom_adjustment.connect(
            "value-changed",
            lambda adj: self._set_icon_type(image_sizes[int(adj.props.value)]),
        )

    @staticmethod
    def check_update():
        """Verify availability of client update."""
        version_request = http.Request("https://lutris.net/version")
        version_request.get()
        version = version_request.content
        if version:
            latest_version = settings.read_setting("latest_version")
            if version > (latest_version or settings.VERSION):
                dialogs.ClientUpdateDialog()
                # Store latest version seen to avoid showing
                # the dialog more than once.
                settings.write_setting("latest_version", version)

    def get_view_type(self):
        """Return the type of view saved by the user"""
        view_type = settings.read_setting("view_type")
        if view_type in ["grid", "list"]:
            return view_type
        return self.default_view_type

    def do_key_press_event(self, event):
        if event.keyval == Gdk.KEY_Escape:
            self.search_toggle.set_active(False)
            return Gdk.EVENT_STOP

        # Probably not ideal for non-english, but we want to limit
        # which keys actually start searching
        if (
            not Gdk.KEY_0 <= event.keyval <= Gdk.KEY_z
            or event.state & Gdk.ModifierType.CONTROL_MASK
            or event.state & Gdk.ModifierType.SHIFT_MASK
            or event.state & Gdk.ModifierType.META_MASK
            or event.state & Gdk.ModifierType.MOD1_MASK
            or self.search_entry.has_focus()
        ):
            return Gtk.ApplicationWindow.do_key_press_event(self, event)

        self.search_toggle.set_active(True)
        self.search_entry.grab_focus()
        return self.search_entry.do_key_press_event(self.search_entry, event)

    def load_icon_type_from_settings(self, view_type):
        """Return the icon style depending on the type of view."""
        if view_type == "list":
            self.icon_type = settings.read_setting("icon_type_listview")
            default = "icon"
        else:
            self.icon_type = settings.read_setting("icon_type_gridview")
            default = "banner"
        if self.icon_type not in IMAGE_SIZES.keys():
            self.icon_type = default
        return self.icon_type

    def switch_view(self, view_type):
        """Switch between grid view and list view."""
        self.view.destroy()
        self.load_icon_type_from_settings(view_type)
        self.game_store.set_icon_type(self.icon_type)

        self.view = self.get_view(view_type)
        self.view.contextual_menu = ContextualMenu(self.game_actions.get_game_actions())
        self._connect_signals()
        scrollwindow_children = self.games_scrollwindow.get_children()
        if scrollwindow_children:
            child = scrollwindow_children[0]
            child.destroy()
        self.games_scrollwindow.add(self.view)
        self.set_selected_filter(self.selected_runner, self.selected_platform)
        self.set_show_installed_state(self.filter_installed)
        self.view.show_all()

        self.zoom_adjustment.props.value = list(IMAGE_SIZES.keys()).index(self.icon_type)

        self.set_viewtype_icon(view_type)
        settings.write_setting("view_type", view_type)

    def set_viewtype_icon(self, view_type):
        self.viewtype_icon.set_from_icon_name(
            "view-%s-symbolic" % ("list" if view_type == "grid" else "grid"),
            Gtk.IconSize.BUTTON
        )

    def sync_library(self):
        """Synchronize games with local stuff and server."""

        def update_gui(result, error):
            if error:
                logger.error("Failed to synchrone library: %s", error)
                return
            if result:
                added_ids, updated_ids = result
                self.game_store.add_games(pga.get_games_by_ids(added_ids))
                for game_id in updated_ids.difference(added_ids):
                    self.game_store.update_game_by_id(game_id)
                GLib.idle_add(self.fetch_media)
            else:
                logger.error("No results returned when syncing the library")
            self.sync_label.set_label("Synchronize library")
            self.sync_spinner.props.active = False
            self.sync_button.set_sensitive(True)

        self.sync_label.set_label("Synchronizing…")
        self.sync_spinner.props.active = True
        self.sync_button.set_sensitive(False)
        AsyncCall(sync_from_remote, update_gui)

    def open_sync_dialog(self):
        """Opens the service sync dialog"""
        self.add_popover.hide()
        SyncServiceWindow(application=self.application)

    def fetch_media(self):
        """Called to update the media on the view"""
        AsyncCall(resources.get_missing_media,
                  self.on_media_returned,
                  self.game_store.game_slugs)
        return False

    def on_media_returned(self, lutris_media, _error=None):
        """Called when the Lutris API has provided a list of downloadable media"""
        icons_sync = AsyncCall(resources.fetch_icons, None, lutris_media, self.update_game)
        self.threads_stoppers.append(icons_sync.stop_request.set)

    def update_runtime(self):
        """Check that the runtime is up to date"""
        runtime_sync = AsyncCall(self.runtime_updater.update, None)
        self.threads_stoppers.append(runtime_sync.stop_request.set)

    def on_dark_theme_state_change(self, action, value):
        """Callback for theme switching action"""
        action.set_state(value)
        settings.write_setting("dark_theme", "true" if value.get_boolean() else "false")
        self.set_dark_theme()

    @GtkTemplate.Callback
    def on_connect(self, *_args):
        """Callback when a user connects to his account."""
        login_dialog = dialogs.ClientLoginDialog(self)
        login_dialog.connect("connected", self.on_connect_success)
        return True

    def on_connect_success(self, _dialog, username):
        """Callback for user connect success"""
        self.toggle_connection(True, username)
        self.sync_library()
        self.actions["synchronize"].props.enabled = True
        self.actions["register-account"].props.enabled = False

    @GtkTemplate.Callback
    def on_disconnect(self, *_args):
        """Callback from user disconnect"""
        api.disconnect()
        self.toggle_connection(False)
        self.actions["synchronize"].props.enabled = False

    def toggle_connection(self, is_connected, username=None):
        """Sets or unset connected state for the current user"""
        self.connect_button.props.visible = not is_connected
        self.register_button.props.visible = not is_connected
        self.disconnect_button.props.visible = is_connected
        self.sync_button.props.visible = is_connected
        if is_connected:
            self.connection_label.set_text(username)
            logger.info("Connected to lutris.net as %s", username)

    @GtkTemplate.Callback
    def on_resize(self, widget, *_args):
        """Size-allocate signal.

        Updates stored window size and maximized state.
        """
        if not widget.get_window():
            return
        self.maximized = widget.is_maximized()
        if not self.maximized:
            self.window_size = widget.get_size()

    @GtkTemplate.Callback
    def on_destroy(self, *_args):
        """Signal for window close."""
        # Stop cancellable running threads
        for stopper in self.threads_stoppers:
            stopper()
        # self.steam_watcher = None

        # Save settings
        width, height = self.window_size
        settings.write_setting("width", width)
        settings.write_setting("height", height)
        settings.write_setting("maximized", self.maximized)

    @GtkTemplate.Callback
    def on_preferences_activate(self, *_args):
        """Callback when preferences is activated."""
        SystemConfigDialog(parent=self)

    @GtkTemplate.Callback
    def on_manage_runners(self, *args):
        return RunnersDialog(transient_for=self)

    def invalidate_game_filter(self):
        """Refilter the game view based on current filters"""
        self.game_store.modelfilter.refilter()
        self.game_store.modelsort.clear_cache()
        self.game_store.sort_view(self.view_sorting, self.view_sorting_ascending)
        self.no_results_overlay.props.visible = len(self.game_store.modelfilter) == 0

    def on_show_installed_first_state_change(self, action, value):
        """Callback to handle installed games first toggle"""
        action.set_state(value)
        self.set_show_installed_first_state(value.get_boolean())

    def set_show_installed_first_state(self, show_installed_first):
        """Shows the installed games first in the view"""
        settings.write_setting("show_installed_first", "true" if show_installed_first else "false")
        self.game_store.sort_view(show_installed_first)
        self.game_store.modelfilter.refilter()

    def on_show_installed_state_change(self, action, value):
        """Callback to handle uninstalled game filter switch"""
        action.set_state(value)
        self.set_show_installed_state(value.get_boolean())

    def set_show_installed_state(self, filter_installed):
        """Shows or hide uninstalled games"""
        settings.write_setting("filter_installed", "true" if filter_installed else "false")
        self.game_store.filter_installed = filter_installed
        self.invalidate_game_filter()

    @GtkTemplate.Callback
    def on_search_entry_changed(self, widget):
        """Callback for the search input keypresses"""
        self.game_store.filter_text = widget.get_text()
        self.invalidate_game_filter()

    @GtkTemplate.Callback
    def on_search_toggle(self, button):
        active = button.props.active
        self.search_revealer.set_reveal_child(active)
        if not active:
            self.search_entry.props.text = ""
        else:
            self.search_entry.grab_focus()

    @GtkTemplate.Callback
    def on_about_clicked(self, *_args):
        """Open the about dialog."""
        dialogs.AboutDialog(parent=self)

    def on_game_error(self, game, error):
        """Called when a game has sent the 'game-error' signal"""
        logger.error("%s crashed", game)
        dialogs.ErrorDialog(error, parent=self)

    def game_selection_changed(self, widget):
        """Callback to handle the selection of a game in the view"""
        child = self.game_scrolled.get_child()
        if child:
            self.game_scrolled.remove(child)
            child.destroy()

        if not self.view.selected_game:
            return
        self.game_actions.set_game(game_id=self.view.selected_game)
        self.game_panel = GamePanel(self.game_actions)
        self.game_scrolled.add(self.game_panel)

    def on_game_installed(self, view, game_id):
        """Callback to handle newly installed games"""
        if not isinstance(game_id, int):
            raise ValueError("game_id must be an int")
        self.game_store.add_or_update(game_id)
        self.sidebar_listbox.update()

    def update_game(self, slug):
        for pga_game in pga.get_games_where(slug=slug):
            self.game_store.update_game_by_id(pga_game["id"])

    @GtkTemplate.Callback
    def on_add_game_button_clicked(self, *_args):
        """Add a new game manually with the AddGameDialog."""
        self.add_popover.hide()
        dialog = AddGameDialog(
            self,
            runner=self.selected_runner,
            callback=lambda: self.game_store.add_game_by_id(dialog.game.id),
        )
        return True

    def remove_game_from_view(self, game_id, from_library=False):
        """Remove a game from the view"""

        def do_remove_game():
            self.game_store.remove_game(game_id)

        if from_library:
            GLib.idle_add(do_remove_game)
        else:
            self.game_store.update(game_id)
        self.sidebar_listbox.update()

    def on_toggle_viewtype(self, *args):
        self.switch_view("list" if self.current_view_type == "grid" else "grid")

    def on_viewtype_state_change(self, action, val):
        """Callback to handle view type switch"""
        action.set_state(val)
        view_type = val.get_string()
        if view_type != self.current_view_type:
            self.switch_view(view_type)

    def _set_icon_type(self, icon_type):
        self.icon_type = icon_type
        if self.icon_type == self.game_store.icon_type:
            return
        if self.current_view_type == "grid":
            settings.write_setting("icon_type_gridview", self.icon_type)
        elif self.current_view_type == "list":
            settings.write_setting("icon_type_listview", self.icon_type)
        self.game_store.set_icon_type(self.icon_type)
        self.switch_view(self.get_view_type())

    def on_icontype_state_change(self, action, value):
        action.set_state(value)
        self._set_icon_type(value.get_string())

    def on_view_sorting_state_change(self, action, value):
        self.game_store.sort_view(value.get_string(), self.view_sorting_ascending)

    def on_view_sorting_direction_change(self, action, value):
        self.game_store.sort_view(self.view_sorting, value.get_boolean())

    def on_game_store_sorting_changed(self, _game_store, key, ascending):
        self.actions["view-sorting"].set_state(GLib.Variant.new_string(key))
        settings.write_setting("view_sorting", key)

        self.actions["view-sorting-ascending"].set_state(GLib.Variant.new_boolean(ascending))
        settings.write_setting("view_sorting_ascending", "true" if ascending else "false")

    def on_sidebar_state_change(self, action, value):
        """Callback to handle siderbar toggle"""
        action.set_state(value)
        sidebar_visible = value.get_boolean()
        settings.write_setting("sidebar_visible", "true" if sidebar_visible else "false")
        self.sidebar_revealer.set_reveal_child(sidebar_visible)

    def on_sidebar_changed(self, widget):
        row = widget.get_selected_row()
        if row is None:
            self.set_selected_filter(None, None)
        elif row.type == "runner":
            self.set_selected_filter(row.id, None)
        else:
            self.set_selected_filter(None, row.id)

    def on_tray_icon_toggle(self, action, value):
        """Callback for handling tray icon toggle"""
        action.set_state(value)
        settings.write_setting("show_tray_icon", value)
        self.application.set_tray_icon(value)

    def set_selected_filter(self, runner, platform):
        """Filter the view to a given runner and platform"""
        self.selected_runner = runner
        self.selected_platform = platform
        self.game_store.filter_runner = self.selected_runner
        self.game_store.filter_platform = self.selected_platform
        self.invalidate_game_filter()
