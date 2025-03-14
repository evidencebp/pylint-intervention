# -*- coding: utf-8 -*-

# PyRadio: Curses based Internet Radio Player
# http://www.coderholic.com/pyradio
# Ben Dowling - 2009 - 2010
# Kirill Klenov - 2012
# Peter Stevenson (2E0PGS) - 2018
# Spiros Georgaras - 2018, 2019

import curses
import curses.ascii
import threading
import logging
import os
import random
#import signal
from sys import version as python_version, version_info, platform
from os.path import join, basename, getmtime, getsize
from platform import system
from time import ctime, sleep
from datetime import datetime

from .config import HAS_REQUESTS
from .common import *
from .window_stack import Window_Stack
from .config_window import *
from .log import Log
from .edit import PyRadioSearch, PyRadioEditor
from .themes import *
from .simple_curses_widgets import cjklen
from . import player
import logging

CAN_CHECK_FOR_UPDATES = True
try:
    from urllib.request import urlopen
except ImportError:
    try:
        from urllib2 import urlopen
    except ImportError:
        CAN_CHECK_FOR_UPDATES = False

logger = logging.getLogger(__name__)

import locale
locale.setlocale(locale.LC_ALL, "")

def rel(path):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

class PyRadio(object):
    ws = Window_Stack()

    _redisplay_list = []

    """ number of items (stations or playlists) in current view """
    number_of_items = 0

    playing = -1
    jumpnr = ""
    _backslash = False
    """ Help window
        also used for displaying messages,
        asking for confirmation etc. """
    helpWinContainer = None
    helpWin = None

    """ Window to display line number (jumpnr) """
    transientWin = None

    """ Used when loading new playlist.
        If the first station (selection) exists in the new playlist,
        we mark it as selected
        If the seconf station (playing) exists in the new playlist,
        we continue playing, otherwise, we stop playback """
    active_stations = [ [ '', 0 ], [ '', -1 ] ]

    """ Characters to be "ignored" by windows, so that certain
        functions still work (like changing volume) """
    _chars_to_bypass = (ord('m'), ord('v'), ord('.'),
            ord(','), ord('+'), ord('-'),
            ord('?'), ord('#'), curses.KEY_RESIZE)

    """ Characters to be "ignored" by windows that support search"""
    _chars_to_bypass_for_search = (ord('/'), ord('n'), ord('N'))

    """ Characters to "ignore" when station editor window
        is onen and focus is not in line editor """
    _chars_to_bypass_on_editor = (ord('m'), ord('v'), ord('.'),
            ord(','), ord('+'), ord('-'))

    # Number of stations to change with the page up/down keys
    pageChange = 5

    search = None

    _last_played_station = ''

    _random_requested = False

    _theme = None
    _theme_name = 'dark'
    _theme_selector = None
    _theme_not_supported_thread = None
    _theme_not_supported_notification_duration = 1.75
    theme_forced_selection = []

    _config_win = None

    _color_config_win = None

    _player_select_win = None
    _encoding_select_win = None
    _playlist_select_win = None
    _station_select_win = None

    _old_config_encoding = ''

    # update notification
    _update_version = ''
    _update_version_do_display = ''
    _update_notification_thread = None
    stop_update_notification_thread = False
    _update_notify_lock = threading.Lock()

    """ editor class """
    _station_editor = None

    _force_exit = False

    _help_metrics = {}

    def __init__(self, pyradio_config, play=False, req_player='', theme=''):
        self._cnf = pyradio_config
        self._theme = PyRadioTheme(self._cnf)
        if theme:
            self._theme_name = theme
        ind = self._cnf.current_playlist_index()
        self.selections = [ [0, 0, -1, self._cnf.stations],
                            [ind, 0, ind, self._cnf.playlists]]
        self.selection, self.startPos, self.playing, self.stations = self.selections[self.ws.operation_mode]
        self.play = play
        self.stdscr = None
        self.requested_player = req_player
        self.number_of_items = len(self._cnf.stations)

        """ list of functions to open for entering
            or redisplaying a mode """
        self._redisplay = {
                self.ws.NORMAL_MODE: self._redisplay_stations_and_playlists,
                self.ws.PLAYLIST_MODE: self._redisplay_stations_and_playlists,
                self.ws.CONFIG_MODE: self._redisplay_config,
                self.ws.SELECT_PLAYER_MODE: self._redisplay_player_select_win_refresh_and_resize,
                self.ws.SELECT_ENCODING_MODE: self._redisplay_encoding_select_win_refresh_and_resize,
                self.ws.SELECT_STATION_ENCODING_MODE: self._redisplay_encoding_select_win_refresh_and_resize,
                self.ws.SELECT_PLAYLIST_MODE: self._playlist_select_win_refresh_and_resize,
                self.ws.SELECT_STATION_MODE: self._redisplay_station_select_win_refresh_and_resize,
                self.ws.MAIN_HELP_MODE: self._show_main_help,
                self.ws.MAIN_HELP_MODE_PAGE_2: self._show_main_help_page_2,
                self.ws.PLAYLIST_HELP_MODE: self._show_playlist_help,
                self.ws.THEME_HELP_MODE: self._show_theme_help,
                self.ws.CONFIG_HELP_MODE: self._show_config_help,
                self.ws.SELECT_PLAYER_HELP_MODE: self._show_config_player_help,
                self.ws.SELECT_PLAYLIST_HELP_MODE: self._show_config_playlist_help,
                self.ws.SELECT_STATION_HELP_MODE: self._show_config_station_help,
                self.ws.SESSION_LOCKED_MODE: self._print_session_locked,
                self.ws.UPDATE_NOTIFICATION_MODE: self._print_update_notification,
                self.ws.SELECT_ENCODING_HELP_MODE: self._show_config_encoding_help,
                self.ws.SELECT_STATION_ENCODING_MODE: self._redisplay_encoding_select_win_refresh_and_resize,
                self.ws.EDIT_STATION_ENCODING_MODE: self._redisplay_encoding_select_win_refresh_and_resize,
                self.ws.PLAYLIST_NOT_FOUND_ERROR_MODE: self._print_playlist_not_found_error,
                self.ws.PLAYLIST_LOAD_ERROR_MODE: self._print_playlist_load_error,
                self.ws.ASK_TO_SAVE_PLAYLIST_WHEN_OPENING_PLAYLIST_MODE: self._redisplay_print_save_modified_playlist,
                self.ws.ASK_TO_SAVE_PLAYLIST_WHEN_EXITING_MODE: self._redisplay_print_save_modified_playlist,
                self.ws.PLAYLIST_RELOAD_CONFIRM_MODE: self._print_playlist_reload_confirmation,
                self.ws.PLAYLIST_DIRTY_RELOAD_CONFIRM_MODE: self._print_playlist_dirty_reload_confirmation,
                self.ws.PLAYLIST_RELOAD_ERROR_MODE: self._print_playlist_reload_error,
                self.ws.SAVE_PLAYLIST_ERROR_1_MODE: self._print_save_playlist_error_1,
                self.ws.SAVE_PLAYLIST_ERROR_2_MODE: self._print_save_playlist_error_2,
                self.ws.REMOVE_STATION_MODE: self.removeStation,
                self.ws.FOREIGN_PLAYLIST_ASK_MODE: self._print_handle_foreign_playlist,
                self.ws.FOREIGN_PLAYLIST_MESSAGE_MODE: self._print_foreign_playlist_message,
                self.ws.FOREIGN_PLAYLIST_COPY_ERROR_MODE: self._print_foreign_playlist_copy_error,
                self.ws.SEARCH_NORMAL_MODE: self._redisplay_search_show,
                self.ws.SEARCH_PLAYLIST_MODE: self._redisplay_search_show,
                self.ws.SEARCH_THEME_MODE: self._redisplay_search_show,
                self.ws.THEME_MODE: self._redisplay_theme_mode,
                self.ws.PLAYLIST_RECOVERY_ERROR_MODE: self._print_playlist_recovery_error,
                self.ws.ASK_TO_CREATE_NEW_THEME_MODE: self._redisplay_ask_to_create_new_theme,
                self.ws.SEARCH_HELP_MODE: self._show_search_help,
                self.ws.ADD_STATION_MODE: self._show_station_editor,
                self.ws.EDIT_STATION_MODE: self._show_station_editor,
                self.ws.LINE_EDITOR_HELP: self._show_line_editor_help,
                self.ws.EDIT_STATION_NAME_ERROR: self._print_editor_name_error,
                self.ws.EDIT_STATION_URL_ERROR: self._print_editor_url_error,
                self.ws.PY2_EDITOR_ERROR: self._print_py2_editor_error,
                self.ws.REQUESTS_MODULE_NOT_INSTALLED_ERROR: self._print_requests_not_installed_error,
                self.ws.UNKNOWN_BROWSER_SERVICE_ERROR: self._print_unknown_browser_service,
                self.ws.SERVICE_CONNECTION_ERROR: self._print_service_connection_error,
                self.ws.PLAYER_CHANGED_INFO_MODE: self._show_player_changed_in_config,
                }

        """ list of help functions """
        self._display_help = {
                self.ws.NORMAL_MODE: self._show_main_help,
                self.ws.PLAYLIST_MODE: self._show_playlist_help,
                self.ws.THEME_MODE: self._show_theme_help,
                self.ws.SEARCH_NORMAL_MODE: self._show_search_help,
                self.ws.SEARCH_PLAYLIST_MODE: self._show_search_help,
                self.ws.CONFIG_MODE: self._show_config_help,
                self.ws.SELECT_PLAYER_MODE: self._show_config_player_help,
                self.ws.SELECT_PLAYLIST_MODE: self._show_config_playlist_help,
                self.ws.SELECT_STATION_MODE: self._show_config_station_help,
                self.ws.SELECT_STATION_ENCODING_MODE: self._show_config_encoding_help,
                self.ws.SELECT_ENCODING_MODE: self._show_config_encoding_help,
                self.ws.EDIT_STATION_ENCODING_MODE: self._show_config_encoding_help,
                self.ws.LINE_EDITOR_HELP: self._show_line_editor_help,
                }

        """ search classes
            0 - station search
            1 - playlist search
            2 - theme search
        """
        self._search_classes = [ None, None, None ]

        """ points to list in which the search will be performed """
        self._search_list = []

        """ points to _search_classes for each supported mode """
        self._mode_to_search = {
                self.ws.NORMAL_MODE: 0,
                self.ws.SELECT_STATION_MODE: 0,
                self.ws.PLAYLIST_MODE: 1,
                self.ws.SELECT_PLAYLIST_MODE: 1,
                self.ws.THEME_MODE: 2,
                }

        # which search mode opens from each allowed mode
        self._search_modes = {
                self.ws.NORMAL_MODE: self.ws.SEARCH_NORMAL_MODE,
                self.ws.PLAYLIST_MODE: self.ws.SEARCH_PLAYLIST_MODE,
                self.ws.THEME_MODE: self.ws.SEARCH_THEME_MODE,
                self.ws.SELECT_PLAYLIST_MODE: self.ws.SEARCH_SELECT_PLAYLIST_MODE,
                self.ws.SELECT_STATION_MODE: self.ws.SEARCH_SELECT_STATION_MODE,
                }

        # search modes opened from main windows
        self.search_main_window_modes = (
                self.ws.SEARCH_NORMAL_MODE,
                self.ws.SEARCH_PLAYLIST_MODE,
                )

        # keyboard will be dead in theses modes
        self._no_keyboard = (
                self.ws.HISTORY_EMPTY_NOTIFICATION,
                )

        # volume functions
        self.volume_functions = {
                '+': self._volume_up,
                '=': self._volume_up,
                '.': self._volume_up,
                '-': self._volume_down,
                ',': self._volume_down,
                'm': self._volume_mute,
                'v': self._volume_save
        }

    def __del__(self):
        self.transientWin = None

    def setup(self, stdscr):
        self.setup_return_status = True
        if not curses.has_colors():
            self.setup_return_status = False
            return
        if logger.isEnabledFor(logging.INFO):
            logger.info("TUI initialization on python v. {0} on {1}".format(python_version.replace('\n', ' ').replace('\r', ' '), system()))
            logger.info('Terminal supports {} colors'.format(curses.COLORS))
        self.stdscr = stdscr
        from pyradio import version
        self.info = " PyRadio {0} ".format(version)
        # git_description can be set at build time
        # if so, revision will be shown along with the version
        # if revision is not 0
        git_description = ''
        if git_description:
            if git_description == 'not_from_git':
                if logger.isEnabledFor(logging.INFO):
                    logger.info("RyRadio built from zip file (revision unknown)")
            else:
                git_info = git_description.split('-')
                if git_info[1] != '0':
                    self.info = " PyRadio {0}-r{1} ".format(version, git_info[1])
                if logger.isEnabledFor(logging.INFO):
                    logger.info("RyRadio built from git: https://github.com/coderholic/pyradio/commit/{0} (rev. {1})".format(git_info[-1], git_info[1]))

        try:
            curses.curs_set(0)
        except:
            pass

        curses.use_default_colors()
        self._theme._transparent = self._cnf.use_transparency
        self._theme.config_dir = self._cnf.stations_dir
        ret, ret_theme_name = self._theme.readAndApplyTheme(self._theme_name)
        if ret == 0:
            self._theme_name = self._theme.applied_theme_name
        else:
            self._theme_name = ret_theme_name
            self._cnf.theme_not_supported = True

        self.log = Log()
        # For the time being, supported players are mpv, mplayer and vlc.
        try:
            self.player = player.probePlayer(requested_player=self.requested_player)(self.log, self._cnf.connection_timeout, self.connectionFailed)
        except:
            # no player
            self.ws.operation_mode = self.ws.NO_PLAYER_ERROR_MODE

        self.stdscr.nodelay(0)
        self.setupAndDrawScreen()

        # position playlist in window
        self.outerBodyMaxY, self.outerBodyMaxX = self.outerBodyWin.getmaxyx()
        self.bodyMaxY, self.bodyMaxX = self.bodyWin.getmaxyx()
        # logger.error('\n\nDE self.selections before')
        # for n in self.selections:
        #     logger.error('{}\n'.format(n))
        if self.selections[self.ws.PLAYLIST_MODE][0] < self.bodyMaxY:
            self.selections[self.ws.PLAYLIST_MODE][1] = 0
        elif self.selections[self.ws.PLAYLIST_MODE][0] > len(self._cnf.playlists) - self.bodyMaxY + 1:
            # TODO make sure this is ok
            self.selections[self.ws.PLAYLIST_MODE][1] = len(self._cnf.playlists) - self.bodyMaxY
        else:
            self.selections[self.ws.PLAYLIST_MODE][1] = self.selections[self.ws.PLAYLIST_MODE][0] - int(self.bodyMaxY/2)
        # logger.error('\nDE self.selections after')
        # for n in self.selections:
        #     logger.error('{}\n'.format(n))
        # logger.error('DE\n')
        self.run()

    def setupAndDrawScreen(self):
        self.maxY, self.maxX = self.stdscr.getmaxyx()

        self.headWin = None
        self.bodyWin = None
        self.outerBodyWin = None
        self.footerWin = None
        self.headWin = curses.newwin(1, self.maxX, 0, 0)
        self.outerBodyWin = curses.newwin(self.maxY - 2, self.maxX, 1, 0)
        #self.bodyWin = curses.newwin(self.maxY - 2, self.maxX, 1, 0)
        self.bodyWin = curses.newwin(self.maxY - 4 - self._cnf.internal_header_height,
                self.maxX - 2,
                2 + self._cnf.internal_header_height,
                1)
        self.footerWin = curses.newwin(1, self.maxX, self.maxY - 1, 0)
        # txtWin used mainly for error reports
        self.txtWin = None
        self.txtWin = curses.newwin(self.maxY - 4, self.maxX - 4, 2, 2)
        self.initHead(self.info)
        # for light color scheme
         # TODO
        self.outerBodyWin.bkgdset(' ', curses.color_pair(5))
        self.bodyWin.bkgdset(' ', curses.color_pair(5))
        self.initBody()
        self.initFooter()

        self.log.setScreen(self.footerWin)

        #self.stdscr.timeout(100)
        self.bodyWin.keypad(1)

        #self.stdscr.noutrefresh()

        curses.doupdate()

    def initHead(self, info):
        try:
            self.headWin.addstr(0, 0, info, curses.color_pair(4))
            if self._cnf.locked:
                d_info = (self.maxX - len(info) - 16) * ' '
                self.headWin.addstr('[', curses.color_pair(5))
                self.headWin.addstr('Session Locked', curses.color_pair(4))
                self.headWin.addstr(']', curses.color_pair(5))
            else:
                d_info = (self.maxX - len(info)) * ' '
            self.headWin.addstr(d_info, curses.color_pair(4))
        except:
            pass
        rightStr = " www.coderholic.com/pyradio"
        rightStr = " https://github.com/coderholic/pyradio"
        try:
            self.headWin.addstr(0, self.maxX - len(rightStr) -1, rightStr,
                                curses.color_pair(2))
        except:
            pass
        self.headWin.bkgd(' ', curses.color_pair(7))
        self.headWin.noutrefresh()

    def initBody(self):
        """ Initializes the body/story window """
        #self.bodyWin.timeout(100)
        #self.bodyWin.keypad(1)
        self.bodyMaxY, self.bodyMaxX = self.bodyWin.getmaxyx()
        self.outerBodyMaxY, self.outerBodyMaxX = self.outerBodyWin.getmaxyx()
        self.bodyWin.noutrefresh()
        self.outerBodyWin.noutrefresh()
        if self.ws.operation_mode == self.ws.NO_PLAYER_ERROR_MODE:
            if platform.startswith('win'):
                txt = '''PyRadio cannot find mplayer.

                    This means that either mplayer is not installed in this system,
                    or its directory is not in the PATH.

                    Please refer to windows.html help file to fix this problem.

                    To get to this file, execute "pyradio -ocd" and navigate to
                    the "help" directory.'''
            else:
                if self.requested_player:
                    txt = """PyRadio is not able to use the player you specified.

                    This means that either this particular player is not supported
                    by PyRadio, or that you have simply misspelled its name.

                    PyRadio currently supports three players: mpv, mplayer and vlc,
                    automatically detected in this order."""
                else:
                    txt = """PyRadio is not able to detect any players.

                    PyRadio currently supports three players: mpv, mplayer and vlc,
                    automatically detected in this order.

                    Please install any one of them and try again."""
            self.refreshNoPlayerBody(txt)
        else:
            #if self.ws.operation_mode == self.ws.MAIN_HELP_MODE:
            #    self.ws.operation_mode = self.ws.window_mode = self.ws.NORMAL_MODE
            #    self.helpWin = None
            #    if logger.isEnabledFor(logging.DEBUG):
            #        logger.debug('MODE: self.ws.MAIN_HELP_MODE => self.ws.NORMAL_MODE')
            #elif self.ws.operation_mode == self.ws.PLAYLIST_HELP_MODE:
            #    self.ws.operation_mode = self.ws.window_mode = self.ws.PLAYLIST_MODE
            #    self.helpWin = None
            #    if logger.isEnabledFor(logging.DEBUG):
            #        logger.debug('MODE: self.ws.PLAYLIST_HELP_MODE =>  self.ws.PLAYLIST_MODE')
            #elif self.ws.operation_mode == self.ws.THEME_HELP_MODE:
            #    self.ws.operation_mode = self.ws.window_mode = self.ws.THEME_MODE
            #    self.helpWin = None
            #    if logger.isEnabledFor(logging.DEBUG):
            #        logger.debug('MODE: self.ws.THEME_HELP_MODE =>  self.ws.THEME_MODE')
            # make sure selected is visible
            self._put_selection_in_the_middle()
            self.refreshBody()

    def initFooter(self):
        """ Initializes the body/story window """
        self.footerWin.bkgd(' ', curses.color_pair(7))
        self.footerWin.noutrefresh()

    def _update_redisplay_list(self):
        def _get_redisplay_index():
            for n in range(-1, - len(self.ws._dq) - 1, -1):
                if self.ws._dq[n][0] == self.ws._dq[n][1]:
                    return n
            return 0
        self._redisplay_list = list(self.ws._dq)[_get_redisplay_index():]
        if not self._redisplay_list:
            self._redisplay_list = [ 0, 0 ]

    def refreshBody(self, start=0):
        self._update_redisplay_list()
        end = len(self._redisplay_list)
        if end == 0: end = 1
        for n in range(start, end):
            if n == 1:
                if self._theme_selector:
                    self.theme_forced_selection = self._theme_selector._themes[self._theme_selector.selection]
            self._redisplay[self._redisplay_list[n][0]]()
            # display playlist recovered
            if self._cnf.playlist_recovery_result == -1:
                self._show_playlist_recovered()
                return
            # display theme not supported
            if self._cnf.theme_not_supported:
                self._show_theme_not_supported()

    def refreshNoPlayerBody(self, a_string):
        col = curses.color_pair(5)
        self.outerBodyWin.bkgdset(' ', col)
        self.bodyWin.bkgdset(' ', col)
        self.outerBodyWin.erase()
        self.bodyWin.erase()
        #self.bodyWin.box()
        self.outerBodyWin.box()
        lines = a_string.split('\n')
        lineNum = 0
        self.txtWin.bkgdset(' ', col)
        self.txtWin.erase()
        for line in lines:
            try:
                self.txtWin.addstr(lineNum , 0, line.replace('\r', '').strip(), col)
            except:
                break
            lineNum += 1
        self.outerBodyWin.refresh()
        self.bodyWin.refresh()
        self.txtWin.refresh()

    def _print_body_header(self):
        cur_mode = self.ws.window_mode
        if cur_mode == self.ws.THEME_MODE:
            cur_mode = self.ws.previous_operation_mode
        if cur_mode == self.ws.NORMAL_MODE:
            if self._cnf.browsing_station_service:
                ticks = self._cnf.online_browser.get_columns_separators(self.bodyMaxX, adjust_for_header=True)
                if ticks:
                    for n in ticks:
                        if version_info < (3, 0):
                            self.outerBodyWin.addstr(0, n + 2, u'┬'.encode('utf-8', 'replace'), curses.color_pair(5))
                            self.outerBodyWin.addstr(self.outerBodyMaxY - 1, n + 2, u'┴'.encode('utf-8', 'replace'), curses.color_pair(5))
                        else:
                            self.outerBodyWin.addstr(0, n + 2, '┬', curses.color_pair(5))
                            self.outerBodyWin.addstr(self.outerBodyMaxY - 1, n + 2, '┴', curses.color_pair(5))

            align = 1
            w_header = self._cnf.station_title
            if self._cnf.dirty_playlist:
                align += 1
                w_header = '*' + self._cnf.station_title
            while len(w_header)> self.bodyMaxX - 14:
                w_header = w_header[:-1]
            self.outerBodyWin.addstr(0,
                    int((self.bodyMaxX - len(w_header)) / 2) - align, '[',
                    curses.color_pair(5))
            self.outerBodyWin.addstr(w_header,curses.color_pair(4))
            self.outerBodyWin.addstr(']',curses.color_pair(5))

        elif cur_mode == self.ws.PLAYLIST_MODE or \
                self.ws.operation_mode == self.ws.PLAYLIST_LOAD_ERROR_MODE or \
                self.ws.operation_mode == self.ws.PLAYLIST_NOT_FOUND_ERROR_MODE:
            """ display playlists header """
            w_header = ' Select playlist to open '
            self.outerBodyWin.addstr(0,
                    int((self.bodyMaxX - len(w_header)) / 2),
                    w_header,
                    curses.color_pair(4))

    def __displayBodyLine(self, lineNum, pad, station):
        col = curses.color_pair(5)
        sep_col = None
        if lineNum + self.startPos == self.selection and \
                self.selection == self.playing:
            col = curses.color_pair(9)
            # initialize col_sep here to have separated cursor
            sep_col = curses.color_pair(5)
            self.bodyWin.hline(lineNum, 0, ' ', self.bodyMaxX, col)
        elif lineNum + self.startPos == self.selection:
            col = curses.color_pair(6)
            # initialize col_sep here to have separated cursor
            sep_col = curses.color_pair(5)
            self.bodyWin.hline(lineNum, 0, ' ', self.bodyMaxX, col)
        elif lineNum + self.startPos == self.playing:
            col = curses.color_pair(4)
            sep_col = curses.color_pair(5)
            self.bodyWin.hline(lineNum, 0, ' ', self.bodyMaxX, col)

        # self.maxY, self.maxX = self.stdscr.getmaxyx()
        #logger.error('DE ==== width = {}'.format(self.maxX - 2))
        if self.ws.operation_mode == self.ws.PLAYLIST_MODE or \
                self.ws.operation_mode == self.ws.PLAYLIST_LOAD_ERROR_MODE or \
                    self.ws.operation_mode == self.ws.PLAYLIST_NOT_FOUND_ERROR_MODE:
            line = self._format_playlist_line(lineNum, pad, station)
            self.bodyWin.addstr(lineNum, 0, line, col)
        else:
            if self._cnf.browsing_station_service:
                played, line = self._cnf.online_browser.format_station_line(lineNum + self.startPos, pad, self.bodyMaxX)
            else:
                line = self._format_station_line("{0}. {1}".format(str(lineNum + self.startPos + 1).rjust(pad), station[0]))
            try:
                self.bodyWin.addstr(lineNum, 0, line, col)
            except:
                pass

            if self._cnf.browsing_station_service and sep_col:
                ticks = self._cnf.online_browser.get_columns_separators(self.bodyMaxX, adjust_for_body=True)
                if ticks:
                    for n in ticks:
                        self.bodyWin.chgat(lineNum, n, 1, sep_col)

    def run(self):
        if self.ws.operation_mode == self.ws.NO_PLAYER_ERROR_MODE:
            if platform.startswith('win'):
                self.log.write('mplayer not found. Press any key to exit....')
            else:
                if self.requested_player:
                    if ',' in self.requested_player:
                        self.log.write('None of "{}" players is available. Press any key to exit....'.format(self.requested_player))
                    else:
                        self.log.write('Player "{}" not available. Press any key to exit....'.format(self.requested_player))
                else:
                    self.log.write("No player available. Press any key to exit....")
            try:
                self.bodyWin.getch()
            except KeyboardInterrupt:
                pass
        else:
            self._register_windows_handlers()

            # start update detection and notification thread
            if CAN_CHECK_FOR_UPDATES:
                if self._cnf.locked:
                    if logger.isEnabledFor(logging.INFO):
                        logger.info('(detectUpdateThread): session locked. Not starting!!!')
                else:
                    self._update_notification_thread = threading.Thread(target=self.detectUpdateThread,
                            args=(self._cnf.stations_dir, self._update_notify_lock,
                                lambda: self.stop_update_notification_thread))
                    self._update_notification_thread.start()

            #signal.signal(signal.SIGINT, self.ctrl_c_handler)
            self.log.write('Selected player: {}'.format(self._format_player_string()), help_msg=True)
            #self.log.write_right('Press ? for help')
            if self.play != 'False':
                if self.play is None:
                    num = random.randint(0, len(self.stations))
                    self._random_requested = True
                else:
                    if self.play.replace('-', '').isdigit():
                        num = int(self.play) - 1
                self.setStation(num)
                if self.number_of_items > 0:
                    self.playSelection()
                    self._goto_playing_station(changing_playlist=True)
                self.refreshBody()
                self.selections[self.ws.NORMAL_MODE] = [self.selection, self.startPos, self.playing, self.stations]

            if self._cnf.foreign_file:
                """ ask to copy this playlist in config dir """
                self._print_handle_foreign_playlist()

            while True:
                try:
                    c = self.bodyWin.getch()
                    #logger.error('DE pressed "{0} - {1}"'.format(c, chr(c)))
                    ret = self.keypress(c)
                    if (ret == -1):
                        return
                except KeyboardInterrupt:
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug('Ctrl-C pressed... Exiting...')
                    self.player.ctrl_c_pressed = True
                    self.ctrl_c_handler(0, 0)
                    break

    def _give_me_a_search_class(self, operation_mode):
        """ get a search class for a givven operation mode
            the class is returned in self.search
        """
        if self._search_classes[self._mode_to_search[operation_mode]] is None:
            self._search_classes[self._mode_to_search[operation_mode]] = PyRadioSearch(parent = self.outerBodyWin,
                width = 33, begin_y = 0, begin_x = 0,
                boxed = True,
                has_history = True,
                box_color = curses.color_pair(5),
                caption_color = curses.color_pair(4),
                edit_color = curses.color_pair(5),
                cursor_color = curses.color_pair(8))
        self.search = self._search_classes[self._mode_to_search[operation_mode]]
        #self.search.pure_ascii = True
        if self.ws.previous_operation_mode == self.ws.CONFIG_MODE:
            self.search.box_color = curses.color_pair(3)
        else:
            self.search.box_color = curses.color_pair(5)

    def ctrl_c_handler(self, signum, frame):
        self.ctrl_c_pressed = True
        self._remove_lock_file()
        if self._cnf.dirty_playlist:
            """ Try to auto save playlist on exit
                Do not check result!!! """
            self.saveCurrentPlaylist()
        """ Try to auto save config on exit
            Do not check result!!! """
        self._cnf.save_config()
        self._wait_for_threads()

    def _wait_for_threads(self):
        if self._update_notification_thread:
            if self._update_notification_thread.is_alive():
                self.stop_update_notification_thread = True
                if self._update_notification_thread:
                    self._update_notification_thread.join()

    def _remove_lock_file(self):
        if not self._cnf.locked:
            lock_file = path.join(self._cnf.stations_dir, '.lock')
            if path.exists(lock_file):
                try:
                    os.remove(lock_file)
                    if logger.isEnabledFor(logging.INFO):
                        logger.info('Lock file removed...')
                except:
                    if logger.isEnabledFor(logging.INFO):
                        logger.info('Failed to remove Lock file...')
            else:
                if logger.isEnabledFor(logging.INFO):
                    logger.info('Lock file not found...')

    def _goto_playing_station(self, changing_playlist=False):
        """ make sure playing station is visible """
        if (self.player.isPlaying() or self.ws.operation_mode == self.ws.PLAYLIST_MODE) and \
            (self.selection != self.playing or changing_playlist):
            if changing_playlist:
                self.startPos = 0
            if logger.isEnabledFor(logging.ERROR):
                logger.error('self.bodyMaxY = {0}, items = {1}, self.playing = {2}'.format(self.bodyMaxY, self.number_of_items, self.playing))
            if self.number_of_items < self.bodyMaxY:
                self.startPos = 0
            elif self.playing < self.startPos or \
                    self.playing >= self.startPos + self.bodyMaxY:
                if logger.isEnabledFor(logging.ERROR):
                    logger.error('DE ==== _goto:adjusting startPos')
                if self.playing < self.bodyMaxY:
                    self.startPos = 0
                    if self.playing - int(self.bodyMaxY/2) > 0:
                        self.startPos = self.playing - int(self.bodyMaxY/2)
                elif self.playing > self.number_of_items - self.bodyMaxY:
                    self.startPos = self.number_of_items - self.bodyMaxY
                else:
                    self.startPos = int(self.playing+1/self.bodyMaxY) - int(self.bodyMaxY/2)
            if logger.isEnabledFor(logging.ERROR):
                logger.error('DE ===== _goto:startPos = {0}, changing_playlist = {1}'.format(self.startPos, changing_playlist))
            self.selection = self.playing
            self.refreshBody()

    def _put_selection_in_the_middle(self, force=False):
        if self.number_of_items < self.bodyMaxY or self.selection < self.bodyMaxY:
            self.startPos = 0
        elif force or self.selection < self.startPos or \
                self.selection >= self.startPos + self.bodyMaxY:
            if logger.isEnabledFor(logging.ERROR):
                logger.error('DE ===== _put:adjusting startPos')
            if self.selection < self.bodyMaxY:
                self.startPos = 0
                if self.selection - int(self.bodyMaxY/2) > 0:
                    self.startPos = self.selection - int(self.bodyMaxY/2)
            elif self.selection > self.number_of_items - self.bodyMaxY:
                self.startPos = self.number_of_items - self.bodyMaxY
            else:
                self.startPos = int(self.selection+1/self.bodyMaxY) - int(self.bodyMaxY/2)
        if logger.isEnabledFor(logging.ERROR):
            logger.error('DE ===== _put:startPos -> {0}, force = {1}'.format(self.startPos, force))

    def setStation(self, number):
        """ Select the given station number """
        # If we press up at the first station, we go to the last one
        # and if we press down on the last one we go back to the first one.
        if number < 0:
            number = len(self.stations) - 1
        elif number >= len(self.stations):
            number = 0

        self.selection = number

        if self.selection - self.startPos >= self.bodyMaxY:
            self.startPos = self.selection - self.bodyMaxY + 1
        elif self.selection < self.startPos:
            self.startPos = self.selection

    def playSelectionBrowser(self):
            #### self._cnf.browsing_station_service = True
            # Add a history item to preserve browsing_station_service
            # Need to add TITLE, if service found
            self._cnf.add_to_playlist_history(self.stations[self.selection][0], 
                    '', '', browsing_station_service=True)
            self._check_to_open_playlist()

    def playSelection(self):
        if self.stations[self.selection][3]:
            self.playSelectionBrowser()
        else:
            self.playing = self.selection
            self._last_played_station = self.stations[self.selection][0]
            stream_url = ''
            if self._cnf.browsing_station_service:
                if self._cnf.online_browser.have_to_retrieve_url:
                    self.log.display_help_message = False
                    self.log.write('Station: "' + self._last_played_station + '" - Retrieving URL...')
                    stream_url = self._cnf.online_browser.url(self.selection)
            if not stream_url:
                stream_url = self.stations[self.selection][1]
            try:
                enc = self.stations[self.selection][2].strip()
            except:
                enc = ''
            self.log.display_help_message = False
            self.log.write('Playing ' + self._last_played_station)
            try:
                self.player.play(self._last_played_station, stream_url, self.get_active_encoding(enc))
            except OSError:
                self.log.write('Error starting player.'
                               'Are you sure a supported player is installed?')

    def connectionFailed(self):
        old_playing = self.playing
        self.stopPlayer(False)
        self.selections[self.ws.NORMAL_MODE][2] = -1
        if self.ws.window_mode == self.ws.NORMAL_MODE:
            if self.ws.operation_mode == self.ws.NORMAL_MODE:
                self.refreshBody()
        else:
            self.playing = old_playing
            #self._update_redisplay_list()
            #self._redisplay_transient_window()
            self.refreshBody(start=1)
        if logger.isEnabledFor(logging.INFO):
            logger.info('start of playback NOT detected!!!')
        self.player.stop_mpv_status_update_thread = True
        self.log.write('Failed to connect to: "{}"'.format(self._last_played_station))
        if self._random_requested and \
                self.ws.operation_mode == self.ws.NORMAL_MODE:
            if logger.isEnabledFor(logging.INFO):
                logger.info('Looking for a working station (random is on)')
            self.play_random()

    def stopPlayer(self, show_message=True):
        """ stop player """
        try:
            self.player.close()
        except:
            pass
        finally:
            self.playing = -1
            if show_message:
                self.log.write('{}: Playback stopped'.format(self._format_player_string()), thread_lock=None, help_msg=True)
                #self.log.write_right('Press ? for help')
            #self.log.write('Playback stopped')

    def removeStation(self):
        if self._cnf.confirm_station_deletion:
            if self._cnf.locked:
                txt = '''Are you sure you want to delete station:
                "|{}|"?

                Press "|y|" to confirm, or any other key to cancel'''
            else:
                txt = '''Are you sure you want to delete station:
                "|{}|"?

                Press "|y|" to confirm, "|Y|" to confirm and not
                be asked again, or any other key to cancel'''

            # truncate parameter to text width
            mwidth = self._get_message_width_from_string(txt)
            msg = self.stations[self.selection][0]
            if len(msg) > mwidth - 3:
                msg = msg[:mwidth-6] + '...'

            self._show_help(txt.format(msg),
                    self.ws.REMOVE_STATION_MODE, caption = ' Station Deletion ',
                    prompt = '', is_message=True)
        else:
            self.ws.operation_mode = self.ws.REMOVE_STATION_MODE
            curses.ungetch('y')

    def saveCurrentPlaylist(self, stationFile =''):
        ret = self._cnf.save_playlist_file(stationFile)
        self.refreshBody()
        if ret == -1:
            self._print_save_playlist_error_1()
        elif ret == -2:
            self._print_save_playlist_error_2()
        if ret < 0 and logger.isEnabledFor(logging.DEBUG):
            logger.debug('Error saving playlist: "{}"'.format(self._cnf.station_path))
        return ret

    def reloadCurrentPlaylist(self, mode):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Reloading current playlist')
        self._set_active_stations()
        #txt = '''Reloading playlist. Please wait...'''
        #self._show_help(txt, self.ws.NORMAL_MODE, caption=' ', prompt=' ', is_message=True)
        self.jumpnr = ''
        self._backslash = False
        ret = self._cnf.read_playlist_file(self._cnf.station_path)
        if ret == -1:
            self.stations = self._cnf.playlists
            self.ws.close_window()
            self.refreshBody()
            self._print_playlist_reload_error()
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Error reloading playlist: "{}"'.format(self._cnf.station_path))
        else:
            self.number_of_items = ret
            self._align_stations_and_refresh(self.ws.NORMAL_MODE)
            self.ws.close_window()
            self.refreshBody()
        return

    def readPlaylists(self):
        num_of_playlists, playing = self._cnf.read_playlists()
        if num_of_playlists == 0:
            txt = '''No playlists found!!!

            This should never have happened; PyRadio is missing its
            default playlist. Therefore, it has to terminate now.
            It will re-create it the next time it is lounched.
            '''
            self._show_help(txt.format(self._cnf.station_file_name),
                    mode_to_set = self.ws.PLAYLIST_SCAN_ERROR_MODE,
                    caption = ' Error ',
                    prompt = ' Press any key to exit ',
                    is_message=True)
            if logger.isEnabledFor(logging.ERROR):
                logger.error('No playlists found!!!')
        return num_of_playlists, playing

    def _format_player_string(self):
        if self.player.PLAYER_CMD == 'cvlc':
            return 'vlc'
        return self.player.PLAYER_CMD

    def _show_theme_selector_from_config(self):
        self._theme_name = self._config_win._config_options['theme'][1]
        # if logger.isEnabledFor(logging.ERROR):
        #     logger.error('DE\n\nreseting self._theme_name = {}\n\n'.format(self._theme_name))
        #self.ws.previous_operation_mode = self.ws.operation_mode
        self.ws.operation_mode = self.ws.THEME_MODE
        self._show_theme_selector(changed_from_config=True)

    def _show_theme_selector(self, changed_from_config=False):
        self.jumpnr = ''
        self._backslash = False
        self._random_requested = False
        self._theme_selector = None
        #if logger.isEnabledFor(logging.ERROR):
        #    logger.error('DE\n\nself._theme = {0}\nself._theme_name = {1}\nself._cnf.theme = {2}\n\n'.format(self._theme, self._theme_name, self._cnf.theme))
        self._theme_selector = PyRadioThemeSelector(self.outerBodyWin,
                self._cnf, self._theme, self._theme_name,
                self._theme._applied_theme_max_colors, self._cnf.theme,
                4, 3, 4, 5, 6, 9, self._theme.getTransparency())
                #'/home/spiros/edit.log')
        self._theme_selector.changed_from_config = changed_from_config
        self._theme_selector.show()

    def _get_message_width_from_list(self, lines):
        mwidth = 0
        for n in lines:
            llen = len(n.replace('|', ''))
            if llen > mwidth:
                mwidth = llen
        return mwidth

    def _get_message_width_from_string(self, txt):
        lines = txt.split('\n')
        st_lines = [item.replace('\r','') for item in lines]
        lines = [item.strip() for item in st_lines]
        return self._get_message_width_from_list(lines)

    def _show_help(self, txt,
                mode_to_set=0,
                caption=' Help ',
                prompt=' Press any key to hide ',
                too_small_msg='Window too small to show message',
                is_message=False):
        """ Display a help, info or question window.  """
        if mode_to_set == self.ws.MAIN_HELP_MODE:
            caption = ' Help (1/2) '
            prompt=' Press n/p or any other key to hide '
        elif mode_to_set == self.ws.MAIN_HELP_MODE_PAGE_2:
            caption = ' Help (2/2) '
            prompt=' Press n/p or any other key to hide '
        self.helpWinContainer = None
        self.helpWin = None
        self.ws.operation_mode = mode_to_set
        txt_col = curses.color_pair(5)
        box_col = curses.color_pair(3)
        caption_col = curses.color_pair(4)
        lines = txt.split('\n')
        st_lines = [item.replace('\r','') for item in lines]
        lines = [item.strip() for item in st_lines]

        if mode_to_set in self._help_metrics.keys():
            inner_height, inner_width, outer_height, outer_width = self._help_metrics[mode_to_set]
        else:
            inner_height = len(lines) + 2
            inner_width = self._get_message_width_from_list(lines) + 4
            outer_height = inner_height + 2
            outer_width = inner_width + 2
            self._help_metrics[mode_to_set] = [inner_height, inner_width, outer_height, outer_width]
            if mode_to_set == self.ws.MAIN_HELP_MODE:
                self._help_metrics[self.ws.MAIN_HELP_MODE_PAGE_2] = self._help_metrics[mode_to_set]

        if ((self.ws.window_mode == self.ws.CONFIG_MODE and \
                self.ws.operation_mode > self.ws.CONFIG_HELP_MODE) or \
                (self.ws.window_mode == self.ws.NORMAL_MODE and \
                self.ws.operation_mode == self.ws.SELECT_ENCODING_HELP_MODE)) and \
                self.ws.operation_mode != self.ws.ASK_TO_CREATE_NEW_THEME_MODE:
            use_empty_win = True
            height_to_use = outer_height
            width_to_use = outer_width
        else:
            use_empty_win = False
            height_to_use = inner_height
            width_to_use = inner_width
        if self.maxY - 2 < outer_height or self.maxX < outer_width:
            txt = too_small_msg
            prompt = ''
            caption = ''
            inner_height = 3
            inner_width = len(txt) + 4
            if use_empty_win:
                height_to_use = inner_height +2
                width_to_use = inner_width + 2
            else:
                height_to_use = inner_height
                width_to_use = inner_width
            if self.maxX < width_to_use:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('  ***  Window too small even to show help warning  ***')
                self.ws.close_window()
                self.refreshBody()
                return
            lines = [ txt , ]
        if use_empty_win:
            self.helpWinContainer = curses.newwin(height_to_use,width_to_use,int((self.maxY-height_to_use)/2),int((self.maxX-width_to_use)/2))
            self.helpWinContainer.bkgdset(' ', box_col)
            self.helpWinContainer.erase()
        self.helpWin = curses.newwin(inner_height,inner_width,int((self.maxY-inner_height)/2),int((self.maxX-inner_width)/2))
        self.helpWin.bkgdset(' ', box_col)
        self.helpWin.erase()
        self.helpWin.box()
        if is_message:
            start_with = txt_col
            follow = caption_col
        else:
            start_with = caption_col
            follow = txt_col
        if caption.strip():
            self.helpWin.addstr(0, int((inner_width-len(caption))/2), caption, caption_col)
        splited = []
        for i, n in enumerate(lines):
            #a_line = self._replace_starting_undesscore(n)
            a_line = n
            if a_line.startswith('%'):
                self.helpWin.move(i + 1, 0)
                try:
                    self.helpWin.addstr('├', curses.color_pair(3))
                    self.helpWin.addstr('─' * (inner_width - 2), curses.color_pair(3))
                    self.helpWin.addstr('┤', curses.color_pair(3))
                except:
                    self.helpWin.addstr('├'.encode('utf-8'), curses.color_pair(3))
                    self.helpWin.addstr('─'.encode('utf-8') * (inner_width - 2), curses.color_pair(3))
                    self.helpWin.addstr('┤'.encode('utf-8'), curses.color_pair(3))
                self.helpWin.addstr(i + 1, inner_width-len(a_line[1:]) - 1, a_line[1:].replace('_', ' '), caption_col)
                #self.helpWin.addstr(i + 1, int((inner_width-len(a_line[1:]))/2), a_line[1:].replace('_', ' '), caption_col)
            elif a_line.startswith('!'):
                self.helpWin.move(i + 1, 2)
                lin = ' ' + a_line[1:] + ' '
                llin = len(lin)

                wsp = inner_width - 4
                try:
                    self.helpWin.addstr('─' * wsp , curses.color_pair(3))
                except:
                    self.helpWin.addstr('─'.encode('utf-8') * wsp, curses.color_pair(3))
                self.helpWin.addstr(i + 1, 5, lin, caption_col)

            else:
                splited = a_line.split('|')
                self.helpWin.move(i + 1, 2)
                for part, part_string in enumerate(splited):
                    if part_string.strip():
                        if part == 0 or part % 2 == 0:
                            self.helpWin.addstr(splited[part].replace('_', ' '), start_with)
                        else:
                            self.helpWin.addstr(splited[part].replace('_', ' '), follow)
        if prompt.strip():
            self.helpWin.addstr(inner_height - 1, int(inner_width-len(prompt)-1), prompt)
        if use_empty_win:
            self.helpWinContainer.refresh()
        self.helpWin.refresh()

    def _replace_starting_undesscore(self, a_string):
        ret = ''
        for i, ch in enumerate(a_string):
            if ch == '_':
                ret += ' '
            else:
                ret += a_string[i:]
                break
        return ret

    def _format_playlist_line(self, lineNum, pad, station):
        """ format playlist line so that if fills self.maxX """
        line = "{0}. {1}".format(str(lineNum + self.startPos + 1).rjust(pad), station[0])
        f_data = ' [{0}, {1}]'.format(station[2], station[1])
        if version_info < (3, 0):
            if cjklen(line.decode('utf-8', 'replace')) + cjklen(f_data.decode('utf-8', 'replace')) > self.bodyMaxX:
                """ this is too long, try to shorten it
                    by removing file size """
                f_data = ' [{0}]'.format(station[1])
            if cjklen(line.decode('utf-8', 'replace')) + cjklen(f_data.decode('utf-8', 'replace')) > self.bodyMaxX:
                """ still too long. start removing chars """
                while cjklen(line.decode('utf-8', 'replace')) + cjklen(f_data.decode('utf-8', 'replace')) > self.bodyMaxX - 1:
                    f_data = f_data[:-1]
                f_data += ']'
            """ if too short, pad f_data to the right """
            if cjklen(line.decode('utf-8', 'replace')) + cjklen(f_data.decode('utf-8', 'replace')) < self.bodyMaxX:
                while cjklen(line.decode('utf-8', 'replace')) + cjklen(f_data.decode('utf-8', 'replace')) < self.maxX:
                    line += ' '
        else:
            if cjklen(line) + cjklen(f_data) > self.bodyMaxX:
                """ this is too long, try to shorten it
                    by removing file size """
                f_data = ' [{0}]'.format(station[1])
            if cjklen(line) + cjklen(f_data) > self.bodyMaxX:
                """ still too long. start removing chars """
                while cjklen(line) + cjklen(f_data) > self.bodyMaxX - 1:
                    f_data = f_data[:-1]
                f_data += ']'
            """ if too short, pad f_data to the right """
            if cjklen(line) + cjklen(f_data) < self.maxX:
                while cjklen(line) + cjklen(f_data) < self.bodyMaxX:
                    line += ' '
        line += f_data
        return line

    def _format_station_line(self, line):
        if version_info < (3, 0):
            if len(line.decode('utf-8', 'replace')) != cjklen(line.decode('utf-8', 'replace')):
                while cjklen(line.decode('utf-8', 'replace')) > self.bodyMaxX:
                    line = line[:-1]
                return line
            else:
                return line[:self.bodyMaxX]
        else:
            if len(line) != cjklen(line):
                while cjklen(line) > self.bodyMaxX:
                    line = line[:-1]
                return line
            else:
                return line[:self.bodyMaxX]

    def _print_help(self):
        #logger.error('DE \n\nself.ws.operation_mode = {}'.format(self.ws.operation_mode))
        if self.ws.operation_mode in self._display_help.keys():
            self._display_help[self.ws.operation_mode]()
        else:
            self._redisplay[self.ws.operation_mode]()

    def _show_playlist_recovered(self):
        txt = 'Playlist recoverd!'
        self._show_help(txt, mode_to_set=self.ws.operation_mode, caption='',
                prompt='', is_message=True)
        # start 1250 ms counter
        th = threading.Timer(1.25, self.closeRecoveryNotification)
        th.start()

    def closeRecoveryNotification(self, *arg, **karg):
        #arg[1].acquire()
        self._cnf.playlist_recovery_result = 0
        #arg[1].release()
        self.refreshBody()

    def _show_no_more_playlist_history(self):
        txt = 'Top of history reached!!!'
        self._show_help(txt, mode_to_set=self.ws.HISTORY_EMPTY_NOTIFICATION, caption='',
                prompt='', is_message=True)
        # start 1250 ms counter
        th = threading.Timer(.5, self.closeHistoryEmptyNotification)
        th.start()

    def closeHistoryEmptyNotification(self):
        self.ws.close_window()
        self.refreshBody()

    def _show_theme_not_supported(self):
        if self._cnf.theme_not_supported_notification_shown:
            return
        txt = 'Error loading selected theme!\n____Using default theme.'
        self._show_help(txt, mode_to_set=self.ws.operation_mode, caption='',
                prompt='', is_message=True)
        # start 1750 ms counter
        if self._theme_not_supported_thread:
            if self._theme_not_supported_thread.is_alive:
                self._theme_not_supported_thread.cancel()
            self._theme_not_supported_thread = None
        self._theme_not_supported_thread = threading.Timer(self._theme_not_supported_notification_duration, self.closeThemeNotSupportedNotification)
        self._theme_not_supported_thread.start()
        curses.doupdate()

    def closeThemeNotSupportedNotification(self, *arg, **karg):
        #arg[1].acquire()
        self._cnf.theme_not_supported = False
        self._cnf.theme_not_supported_notification_shown = True
        self._theme_not_supported_notification_duration = 0.75
        #arg[1].release()
        self.refreshBody()

    def _show_main_help(self):
        txt = """Up|,|j|,|PgUp|,
                 Down|,|k|,|PgDown    |Change station selection.
                 g| / |<n>G         |Jump to first or n-th / last station.
                 H M L            |Go to top / middle / bottom of screen.
                 P                |Go to |P|laying station.
                 Enter|,|Right|,|l    |Play selected station.
                 r                |Select and play a random station.
                 Space|,|Left|,|h     |Stop / start playing selected station.
                 Esc|,|q            |Quit.
                 !Volume management
                 -|/|+| or |,|/|.       |Change volume.
                 m| / |v            ||M|ute player / Save |v|olume (not in vlc).
                 !Misc
                 o| / |s| / |R        ||O|pen / |S|ave / |R|eload playlist.
                 t| / |T            |Load |t|heme / |T|oggle transparency.
                 c                |Open Configuration window."""
        self._show_help(txt, mode_to_set=self.ws.MAIN_HELP_MODE)

    def _show_main_help_page_2(self):
        txt = """!Playlist editing
                 a| / |A            |Add / append new station.
                 e                |Edit current station.
                 E                |Change station's encoding.
                 DEL|,|x            |Delete selected station.
                 !Playlist history
                 \\\\               |Open previous playlist.
                 \\]               |Open first opened playlist.
                 !Moving stations
                 J                |Create a |J|ump tag.
                 <n>^U|,|<n>^D      |Move station |U|p / |D|own.
                 ||_________________|If a |jump tag| exists, move it there.
                 !Searching
                 /| / |n| / |N        |Search, go to next / previous result."""
        self._show_help(txt, mode_to_set=self.ws.MAIN_HELP_MODE_PAGE_2)

    def _show_playlist_help(self):
        txt = """Up|,|j|,|PgUp|,
                 Down|,|k|,|PgDown    |Change playlist selection.
                 g| / |<n>G         |Jump to first or n-th / last playlist.
                 M| / |P            |Jump to |M|iddle / loaded |P|laylist.
                 Enter|,|Right|,|l    |Open selected playlist.
                 r                |Re-read playlists from disk.
                 /| / |n| / |N        |Search, go to next / previous result.
                 Esc|,|q|,|Left|,|h     |Cancel.
                 %_Player Keys_
                 -|/|+| or |,|/|.       |Change volume.
                 m| / |v            ||M|ute player / Save |v|olume (not in vlc).
                 %_Other Keys_
                 t| / |T            |Load |t|heme / |T|oggle transparency."""
        self._show_help(txt, mode_to_set=self.ws.PLAYLIST_HELP_MODE, caption=' Playlist Help ')

    def _show_theme_help(self):
            txt = """Up|,|j|,|PgUp|,
                     Down|,|k|,|PgDown    |Change theme selection.
                     g| / |<n>G         |Jump to first or n-th / last theme.
                     Enter|,|Right|,|l    |Apply selected theme.
                     Space            |Apply theme and make it default.
                     s                |Make theme default and close window.
                     /| / |n| / |N        |Search, go to next / previous result.
                     Esc|,|q|,|Left|,|h     |Close window.
                     %_Player Keys_
                     -|/|+| or |,|/|.       |Change volume.
                     m| / |v            ||M|ute player / Save |v|olume (not in vlc)."""
            self._show_help(txt, mode_to_set=self.ws.THEME_HELP_MODE, caption=' Themes Help ')

    def _show_search_help(self):
        if platform.lower().startswith('darwin'):
            txt = """Left| / |Right        |Move to next / previous character.
            HOME|,|^A| / |END|,|^E    |Move to start / end of line.
            ^W| / |^K             |Clear to start / end of line.
            ^U                  |Clear line.
            DEL|,|^D              |Delete character.
            Backspace|,|^H        |Backspace (delete previous character).
            Up|,|^P| / |Down|,|^N     |Get previous / next history item.
            \\?| / |\\\\             |Insert a "|?|" or a "|\\|", respectively.
            Enter| / |Esc         |Perform / cancel search.

            |Managing player volume does not work in search mode.
            """
        else:
            txt = """Left| / |Right        |Move to next / previous character.
            M-F| / |M-B           |Move to next / previous word.
            HOME|,|^A| / |END|,|^E    |Move to start / end of line.
            ^W| / |M-D|,|^K         |Clear to start / end of line.
            ^U                  |Clear line.
            DEL|,|^D              |Delete character.
            Backspace|,|^H        |Backspace (delete previous character).
            Up|,|^P| / |Down|,|^N     |Get previous / next history item.
            \\?| / |\\\\             |Insert a "|?|" or a "|\\|", respectively.
            Enter| / |Esc         |Perform / cancel search.

            |Managing player volume does not work in search mode.
            """
            if platform.startswith('win'):
                txt = txt.replace('M-', 'A-')
        self._show_help(txt, mode_to_set=self.ws.SEARCH_HELP_MODE, caption=' Search Help ')

    def _show_line_editor_help(self):
        if platform.lower().startswith('darwin'):
            txt = """Left| / |Right        |Move to next / previous character.
            HOME|,|^A| / |END|,|^E    |Move to start / end of line.
            ^W| / |^K             |Clear to start / end of line.
            ^U                  |Clear line.
            DEL|,|^D              |Delete character.
            Backspace|,|^H        |Backspace (delete previous character).
            Up| / |Down           |Go to previous / next field.
            \\?| / |\\\\             |Insert a "|?|" or a "|\\|", respectively.
            Esc                 |Cancel operation.

            |Managing player volume does not work in editing mode.
            """
        else:
            txt = """Left| / |Right        |Move to next / previous character.
            M-F| / |M-B           |Move to next / previous word.
            HOME|,|^A| / |END|,|^E    |Move to start / end of line.
            ^W| / |M-D|,|^K         |Clear to start / end of line.
            ^U                  |Clear line.
            DEL|,|^D              |Delete character.
            Backspace|,|^H        |Backspace (delete previous character).
            Up| / |Down           |Go to previous / next field.
            \\?| / |\\\\             |Insert a "|?|" or a "|\\|", respectively.
            Esc                 |Cancel operation.

            |Managing player volume does not work in editing mode.
            """
            if platform.startswith('win'):
                txt = txt.replace('M-', 'A-')
        self._show_help(txt, mode_to_set=self.ws.LINE_EDITOR_HELP, caption=' Line Editor Help ')

    def _show_config_help(self):
            txt = """Up|,|j|,|PgUp|,
                     Down|,|k|,|PgDown          |Change option selection.
                     g|,|Home| / |G|,|End         |Jump to first / last option.
                     Enter|,|Space|,|Right|,|l    |Change option value.
                     r                      |Revert to saved values.
                     d                      |Load default values.
                     s                      |Save config.
                     Esc|,|q|,|Left|,|h           |Cancel.
                     %_Player Keys_
                     -|/|+| or |,|/|.             |Change volume.
                     m| / |v                  ||M|ute player / Save |v|olume (not in vlc)."""
            self._show_help(txt, mode_to_set=self.ws.CONFIG_HELP_MODE, caption=' Configuration Help ')

    def _show_config_player_help(self):
            txt = """Up|,|j|,|Down|,|k      |Change player selection.
                     TAB              |Move selection to other column.
                     Enter|,|Space      |Move player to other column.
                     Right|,|l          |Move player to the end of the list.
                     r                |Revert to saved values.
                     s                |Save players.
                     Esc|,|q|,|Left|,|h     |Cancel.
                     %_Player Keys_
                     -|/|+| or |,|/|.       |Change volume.
                     m| / |v            ||M|ute player / Save |v|olume (not in vlc)."""
            self._show_help(txt, mode_to_set=self.ws.SELECT_PLAYER_HELP_MODE, caption=' Player Selection Help ')

    def _show_config_playlist_help(self):
            txt = """Up|,|j|,|PgUp|,
                     Down|,|k|,|PgDown    |Change playlist selection.
                     g| / |<n>G         |Jump to first or n-th / last playlist.
                     Enter|,|Space|,
                     Right|,|l          |Select default playlist.
                     /| / |n| / |N        |Search, go to next / previous result.
                     r                |Revert to saved value.
                     Esc|,|q|,|Left|,|h     |Canel.
                     %_Player Keys_
                     -|/|+| or |,|/|.       |Change volume.
                     m| / |v            ||M|ute player / Save |v|olume (not in vlc)."""
            self._show_help(txt, mode_to_set=self.ws.SELECT_PLAYLIST_HELP_MODE, caption=' Playlist Selection Help ')

    def _show_config_station_help(self):
            txt = """Up|,|j|,|PgUp|,
                     Down|,|k|,|PgDown    |Change station selection.
                     g| / |<n>G         |Jump to first or n-th / last station.
                     M                |Jump to the middle of the list.
                     Enter|,|Space|,
                     Right|,|l          |Select default station.
                     /| / |n| / |N        |Search, go to next / previous result.
                     r                |Revert to saved value.
                     Esc|,|q|,|Left|,|h     |Canel.
                     %_Player Keys_
                     -|/|+| or |,|/|.       |Change volume.
                     m| / |v            ||M|ute player / Save |v|olume (not in vlc)."""
            self._show_help(txt, mode_to_set=self.ws.SELECT_STATION_HELP_MODE, caption=' Station Selection Help ')

    def _show_config_encoding_help(self):
            txt = """Arrows|,|h|,|j|,|k|,|l|,|PgUp|,|,PgDn
                     g|,|Home|,|G|,|End     |Change encoding selection.
                     Enter|,|Space|,|s    |Save encoding.
                     r                |Revert to saved value.
                     Esc|,|q            |Cancel.
                     %_Player Keys_
                     -|/|+| or |,|/|.       |Change volume.
                     m| / |v            ||M|ute player / Save |v|olume (not in vlc)."""
            self._show_help(txt, mode_to_set=self.ws.SELECT_ENCODING_HELP_MODE, caption=' Encoding Selection Help ')

    def _print_session_locked(self):
        txt = '''This session is |locked| by another |PyRadio instance|.

                 You can still play stations, load and edit playlists,
                 load and test themes, but any changes will |not| be
                 recorded in the configuration file.

                 If you are sure this is the |only| active |PyRadio|
                 instance, exit |PyRadio| now and execute the following
                 command: |pyradio --unlock|
                 '''
        self._show_help(txt, self.ws.SESSION_LOCKED_MODE,
                caption = ' Session Locked ',
                prompt = ' Press any key... ',
                is_message=True)

    def _print_not_implemented_yet(self):
        self.ws.previous_operation_mode = self.ws.operation_mode
        txt = '''This feature has not been implemented yet...
        '''
        self._show_help(txt, self.ws.NOT_IMPLEMENTED_YET_MODE,
                caption = ' PyRadio ',
                prompt = ' Press any key... ',
                is_message=True)

    def _print_handle_foreign_playlist(self):
        txt ='''This is a "|foreign|" playlist (i.e. it does not
            reside in PyRadio's config directory). If you
            want to be able to easily load it again in the
            future, it should be copied there.

            Do you want to copy it in the config directory?

            Press "|y|" to confirm or "|n|" to reject'''
        self._show_help(txt, self.ws.FOREIGN_PLAYLIST_ASK_MODE,
                caption = ' Foreign playlist ',
                prompt = ' ',
                is_message=True)

    def _print_foreign_playlist_message(self):
        """ reset previous message """
        self.ws.close_window()
        self.refreshBody()
        """ display new message """
        txt='''A playlist by this name:
            __"|{0}|"
            already exists in the config directory.

            This playlist was saved as:
            __"|{1}|"
            '''.format(self._cnf.foreign_title,
                    self._cnf.station_title)
        self._show_help(txt, self.ws.FOREIGN_PLAYLIST_MESSAGE_MODE,
                caption = ' Foreign playlist ',
                prompt = ' Press any key ',
                is_message=True)

    def _print_foreign_playlist_copy_error(self):
        """ reset previous message """
        self.ws.close_window()
        self.refreshBody()
        txt ='''Foreign playlist copying |failed|!

            Make sure the file is not open with another
            application and try to load it again
            '''
        self._show_help(txt, self.ws.FOREIGN_PLAYLIST_COPY_ERROR_MODE,
                caption = ' Error ',
                prompt = ' Press any key ',
                is_message=True)

    def _print_playlist_recovery_error(self):
        if self._playlist_error_message:
            txt = self._playlist_error_message
        else:
            if self._cnf.playlist_recovery_result == 1:
                txt = """Both a playlist file (CSV) and a playlist backup
    file (TXT) exist for the selected playlist. In
    this case, PyRadio would try to delete the CSV
    file, and then rename the TXT file to CSV.\n
    Unfortunately, deleting the CSV file has failed,
    so you have to manually address the issue.
    """
            else:
                txt = """A playlist backup file (TXT) has been found for
    the selected playlist. In this case, PyRadio would
    try to rename this file to CSV.\n
    Unfortunately, renaming this file has failed, so
    you have to manually address the issue.
    """
        self._show_help(txt, self.ws.PLAYLIST_RECOVERY_ERROR_MODE,
                caption = ' Error ',
                prompt = ' Press any key ',
                is_message=True)

    def _print_playlist_not_found_error(self):
        if self._playlist_error_message:
            txt = self._playlist_error_message
        else:
            txt = """Playlist |not| found!

                This means that the playlist file was deleted
                (or renamed) some time after you opened the
                Playlist Selection window.
                """
        self._show_help(txt, self.ws.PLAYLIST_NOT_FOUND_ERROR_MODE,
                caption = ' Error ',
                prompt = ' Press any key ',
                is_message=True)

    def _print_playlist_load_error(self):
        if self._playlist_error_message:
            txt = self._playlist_error_message
        else:
            txt = """Playlist loading |failed|!

                This means that either the file is corrupt,
                or you are not permitted to access it.
                """
        self._show_help(txt, self.ws.PLAYLIST_LOAD_ERROR_MODE,
                caption = ' Error ',
                prompt = ' Press any key ',
                is_message=True)

    def _print_playlist_reload_error(self):
        txt ='''Playlist reloading |failed|!

            You have probably edited the playlist with an
            external program. Please re-edit it and make
            sure that only one "," exists in each line.
            '''
        self._show_help(txt, self.ws.PLAYLIST_RELOAD_ERROR_MODE,
                caption = ' Error ',
                prompt = ' Press any key ',
                is_message=True)

    def _print_py2_editor_error(self):
        txt ='''Non-ASCII characters editing is |not supported!|

            You running |PyRadio| on |Python 2|. As a result, the
            station editor only supports |ASCII characters|, but
            the station name you are trying to edit contains
            |non-ASCII| characters.

            To edit this station, either run |PyRadio| on |Python 3|,
            or edit the playlist with an external editor and then
            reload the playlist.
            '''
        self._show_help(txt, self.ws.PY2_EDITOR_ERROR,
                caption = ' Error ',
                prompt = ' Press any key ',
                is_message=True)

    def _print_requests_not_installed_error(self):
        txt = '''Module "|requests|" not found!

        In order to use an online stations directory
        service, the "|requests|" module must be installed.

        Exit |PyRadio| now, install the module (named
        |python-requests| or |python{}-reuqests|) and try
        executing |PyRadio| again.
        '''
        self._show_help(txt.format(python_version[0]), self.ws.REQUESTS_MODULE_NOT_INSTALLED_ERROR,
                caption = ' Module Error ',
                prompt = ' Press any key ',
                is_message=True)

    def _print_unknown_browser_service(self):
        txt = '''The service you are trying to use is not supported.

        The service "|{0}|"
        (url: "|{1}|")
        is not implemented (yet?)

        If you want to help implementing it, please open an
        issue at "|https://github.com/coderholic/pyradio/issues|".
        '''
        self._show_help(txt.format(self.stations[self.selection][0],
                self.stations[self.selection][1]),
                self.ws.UNKNOWN_BROWSER_SERVICE_ERROR,
                caption = ' Unknown Service ',
                prompt = ' Press any key ',
                is_message=True)

    def _print_service_connection_error(self):
        txt = '''Service temporarily unavailable.

        This may mean that your internet connection has
        failed, or that the service has failed, in which
        case you should try again later.
        '''
        self._show_help(txt.format(self.stations[self.selection][0],
                self.stations[self.selection][1]),
                self.ws.SERVICE_CONNECTION_ERROR,
                caption = ' Service Unavailable ',
                prompt = ' Press any key ',
                is_message=True)

    def _show_player_changed_in_config(self):
        txt = '''|PyRadio| default player has changed from
        __"|{0}|"
        to
        __"|{1}|".

        This change may lead to changing the player used,
        and will take effect next time you open |PyRadio|.
        '''
        self._show_help(txt.format(*self._cnf.player_values),
                self.ws.PLAYER_CHANGED_INFO_MODE,
                caption = ' Default Player Changed ',
                prompt = ' Press any key ',
                is_message=True)

    def _print_playlist_reload_confirmation(self):
        if self._cnf.locked:
            txt ='''This playlist has not been modified within
                PyRadio. Do you still want to reload it?

                Press "|y|" to confirm, or any other key to cancel'''
        else:
            txt ='''This playlist has not been modified within
                PyRadio. Do you still want to reload it?

                Press "|y|" to confirm, "|Y|" to confirm and not
                be asked again, or any other key to cancel'''
        self._show_help(txt, self.ws.PLAYLIST_RELOAD_CONFIRM_MODE,
                caption = ' Playlist Reload ',
                prompt = ' ',
                is_message=True)

    def _print_playlist_dirty_reload_confirmation(self):
        if self._cnf.locked:
            txt ='''This playlist has been modified within PyRadio.
                If you reload it now, all modifications will be
                lost. Do you still want to reload it?

                Press "|y|" to confirm, or "|n|" to cancel'''
        else:
            txt ='''This playlist has been modified within PyRadio.
                If you reload it now, all modifications will be
                lost. Do you still want to reload it?

                Press "|y|" to confirm, "|Y|" to confirm and not be
                asked again, or "|n|" to cancel'''
        self._show_help(txt, self.ws.PLAYLIST_DIRTY_RELOAD_CONFIRM_MODE,
                caption = ' Playlist Reload ',
                prompt = ' ',
                is_message=True)

    def _print_save_modified_playlist(self, mode):
        if self._cnf.locked:
            txt ='''This playlist has been modified within
                PyRadio. Do you want to save it?

                If you choose not to save it now, all
                modifications will be lost.

                Press "|y|" to confirm, "|n|" to reject,
                or "|q|" or "|ESCAPE|" to cancel'''
        else:
            txt ='''This playlist has been modified within
                PyRadio. Do you want to save it?

                If you choose not to save it now, all
                modifications will be lost.

                Press "|y|" to confirm, "|Y|" to confirm and not
                be asked again, "|n|" to reject, or "|q|" or
                "|ESCAPE|" to cancel'''
        self._show_help(txt, mode,
                caption = ' Playlist Modified ',
                prompt = ' ',
                is_message=True)

    def _print_save_playlist_error_1(self):
        txt = '''Saving current playlist |failed|!

            Could not open file for writing
            "|{}|"
            '''
        self._show_help(txt.format(self._cnf.station_path.replace('.csv', '.txt')),
                mode_to_set = self.ws.SAVE_PLAYLIST_ERROR_1_MODE,
                caption = ' Error ',
                prompt = ' Press any key ',
                is_message=True)

    def _print_save_playlist_error_2(self):
        txt = '''Saving current playlist |failed|!

            You will find a copy of the saved playlist in
            "|{}|"

            Pyradio will open this file when the playlist
            is opened in the future.
            '''
        self._show_help(txt.format(self._cnf.station_path.replace('.csv', '.txt')),
                mode_to_set = self.ws.SAVE_PLAYLIST_ERROR_2_MODE,
                caption = ' Error ',
                prompt = ' Press any key ',
                is_message=True)

    def _print_editor_name_error(self):
        txt = '''
            ___Incomplete Station Data provided!___

            ___Please provide a Station Name.___

            '''
        self._show_help(txt,
                mode_to_set = self.ws.EDIT_STATION_NAME_ERROR,
                caption = ' Error ',
                prompt = ' Press any key ',
                is_message=True)

    def _print_editor_url_error(self):
        if self._station_editor._line_editor[1].string.strip():
            txt = '''
                ___Errorenous Station Data provided!___

                ___Station URL is invalid!___
                ___Please provide a valid Station URL.___

                '''
        else:
            txt = '''
                ___Incomplete Station Data provided!___

                ___Station URL is empty!___
                ___Please provide a valid Station URL.___

                '''
        self._show_help(txt,
                mode_to_set = self.ws.EDIT_STATION_URL_ERROR,
                caption = ' Error ',
                prompt = ' Press any key ',
                is_message=True)

    def _print_ask_to_create_theme(self):
        txt ='''You have requested to edit a |read-only| theme,
            which is not possible. Do you want to create a
            new theme instead?

            Press "|y|" to accept or any other key to cancel.'''
        self._show_help(txt, self.ws.ASK_TO_CREATE_NEW_THEME_MODE,
                caption = ' Read-only theme ',
                prompt = ' ',
                is_message=True)

    def _print_config_save_error(self):
        txt = '''An error occured while saving the configuration file!

            |PyRadio| will try to |restore| your previous settings,
            but in order to do so, it has to |terminate now!

            '''
        self._show_help(txt,
                mode_to_set = self.ws.CONFIG_SAVE_ERROR_MODE,
                caption = ' Error Saving Config ',
                prompt = ' Press any key to exit ',
                is_message=True)

    def _print_update_notification(self):
        txt = '''A new |PyRadio| release (|{0}|) is available!

                 You are strongly encouraged to update now, so that
                 you enjoy new features and bug fixes.

                 You can get more info at:
                 |https://github.com/coderholic/pyradio#installation|
            '''
        self._show_help(txt.format(self._update_version_do_display),
                mode_to_set = self.ws.UPDATE_NOTIFICATION_MODE,
                caption = ' New Release Available ',
                prompt = ' Press any key to hide ',
                is_message=True)
        self._update_version = ''

    def _align_stations_and_refresh(self, cur_mode, a_startPos=-1, a_selection=-1):
        need_to_scan_playlist = False
        """ refresh reference """
        self.stations = self._cnf.stations
        self.number_of_items = len(self.stations)

        if self.number_of_items == 0:
            """ The playlist is empty """
            if self.player.isPlaying():
                self.stopPlayer()
            self.playing,self.selection, self.stations, \
                self.number_of_items = (-1, 0, 0, 0)
            ##self.ws.operation_mode = self.ws.window_mode = self.ws.NORMAL_MODE
            #self.ws.close_window()
            #self.refreshBody()
            return
        else:
            #if logger.isEnabledFor(logging.DEBUG):
            #    logger.debug('self.playing = {}'.format(self.playing))
            if cur_mode == self.ws.REMOVE_STATION_MODE:
                """ Remove selected station """
                if self.player.isPlaying():
                    if self.selection == self.playing:
                        self.stopPlayer()
                        self.playing = -1
                    elif self.selection < self.playing:
                        self.playing -= 1
                else:
                    self.playing = -1

                if self.selection > self.number_of_items - self.bodyMaxY:
                    self.startPos -= 1
                    if self.selection >= self.number_of_items:
                        self.selection -= 1
                if self.startPos < 0:
                    self.startPos = 0
            else:
                if self.player.isPlaying():
                    """ The playlist is not empty """
                    if self.playing > self.number_of_items - 1:
                        """ Previous playing station is now invalid
                            Need to scan playlist """
                        need_to_scan_playlist = True
                    else:
                        if self.stations[self.playing][0] == self.active_stations[1][0]:
                            """ ok, self.playing found, just find selection """
                            self.selection = self._get_station_id(self.active_stations[0][0])
                            if logger.isEnabledFor(logging.DEBUG):
                                logger.debug('** Selected station is {0} at {1}'.format(self.stations[self.selection], self.selection))
                        else:
                            """ station playing id changed, try previous station """
                            self.playing -= 1
                            if self.playing == -1:
                                self.playing = len(self.stations) - 1
                            if self.stations[self.playing][0] == self.active_stations[1][0]:
                                """ ok, self.playing found, just find selection """
                                self.selection = self._get_station_id(self.active_stations[0][0])
                                if logger.isEnabledFor(logging.DEBUG):
                                    logger.debug('** Selection station is {0} at {1}'.format(self.stations[self.playing], self.playing))
                            else:
                                """ self.playing still not found, have to scan playlist """
                                need_to_scan_playlist = True
                else:
                    """ not playing, can i get a selection? """
                    need_to_scan_playlist = True

            if need_to_scan_playlist:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('Scanning playlist for stations...')
                self.selection, self.playing = self._get_stations_ids((
                    self.active_stations[0][0],
                    self.active_stations[1][0]))
                if self.playing == -1:
                    self.stopPlayer()
                need_to_calulate_position = True

                """ calculate new position """
                if self.player.isPlaying():
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug('Setting playing station at {}'.format(self.playing))
                    self.setStation(self.playing)
                else:
                    if self.selection == -1:
                        if a_selection > -1:
                            self.selection = a_selection
                            self.startPos = a_startPos
                        else:
                            self.selection = 0
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug('Setting selection station at {}'.format(self.selection))
                    self.setStation(self.selection)

        if self.selection < 0:
            """ make sure we have a valid selection """
            self.selection = 0
            self.startPos = 0
        """ make sure playing station is visible """
        self._goto_playing_station(changing_playlist=True)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('self.selection = {0}, self.playing = {1}, self.startPos = {2}'.format(self.selection, self.playing, self.startPos))
        self.selections[self.ws.NORMAL_MODE] = [self.selection, self.startPos, self.playing, self._cnf.stations]
        self.refreshBody()

    def _open_playlist(self):
        """ open playlist """
        self._cnf.save_station_position(self.startPos, self.selection, self.playing)
        self._set_active_stations()
        self.jumpnr = ''
        self._backslash = False
        self._random_requested = False
        if self._cnf.browsing_station_service:
            # TODO
            if HAS_REQUESTS:
                txt = '''Connecting to service. Please wait...'''
                self._show_help(txt, self.ws.NORMAL_MODE, caption=' ', prompt=' ', is_message=True)
                try:
                    self._cnf.open_browser(self.stations[self.selection][1])
                except TypeError:
                    pass
                if self._cnf.online_browser:
                    tmp_stations = self._cnf.stations
                    if tmp_stations:
                        #self._cnf.add_to_playlist_history(self._cnf.online_browser.BASE_URL, '', self._cnf.online_browser.TITLE, browsing_station_service=True)
                        self._cnf.station_path = self._cnf.online_browser.BASE_URL
                        self._cnf.station_title = self._cnf.online_browser.title
                        self.stations = tmp_stations[:]
                        self.stations = self._cnf.stations
                        if self.player.isPlaying():
                            self.stopPlayer()
                        self.selection = 0
                        self.startPos = 0
                        self.number_of_items = len(self.stations)
                        self.setupAndDrawScreen()
                        #self.refreshBody()
                    else:
                        self._cnf.remove_from_playlist_history()
                        self._print_service_connection_error()
                        self._cnf.browsing_station_service = False
                else:
                    self._cnf.remove_from_playlist_history()
                    self._print_unknown_browser_service()
                    self._cnf.browsing_station_service = False
            else:
                self._cnf.remove_from_playlist_history()
                self._print_requests_not_installed_error()
                self._cnf.browsing_station_service = False
        else:
            txt = '''Reading playlists. Please wait...'''
            self._show_help(txt, self.ws.NORMAL_MODE, caption=' ', prompt=' ', is_message=True)
            self.selections[self.ws.operation_mode] = [self.selection, self.startPos, self.playing, self._cnf.stations]
            self.ws.window_mode = self.ws.PLAYLIST_MODE
            self.selection, self.startPos, self.playing, self.stations = self.selections[self.ws.operation_mode]
            self.number_of_items, self.playing = self.readPlaylists()
            self.stations = self._cnf.playlists
            if self.number_of_items > 0:
                self.refreshBody()
        return

    def _get_station_id(self, find):
        for i, a_station in enumerate(self.stations):
            if a_station[0] == find:
                return i
        return -1

    def _get_stations_ids(self, find):
        ch = -2
        i_find = [ -1, -1 ]
        debug_str = ('selection', 'playing')
        for j, a_find in enumerate(find):
            if a_find.strip():
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('** Looking for {0} station: "{1}"'.format(debug_str[j], a_find))

                for i, a_station in enumerate(self.stations):
                    if i_find[j] == -1:
                        if j == 1 and find[0] == find[1]:
                            """ No need to scan again for the same station """
                            i_find[1] = i_find[0]
                            if logger.isEnabledFor(logging.DEBUG):
                                logger.debug('** Got it at {}'.format(i_find[0]))
                            break
                        if a_station[0] == a_find:
                            i_find[j] = i
                            if logger.isEnabledFor(logging.DEBUG):
                                logger.debug('** Found at {}'.format(i))
                            ch += 1
                            if ch == 0:
                                break
        return i_find

    def _set_active_stations(self):
        if self.player.isPlaying():
            self.active_stations = [
                    [ self.stations[self.selection][0], self.selection ],
                    [ self.stations[self.playing][0], self.playing ]
                    ]
        else:
            if self.number_of_items > 0:
                self.active_stations = [
                        [ self.stations[self.selection][0], self.selection ],
                        [ '', -1 ] ]
            else:
                self.active_stations = [
                        [ '', self.selection ],
                        [ '', -1 ] ]
        #logger.error('DE active_stations = \n\n{}\n\n'.format(self.active_stations))

    def get_active_encoding(self, an_encoding):
        if an_encoding:
            return an_encoding
        else:
            return self._cnf.default_encoding

    def play_random(self):
        # Pick a random radio station
        if self.number_of_items > 0:
            self.setStation(random.randint(0, len(self.stations)))
            self.playSelection()
            self._put_selection_in_the_middle(force=True)
            self.refreshBody()

    def _toggle_transparency(self, changed_from_config_window=False, force_value=None):
        """ Toggles theme trasparency.

            changed_from_config_window is used to inhibit toggling from within
            Config Window when 'T' is pressed.

            force_value will set trasparency if True or False,
            or toggle trasparency if None
        """
        if self.ws.window_mode == self.ws.CONFIG_MODE and not changed_from_config_window:
            return
        self._theme.toggleTransparency(force_value)
        self._cnf.use_transparency = self._theme.getTransparency()
        if self.ws.operation_mode == self.ws.THEME_MODE:
            self._theme_selector.transparent = self._cnf.use_transparency
        self.headWin.refresh()
        self.bodyWin.refresh()
        self.footerWin.refresh()
        if self._config_win:
            self._config_win._config_options['use_transparency'][1] = self._cnf.use_transparency
            if not changed_from_config_window:
                self._config_win._saved_config_options['use_transparency'][1] = self._cnf.use_transparency
                self._config_win._old_use_transparency = self._cnf.use_transparency

    def _show_config_window(self):
        if self._config_win is None:
            self._config_win = PyRadioConfigWindow(self.outerBodyWin,
                self._cnf,
                self._toggle_transparency,
                self._show_theme_selector_from_config)
        else:
            self._config_win.parent = self.outerBodyWin
            self._config_win.refresh_config_win()

    def detectUpdateThread(self, a_path, a_lock, stop):
        """ a thread to check if an update is available """

        def delay(secs, stop):
            for i in range(0, 2 * secs):
                sleep(.5)
                if stop():
                    return

        def to_ver(this_version):
            a_v = this_version.replace('-r', '.')
            a_l = a_v.split('.')
            a_n_l = []
            for n in a_l:
                a_n_l.append(int(n))
            return a_n_l

        def clean_date_files(files, start=0):
            files_to_delete = files[start+1:]
            for a_file in files_to_delete:
                try:
                    remove(a_file)
                except:
                    pass

        def create_tadays_date_file(a_path):
            d1 = datetime.now()
            now_str = d1.strftime('%Y-%m-%d')
            try:
                with open(path.join(a_path, '.' + now_str + '.date'), 'w') as f:
                    pass
            except:
                pass

        check_days = 10
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('detectUpdateThread: starting...')
        ##################
        #delay(5, stop)
        from pyradio import version as this_version
        connection_fail_count = 0
        delay(random.randint(25, 45), stop)
        if stop():
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('detectUpdateThread: Asked to stop. Stoping...')
            return
        files = glob.glob(path.join(a_path, '.*.date'))
        if files:
            files.sort(reverse=True)
            if len(files) > 1:
                clean_date_files(files)
            a_date = path.split(path.splitext(files[0])[0])[1][1:]


            d1 = datetime.now()
            d2 = datetime.strptime(a_date, '%Y-%m-%d')
            delta = (d1 - d2).days

            if delta >= check_days:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('detectUpdateThread: checking for updates')
            else:
                clean_date_files(files)
                if logger.isEnabledFor(logging.DEBUG):
                    if check_days - delta == 1:
                        logger.debug('detectUpdateThread: Will check again tomorrow...')
                    else:
                        logger.debug('detectUpdateThread: Will check again in {} days...'.format(check_days - delta))
                return

        url = 'https://api.github.com/repos/coderholic/pyradio/tags'
        while True:
            if stop():
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('detectUpdateThread: Asked to stop. Stoping...')
                break
            if version_info < (3, 0):
                try:
                    last_tag = urlopen(url).read(300)
                except:
                    last_tag = None
            else:
                try:
                    with urlopen(url) as https_response:
                        last_tag = https_response.read(300)
                except:
                    last_tag = None

            if stop():
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('detectUpdateThread: Asked to stop. Stoping...')
                break
            if last_tag:
                connection_fail_count = 0
                x = str(last_tag).split('"name":"')
                last_tag = x[1].split('"')[0]
                #last_tag = '0.9.9'
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('detectUpdateThread: Upstream version found: {}'.format(last_tag))
                if this_version == last_tag:
                    clean_date_files(files, -1)
                    create_tadays_date_file(a_path)
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug('detectUpdateThread: No update found. Will check again in {} days. Exiting...'.format(check_days))
                    break
                else:
                    existing_version = to_ver(this_version)
                    new_version = to_ver(last_tag)
                    if existing_version < new_version:
                        if stop():
                            if logger.isEnabledFor(logging.DEBUG):
                                logger.debug('detectUpdateThread: Asked to stop. Stoping...')
                            break
                        # remove all existing date files
                        clean_date_files(files, -1)
                        ############
                        #delay(5 , stop)
                        delay(random.randint(120, 300), stop)
                        if stop():
                            if logger.isEnabledFor(logging.DEBUG):
                                logger.debug('detectUpdateThread: Asked to stop. Stoping...')
                            break
                        # set new verion
                        if logger.isEnabledFor(logging.INFO):
                            logger.info('detectUpdateThread: Update available: {}'.format(last_tag))
                        a_lock.acquire()
                        self._update_version = last_tag
                        a_lock.release()
                        while True:
                            """ Wait until self._update_version becomes ''
                                which means that notification window has been
                                displayed. Then create date file and exit.
                                If asked to terminate, do not write date file """
                            ########################
                            #delay(5, stop)
                            delay(60, stop)
                            if stop():
                                if logger.isEnabledFor(logging.DEBUG):
                                    logger.debug('detectUpdateThread: Asked to stop. Stoping but not writing date file...')
                                return
                            a_lock.acquire()
                            if self._update_version == '':
                                a_lock.release()
                                # create today's date file
                                create_tadays_date_file(a_path)
                                if logger.isEnabledFor(logging.INFO):
                                    logger.info('detectUpdateThread: Terminating after notification issued... I will check again in {} days'.format(check_days))
                                return
                            a_lock.release()
                    else:
                        if logger.isEnabledFor(logging.ERROR):
                            logger.error('detectUpdateThread: Ahead of upstream? (current version: {0}, upstream version: {1})'.format(this_version, last_tag))
                        break

            else:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('detectUpdateThread: Error: Cannot get upstream version!!!')
                connection_fail_count += 1
                if connection_fail_count > 4:
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug('detectUpdateThread: Error: Too many connection failures. Exiting...')
                    break
                delay(60, stop)

    def is_search_mode(self, a_mode):
        for it in self._search_modes.items():
            if it[1] == a_mode:
                return True
        return False

    def _apply_search_result(self, ret, reapply=False):
        def _apply_main_windows(ret):
            self.setStation(ret)
            self._put_selection_in_the_middle(force=True)
        if reapply:
            if self.ws.operation_mode in \
                    [ self._mode_to_search[x] for x in self._mode_to_search.keys() ]:
                _apply_main_windows(ret)
            elif self.ws.operation_mode == self.ws.THEME_MODE:
                self._theme_selector.set_theme(self._theme_selector._themes[ret])
            elif self.ws.operation_mode == self.ws.SELECT_PLAYLIST_MODE:
                self._playlist_select_win.setPlaylistById(ret, adjust=True)
            elif self.ws.operation_mode == self.ws.SELECT_STATION_MODE:
                self._station_select_win.setPlaylistById(ret, adjust=True)
            self.refreshBody()

        else:
            if self.ws.operation_mode in self.search_main_window_modes:
                _apply_main_windows(ret)
            elif self.ws.previous_operation_mode == self.ws.THEME_MODE:
                self._theme_selector.set_theme(self._theme_selector._themes[ret])
            elif self.ws.previous_operation_mode == self.ws.SELECT_PLAYLIST_MODE:
                self._playlist_select_win.setPlaylistById(ret, adjust=True)
            elif self.ws.previous_operation_mode == self.ws.SELECT_STATION_MODE:
                self._station_select_win.setPlaylistById(ret, adjust=True)
            self.ws.close_window()
            self.refreshBody()

    def _show_station_editor(self):
        self._station_editor.set_parent(self.outerBodyWin)

    def _move_station(self, direction):
        if self.jumpnr:
            try:
                target = int(self.jumpnr) - 1
            except:
                return False
            source = self.selection
        elif self._cnf.jump_tag >= 0:
            source = self.selection
            target = self._cnf.jump_tag
            self._cnf.jump_tag = -1
        else:
            source = self.selection
            target = self.selection + direction
        ret = self._cnf.move_station(source, target)
        if ret:
            """ refresh reference """
            self.stations = self._cnf.stations
            self._cnf.dirty_playlist = True
            if self.playing == source:
                self.playing = target
            elif self.playing == target:
                self.playing = source - 1
            self.selection = target
            self.setStation(self.selection)
            self.refreshBody()
        return ret

    def _do_display_notify(self):
        self._update_notify_lock.acquire()
        if self._update_version:
            self._update_version_do_display = self._update_version
            self._print_update_notification()
        self._update_notify_lock.release()

    def _check_to_open_playlist(self):
        if self._cnf.dirty_playlist:
            if self._cnf.auto_save_playlist:
                # save playlist and open playlist
                ret = self.saveCurrentPlaylist()
                if ret == 0:
                    self._open_playlist()
                else:
                    if self._cnf.browsing_station_service:
                        self._cnf.removed_playlist_history_item()
            else:
                # ask to save playlist
                self._print_save_modified_playlist(self.ws.ASK_TO_SAVE_PLAYLIST_WHEN_OPENING_PLAYLIST_MODE)
        else:
            self._open_playlist()

    def _open_playlist_from_history(self, reset=False):
        """Loads a playlist from history

        Parameters
        ----------
        reset
            if True, load the first history item (which will
            always be a local playlist).
            Default is False.

        Returns
        -------
            True:  browsing_station_service goes from True to False
                   i.e. going from online service browsing to local
                   playlist (needs resize to repaint the whole screen
                   and recalculate all windows)
            False: We do not need resize
        """

        if not self._cnf.can_go_back_in_time:
            self._show_no_more_playlist_history()
            return False
        playlist_history = self._cnf.copy_playlist_history()
        #logger.error('DE playlist_history\n\n{}\n\n'.format(playlist_history))
        self._set_active_stations()
        if reset:
            self._cnf.reset_playlist_history()
        removed_playlist_history_item = self._cnf.remove_from_playlist_history()
        err_string = '"|{}|"'.format(self._cnf.station_title)

        #logger.error('DE\n\n Opening: "{}"\n\n'.format(self._cnf.station_path))
        ret = self._cnf.read_playlist_file(self._cnf.station_path)

        if ret == -1:
            #self.stations = self._cnf.playlists
            self._cnf.add_to_playlist_history(*removed_playlist_history_item)
            self._playlist_error_message = ''
            self._playlist_error_message = """Cannot restore playlist
                {}

                The playlist file has been edited (and corrupted)
                time after you opened subsequent playlist(s), or
                its access rights have been changed since then.
                """.format(err_string.center(48, '_'))
            self._print_playlist_load_error()
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Error loading playlist: "{}"'.format(self.stations[self.selection][-1]))
            return False
        elif ret == -2:
            #self.stations = self._cnf.playlists
            self._cnf.add_to_playlist_history(*removed_playlist_history_item)
            self._playlist_error_message = """Cannot restore playlist
                {}

                The playlist file was deleted (or renamed) some
                time after you opened subsequent playlist(s).
                """.format(err_string.center(48, '_'))
            self._print_playlist_not_found_error()
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Playlist not found: "{}"'.format(self.stations[self.selection][-1]))
            return False
        elif ret == -7:
            self._cnf.add_to_playlist_history(*removed_playlist_history_item)
            if self._cnf.playlist_recovery_result == 1:
                self._playlist_error_message = """Cannot restore playlist
                    {}

                    Both a playlist file (CSV) and a playlist backup
                    file (TXT) exist for the selected playlist. In
                    this case, PyRadio would try to delete the CSV
                    file, and then rename the TXT file to CSV.\n
                    Unfortunately, deleting the CSV file has failed,
                    so you have to manually address the issue.
                    """.format(err_string.center(48, '_'))
            else:
                self._playlist_error_message = """Cannot restore playlist
                    {}

                    A playlist backup file (TXT) has been found for
                    the selected playlist. In this case, PyRadio would
                    try to rename this file to CSV.\n
                    Unfortunately, renaming this file has failed, so
                    you have to manually address the issue.
                    """.format(err_string.center(50, '_'))
            self._print_playlist_recovery_error()
            return False
        else:
            self._playlist_error_message = ''
            self.number_of_items = ret
            if removed_playlist_history_item[-1]:
                # coming back from online browser
                self.playing = removed_playlist_history_item[-2]
                self.selection = removed_playlist_history_item[-3]
                self.startPos = removed_playlist_history_item[-4]
            else:
                # coming back from local playlist
                self.selection = self._cnf.history_selection
                self.startPos = self._cnf.history_startPos

            #logger.error('DE old {}'.format(removed_playlist_history_item))
            #for n in self._cnf._ps._p:
            #    logger.error('DE cur {}'.format(n))
            #logger.error('DE \n\nselection = {0}, startPos = {1}, playing = {2}\n\n'.format(self.selection, self.startPos, self.playing))
            self.stations = self._cnf.stations
            self._align_stations_and_refresh(self.ws.PLAYLIST_MODE, 
                    a_startPos=self.startPos,
                    a_selection=self.selection)
            if self.playing < 0:
                self._put_selection_in_the_middle(force=True)
                self.refreshBody()
            if not self._cnf.browsing_station_service and \
                    self._cnf.online_browser:
                if logger.isEnabledFor(logging.INFO):
                    logger.info('Closing online browser!')
                self._cnf.online_browser = None
            # check if browsing_station_service has changed
            if not self._cnf.browsing_station_service and \
                    removed_playlist_history_item[-1]:
                return True
            return False

    def _normal_mode_resize(self):
        if platform.startswith('win'):
            curses.resize_term(0, 0)
            try:
                curses.curs_set(0)
            except:
                pass
        if self.player.isPlaying():
            self.log.display_help_message = False
        self.setupAndDrawScreen()
        if self.selection >= self.number_of_items - self.bodyMaxY and \
                self.number_of_items > self.bodyMaxY:
            self.startPos = self.number_of_items - self.bodyMaxY
            logger.error('DE *** refreshing body from normal resize')
            self.refreshBody()

    def keypress(self, char):
        if self.ws.operation_mode in self._no_keyboard:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Rejecting keyboard input...')
            return

        if self._force_exit or \
                self.ws.operation_mode == self.ws.CONFIG_SAVE_ERROR_MODE:
            return -1
        #if logger.isEnabledFor(logging.ERROR):
        #    logger.error('DE {}'.format(self.ws._dq))

        elif not self._backslash and char == ord('\\') and \
                self.ws.operation_mode == self.ws.NORMAL_MODE:
            self._backslash = True
            return
        elif self._backslash and char == ord('\\') and \
                self.ws.operation_mode == self.ws.NORMAL_MODE:
            self._backslash = False
            if self._cnf.can_go_back_in_time:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('opening previous playlist')
                if self._open_playlist_from_history():
                    self._normal_mode_resize()
            else:
                self._show_no_more_playlist_history()
            return
        elif self._backslash and char == ord(']') and \
                self.ws.operation_mode == self.ws.NORMAL_MODE:
            self._backslash = False
            if self._cnf.can_go_back_in_time:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('opening first playlist')
                if self._open_playlist_from_history(reset=True):
                    self._normal_mode_resize()
            else:
                self._show_no_more_playlist_history()
            return

        elif char in (ord('#'), curses.KEY_RESIZE):
            self._normal_mode_resize()
            return

        elif self.ws.operation_mode in (self.ws.NO_PLAYER_ERROR_MODE, \
                self.ws.CONFIG_SAVE_ERROR_MODE):
            """ if no player, don't serve keyboard """
            return

        elif char == ord('H') and self.ws.operation_mode in \
                (self.ws.NORMAL_MODE, self.ws.PLAYLIST_MODE):
            self.jumpnr = ''
            self._backslash = False
            self._random_requested = False
            if self.number_of_items > 0:
                self.selection = self.startPos
                self.refreshBody()
            return

        elif char == ord('M') and self.ws.operation_mode in \
                (self.ws.NORMAL_MODE, self.ws.PLAYLIST_MODE):
            self.jumpnr = ''
            self._backslash = False
            self._random_requested = False
            if self.number_of_items > 0:
                if self.number_of_items < self.bodyMaxY:
                    self.selection = int(self.number_of_items / 2)
                else:
                    self.selection = self.startPos + int((self.bodyMaxY - 1) / 2)
                self.refreshBody()
            return

        elif char == ord('L') and self.ws.operation_mode in \
                (self.ws.NORMAL_MODE, self.ws.PLAYLIST_MODE):
            self.jumpnr = ''
            self._backslash = False
            self._random_requested = False
            if self.number_of_items > 0:
                if self.number_of_items < self.bodyMaxY:
                    self.setStation(-1)
                else:
                    self.selection = self.startPos + self.bodyMaxY - 1
                self.refreshBody()
            return

        elif char in (ord('t'), ) and \
                self.ws.operation_mode not in (self.ws.EDIT_STATION_MODE,
                    self.ws.ADD_STATION_MODE, self.ws.THEME_MODE) and \
                self.ws.operation_mode not in self.ws.PASSIVE_WINDOWS and \
                not self.is_search_mode(self.ws.operation_mode):
            self.jumpnr = ''
            self._backslash = False
            self._random_requested = False
            self._config_win = None
            self.theme_forced_selection = None
            if self.ws.operation_mode == self.ws.NORMAL_MODE:
                self.selections[self.ws.operation_mode] = [self.selection, self.startPos, self.playing, self.stations]
            #self.ws.previous_operation_mode = self.ws.operation_mode
            #self.ws.operation_mode = self.ws.window_mode = self.ws.THEME_MODE
            self.ws.operation_mode = self.ws.THEME_MODE
            self._show_theme_selector()
            return

        elif char == ord('P') and self.ws.operation_mode in \
                (self.ws.NORMAL_MODE, self.ws.PLAYLIST_MODE):
            self.jumpnr = ''
            self._backslash = False
            self._random_requested = False
            self._goto_playing_station()
            return

        elif self.ws.operation_mode == self.ws.CONFIG_MODE and \
                char not in self._chars_to_bypass:
            if char not in self._chars_to_bypass:
                if char in (ord('r'), ord('d')):
                    self._player_select_win = None
                    self._encoding_select_win = None
                    self._playlist_select_win = None
                    self._station_select_win = None
                ret, ret_list = self._config_win.keypress(char)
                if ret == self.ws.SELECT_PLAYER_MODE:
                    """ Config > Select Player """
                    self.ws.operation_mode = self.ws.SELECT_PLAYER_MODE
                    if self._player_select_win is None:
                        self._player_select_win = PyRadioSelectPlayer(
                                self.outerBodyMaxY,
                                self.outerBodyMaxX,
                                self._config_win._config_options['player'][1])
                    else:
                        self._player_select_win._parent_maxY, self._player_select_win._parent_maxX = self.outerBodyWin.getmaxyx()
                    self._player_select_win.init_window()
                    self._player_select_win.refresh_win()
                    self._player_select_win.setPlayers(self._config_win._config_options['player'][1])
                    self._player_select_win.refresh_selection()

                elif ret == self.ws.SELECT_ENCODING_MODE:
                    """ Config > Select Default Encoding """
                    self.ws.operation_mode = self.ws.SELECT_ENCODING_MODE
                    if self._encoding_select_win is None:
                        self._encoding_select_win = PyRadioSelectEncodings(
                                self.outerBodyMaxY,
                                self.outerBodyMaxX,
                                self._cnf.default_encoding)
                    else:
                        self._encoding_select_win._parent_maxY, self._encoding_select_win._parent_maxX = self.outerBodyWin.getmaxyx()
                    self._encoding_select_win.init_window()
                    self._encoding_select_win.refresh_win()
                    self._encoding_select_win.setEncoding(self._config_win._config_options['default_encoding'][1])

                elif ret == self.ws.SELECT_PLAYLIST_MODE:
                    """ Config > Select Default Playlist """
                    self.ws.operation_mode = self.ws.SELECT_PLAYLIST_MODE
                    if self._playlist_select_win is None:
                        self._playlist_select_win = PyRadioSelectPlaylist(self.bodyWin,
                                self._cnf.stations_dir,
                                self._config_win._config_options['default_playlist'][1])
                    else:
                        self._playlist_select_win._parent_maxY, self._playlist_select_win._parent_maxX = self.bodyWin.getmaxyx()
                    self._playlist_select_win.init_window()
                    self._playlist_select_win.refresh_win()
                    self._playlist_select_win.setPlaylist(self._config_win._config_options['default_playlist'][1])

                elif ret == self.ws.SELECT_STATION_MODE:
                    """ Config > Select Default Station """
                    self.ws.operation_mode = self.ws.SELECT_STATION_MODE
                    if self._station_select_win is None:
                        self._station_select_win = PyRadioSelectStation(self.outerBodyWin,
                                self._cnf.stations_dir,
                                self._config_win._config_options['default_playlist'][1],
                                self._config_win._config_options['default_station'][1])
                    else:
                        self._station_select_win._parent_maxY, self._station_select_win._parent_maxX = self.outerBodyWin.getmaxyx()
                        self._station_select_win.update_playlist_and_station(self._config_win._config_options['default_playlist'][1], self._config_win._config_options['default_station'][1])
                    self._station_select_win.init_window()
                    self._station_select_win.refresh_win()
                    self._station_select_win.setStation(self._config_win._config_options['default_station'][1])

                elif ret >= 0:
                    msg = ( 'Error saving config. Press any key to exit...',
                            'Config saved successfully!',
                            'Config saved - Restarting playback (encoding changed)')
                    self.ws.close_window()
                    self.bodyWin.box()
                    self._print_body_header()
                    self.refreshBody()
                    if ret == 0:
                        ret = self._cnf.save_config()
                        if ret == -1:
                            # Error saving config
                            if self.player.isPlaying():
                                self.stopPlayer()
                                self.refreshBody()
                            self.log.display_help_message = False
                            self.log.write(msg[0], thread_lock=None, help_msg=False)
                            self._print_config_save_error()
                        elif ret == 0:
                            # Config saved successfully
                            if self.player.isPlaying():
                                if self._cnf.opts['default_encoding'][1] == self._old_config_encoding:
                                    self.log.write(msg[1])
                                    self.player.threadUpdateTitle(self.player.status_update_lock)
                                else:
                                    self.log.write(msg[2])
                                    self.player.threadUpdateTitle(self.player.status_update_lock)
                                    sleep(1.5)
                                    self.playSelection()
                            else:

                                self.log.write(msg[1], thread_lock=None, help_msg=True)
                            self._old_config_encoding = self._cnf.opts['default_encoding'][1]
                            if self._config_win:
                                self._config_win._old_use_transparency = self._cnf.use_transparency
                            if self._cnf.player_changed:
                                self._show_player_changed_in_config()
                                self._cnf.player_changed = False
                    else:
                        # restore transparency, if necessary
                        if self._config_win._config_options['use_transparency'][1] != self._config_win._saved_config_options['use_transparency'][1]:
                            self._toggle_transparency(changed_from_config_window=False,
                                    force_value=self._config_win._saved_config_options['use_transparency'][1])
                        # restore theme, if necessary
                        if self._cnf.opts['theme'][1] != self._config_win._config_options['theme'][1]:
                            #self._config_win._apply_a_theme(self._cnf.opts['theme'][1])
                            ret, ret_theme_name = self._theme.readAndApplyTheme(self._cnf.opts['theme'][1])
                            if ret == 0:
                                self._theme_name = self._cnf.theme
                            else:
                                self._theme_name = ret_theme_name
                                self._cnf.theme_not_supported = True
                            curses.doupdate()
                        # make sure config is not saved
                        self._config_win._saved_config_options['dirty_config'][1] = False
                        self._cnf.dirty_config = False
                    # clean up
                    self._player_select_win = None
                    self._encoding_select_win = None
                    self._playlist_select_win = None
                    self._station_select_win = None
                    self._config_win = None
                return

        elif self.ws.operation_mode == self.ws.SELECT_PLAYER_MODE and \
                char not in self._chars_to_bypass:
            if char not in self._chars_to_bypass:
                ret, ret_list = self._player_select_win.keypress(char)
                if ret >= 0:
                    if ret == 0:
                        new_players = ','.join(ret_list)
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug('new_players = {}'.format(new_players))
                        self._config_win._config_options['player'][1] = new_players
                    self.ws.close_window()
                    self._config_win.refresh_config_win()
                return

        elif self.ws.operation_mode == self.ws.SELECT_STATION_ENCODING_MODE and \
                char not in self._chars_to_bypass:
            """ select station's encoding from main window """
            if char not in self._chars_to_bypass:
                ret, ret_encoding = self._encoding_select_win.keypress(char)
                if ret >= 0:
                    if ret == 0:
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug('new station encoding = {}'.format(ret_encoding))
                        """ save encoding and playlist """
                        if self._old_station_encoding == 'utf-8':
                            self._old_station_encoding = ''
                        if ret_encoding == 'utf-8':
                            ret_encoding = ''
                        if self._old_station_encoding != ret_encoding:
                            self._cnf.dirty_playlist = True
                            logger.info('self.stations[self.selection] = {}'.format(self.stations[self.selection]))
                            self.stations[self.selection][2] = ret_encoding
                            if self._cnf.browsing_station_service:
                                self._cnf.dirty_playlist = False
                                self._cnf.online_browser.set_encoding(self.selection, ret_encoding)
                            if self.player.isPlaying():
                                self.stopPlayer()
                                self.playSelection
                        #self._config_win._config_options['default_encoding'][1] = ret_encoding
                    self.ws.close_window()
                    self.refreshBody()
                    self._encoding_select_win = None
                return

        elif self.ws.operation_mode in \
                (self.ws.ADD_STATION_MODE, self.ws.EDIT_STATION_MODE):
            """ In station editor """
            #logger.error('DE char = {0} - {1}'.format(char, chr(char)))
            if char in self._chars_to_bypass_on_editor and \
                    self._station_editor.focus > 1:
                self.volume_functions[chr(char)]()
                return
            ret = self._station_editor.keypress(char)
            if ret == -3:
                self._print_editor_url_error()
            elif ret == -2:
                self._print_editor_name_error()
            elif ret == -1:
                # Cancel
                self.ws.close_window()
                self._station_editor = None
                self.refreshBody()
            elif ret == 1:
                # ok
                if self.ws.operation_mode == self.ws.EDIT_STATION_MODE:
                    if self.stations[self.selection] != self._station_editor.new_station:
                        self._cnf.dirty_playlist = True
                    self.stations[self.selection] = self._station_editor.new_station
                else:
                    self._cnf.dirty_playlist = True
                    if self._station_editor.append:
                        self.stations.append(self._station_editor.new_station)
                        self.number_of_items = len(self.stations)
                        self._cnf.number_of_stations = self.number_of_items
                        self.selection = self.number_of_items - 1
                        self.startPos = self.number_of_items - self.bodyMaxY
                    else:
                        ret, self.number_of_items = self._cnf.insert_station(self._station_editor.new_station, self.selection + 1)
                        self.stations = self._cnf.stations
                        self.selection += 1
                        if self.selection >= self.startPos + self.bodyMaxY:
                            self.startPos += 1

                self.ws.close_window()
                self._station_editor = None
                self.refreshBody()
            elif ret == 2:
                # display line editor help
                self._show_line_editor_help()
            elif ret == 3:
                # show encoding
                if self._station_editor._encoding == '':
                    self._station_editor._encoding = 'utf-8'
                self.ws.operation_mode = self.ws.EDIT_STATION_ENCODING_MODE
                self._encoding_select_win = PyRadioSelectEncodings(self.outerBodyMaxY,
                        self.outerBodyMaxX, self._station_editor._encoding)
                self._encoding_select_win.init_window()
                self._encoding_select_win.refresh_win()
                self._encoding_select_win.setEncoding(self._station_editor._encoding)
            return

        elif self.ws.operation_mode == self.ws.EDIT_STATION_ENCODING_MODE and \
                char not in self._chars_to_bypass:
            """ In station editor; select encoding for station """
            ret, ret_encoding = self._encoding_select_win.keypress(char)
            if ret >= 0:
                if ret_encoding:
                    self._station_editor._encoding = ret_encoding
                    self._station_editor._old_encoding = ret_encoding
                else:
                    self._station_editor._encoding = self._station_editor._old_encoding
                self.ws.close_window()
                self._station_editor.show()
                self._encoding_select_win = None
            return

        elif self.ws.operation_mode == self.ws.SELECT_ENCODING_MODE and \
                char not in self._chars_to_bypass:
            """ In Config window; select global encoding """
            ret, ret_encoding = self._encoding_select_win.keypress(char)
            if ret >= 0:
                if ret == 0:
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug('new encoding = {}'.format(ret_encoding))
                    self._config_win._config_options['default_encoding'][1] = ret_encoding
                self.ws.close_window()
                self._config_win.refresh_config_win()
                self._encoding_select_win = None
            return

        elif self.ws.operation_mode == self.ws.SELECT_PLAYLIST_MODE and \
                char not in self._chars_to_bypass and \
                char not in self._chars_to_bypass_for_search:
            """ In Config window; select playlist """
            ret, ret_playlist = self._playlist_select_win.keypress(char)
            if ret >= 0:
                if ret == 0:
                    self._config_win._config_options['default_playlist'][1] = ret_playlist
                    if ret_playlist == self._config_win._saved_config_options['default_playlist'][1]:
                        self._config_win._config_options['default_station'][1] = self._config_win._saved_config_options['default_station'][1]
                    else:
                        self._config_win._config_options['default_station'][1] = 'False'
                    if logger.isEnabledFor(logging.INFO):
                        logger.info('New default_playlist = "{0}", New default station = "{1}"'.format(ret_playlist, self._config_win._config_options['default_station'][1]))
                self.ws.close_window()
                self._config_win.refresh_config_win()
            return

        elif self.ws.operation_mode == self.ws.SELECT_STATION_MODE and \
                char not in self._chars_to_bypass and \
                char not in self._chars_to_bypass_for_search:
            """ In Config window; select station """
            ret, ret_station = self._station_select_win.keypress(char)
            if ret >= 0:
                if ret == 0:
                    if logger.isEnabledFor(logging.INFO):
                        logger.info('New default station = "{}"'.format(ret_station))
                    self._config_win._config_options['default_station'][1] = ret_station
                self.ws.close_window()
                self._config_win.refresh_config_win()
            return

        elif self.ws.operation_mode == self.ws.ASK_TO_CREATE_NEW_THEME_MODE:
            if self.theme_forced_selection:
                self._theme_selector.set_theme(self.theme_forced_selection)
            if char in (ord('y'), ):
                pass
                #ret = self._cnf.copy_playlist_to_config_dir()
                #if ret == 0:
                #    self.ws.close_window()
                #    self.refreshBody()
                #    if logger.isEnabledFor(logging.DEBUG):
                #        logger.debug('MODE: self.ws.ASK_TO_CREATE_NEW_THEME_MODE -> self.ws.THEME_MODE')
                #elif ret == 1:
                #    self._print_foreign_playlist_message()
                #else:
                #    """ error """
                #    self._print_foreign_playlist_copy_error()
            elif not char in (ord('#'), curses.KEY_RESIZE):
                    self.ws.close_window()
                    self.refreshBody()
                    # Do this here to properly resize
                    return

        elif self.ws.operation_mode == self.ws.THEME_MODE:
            if char not in self._chars_to_bypass and \
                    char not in self._chars_to_bypass_for_search and \
                    char not in (ord('T'),):
                theme_id, save_theme = self._theme_selector.keypress(char)

                #if self._cnf.theme_not_supported:
                #    self._show_theme_not_supported()
                if theme_id == -1:
                    """ cancel or hide """
                    self._theme_name = self._theme_selector._applied_theme_name
                    if self._config_win:
                        self._config_win._config_options['theme'][1] = self._theme_selector._applied_theme_name
                    self._theme_selector = None
                    self.ws.close_window()
                    if self.ws.operation_mode == self.ws.NORMAL_MODE:
                        self.selection, self.startPos, self.playing, self.stations = self.selections[self.ws.operation_mode]
                    self.refreshBody()

                elif theme_id == -2:
                    self.theme_forced_selection = self._theme_selector._themes[self._theme_selector.selection]
                    # ask to create new theme
                    self._print_ask_to_create_theme()

                elif theme_id >= 0:
                    """ valid theme selection """
                    self._theme_name = self._theme_selector.theme_name(theme_id)
                    if self._config_win:
                        self._config_win._config_options['theme'][1] = self._theme_name
                        self._config_win._saved_config_options['theme'][1] = self._theme_name
                    if logger.isEnabledFor(logging.INFO):
                        logger.info('Activating theme: {}'.format(self._theme_name))
                    ret, ret_theme_name = self._theme.readAndApplyTheme(self._theme_name,
                            theme_path=self._theme_selector._themes[theme_id][1])
                    if isinstance(ret, tuple):
                        ret = ret[0]
                    if ret == -1:
                        self._theme_name = ret_theme_name
                        self._cnf.theme_not_supported = True
                        self._cnf.theme_not_supported_notification_shown = False
                        self._show_theme_not_supported()
                    #self.refreshBody()
                    curses.doupdate()
                    # update config window
                    if self._config_win:
                        self._config_win._config_options['theme'][1] = self._theme_name
                    if self.ws.window_mode == self.ws.CONFIG_MODE:
                        save_theme = True
                    # make default
                    if save_theme:
                        self._cnf.theme = self._theme_name
                        if logger.isEnabledFor(logging.INFO):
                            logger.info('Setting default theme: {}'.format(self._theme_name))
                return

        elif char in (ord('/'), ) and self.ws.operation_mode in self._search_modes.keys():
            self.jumpnr = ''
            self._backslash = False
            self._random_requested = False
            self._give_me_a_search_class(self.ws.operation_mode)
            self.search.show(self.outerBodyWin)
            self.ws.operation_mode = self._search_modes[self.ws.operation_mode]
            return

        elif char in (ord('n'), ) and \
                self.ws.operation_mode in self._search_modes.keys():
            #logger.error('DE n operation_mode = {}'.format(self.ws.operation_mode))
            self._give_me_a_search_class(self.ws.operation_mode)
            if self.ws.operation_mode == self.ws.NORMAL_MODE:
                self.jumpnr = ''
                self._backslash = False
                self._random_requested = False
            """ search forward """
            if self.ws.operation_mode in \
                    ( self.ws.NORMAL_MODE, self.ws.PLAYLIST_MODE ):
                self._search_list = self.stations
                sel = self.selection + 1
            elif self.ws.operation_mode == self.ws.THEME_MODE:
                self._search_list = self._theme_selector._themes
                sel = self._theme_selector.selection + 1
            elif self.ws.operation_mode == self.ws.SELECT_PLAYLIST_MODE:
                self._search_list = self._playlist_select_win._items
                sel = self._playlist_select_win._selected_playlist_id + 1
            elif self.ws.operation_mode == self.ws.SELECT_STATION_MODE:
                self._search_list = self._station_select_win._items
                sel = self._station_select_win._selected_playlist_id + 1

            if self.search.string:
                if sel == len(self._search_list):
                    sel = 0
                ret = self.search.get_next(self._search_list, sel)
                if ret is not None:
                    self._apply_search_result(ret, reapply=True)
            else:
                    curses.ungetch('/')
            return

        elif char in (ord('N'), ) and \
                self.ws.operation_mode in self._search_modes.keys():
            self._give_me_a_search_class(self.ws.operation_mode)
            if self.ws.operation_mode == self.ws.NORMAL_MODE:
                self.jumpnr = ''
                self._backslash = False
                self._random_requested = False
            """ search backwards """
            if self.ws.operation_mode in \
                    ( self.ws.NORMAL_MODE, self.ws.PLAYLIST_MODE ):
                self._search_list = self.stations
                sel = self.selection - 1
            elif self.ws.operation_mode == self.ws.THEME_MODE:
                self._search_list = self._theme_selector._themes
                sel = self._theme_selector.selection - 1
            elif self.ws.operation_mode == self.ws.SELECT_PLAYLIST_MODE:
                self._search_list = self._playlist_select_win._items
                sel = self._playlist_select_win._selected_playlist_id - 1
            elif self.ws.operation_mode == self.ws.SELECT_STATION_MODE:
                self._search_list = self._station_select_win._items
                sel = self._station_select_win._selected_playlist_id - 1

            if self.search.string:
                if sel < 0:
                    sel = len(self._search_list) - 1
                ret = self.search.get_previous(self._search_list, sel)
                if ret is not None:
                    self._apply_search_result(ret, reapply=True)
            else:
                curses.ungetch('/')
            return

        elif self.ws.operation_mode in \
                [ self._search_modes[x] for x in self._search_modes.keys()]:
            # serve search results
            ret = self.search.keypress(self.search._edit_win, char)
            if ret == 0:
                if self.ws.operation_mode in self.search_main_window_modes:
                    self._search_list = self.stations
                    sel = self.selection + 1
                elif self.ws.previous_operation_mode == self.ws.THEME_MODE:
                    self._search_list = self._theme_selector._themes
                    sel = self._theme_selector.selection + 1
                elif self.ws.previous_operation_mode == self.ws.SELECT_PLAYLIST_MODE:
                    self._search_list = self._playlist_select_win._items
                    sel = self._playlist_select_win._selected_playlist_id + 1
                elif self.ws.previous_operation_mode == self.ws.SELECT_STATION_MODE:
                    self._search_list = self._station_select_win._items
                    sel = self._station_select_win._selected_playlist_id + 1

                # perform search
                if sel == len(self._search_list):
                    sel = 0
                ret = self.search.get_next(self._search_list, sel)
                if ret is None:
                    if self.search.string:
                        self.search.print_not_found()
                else:
                    self._apply_search_result(ret)
            elif ret == 2:
                # display help
                self._show_search_help()
            elif ret == -1:
                # cancel search
                self.ws.close_window()
                self.refreshBody()
                return

        elif char in (ord('T'), ):
            self.jumpnr = ''
            self._backslash = False
            self._random_requested = False
            self._toggle_transparency()
            return

        elif char in (ord('+'), ord('='), ord('.')):
            self._volume_up()
            return

        elif char in (ord('-'), ord(',')):
            self._volume_down()
            return

        elif char in (ord('m'), ):
            self._volume_mute()
            return

        elif char in (ord('v'), ):
            self._volume_save()
            return

        elif self.ws.operation_mode == self.ws.PLAYLIST_SCAN_ERROR_MODE:
            """ exit due to scan error """
            self.stopPlayer()
            return -1

        elif self.ws.operation_mode == self.ws.PLAYLIST_RECOVERY_ERROR_MODE:
            self._cnf.playlist_recovery_result = 0
            self.ws.close_window()
            self.refreshBody()
            return

        elif self.ws.operation_mode == self.ws.UPDATE_NOTIFICATION_MODE:
            self.helpWinContainer = None
            self.helpWin = None
            self.ws.close_window()
            self._update_notify_lock.acquire()
            self._update_version = ''
            self._update_notify_lock.release()
            self.refreshBody()
            return

        elif self.ws.operation_mode == self.ws.ASK_TO_SAVE_PLAYLIST_WHEN_EXITING_MODE:
            if char in (ord('y'), ord('Y')):
                if not self._cnf.locked and char == ord('Y'):
                    self._cnf.auto_save_playlist = True
                ret = self.saveCurrentPlaylist()
                #if ret == -1:
                #    # do not exit
                #    return
                # exit program
                if self.player:
                    self.stopPlayer()
                self.ctrl_c_handler(0,0)
                return -1
            elif char in (ord('n'), ):
                # exit program
                if self.player:
                    self.stopPlayer()
                self._cnf.save_config()
                self._wait_for_threads()
                self._remove_lock_file()
                return -1
            elif char in (curses.KEY_EXIT, ord('q'), 27):
                self.bodyWin.nodelay(True)
                char = self.bodyWin.getch()
                self.bodyWin.nodelay(False)
                if char == -1:
                    """ ESCAPE """
                    self._cnf.save_config()
                    self.ws.close_window()
                    self.refreshBody()
                    #return -1
                    return
            return

        elif self.ws.operation_mode == self.ws.ASK_TO_SAVE_PLAYLIST_WHEN_OPENING_PLAYLIST_MODE:
            self.ws.close_window()
            if char in (ord('y'), ord('Y')):
                if not self._cnf.locked and char == ord('Y'):
                    self._cnf.auto_save_playlist = True
                ret = self.saveCurrentPlaylist()
                if ret == 0:
                    self._open_playlist()
                else:
                    if self._cnf.browsing_station_service:
                        self._cnf.removed_playlist_history_item()
            elif char in (ord('n'), ):
                    self._open_playlist()
            elif char in (curses.KEY_EXIT, ord('q'), 27):
                self.bodyWin.nodelay(True)
                char = self.bodyWin.getch()
                self.bodyWin.nodelay(False)
                if char == -1:
                    """ ESCAPE """
                    if self._cnf.browsing_station_service:
                        self._cnf.removed_playlist_history_item()
                    self.refreshBody()
            return

        elif self.ws.operation_mode == self.ws.PLAYLIST_DIRTY_RELOAD_CONFIRM_MODE:
            if char in (ord('y'), ord('Y')):
                if not self._cnf.locked and char == ord('Y'):
                    self._cnf.confirm_playlist_reload = False
                self.ws.close_window()
                self.reloadCurrentPlaylist(self.ws.PLAYLIST_DIRTY_RELOAD_CONFIRM_MODE)
            elif char in (ord('n'), ):
                """ close confirmation message """
                self.stations = self._cnf.stations
                self.ws.close_window()
                self.refreshBody()
            else:
                pass
            return

        elif self.ws.operation_mode == self.ws.PLAYLIST_RELOAD_CONFIRM_MODE:
            if char in (ord('y'), ord('Y')):
                if not self._cnf.locked and char == ord('Y'):
                    self._cnf.confirm_playlist_reload = False
                self.reloadCurrentPlaylist(self.ws.PLAYLIST_DIRTY_RELOAD_CONFIRM_MODE)
                self.ws.close_window()
                self.refreshBody()
            else:
                """ close confirmation message """
                self.stations = self._cnf.stations
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('Canceling Playlist Reload')
                self.ws.close_window()
                self.refreshBody()
            return

        #elif self.ws.operation_mode == self.ws.PLAYLIST_HELP_MODE or \
        #        self.ws.operation_mode == self.ws.PLAYLIST_LOAD_ERROR_MODE or \
        #            self.ws.operation_mode == self.ws.PLAYLIST_NOT_FOUND_ERROR_MODE:
        #    """ close playlist help """
        #    self.ws.operation_mode = self.ws.window_mode = self.ws.PLAYLIST_MODE
        #    self.refreshBody()
        #    if logger.isEnabledFor(logging.DEBUG):
        #        if self.ws.operation_mode == self.ws.PLAYLIST_HELP_MODE:
        #            logger.debug('MODE: self.ws.PLAYLIST_HELP_MODE -> self.ws.PLAYLIST_MODE')
        #        elif self.ws.operation_mode == self.ws.PLAYLIST_LOAD_ERROR_MODE:
        #            logger.debug('MODE: self.ws.PLAYLIST_LOAD_ERROR_MODE -> self.ws.PLAYLIST_MODE')
        #        else:
        #            logger.debug('MODE: self.ws.PLAYLIST_NOT_FOUND_ERROR_MODE -> self.ws.PLAYLIST_MODE')
        #    return

        elif self.ws.operation_mode == self.ws.REMOVE_STATION_MODE:
            if char in (ord('y'), ord('Y')):
                self._set_active_stations()
                deleted_station, self.number_of_items = self._cnf.remove_station(self.selection)
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('Deleted station: "{}"'.format(deleted_station[0]))
                self.ws.close_window()
                self._align_stations_and_refresh(self.ws.REMOVE_STATION_MODE)
                if not self._cnf.locked and char == ord('Y'):
                    self._cnf.confirm_station_deletion = False
            else:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('Canceling: Remove station')
            self.ws.close_window()
            self.refreshBody()
            return

        elif self.ws.operation_mode == self.ws.FOREIGN_PLAYLIST_ASK_MODE:
            if char in (ord('y'), ):
                ret = self._cnf.copy_playlist_to_config_dir()
                if ret == 0:
                    ind = self._cnf.current_playlist_index()
                    self.selections[self.ws.PLAYLIST_MODE][0] = self.selections[self.ws.PLAYLIST_MODE][2] = ind
                    self.ws.close_window()
                    self.refreshBody()
                elif ret == 1:
                    self._print_foreign_playlist_message()
                else:
                    """ error """
                    self._print_foreign_playlist_copy_error()
            elif char in (ord('n'), ):
                self.ws.close_window()
                self.refreshBody()
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('Canceling: Move foreign playlist...')
            return

        elif self.ws.operation_mode in self.ws.PASSIVE_WINDOWS:
            if self.ws.operation_mode in (self.ws.MAIN_HELP_MODE,
                        self.ws.MAIN_HELP_MODE_PAGE_2):
                if char in ( ord('n'), ord('p'), ):
                    self.helpWinContainer = None
                    self.helpWin = None
                    if self.ws.operation_mode == self.ws.MAIN_HELP_MODE:
                        self.ws.close_window()
                        #self.refreshBody()
                        self._show_main_help_page_2()
                    else:
                        self.ws.close_window()
                        #self.refreshBody()
                        self._show_main_help()
                    return
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Part of PASSIVE_WINDOWS')
            self.helpWinContainer = None
            self.helpWin = None
            self.ws.close_window()
            self.refreshBody()
            return

        else:

            if char in (ord('?'), ):
                self.jumpnr = ''
                self._backslash = False
                self._random_requested = False
                self._print_help()
                return

            if char in (curses.KEY_END, ):
                self.jumpnr = ''
                self._backslash = False
                self._random_requested = False
                if self.number_of_items > 0:
                    self.setStation(-1)
                    self.refreshBody()
                return

            if char in (ord('G'), ):
                self._random_requested = False
                if self.number_of_items > 0:
                    if self.jumpnr == "":
                        self.setStation(-1)
                    else:
                        force_center = False
                        jumpto=min(int(self.jumpnr)-1,len(self.stations)-1)
                        jumpto=max(0,jumpto)
                        if jumpto < self.startPos - 1 or \
                                jumpto > self.startPos + self.bodyMaxY:
                            force_center = True
                        self.setStation(jumpto)
                        self._put_selection_in_the_middle(force=force_center)
                    self.jumpnr = ""
                    self.refreshBody()
                return

            if char in map(ord,map(str,range(0,10))):
                self._random_requested = False
                if self.number_of_items > 0:
                    self.jumpnr += chr(char)
                    return
            else:
                if char not in (curses.ascii.EOT, curses.ascii.NAK, 4, 21):
                    self._random_requested = False
                    self.jumpnr = ""

            if char in (ord('g'), curses.KEY_HOME):
                self.jumpnr = ''
                self._backslash = False
                self._random_requested = False
                self.setStation(0)
                self.refreshBody()
                return

            if char in (curses.KEY_EXIT, ord('q'), 27) or \
                    (self.ws.operation_mode == self.ws.PLAYLIST_MODE and \
                    char in (ord('h'), curses.KEY_LEFT)):
                self.bodyWin.nodelay(True)
                char = self.bodyWin.getch()
                self.bodyWin.nodelay(False)
                if char == -1:
                    """ ESCAPE """
                    self.jumpnr = ''
                    self._backslash = False
                    self._random_requested = False
                    if self.ws.operation_mode == self.ws.PLAYLIST_MODE:
                        """ return to stations view """
                        self.jumpnr = ''
                        self._backslash = False
                        self.selections[self.ws.operation_mode] = [self.selection, self.startPos, self.playing, self._cnf.playlists]
                        self.ws.close_window()
                        self._give_me_a_search_class(self.ws.operation_mode)
                        self.selection, self.startPos, self.playing, self.stations = self.selections[self.ws.operation_mode]
                        self.stations = self._cnf.stations
                        self.number_of_items = len(self.stations)
                        self.refreshBody()
                        return
                    else:
                        """ exit """
                        # stop updating the status bar
                        self.log.asked_to_stop = True
                        if self._cnf.dirty_playlist:
                            if self._cnf.auto_save_playlist:
                                # save playlist and exit
                                ret = self.saveCurrentPlaylist()
                                #if ret == -1:
                                #    # do not exit program
                                #    return
                            else:
                                # ask to save playlist
                                self._print_save_modified_playlist(self.ws.ASK_TO_SAVE_PLAYLIST_WHEN_EXITING_MODE)
                                return
                        #else:
                        #    self._open_playlist()
                        if self.player:
                            self.stopPlayer()
                        self.ctrl_c_handler(0,0)
                        return -1
                else:
                    return

            if char in (curses.KEY_DOWN, ord('j')):
                self.jumpnr = ''
                self._backslash = False
                self._random_requested = False
                if self.number_of_items > 0:
                    self.setStation(self.selection + 1)
                    self.refreshBody()
                return

            if char in (curses.KEY_UP, ord('k')):
                self.jumpnr = ''
                self._backslash = False
                self._random_requested = False
                if self.number_of_items > 0:
                    self.setStation(self.selection - 1)
                    self.refreshBody()
                return

            if char in (curses.KEY_PPAGE, ):
                self.jumpnr = ''
                self._backslash = False
                self._random_requested = False
                if self.number_of_items > 0:
                    sel = self.selection - self.pageChange
                    if sel < 0 and self.selection > 0:
                        sel = 0
                    self.setStation(sel)
                    self.refreshBody()
                return

            if char in (curses.KEY_NPAGE, ):
                self.jumpnr = ''
                self._backslash = False
                self._random_requested = False
                if self.number_of_items > 0:
                    sel = self.selection + self.pageChange
                    if self.selection == len(self.stations) - 1:
                        sel = 0
                    elif sel >= len(self.stations):
                        sel = len(self.stations) - 1
                    self.setStation(sel)
                    self.refreshBody()
                return

            if self.ws.operation_mode == self.ws.NORMAL_MODE:
                if char in ( ord('a'), ord('A') ):
                    self.jumpnr = ''
                    self._backslash = False
                    self._random_requested = False
                    if self._cnf.browsing_station_service: return
                    self._station_editor = PyRadioEditor(self.stations, self.selection, self.outerBodyWin)
                    if char == ord('A'):
                        self._station_editor.append = True
                    self._station_editor.show()
                    self._station_editor.item = [ '', '', '' ]
                    self.ws.operation_mode = self.ws.ADD_STATION_MODE

                elif char == ord('e'):
                    self.jumpnr = ''
                    self._backslash = False
                    self._random_requested = False
                    if self._cnf.browsing_station_service: return
                    if python_version[0] == '2':
                        if not is_ascii(self.stations[self.selection][0]):
                            self._print_py2_editor_error()
                            return
                    self._station_editor = PyRadioEditor(self.stations, self.selection, self.outerBodyWin, adding=False)
                    self._station_editor.show(self.stations[self.selection])
                    self.ws.operation_mode = self.ws.EDIT_STATION_MODE

                elif char == ord('c'):
                    self.jumpnr = ''
                    self._backslash = False
                    self._random_requested = False
                    if self._cnf.locked:
                        self._print_session_locked()
                        return
                    self._old_config_encoding = self._cnf.opts['default_encoding'][1]
                    # open config window
                    #self.ws.operation_mode = self.ws.window_mode = self.ws.CONFIG_MODE
                    self.ws.window_mode = self.ws.CONFIG_MODE
                    if not self.player.isPlaying():
                        self.log.write('Selected player: {}'.format(self._format_player_string()), help_msg=True)
                    self._show_config_window()
                    return

                elif char in (ord('E'), ):
                    self.jumpnr = ''
                    self._backslash = False
                    self._random_requested = False
                    self._old_station_encoding = self.stations[self.selection][2]
                    if self._old_station_encoding == '':
                        self._old_station_encoding = 'utf-8'
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.info('encoding = {}'.format(self._old_station_encoding))
                    self.ws.operation_mode = self.ws.SELECT_STATION_ENCODING_MODE
                    self._encoding_select_win = PyRadioSelectEncodings(self.outerBodyMaxY,
                            self.outerBodyMaxX, self._old_station_encoding)
                    self._encoding_select_win.init_window()
                    self._encoding_select_win.refresh_win()
                    self._encoding_select_win.setEncoding(self._old_station_encoding)

                elif char in (ord('o'), ):
                    self.jumpnr = ''
                    self._backslash = False
                    self._random_requested = False
                    if self._cnf.browsing_station_service:
                        return
                    self._check_to_open_playlist()
                    return

                elif char in (curses.KEY_ENTER, ord('\n'), ord('\r'),
                        curses.KEY_RIGHT, ord('l')):
                    self.jumpnr = ''
                    self._backslash = False
                    self._random_requested = False
                    if self.number_of_items > 0:
                        self.playSelection()
                        self.refreshBody()
                    self._do_display_notify()
                    return

                elif char in (ord(' '), curses.KEY_LEFT, ord('h')):
                    self.jumpnr = ''
                    self._backslash = False
                    self._random_requested = False
                    if self.number_of_items > 0:
                        if self.player.isPlaying():
                            self.stopPlayer()
                        else:
                            self.playSelection()
                        self.refreshBody()
                    self._do_display_notify()
                    return

                elif char in(ord('x'), curses.KEY_DC):
                    # TODO: make it impossible when session locked?
                    self.jumpnr = ''
                    self._backslash = False
                    self._random_requested = False
                    if self._cnf.browsing_station_service: return
                    if self.number_of_items > 0:
                        self.removeStation()
                    return

                elif char in(ord('s'), ):
                    self.jumpnr = ''
                    self._backslash = False
                    self._random_requested = False
                    if self._cnf.browsing_station_service: return
                    if self.number_of_items > 0 and \
                            self._cnf.dirty_playlist:
                        self.saveCurrentPlaylist()
                    return

                elif char in (ord('r'), ):
                    self.jumpnr = ''
                    self._backslash = False
                    self._random_requested = True
                    # Pick a random radio station
                    self.play_random()
                    return

                elif char in (ord('R'), ):
                    self.jumpnr = ''
                    self._backslash = False
                    self._random_requested = False
                    if self._cnf.browsing_station_service: return
                    # Reload current playlist
                    if self._cnf.dirty_playlist:
                        if self._cnf.confirm_playlist_reload:
                            self._print_playlist_dirty_reload_confirmation()
                        else:
                            self.ws.operation_mode = self.ws.PLAYLIST_RELOAD_CONFIRM_MODE
                            curses.ungetch('y')
                    else:
                        if self._cnf.confirm_playlist_reload:
                            self._print_playlist_reload_confirmation()
                        else:
                            self.ws.operation_mode = self.ws.PLAYLIST_RELOAD_CONFIRM_MODE
                            curses.ungetch('y')
                    return

                elif char == ord('J'):
                    # tag for jump
                    self._cnf.jump_tag = self.selection
                    return

                elif char in (curses.ascii.NAK, 21):
                    # ^U, move station Up
                    self._random_requested = False
                    self._move_station(-1)
                    self.jumpnr = ''
                    self._backslash = False
                    return

                elif char in (curses.ascii.EOT, 4):
                    # ^D, move station Down
                    self._random_requested = False
                    self._move_station(1)
                    self.jumpnr = ''
                    self._backslash = False
                    return

            elif self.ws.operation_mode == self.ws.PLAYLIST_MODE:
                self._random_requested = False

                if char in (curses.KEY_ENTER, ord('\n'), ord('\r'),
                        curses.KEY_RIGHT, ord('l')):
                    self.jumpnr = ''
                    self._backslash = False
                    """ return to stations view """
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug('Loading playlist: "{}"'.format(self.stations[self.selection][-1]))
                    ret = self._cnf.read_playlist_file(self.stations[self.selection][-1])
                    if ret == -1:
                        self.stations = self._cnf.playlists
                        self._print_playlist_load_error()
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug('Error loading playlist: "{}"'.format(self.stations[self.selection][-1]))
                        return
                    elif ret == -2:
                        self.stations = self._cnf.playlists
                        self._print_playlist_not_found_error()
                        if logger.isEnabledFor(logging.DEBUG):
                            logger.debug('Playlist not found: "{}"'.format(self.stations[self.selection][-1]))
                        return
                    elif ret == -7:
                        self._print_playlist_recovery_error()
                        return
                    else:
                        self._playlist_error_message = ''
                        self.number_of_items = ret
                        self.selections[self.ws.operation_mode] = [self.selection, self.startPos, self.playing, self._cnf.playlists]
                        self.ws.close_window()
                        self.selection, self.startPos, self.playing, self.stations = self.selections[self.ws.operation_mode]
                        self._align_stations_and_refresh(self.ws.PLAYLIST_MODE)
                        self._give_me_a_search_class(self.ws.operation_mode)
                        if self.playing < 0:
                            self._put_selection_in_the_middle(force=True)
                            self.refreshBody()
                    return

                elif char in (ord('r'), ):
                    self.jumpnr = ''
                    self._backslash = False
                    """ read playlists from disk """
                    txt = '''Reading playlists. Please wait...'''
                    self._show_help(txt, self.ws.PLAYLIST_MODE, caption=' ', prompt=' ', is_message=True)
                    old_playlist = self._cnf.playlists[self.selection][0]
                    self.number_of_items, self.playing = self.readPlaylists()
                    if self.number_of_items > 0:
                        """ refresh reference """
                        self.stations = self._cnf.playlists
                        if self.playing == -1:
                            self.selections[self.ws.operation_mode] = [0, 0, -1, self._cnf.playlists]
                        else:
                            self.selections[self.ws.operation_mode] = (self.selection, self.startPos, self.playing, self._cnf.playlists)
                        self.refreshBody()

    def _volume_up(self):
        self.jumpnr = ''
        self._backslash = False
        self._random_requested = False
        if self.player.isPlaying():
            if self.player.playback_is_on:
                self.player.volumeUp()
        else:
            if self.ws.operation_mode in self.ws.PASSIVE_WINDOWS:
                self.ws.close_window()
                self.refreshBody()
            if logger.isEnabledFor(logging.INFO):
                logger.info('Volume adjustment inhibited because playback is off')


    def _volume_down(self):
        self.jumpnr = ''
        self._backslash = False
        self._random_requested = False
        if self.player.isPlaying():
            if self.player.playback_is_on:
                self.player.volumeDown()
        else:
            if self.ws.operation_mode in self.ws.PASSIVE_WINDOWS:
                self.ws.close_window()
                self.refreshBody()
            if logger.isEnabledFor(logging.INFO):
                logger.info('Volume adjustment inhibited because playback is off')

    def _volume_mute(self):
        self.jumpnr = ''
        self._backslash = False
        self._random_requested = False
        if self.player.isPlaying():
            if self.player.playback_is_on:
                self.player.toggleMute()
        else:
            if self.ws.operation_mode in self.ws.PASSIVE_WINDOWS:
                self.ws.close_window()
                self.refreshBody()
            if logger.isEnabledFor(logging.INFO):
                logger.info('Muting inhibited because playback is off')

    def _volume_save(self):
        self.jumpnr = ''
        self._backslash = False
        self._random_requested = False
        if self.player.isPlaying():
            if self.player.playback_is_on:
                ret_string = self.player.save_volume()
                if ret_string:
                    self.log.write(ret_string)
                    self.player.threadUpdateTitle(self.player.status_update_lock)
        else:
            if self.ws.operation_mode in self.ws.PASSIVE_WINDOWS:
                self.ws.close_window()
                self.refreshBody()
            if logger.isEnabledFor(logging.INFO):
                logger.info('Volume save inhibited because playback is off')

    def _redisplay_stations_and_playlists(self):
        self.bodyWin.erase()
        self.outerBodyWin.erase()
        self.outerBodyWin.box()
        self.bodyWin.move(1, 1)
        self.bodyWin.move(0, 0)
        self._print_body_header()
        pad = len(str(self.startPos + self.bodyMaxY))
        if self.number_of_items > 0:
            for lineNum in range(self.bodyMaxY):
                i = lineNum + self.startPos
                if i < len(self.stations):
                    self.__displayBodyLine(lineNum, pad, self.stations[i])
                else:
                    break
        if self._cnf.browsing_station_service:
            if self._cnf.internal_header_height > 0:
                headers = self._cnf.online_browser.get_internal_header(pad, self.bodyMaxX)
                # logger.error('DE {}'.format(headers))
                for i, a_header in enumerate(headers):
                    self.outerBodyWin.addstr(i + 1, 1, a_header[0], curses.color_pair(2))
                    column_separator = a_header[1]
                    column_name = a_header[2]
                    #logger.error('DE {}'.format(column_separator))
                    #logger.error('DE {}'.format(column_name))
                    for j, col in enumerate(column_separator):
                        if version_info < (3, 0):
                            self.outerBodyWin.addstr(i + 1, col + 2, u'│'.encode('utf-8', 'replace'), curses.color_pair(5))
                        else:
                            self.outerBodyWin.addstr(i + 1, col + 2, '│', curses.color_pair(5))
                        try:
                            self.outerBodyWin.addstr(column_name[j], curses.color_pair(2))
                        except:
                            pass
        self.outerBodyWin.refresh()
        self.bodyWin.refresh()

    def _redisplay_config(self):
        self._config_win.parent = self.outerBodyWin
        self._config_win.init_config_win()
        self._config_win.refresh_config_win()

    def _redisplay_player_select_win_refresh_and_resize(self):
        self._player_select_win.refresh_and_resize(self.outerBodyMaxY, self.outerBodyMaxX)

    def _redisplay_encoding_select_win_refresh_and_resize(self):
        self._encoding_select_win.refresh_and_resize(self.outerBodyMaxY, self.outerBodyMaxX)

    def _playlist_select_win_refresh_and_resize(self):
        self._playlist_select_win.refresh_and_resize(self.bodyWin.getmaxyx())

    def _redisplay_encoding_select_win_refresh_and_resize(self):
        self._encoding_select_win.refresh_and_resize(self.outerBodyMaxY, self.outerBodyMaxX)

    def _redisplay_station_select_win_refresh_and_resize(self):
        self._station_select_win.refresh_and_resize(self.outerBodyWin.getmaxyx())

    def _redisplay_print_save_modified_playlist(self):
        self._print_save_modified_playlist(self.ws.operation_mode)

    def _redisplay_search_show(self):
        self.search.show(self.outerBodyWin, repaint=True)

    def _redisplay_theme_mode(self):
        self._theme_selector.parent = self.outerBodyWin
        self._show_theme_selector()
        if self.theme_forced_selection:
            self._theme_selector.set_theme(self.theme_forced_selection)

    def _redisplay_ask_to_create_new_theme(self):
        if logger.isEnabledFor(logging.ERROR):
            logger.error('DE self.ws.previous_operation_mode = {}'.format(self.ws.previous_operation_mode))
        self._theme_selector.parent = self.outerBodyWin
        if self.ws.previous_operation_mode == self.ws.CONFIG_MODE:
            self._show_theme_selector_from_config()
        else:
            self._show_theme_selector()
        if self.theme_forced_selection:
            self._theme_selector.set_theme(self.theme_forced_selection)
        self._print_ask_to_create_theme()


    """''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Windows only section
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''"""
    def _register_windows_handlers(self):
        if platform.startswith('win'):
            """ disable close button """
            import win32console, win32gui, win32con, win32api
            hwnd = win32console.GetConsoleWindow()
            if hwnd:
               hMenu = win32gui.GetSystemMenu(hwnd, 0)
               if hMenu:
                   try:
                       win32gui.DeleteMenu(hMenu, win32con.SC_CLOSE, win32con.MF_BYCOMMAND)
                   except:
                       pass
            """ install handlers for exit / close signals"""
            try:
                result = win32api.SetConsoleCtrlHandler(self._windows_signal_handler, True)
                if logger.isEnabledFor(logging.DEBUG):
                    if result == 0:
                        logger.debug('SetConsoleCtrlHandler: Failed to register!!!')
                    else:
                        logger.debug('SetConsoleCtrlHandler: Registered!!!')
            except:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('SetConsoleCtrlHandler: Failed to register (with Exception)!!!')
            # Trying to catch Windows log-ogg, reboot, halt
            # No luck....
            #import signal
            #try:
            #    signal.signal(signal.SIGINT, self._windows_signal_handler)
            #except:
            #    if logger.isEnabledFor(logging.DEBUG):
            #        logger.debug('SetConsoleCtrlHandler: Signal SIGINT failed to register (with Exception)!!!')

            #try:
            #    signal.signal(signal.SIGINT, self._windows_signal_handler)
            #except:
            #    if logger.isEnabledFor(logging.DEBUG):
            #        logger.debug('SetConsoleCtrlHandler: Signal SIGINT failed to register (with Exception)!!!')

    def _windows_signal_handler(self, event):
        """ windows signal handler
            https://danielkaes.wordpress.com/2009/06/04/how-to-catch-kill-events-with-python/
        """
        import win32con, win32api, signal
        if event in (win32con.CTRL_C_EVENT,
                            win32con.CTRL_LOGOFF_EVENT,
                             win32con.CTRL_BREAK_EVENT,
                             win32con.CTRL_SHUTDOWN_EVENT,
                             win32con.CTRL_CLOSE_EVENT,
                             signal.SIGINT,
                             signal.SIGBREAK):
            self._force_exit = True
            self.ctrl_c_handler(0,0)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('Windows asked me to terminate!!')
            try:
                result = win32api.SetConsoleCtrlHandler(self._windows_signal_handler, False)
            except:
                pass
        return False

# pymode:lint_ignore=W901
