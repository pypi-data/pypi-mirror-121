# ------------------------------------------------------------------------------
#  Copyleft 2015-2021  PacMiam
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
# ------------------------------------------------------------------------------

# Configuration
from configparser import ExtendedInterpolation

# Datetime
from datetime import date, datetime, timedelta

# Filesystem
from os import R_OK, W_OK, X_OK, access, remove
from os.path import getctime
from pathlib import Path
from shutil import rmtree

# GEM
from geode_gem.engine import utils as engine_utils
from geode_gem.engine.api import GEM
from geode_gem.engine.console import Console
from geode_gem.engine.emulator import Emulator
from geode_gem.engine.lib.configuration import Configuration

from geode_gem.ui import GeodeGEM, utils as ui_utils
from geode_gem.ui.data import Icons, Columns, Folders, Metadata
from geode_gem.ui.widgets.game import GameThread, GamesLoadingThread
from geode_gem.ui.widgets.script import ScriptThread
from geode_gem.ui.dialog import GeodeDialog
from geode_gem.widgets import GeodeGtk

# GObject
from gi.repository import Gtk, GLib, GObject, Gio, Gdk, GdkPixbuf, Pango

# Python
from copy import deepcopy

# Random
from random import shuffle

# Regex
from re import match

# System
from sys import version_info
from shlex import split as shlex_split

# Thread
from threading import (enumerate as thread_enumerate,
                       main_thread as thread_main_thread)

# Translation
from gettext import gettext as _, ngettext

# URL
from urllib.parse import urlparse
from urllib.request import url2pathname


class MainWindow(Gtk.ApplicationWindow):

    __gsignals__ = {
        "game-started": (GObject.SignalFlags.RUN_FIRST, None, [object]),
        "game-terminate": (GObject.SignalFlags.RUN_LAST, None, [object]),
        "games-terminate": (GObject.SignalFlags.RUN_LAST, None, [object]),
        "script-terminate": (GObject.SignalFlags.RUN_LAST, None, [object]),
    }

    flags = ("favorite", "multiplayer", "finish")
    columns = ("play", "play_time", "last_play", "score", "installed", "flags")

    filters = ("favorite_switch", "unfavorite_switch", "multiplayer_switch",
               "singleplayer_switch", "finish_switch", "unfinish_switch")

    toolbar_sizes = {
        "button": Gtk.IconSize.BUTTON,
        "dialog": Gtk.IconSize.DIALOG,
        "dnd": Gtk.IconSize.DND,
        "large-toolbar": Gtk.IconSize.LARGE_TOOLBAR,
        "menu": Gtk.IconSize.MENU,
        "small-toolbar": Gtk.IconSize.SMALL_TOOLBAR,
    }

    treeview_grid_lines = {
        "both": Gtk.TreeViewGridLines.BOTH,
        "horizontal": Gtk.TreeViewGridLines.HORIZONTAL,
        "none": Gtk.TreeViewGridLines.NONE,
        "vertical": Gtk.TreeViewGridLines.VERTICAL,
    }

    treeview_icons = {
        Columns.List.FAVORITE: ("favorite", None),
        Columns.List.MULTIPLAYER: ("users", "avatar"),
        Columns.List.FINISH: ("ok", None),
        Columns.List.SCORE: ("starred", "no_starred"),
        Columns.List.PARAMETER: ("properties", None),
        Columns.List.SCREENSHOT: ("camera", None),
        Columns.List.SAVESTATE: ("floppy", None),
    }

    def __init__(self, api, cache):
        """ Constructor

        Parameters
        ----------
        api : gem.engine.api.GEM
            GEM API instance
        cache : pathlib.Path
            Cache folder path

        Raises
        ------
        TypeError
            if api type is not gem.engine.api.GEM
            if metadata type is not gem.engine.lib.configuration.Configuration
            if cache type is not pathlib.Path
        """

        if not type(api) is GEM:
            raise TypeError("Wrong type for api, expected gem.engine.api.GEM")

        if not isinstance(cache, Path):
            raise TypeError("Wrong type for cache, expected pathlib.Path")

        Gtk.ApplicationWindow.__init__(self)

        # Application objects instances
        self.api = api
        self.logger = api.logger

        # Cache folder
        self.__cache = cache
        # Check development version
        self.__version = self.check_version()
        # Check mednafen status
        self.__mednafen_status = ui_utils.check_mednafen()

        # Interface variables cache storage
        self.__geode_cache = {
            "fullscreen": False,
            "keys": list(),
            "row": None,
            "shortcuts": list(),
            "signals": list(),
        }
        self.__sidebar_cache = {
            "image": None,
            "orientation": None,
        }
        self.__toolbar_cache = {
            "size": None,
            "tags": set(),
        }
        self.__tooltip_cache = {
            "data": list(),
            "instance": None,
            "pixbuf": None,
        }
        # Store selected game informations with console, game and name as keys
        self.selection = dict()
        # Store consoles iters
        self.consoles_iter = dict()
        # Store threads with basename game file without extension as key
        self.threads = {
            "listing": int(),
            "loading": dict(),
            "notes": dict(),
            "playing": dict(),
            "scripts": dict(),
        }

        # Initialize interface
        self.__init_widgets()
        self.__init_packing()
        self.__init_signals()
        self.__init_storage()
        # Start interface
        self.__start_interface()

    def __init_widgets(self):
        """ Initialize interface widgets
        """

        # Initialize icons
        self.icons_theme = Gtk.IconTheme.get_default()
        self.icons_theme.append_search_path(
            str(engine_utils.get_data("data", "icons").resolve()))

        self.icons_blank = ui_utils.generate_blank_icons()

        # Clipboard
        self.clipboard = Gtk.Clipboard.get(Gdk.Atom.intern("CLIPBOARD", False))

        # Main display
        self.window_display = Gdk.Display.get_default()

        # Main window size
        self.window_size = Gdk.Geometry()
        self.window_size.min_width = 800
        self.window_size.min_height = 600
        self.window_size.base_width = 1024
        self.window_size.base_height = 768

        # Main window
        self.set_title(
            f"{Metadata.NAME} {self.__version} - {Metadata.CODE_NAME}")

        icon_path = str(engine_utils.get_data("data", "desktop", "gem.svg"))
        self.set_default_icon(GdkPixbuf.Pixbuf.new_from_file(icon_path))
        self.set_default_icon_from_file(icon_path)

        self.set_position(Gtk.WindowPosition.CENTER)

        # Shortcuts
        self.shortcuts_group = Gtk.AccelGroup()
        self.add_accel_group(self.shortcuts_group)

        self.shortcuts_map = Gtk.AccelMap()

        # ------------------------------------
        #   External applications
        # ------------------------------------

        try:
            self.__xdg_open_instance = Gio.AppInfo.create_from_commandline(
                "xdg-open", None, Gio.AppInfoCreateFlags.SUPPORTS_URIS)

        except GLib.Error:
            self.logger.exception("Cannot generate xdg-open instance")

        # ------------------------------------
        #   Grid
        # ------------------------------------

        self.grid = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.grid_consoles = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.grid_games = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)

        # ------------------------------------
        #   Headerbar
        # ------------------------------------

        self.headerbar = GeodeGtk.HeaderBar(
            GeodeGtk.MenuButton(
                _("Main menu"),
                GeodeGtk.MenuItem(
                    _("_Preferences..."), identifier="preferences"),
                GeodeGtk.MenuItem(_("Application _log..."), identifier="log"),
                None,
                GeodeGtk.MenuItem(
                    _("Rebuild icons _cache..."), identifier="clean_cache"),
                None,
                GeodeGtk.MenuItem(_("_Website"), identifier="website"),
                GeodeGtk.MenuItem(_("_Report problem"), identifier="report"),
                None,
                GeodeGtk.MenuItem(_("_About"), identifier="about"),
                None,
                GeodeGtk.MenuItem(_("_Quit"), identifier="quit"),
                icon_name=Icons.Symbolic.MENU,
                identifier="main",
            ),
            GeodeGtk.MenuButton(
                _("Display menu"),
                GeodeGtk.MenuItem(
                    _("_Games lists"),
                    GeodeGtk.MenuItem(
                        _("_Columns visibility"),
                        GeodeGtk.CheckMenuItem(
                            _("Favorite"), identifier="favorite"),
                        GeodeGtk.CheckMenuItem(
                            _("Multiplayer"), identifier="multiplayer"),
                        GeodeGtk.CheckMenuItem(
                            _("Finish"), identifier="finish"),
                        GeodeGtk.CheckMenuItem(
                            _("Launch number"), identifier="play"),
                        GeodeGtk.CheckMenuItem(
                            _("Play time"), identifier="play_time"),
                        GeodeGtk.CheckMenuItem(
                            _("Last launch date"), identifier="last_play"),
                        GeodeGtk.CheckMenuItem(
                            _("Score"), identifier="score"),
                        GeodeGtk.CheckMenuItem(
                            _("Installed date"), identifier="installed"),
                        GeodeGtk.CheckMenuItem(
                            _("Emulator flags"), identifier="flags"),
                    ),
                    None,
                    GeodeGtk.RadioMenuItem(
                        _("List view"), identifier="list"),
                    GeodeGtk.RadioMenuItem(
                        _("Grid icons view"), group="list", identifier="grid"),
                ),
                None,
                GeodeGtk.MenuItem(
                    _("_Sidebar"),
                    GeodeGtk.CheckMenuItem(
                        _("Show _sidebar"), identifier="show_sidebar"),
                    None,
                    GeodeGtk.RadioMenuItem(
                        _("Right"), identifier="right"),
                    GeodeGtk.RadioMenuItem(
                        _("Bottom"), identifier="bottom", group="right")
                ),
                GeodeGtk.MenuItem(
                    _("_Statusbar"),
                    GeodeGtk.CheckMenuItem(
                        _("Show _statusbar"), identifier="show_statusbar")
                ),
                None,
                GeodeGtk.CheckMenuItem(
                    _("Use _dark theme"), identifier="dark_theme"),
                icon_name=Icons.Symbolic.VIDEO,
                identifier="display",
            ),
            identifier="headerbar",
            set_title=self.get_title(),
        )

        # ------------------------------------
        #   Menubar
        # ------------------------------------

        self.menubar = Gtk.MenuBar()

        self.menubar_main = GeodeGtk.MenuItem(
            _("_Application"),
            GeodeGtk.MenuItem(_("_Preferences..."), identifier="preferences"),
            GeodeGtk.MenuItem(_("Application _log..."), identifier="log"),
            None,
            GeodeGtk.MenuItem(
                _("Rebuild icons _cache..."), identifier="clean_cache"),
            None,
            GeodeGtk.MenuItem(_("_Quit"), identifier="quit"),
            identifier="menubar_main",
        )

        self.menubar_view = GeodeGtk.MenuItem(
            _("_Display"),
            GeodeGtk.MenuItem(
                _("_Games lists"),
                GeodeGtk.MenuItem(
                    _("_Columns visibility"),
                    GeodeGtk.CheckMenuItem(
                        _("Favorite"), identifier="favorite"),
                    GeodeGtk.CheckMenuItem(
                        _("Multiplayer"), identifier="multiplayer"),
                    GeodeGtk.CheckMenuItem(
                        _("Finish"), identifier="finish"),
                    GeodeGtk.CheckMenuItem(
                        _("Launch number"), identifier="play"),
                    GeodeGtk.CheckMenuItem(
                        _("Play time"), identifier="play_time"),
                    GeodeGtk.CheckMenuItem(
                        _("Last launch date"), identifier="last_play"),
                    GeodeGtk.CheckMenuItem(
                        _("Score"), identifier="score"),
                    GeodeGtk.CheckMenuItem(
                        _("Installed date"), identifier="installed"),
                    GeodeGtk.CheckMenuItem(
                        _("Emulator flags"), identifier="flags"),
                ),
                None,
                GeodeGtk.RadioMenuItem(_("List view"), identifier="list"),
                GeodeGtk.RadioMenuItem(
                    _("Grid icons"), identifier="grid", group="list"),
            ),
            None,
            GeodeGtk.MenuItem(
                _("_Sidebar"),
                GeodeGtk.CheckMenuItem(
                    _("Show _sidebar"), identifier="show_sidebar"),
                None,
                GeodeGtk.RadioMenuItem(_("Right"), identifier="right"),
                GeodeGtk.RadioMenuItem(
                    _("Bottom"), identifier="bottom", group="right"),
                identifier="sidebar",
            ),
            GeodeGtk.MenuItem(
                _("_Statusbar"),
                GeodeGtk.CheckMenuItem(
                    _("Show _statusbar"), identifier="show_statusbar"),
                identifier="statusbar",
            ),
            None,
            GeodeGtk.CheckMenuItem(
                _("Use _dark theme"), identifier="dark_theme"),
            identifier="menubar_display",
        )

        self.menubar_game = GeodeGtk.MenuItem(
            _("_Game"),
            GeodeGtk.MenuItem(_("_Launch"), identifier="launch"),
            None,
            GeodeGtk.CheckMenuItem(_("_Favorite"), identifier="favorite"),
            GeodeGtk.CheckMenuItem(
                _("_Multiplayer"), identifier="multiplayer"),
            GeodeGtk.CheckMenuItem(_("_Finished"), identifier="finish"),
            None,
            GeodeGtk.MenuItem(_("_Properties..."), identifier="properties"),
            None,
            GeodeGtk.MenuItem(_("_Screenshots..."), identifier="screenshots"),
            GeodeGtk.MenuItem(_("Output _log..."), identifier="game_log"),
            GeodeGtk.MenuItem(_("_Notes..."), identifier="notes"),
            None,
            GeodeGtk.CheckMenuItem(
                _("Fullscreen mode"), identifier="fullscreen"),
            identifier="menubar_game",
        )

        self.menubar_edit = GeodeGtk.MenuItem(
            _("_Edit"),
            GeodeGtk.MenuItem(
                _("_Score"),
                GeodeGtk.MenuItem(_("_Increase score"), identifier="increase"),
                GeodeGtk.MenuItem(_("_Decrease score"), identifier="decrease"),
                None,
                GeodeGtk.MenuItem(_("Set score as 0"), identifier="score_0"),
                GeodeGtk.MenuItem(_("Set score as 1"), identifier="score_1"),
                GeodeGtk.MenuItem(_("Set score as 2"), identifier="score_2"),
                GeodeGtk.MenuItem(_("Set score as 3"), identifier="score_3"),
                GeodeGtk.MenuItem(_("Set score as 4"), identifier="score_4"),
                GeodeGtk.MenuItem(_("Set score as 5"), identifier="score_5"),
                identifier="score",
            ),
            None,
            GeodeGtk.MenuItem(_("_Rename..."), identifier="rename"),
            None,
            GeodeGtk.MenuItem(_("_Duplicate..."), identifier="duplicate"),
            None,
            GeodeGtk.MenuItem(
                _("Define _memory type files..."), identifier="memory_type"),
            None,
            GeodeGtk.MenuItem(_("_Edit game file"), identifier="game_file"),
            None,
            GeodeGtk.MenuItem(
                _("_Copy game path to clipboard"), identifier="copy_path"),
            GeodeGtk.MenuItem(_("_Open game path"), identifier="open_path"),
            GeodeGtk.MenuItem(
                _("_Generate a desktop menu entry"), identifier="menu_entry"),
            None,
            GeodeGtk.MenuItem(_("_Maintenance..."), identifier="maintenance"),
            None,
            GeodeGtk.MenuItem(
                _("_Remove game file from disk..."), identifier="remove"),
            identifier="menubar_edit",
        )

        self.menubar_help = GeodeGtk.MenuItem(
            _("_Help"),
            GeodeGtk.MenuItem(_("_Website"), identifier="website"),
            GeodeGtk.MenuItem(_("_Report problem"), identifier="report"),
            None,
            GeodeGtk.MenuItem(_("_About"), identifier="about"),
            identifier="menubar_help",
        )

        # ------------------------------------
        #   Submenu
        # ------------------------------------

        self.menu_consoles = GeodeGtk.Menu(
            GeodeGtk.MenuItem(_("_Edit console"), identifier="edit_console"),
            GeodeGtk.MenuItem(
                _("_Remove console"), identifier="remove_console"),
            None,
            GeodeGtk.MenuItem(_("_Edit emulator"), identifier="edit_emulator"),
            GeodeGtk.MenuItem(
                _("_Edit emulator configuration file"), identifier="edit_file"),
            None,
            GeodeGtk.MenuItem(_("_Copy games directory path to clipboard"),
                              identifier="copy_path"),
            GeodeGtk.MenuItem(
                _("_Open games directory"), identifier="open_path"),
            None,
            GeodeGtk.MenuItem(_("_Reload games list"), identifier="reload"),
            None,
            GeodeGtk.CheckMenuItem(_("_Favorite"), identifier="favorite"),
            GeodeGtk.CheckMenuItem(
                _("_Recursive"),
                identifier="recursive",
                set_tooltip_text=_(
                    "You need to reload games list to apply changes"),
            ),
            identifier="menu_consoles",
        )

        self.menu_game = GeodeGtk.Menu(
            GeodeGtk.MenuItem(_("_Launch"), identifier="launch"),
            None,
            GeodeGtk.CheckMenuItem(_("_Favorite"), identifier="favorite"),
            GeodeGtk.CheckMenuItem(
                _("_Multiplayer"), identifier="multiplayer"),
            GeodeGtk.CheckMenuItem(_("_Finished"), identifier="finish"),
            None,
            GeodeGtk.MenuItem(_("_Properties..."), identifier="properties"),
            None,
            GeodeGtk.MenuItem(
                _("_Edit"),
                GeodeGtk.MenuItem(_("_Rename..."), identifier="rename"),
                None,
                GeodeGtk.MenuItem(_("_Duplicate..."), identifier="duplicate"),
                None,
                GeodeGtk.MenuItem(
                    _("_Edit game file"), identifier="game_file"),
                None,
                GeodeGtk.MenuItem(
                    _("_Copy game path to clipboard"), identifier="copy_path"),
                GeodeGtk.MenuItem(_("_Open game path"), identifier="open_path"),
                None,
                GeodeGtk.MenuItem(
                    _("_Maintenance..."), identifier="maintenance"),
                None,
                GeodeGtk.MenuItem(
                    _("_Remove game file from disk..."), identifier="remove"),
                identifier="edit",
            ),
            GeodeGtk.MenuItem(
                _("_Score"),
                GeodeGtk.MenuItem(_("_Increase score"), identifier="increase"),
                GeodeGtk.MenuItem(_("_Decrease score"), identifier="decrease"),
                None,
                GeodeGtk.MenuItem(_("Set score as 0"), identifier="score_0"),
                GeodeGtk.MenuItem(_("Set score as 1"), identifier="score_1"),
                GeodeGtk.MenuItem(_("Set score as 2"), identifier="score_2"),
                GeodeGtk.MenuItem(_("Set score as 3"), identifier="score_3"),
                GeodeGtk.MenuItem(_("Set score as 4"), identifier="score_4"),
                GeodeGtk.MenuItem(_("Set score as 5"), identifier="score_5"),
                identifier="score",
            ),
            GeodeGtk.MenuItem(
                _("_Tools"),
                GeodeGtk.MenuItem(
                    _("_Screenshots..."), identifier="screenshots"),
                GeodeGtk.MenuItem(_("Game _log..."), identifier="game_log"),
                GeodeGtk.MenuItem(_("_Notes..."), identifier="notes"),
                None,
                GeodeGtk.MenuItem(_("_Generate a desktop menu entry"),
                                  identifier="menu_entry"),
                None,
                GeodeGtk.MenuItem(_("Define _memory type files..."),
                                  identifier="memory_type"),
                identifier="tools",
            ),
            identifier="menu_game",
        )

        # ------------------------------------
        #   Toolbar
        # ------------------------------------

        self.toolbar_consoles = GeodeGtk.Toolbar(
            GeodeGtk.ToolbarBox(
                GeodeGtk.SearchEntry(
                    identifier="entry",
                    set_hexpand=True,
                    set_placeholder_text=_("Filter..."),
                ),
                GeodeGtk.MenuButton(
                    _("Manage consoles and emulators"),
                    GeodeGtk.MenuItem(
                        _("Add _console"), identifier="add_console"),
                    GeodeGtk.MenuItem(
                        _("Add _emulator"), identifier="add_emulator"),
                    None,
                    GeodeGtk.CheckMenuItem(_("_Hide consoles with no game"),
                                           identifier="hide_empty"),
                    icon_name=Icons.Symbolic.VIEW_MORE,
                    identifier="consoles",
                ),
                merge=True,
            ),
            identifier="toolbar_consoles",
            set_border_width=4,
        )

        self.toolbar_games = GeodeGtk.Toolbar(
            GeodeGtk.ToolbarBox(
                GeodeGtk.Button(
                    _("Play"),
                    identifier="launch",
                    set_style=Gtk.STYLE_CLASS_SUGGESTED_ACTION,
                    set_tooltip_text=_("Launch selected game"),
                ),
                GeodeGtk.ToggleButton(
                    _("Switch between fullscreen and windowed mode"),
                    icon_name=Icons.Symbolic.RESTORE,
                    identifier="fullscreen",
                ),
                merge=True,
            ),
            GeodeGtk.Button(
                _("Set selected game properties"),
                icon_name=Icons.Symbolic.PROPERTIES,
                identifier="parameters",
            ),
            GeodeGtk.ToolbarBox(
                GeodeGtk.Button(
                    _("Show selected game screenshots"),
                    icon_name=Icons.Symbolic.PROPERTIES,
                    identifier="screenshots",
                ),
                GeodeGtk.Button(
                    _("Show selected game log"),
                    icon_name=Icons.Symbolic.PROPERTIES,
                    identifier="game_log",
                ),
                GeodeGtk.Button(
                    _("Show selected game notes"),
                    icon_name=Icons.Symbolic.PROPERTIES,
                    identifier="notes",
                ),
                merge=True,
            ),
            GeodeGtk.MenuButton(
                _("Show selected game tags"),
                icon_name=Icons.Symbolic.PAPERCLIP,
                identifier="tags",
            ),
            None,
            GeodeGtk.ToolbarSwitch(
                GeodeGtk.ToggleButton(
                    _("List view"),
                    icon_name=Icons.Symbolic.LIST,
                    identifier="list",
                ),
                GeodeGtk.ToggleButton(
                    _("Grid icons view"),
                    icon_name=Icons.Symbolic.GRID,
                    identifier="grid",
                ),
                default="list",
                identifier="views",
                merge=True,
            ),
            GeodeGtk.ToolbarBox(
                GeodeGtk.SearchEntry(
                    GeodeGtk.EntryCompletion(
                        Gtk.ListStore(str),
                        identifier="completion",
                        set_text_column=0,
                    ),
                    identifier="entry",
                    set_placeholder_text=_("Filter..."),
                ),
                GeodeGtk.MenuButton(
                    _("Advanced filters"),
                    icon_name=Icons.Symbolic.VIEW_MORE,
                    identifier="filters",
                    set_use_popover=True,
                ),
                merge=True,
            ),
            identifier="toolbar_games",
            set_border_width=4,
            set_spacing=8,
        )

        self.menu_tags = GeodeGtk.Menu(identifier="tags")

        # ------------------------------------
        #   Toolbar - Game filter
        # ------------------------------------

        self.popover_filters = GeodeGtk.Popover(
            GeodeGtk.Box(
                GeodeGtk.Frame(
                    GeodeGtk.ListBox(
                        GeodeGtk.ListBoxCheckItem(
                            _("Favorite"), identifier="favorite"),
                        GeodeGtk.ListBoxCheckItem(
                            _("Unfavorite"), identifier="unfavorite"),
                    ),
                ),
                GeodeGtk.Frame(
                    GeodeGtk.ListBox(
                        GeodeGtk.ListBoxCheckItem(
                            _("Multiplayer"), identifier="multiplayer"),
                        GeodeGtk.ListBoxCheckItem(
                            _("Singleplayer"), identifier="singleplayer"),
                    ),
                ),
                GeodeGtk.Frame(
                    GeodeGtk.ListBox(
                        GeodeGtk.ListBoxCheckItem(
                            _("Finish"), identifier="finish"),
                        GeodeGtk.ListBoxCheckItem(
                            _("Unfinished"), identifier="unfinish"),
                    ),
                ),
                GeodeGtk.Button(_("Reset filters"), identifier="reset"),
                set_border_width=6,
                set_orientation=Gtk.Orientation.VERTICAL,
                set_spacing=6,
            ),
            identifier="popover_filters",
        )

        # ------------------------------------
        #   Infobar
        # ------------------------------------

        self.infobar = GeodeGtk.InfoBar()

        # ------------------------------------
        #   Sidebar - Consoles
        # ------------------------------------

        self.hpaned_consoles = GeodeGtk.HPaned(
            set_position=280,
        )

        self.scroll_consoles = GeodeGtk.ScrolledWindow(
            set_min_content_width=200,
        )

        self.listbox_consoles = GeodeGtk.ListBox(
            identifier="consoles",
            placeholder=_("No console available"),
            set_filter_func=self.check_console_is_visible,
            set_header_func=self.on_generate_console_header,
            set_selection_mode=Gtk.SelectionMode.SINGLE,
            set_sort_func=self.on_sort_consoles_list,
        )

        # ------------------------------------
        #   Sidebar - Game
        # ------------------------------------

        self.vpaned_games = GeodeGtk.VPaned()
        self.hpaned_games = GeodeGtk.HPaned()

        self.scroll_sidebar = GeodeGtk.ScrolledWindow(
            GeodeGtk.Grid(
                GeodeGtk.GridItem(
                    GeodeGtk.Label(
                        identifier="title",
                        set_halign=Gtk.Align.CENTER,
                        set_hexpand=True,
                        set_margin_bottom=12,
                        set_valign=Gtk.Align.CENTER,
                        set_xalign=0.0,
                    ),
                    left=0, top=0, width=1, height=1,
                ),
                GeodeGtk.GridItem(
                    GeodeGtk.Box(
                        GeodeGtk.Frame(
                            GeodeGtk.Viewport(
                                GeodeGtk.Image(
                                    identifier="image",
                                    set_halign=Gtk.Align.CENTER,
                                    set_valign=Gtk.Align.CENTER,
                                ),
                                identifier="viewport",
                            ),
                            identifier="frame",
                            is_expandable=True,
                            is_fillable=True,
                            set_halign=Gtk.Align.CENTER,
                            set_valign=Gtk.Align.CENTER,
                            set_visible=False,
                        ),
                        GeodeGtk.Box(
                            GeodeGtk.Image(identifier="score_1"),
                            GeodeGtk.Image(identifier="score_2"),
                            GeodeGtk.Image(identifier="score_3"),
                            GeodeGtk.Image(identifier="score_4"),
                            GeodeGtk.Image(identifier="score_5"),
                            identifier="score",
                            set_halign=Gtk.Align.CENTER,
                            set_hexpand=True,
                            set_spacing=6,
                            set_valign=Gtk.Align.CENTER,
                            set_visible=False,
                        ),
                        identifier="content",
                        set_halign=Gtk.Align.FILL,
                        set_hexpand=False,
                        set_orientation=Gtk.Orientation.VERTICAL,
                        set_spacing=6,
                        set_valign=Gtk.Align.START,
                        set_vexpand=False,
                    ),
                    left=0, top=1, width=1, height=1,
                ),
                GeodeGtk.GridItem(
                    GeodeGtk.Grid(
                        GeodeGtk.GridItem(
                            GeodeGtk.Label(
                                set_halign=Gtk.Align.END,
                                set_margin_bottom=12,
                                set_style=Gtk.STYLE_CLASS_DIM_LABEL,
                                set_text=_("Launch"),
                                set_valign=Gtk.Align.CENTER,
                            ),
                            left=0, top=0, width=1, height=1,
                        ),
                        GeodeGtk.GridItem(
                            GeodeGtk.Label(
                                identifier="played",
                                set_halign=Gtk.Align.START,
                                set_margin_bottom=12,
                                set_valign=Gtk.Align.CENTER,
                            ),
                            left=1, top=0, width=1, height=1,
                        ),
                        GeodeGtk.GridItem(
                            GeodeGtk.Label(
                                set_halign=Gtk.Align.END,
                                set_margin_bottom=12,
                                set_style=Gtk.STYLE_CLASS_DIM_LABEL,
                                set_text=_("Play time"),
                                set_valign=Gtk.Align.CENTER,
                            ),
                            left=0, top=1, width=1, height=1,
                        ),
                        GeodeGtk.GridItem(
                            GeodeGtk.Label(
                                identifier="play_time",
                                set_halign=Gtk.Align.START,
                                set_margin_bottom=12,
                                set_valign=Gtk.Align.CENTER,
                            ),
                            left=1, top=1, width=1, height=1,
                        ),
                        GeodeGtk.GridItem(
                            GeodeGtk.Label(
                                set_halign=Gtk.Align.END,
                                set_style=Gtk.STYLE_CLASS_DIM_LABEL,
                                set_text=_("Last launch"),
                                set_valign=Gtk.Align.CENTER,
                            ),
                            left=0, top=2, width=1, height=1,
                        ),
                        GeodeGtk.GridItem(
                            GeodeGtk.Label(
                                identifier="last_play",
                                set_halign=Gtk.Align.START,
                                set_valign=Gtk.Align.CENTER,
                            ),
                            left=1, top=2, width=1, height=1,
                        ),
                        GeodeGtk.GridItem(
                            GeodeGtk.Label(
                                set_halign=Gtk.Align.END,
                                set_style=Gtk.STYLE_CLASS_DIM_LABEL,
                                set_text=_("Last play time"),
                                set_valign=Gtk.Align.CENTER,
                            ),
                            left=0, top=3, width=1, height=1,
                        ),
                        GeodeGtk.GridItem(
                            GeodeGtk.Label(
                                identifier="last_time",
                                set_halign=Gtk.Align.START,
                                set_valign=Gtk.Align.CENTER,
                            ),
                            left=1, top=3, width=1, height=1,
                        ),
                        GeodeGtk.GridItem(
                            GeodeGtk.Label(
                                set_halign=Gtk.Align.END,
                                set_margin_bottom=12,
                                set_style=Gtk.STYLE_CLASS_DIM_LABEL,
                                set_text=_("Installed"),
                                set_valign=Gtk.Align.CENTER,
                            ),
                            left=0, top=4, width=1, height=1,
                        ),
                        GeodeGtk.GridItem(
                            GeodeGtk.Label(
                                identifier="installed",
                                set_halign=Gtk.Align.START,
                                set_margin_bottom=12,
                                set_valign=Gtk.Align.CENTER,
                            ),
                            left=1, top=4, width=1, height=1,
                        ),
                        GeodeGtk.GridItem(
                            GeodeGtk.Label(
                                set_halign=Gtk.Align.END,
                                set_style=Gtk.STYLE_CLASS_DIM_LABEL,
                                set_text=_("Emulator"),
                                set_valign=Gtk.Align.CENTER,
                            ),
                            left=0, top=5, width=1, height=1,
                        ),
                        GeodeGtk.GridItem(
                            GeodeGtk.Label(
                                identifier="emulator",
                                set_halign=Gtk.Align.START,
                                set_valign=Gtk.Align.CENTER,
                            ),
                            left=1, top=5, width=1, height=1,
                        ),
                        identifier="information",
                        set_border_width=6,
                        set_column_homogeneous=True,
                        set_column_spacing=12,
                        set_halign=Gtk.Align.FILL,
                        set_hexpand=True,
                        set_row_spacing=6,
                        set_vexpand=True,
                        set_visible=False,
                    ),
                    left=0, top=2, width=1, height=1,
                ),
                identifier="grid",
                set_border_width=12,
                set_column_homogeneous=False,
                set_hexpand=True,
                set_vexpand=True,
            ),
        )

        viewport = self.scroll_sidebar.get_widget("viewport")
        viewport.drag_source_set(
            Gdk.ModifierType.BUTTON1_MASK, list(), Gdk.DragAction.COPY)
        viewport.drag_source_add_uri_targets()

        # ------------------------------------
        #   Games - Views
        # ------------------------------------

        self.views_games = GeodeGEM.Views(interface=self)

        self.views_overlay = GeodeGtk.Overlay(
            self.views_games,
            overlay=GeodeGtk.Revealer(
                GeodeGtk.Box(
                    GeodeGtk.Label(
                        set_text=_("Games loading in progress..."),
                        set_valign=Gtk.Align.CENTER,
                        set_halign=Gtk.Align.CENTER,
                        set_margin_bottom=12,
                        set_margin_start=18,
                        set_margin_end=6,
                        set_margin_top=12,
                    ),
                    GeodeGtk.Spinner(
                        identifier="spinner",
                        set_margin_bottom=12,
                        set_margin_start=6,
                        set_margin_end=18,
                        set_margin_top=12,
                    ),
                    set_style=Gtk.STYLE_CLASS_OSD,
                ),
                identifier="revealer",
                set_valign=Gtk.Align.START,
                set_halign=Gtk.Align.CENTER,
            ),
        )

        # ------------------------------------
        #   Statusbar
        # ------------------------------------

        self.statusbar_progressbar = Gtk.ProgressBar.new()
        self.statusbar_progressbar.set_show_text(True)
        setattr(self.statusbar_progressbar, "identifier", "progressbar")

        self.statusbar = GeodeGtk.Statusbar(
            GeodeGtk.Label(
                identifier="console",
                set_use_markup=True,
            ),
            GeodeGtk.Label(
                identifier="emulator",
                set_use_markup=True,
            ),
            GeodeGtk.Label(
                identifier="game",
                ellipsize=Pango.EllipsizeMode.END,
                set_use_markup=True,
            ),
            None,
            self.statusbar_progressbar,
            GeodeGtk.Image(
                identifier="properties",
                set_from_icon_name=(None, Gtk.IconSize.MENU),
            ),
            GeodeGtk.Image(
                identifier="screenshots",
                set_from_icon_name=(None, Gtk.IconSize.MENU),
            ),
            GeodeGtk.Image(
                identifier="savestates",
                set_from_icon_name=(None, Gtk.IconSize.MENU),
            ),
            identifier="statusbar",
        )

    def __init_packing(self):
        """ Initialize widgets packing in main window
        """

        self.add(self.grid)

        # Main widgets
        self.grid.pack_start(self.menubar, False, False, 0)
        self.grid.pack_start(self.hpaned_consoles, True, True, 0)
        self.grid.pack_start(self.statusbar, False, False, 0)

        self.hpaned_consoles.pack1(self.grid_consoles, False, False)
        self.hpaned_consoles.pack2(self.vpaned_games, True, True)

        self.vpaned_games.pack1(self.hpaned_games, True, True)
        self.hpaned_games.pack1(self.grid_games, True, True)

        # Menubar
        self.menubar.append(self.menubar_main)
        self.menubar.append(self.menubar_view)
        self.menubar.append(self.menubar_game)
        self.menubar.append(self.menubar_edit)
        self.menubar.append(self.menubar_help)

        # Consoles
        self.grid_consoles.pack_start(self.toolbar_consoles, False, False, 0)
        self.grid_consoles.pack_start(self.scroll_consoles, True, True, 0)
        self.scroll_consoles.add(self.listbox_consoles)

        # Toolbar - Games
        self.toolbar_games.get_widget("tags").set_popup(self.menu_tags)
        self.toolbar_games.get_widget("filters").set_popover(
            self.popover_filters)

        # Games
        self.grid_games.pack_start(self.toolbar_games, False, False, 0)
        self.grid_games.pack_start(self.infobar, False, False, 0)
        self.grid_games.pack_start(self.views_overlay, True, True, 0)

    def __init_signals(self):
        """ Initialize widgets signals
        """

        self.logger.info("Associate signals to main interface")

        signals = {
            self: {
                "game-started": [
                    {"method": self.emit_game_started},
                ],
                "game-terminate": [
                    {"method": self.emit_game_terminated},
                ],
                "games-terminate": [
                    {"method": self.emit_games_loading_terminated},
                ],
                "script-terminate": [
                    {"method": self.emit_game_script_terminated},
                ],
                "delete-event": [
                    {"method": self.__stop_interface},
                ],
                "key-press-event": [
                    {"method": self.on_events_manager},
                ],
            },
            self.headerbar: {
                "activate": [
                    {
                        "method": self.on_show_preferences_dialog,
                        "widget": "preferences",
                    },
                    {
                        "method": self.on_show_application_log_dialog,
                        "widget": "log",
                    },
                    {
                        "method": self.on_show_clean_cache_dialog,
                        "widget": "clean_cache",
                    },
                    {
                        "method": self.on_redirect_to_external_link,
                        "widget": "website",
                    },
                    {
                        "method": self.on_redirect_to_external_link,
                        "widget": "report",
                    },
                    {
                        "method": self.on_show_about_dialog,
                        "widget": "about",
                    },
                    {
                        "method": self.__stop_interface,
                        "widget": "quit",
                    },
                ] + [
                    {
                        "method": self.set_games_column_visibility,
                        "args": (widget,),
                        "widget": widget,
                        "allow_block_signal": True,
                    } for widget in self.flags + self.columns
                ],
                "toggled": [
                    {
                        "method": self.set_sidebar_visibility,
                        "widget": "show_sidebar",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.set_sidebar_position,
                        "widget": "right",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.set_sidebar_position,
                        "widget": "bottom",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.set_interface_theme,
                        "widget": "dark_theme",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.set_statusbar_visibility,
                        "widget": "show_statusbar",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.on_switch_games_view,
                        "widget": "list",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.on_switch_games_view,
                        "widget": "grid",
                        "allow_block_signal": True,
                    },
                ],
            },
            self.menubar_main: {
                "activate": [
                    {
                        "method": self.on_show_preferences_dialog,
                        "widget": "preferences",
                    },
                    {
                        "method": self.on_show_application_log_dialog,
                        "widget": "log",
                    },
                    {
                        "method": self.on_show_clean_cache_dialog,
                        "widget": "clean_cache",
                    },
                    {
                        "method": self.__stop_interface,
                        "widget": "quit",
                    },
                ],
            },
            self.menubar_view: {
                "activate": [
                    {
                        "method": self.set_games_column_visibility,
                        "args": (widget,),
                        "widget": widget,
                        "allow_block_signal": True,
                    } for widget in self.flags + self.columns
                ],
                "toggled": [
                    {
                        "method": self.set_sidebar_visibility,
                        "widget": "show_sidebar",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.set_sidebar_position,
                        "widget": "right",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.set_sidebar_position,
                        "widget": "bottom",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.set_interface_theme,
                        "widget": "dark_theme",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.set_statusbar_visibility,
                        "widget": "show_statusbar",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.on_switch_games_view,
                        "widget": "list",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.on_switch_games_view,
                        "widget": "grid",
                        "allow_block_signal": True,
                    },
                ],
            },
            self.menubar_game: {
                "activate": [
                    {
                        "method": self.on_prepare_game_launch,
                        "widget": "launch",
                    },
                    {
                        "method": self.on_show_game_properties_dialog,
                        "widget": "properties",
                    },
                    {
                        "method": self.on_show_screenshots_viewer_dialog,
                        "widget": "screenshots",
                    },
                    {
                        "method": self.on_show_game_log_dialog,
                        "widget": "game_log",
                    },
                    {
                        "method": self.on_show_game_note_dialog,
                        "widget": "notes",
                    },
                ] + [
                    {
                        "method": self.set_game_flag,
                        "widget": widget,
                        "allow_block_signal": True,
                    } for widget in self.flags
                ],
                "toggled": [
                    {
                        "method": self.set_game_fullscreen,
                        "widget": "fullscreen",
                        "allow_block_signal": True,
                    },
                ],
            },
            self.menubar_edit: {
                "activate": [
                    {
                        "method": self.on_show_game_renaming_dialog,
                        "widget": "rename",
                    },
                    {
                        "method": self.on_show_game_duplication_dialog,
                        "widget": "duplicate",
                    },
                    {
                        "method": self.on_show_game_editor_dialog,
                        "widget": "game_file",
                    },
                    {
                        "method": self.on_copy_file_path,
                        "widget": "copy_path",
                    },
                    {
                        "method": self.on_open_file_path,
                        "widget": "open_path",
                    },
                    {
                        "method": self.on_generate_game_desktop_file,
                        "widget": "menu_entry",
                    },
                    {
                        "method": self.on_show_game_maintenance_dialog,
                        "widget": "maintenance",
                    },
                    {
                        "method": self.on_show_game_removing_dialog,
                        "widget": "remove",
                    },
                    {
                        "method": self.on_show_game_backup_memory_dialog,
                        "widget": "memory_type",
                    },
                    {
                        "method": self.set_game_score,
                        "widget": "increase",
                    },
                    {
                        "method": self.set_game_score,
                        "widget": "decrease",
                    },
                ] + [
                    {
                        "method": self.set_game_score,
                        "args": (index,),
                        "widget": f"score_{index}",
                    } for index in range(0, 6)
                ],
            },
            self.menubar_help: {
                "activate": [
                    {
                        "method": self.on_redirect_to_external_link,
                        "widget": "website",
                    },
                    {
                        "method": self.on_redirect_to_external_link,
                        "widget": "report",
                    },
                    {
                        "method": self.on_show_about_dialog,
                        "widget": "about",
                    },
                ],
            },
            self.menu_game: {
                "activate": [
                    {
                        "method": self.on_prepare_game_launch,
                        "widget": "launch",
                    },
                    {
                        "method": self.on_show_game_properties_dialog,
                        "widget": "properties",
                    },
                    {
                        "method": self.on_show_game_renaming_dialog,
                        "widget": "rename",
                    },
                    {
                        "method": self.on_show_game_duplication_dialog,
                        "widget": "duplicate",
                    },
                    {
                        "method": self.on_show_game_editor_dialog,
                        "widget": "game_file",
                    },
                    {
                        "method": self.on_copy_file_path,
                        "widget": "copy_path",
                    },
                    {
                        "method": self.on_open_file_path,
                        "widget": "open_path",
                    },
                    {
                        "method": self.on_show_game_maintenance_dialog,
                        "widget": "maintenance",
                    },
                    {
                        "method": self.on_show_game_removing_dialog,
                        "widget": "remove",
                    },
                    {
                        "method": self.set_game_score,
                        "widget": "increase",
                    },
                    {
                        "method": self.set_game_score,
                        "widget": "decrease",
                    },
                    {
                        "method": self.on_show_screenshots_viewer_dialog,
                        "widget": "screenshots",
                    },
                    {
                        "method": self.on_show_game_log_dialog,
                        "widget": "game_log",
                    },
                    {
                        "method": self.on_show_game_note_dialog,
                        "widget": "notes",
                    },
                    {
                        "method": self.on_generate_game_desktop_file,
                        "widget": "menu_entry",
                    },
                    {
                        "method": self.on_show_game_backup_memory_dialog,
                        "widget": "memory_type",
                    },
                ] + [
                    {
                        "method": self.set_game_flag,
                        "args": (widget,),
                        "widget": widget,
                        "allow_block_signal": True,
                    } for widget in self.flags
                ] + [
                    {
                        "method": self.set_game_score,
                        "args": (index,),
                        "widget": f"score_{index}",
                    } for index in range(0, 6)
                ],
            },
            self.menu_consoles: {
                "activate": [
                    {
                        "method": self.on_show_console_editor_dialog,
                        "widget": "edit_console",
                    },
                    {
                        "method": self.on_show_console_remove_dialog,
                        "widget": "remove_console",
                    },
                    {
                        "method": self.on_show_emulator_editor_dialog,
                        "widget": "edit_emulator",
                    },
                    {
                        "method": self.on_show_emulator_file_dialog,
                        "widget": "edit_file",
                    },
                    {
                        "method": self.on_copy_file_path,
                        "widget": "copy_path",
                    },
                    {
                        "method": self.on_open_file_path,
                        "widget": "open_path",
                    },
                    {
                        "method": self.on_reload_console_games,
                        "widget": "reload",
                    },
                    {
                        "method": self.on_update_consoles_filters,
                        "widget": "favorite",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.on_update_consoles_filters,
                        "widget": "recursive",
                        "allow_block_signal": True,
                    },
                ],
            },
            self.popover_filters: {
                "clicked": [
                    {
                        "method": self.clear_game_filters,
                        "widget": "reset",
                    }
                ],
                "state-set": [
                    {
                        "method": self.on_update_games_filters,
                        "widget": widget,
                    } for widget in self.filters
                ],
            },
            self.views_games.treeview: {
                "cursor-changed": [
                    {
                        "method": self.on_select_game_from_list,
                        "allow_block_signal": True,
                    },
                ],
                "row-activated": [
                    {"method": self.on_prepare_game_launch},
                ],
                "button-press-event": [
                    {"method": self.on_show_game_menu_popup},
                ],
                "key-release-event": [
                    {"method": self.on_show_game_menu_popup},
                ],
                "drag-data-get": [
                    {"method": self.on_drag_data_to_external_application},
                ],
                "query-tooltip": [
                    {"method": self.on_generate_game_tooltip},
                ],
            },
            self.views_games.iconview: {
                "selection-changed": [
                    {
                        "method": self.on_select_game_from_list,
                        "allow_block_signal": True,
                    },
                ],
                "item-activated": [
                    {"method": self.on_prepare_game_launch},
                ],
                "button-press-event": [
                    {"method": self.on_show_game_menu_popup},
                ],
                "key-release-event": [
                    {"method": self.on_show_game_menu_popup},
                ],
                "drag-data-get": [
                    {"method": self.on_drag_data_to_external_application},
                ],
                "query-tooltip": [
                    {"method": self.on_generate_game_tooltip},
                ],
            },
            self.listbox_consoles: {
                "row-activated": [
                    {"method": self.on_select_console_from_list},
                ],
                "button-press-event": [
                    {"method": self.on_show_console_menu_popup},
                ],
                "key-release-event": [
                    {"method": self.on_show_console_menu_popup},
                ],
            },
            self.toolbar_consoles: {
                "activate": [
                    {
                        "method": self.on_show_console_editor_dialog,
                        "widget": "add_console",
                    },
                    {
                        "method": self.on_show_emulator_editor_dialog,
                        "widget": "add_emulator",
                    },
                    {
                        "method": self.on_update_consoles_filters,
                        "widget": "hide_empty",
                        "allow_block_signal": True,
                    },
                ],
                "changed": [
                    {
                        "method": self.on_reload_consoles,
                        "widget": "entry",
                    },
                ],
            },
            self.scroll_sidebar: {
                "drag-data-get": [
                    {
                        "method": self.on_drag_data_to_external_application,
                        "widget": "viewport",
                    },
                ],
            },
            self.toolbar_games: {
                "clicked": [
                    {
                        "method": self.on_prepare_game_launch,
                        "widget": "launch",
                    },
                    {
                        "method": self.on_show_screenshots_viewer_dialog,
                        "widget": "screenshots",
                    },
                    {
                        "method": self.on_show_game_log_dialog,
                        "widget": "game_log",
                    },
                    {
                        "method": self.on_show_game_note_dialog,
                        "widget": "notes",
                    },
                    {
                        "method": self.on_show_game_properties_dialog,
                        "widget": "parameters",
                    },
                ],
                "changed": [
                    {
                        "method": self.on_update_games_filters,
                        "widget": "entry",
                    },
                ],
                "toggled": [
                    {
                        "method": self.set_game_fullscreen,
                        "widget": "fullscreen",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.on_switch_games_view,
                        "widget": "list",
                        "allow_block_signal": True,
                    },
                    {
                        "method": self.on_switch_games_view,
                        "widget": "grid",
                        "allow_block_signal": True,
                    },
                ],
            }
        }

        # Connect widgets and store signals
        self.__geode_cache["signals"] = self.load_signals(signals)
        # Remove signals storage from memory
        del signals

    def __init_storage(self):
        """ Initialize references storages
        """

        # Store image references with associate icons
        self.__images_storage = {
            self.headerbar.get_widget("main_image"):
                Icons.Symbolic.MENU,
            self.headerbar.get_widget("display_image"):
                Icons.Symbolic.VIDEO,
            self.toolbar_consoles.get_widget("consoles_image"):
                Icons.Symbolic.VIEW_MORE,
            self.toolbar_games.get_widget("fullscreen_image"):
                Icons.Symbolic.RESTORE,
            self.toolbar_games.get_widget("grid_image"):
                Icons.Symbolic.GRID,
            self.toolbar_games.get_widget("list_image"):
                Icons.Symbolic.LIST,
            self.toolbar_games.get_widget("notes_image"):
                Icons.Symbolic.EDITOR,
            self.toolbar_games.get_widget("game_log_image"):
                Icons.Symbolic.TERMINAL,
            self.toolbar_games.get_widget("parameters_image"):
                Icons.Symbolic.PROPERTIES,
            self.toolbar_games.get_widget("screenshots_image"):
                Icons.Symbolic.CAMERA,
            self.toolbar_games.get_widget("tags_image"):
                Icons.Symbolic.PAPERCLIP,
        }

        # Store treeview columns references
        self.__columns_storage = [*self.flags, "name", *self.columns]

        # Store widgets references which can change sensitive state
        self.__widgets_storage = (
            # Menubar - Game
            self.menubar_game.get_widget("favorite"),
            self.menubar_game.get_widget("finish"),
            self.menubar_game.get_widget("game_log"),
            self.menubar_game.get_widget("launch"),
            self.menubar_game.get_widget("multiplayer"),
            self.menubar_game.get_widget("notes"),
            self.menubar_game.get_widget("properties"),
            self.menubar_game.get_widget("screenshots"),
            # Menubar - Edit
            self.menubar_edit.get_widget("copy_path"),
            self.menubar_edit.get_widget("duplicate"),
            self.menubar_edit.get_widget("game_file"),
            self.menubar_edit.get_widget("maintenance"),
            self.menubar_edit.get_widget("memory_type"),
            self.menubar_edit.get_widget("menu_entry"),
            self.menubar_edit.get_widget("open_path"),
            self.menubar_edit.get_widget("remove"),
            self.menubar_edit.get_widget("rename"),
            self.menubar_edit.get_widget("score"),
            # Toolbar
            self.toolbar_games.get_widget("launch"),
            self.toolbar_games.get_widget("tags"),
            self.toolbar_games.get_widget("notes"),
            self.toolbar_games.get_widget("game_log"),
            self.toolbar_games.get_widget("parameters"),
            self.toolbar_games.get_widget("screenshots"),
            # Game menu
            self.menu_game.get_widget("copy_path"),
            self.menu_game.get_widget("duplicate"),
            self.menu_game.get_widget("favorite"),
            self.menu_game.get_widget("finish"),
            self.menu_game.get_widget("game_file"),
            self.menu_game.get_widget("game_log"),
            self.menu_game.get_widget("maintenance"),
            self.menu_game.get_widget("memory_type"),
            self.menu_game.get_widget("menu_entry"),
            self.menu_game.get_widget("multiplayer"),
            self.menu_game.get_widget("notes"),
            self.menu_game.get_widget("open_path"),
            self.menu_game.get_widget("remove"),
            self.menu_game.get_widget("rename"),
            self.menu_game.get_widget("screenshots"),
        )

    def __init_shortcuts(self):
        """ Generate shortcuts signals from user configuration
        """

        self.logger.info("Associate shortcuts to main interface")

        # Disconnect previous shortcut to avoid multiple allocation
        for key, mod in self.__geode_cache.get("shortcuts"):
            self.shortcuts_group.disconnect_key(key, mod)

        # Retrieve shortcuts metadata from GeodeGEM project
        shortcuts = Configuration(
            engine_utils.get_data("data", "config", "shortcuts.conf"))

        for section in shortcuts.sections():
            shortcut = self.config.item(
                "keys", *shortcuts.get(section, "shortcut").split(" | "))

            # Parse shortcut to Gtk specific format
            accelerator = Gtk.accelerator_parse(shortcut)
            if not Gtk.accelerator_valid(*accelerator):
                self.logger.warning(f"Invalid accelerator for {section}")
                continue

            self.shortcuts_map.change_entry(section, *accelerator, True)

            # Associate shortcut to each widgets
            for widget in shortcuts.get(section, "widgets").split(" | "):
                internal_widget = getattr(self, widget, None)

                # Specified widget must be declared into main interface
                if internal_widget is None:
                    self.logger.warning(
                        f"Cannot retrieve widget '{widget}' from interface")
                    continue

                # Retrieve internal widget for GeodeGtkCommon objects
                if hasattr(internal_widget, "has_widget"):
                    widget_key = shortcuts.get(section, "key")

                    if not internal_widget.has_widget(widget_key):
                        self.logger.warning(
                            f"Cannot retrieve internal widget '{widget_key}'")
                        continue

                    internal_widget = internal_widget.get_widget(widget_key)

                self.logger.debug(f"Associate shortcut '{shortcut}' to "
                                  f"{widget}/{widget_key}")
                internal_widget.add_accelerator("activate",
                                                self.shortcuts_group,
                                                *accelerator,
                                                Gtk.AccelFlags.VISIBLE)

                # Store current shortcut to remove it properly later
                self.__geode_cache["shortcuts"].append(accelerator)

        del shortcuts

    def __init_interface(self):
        """ Init main interface
        """

        self.selection = dict(console=None, game=None)

        # ------------------------------------
        #   Toolbar icons
        # ------------------------------------

        if self.toolbar_icons_size in self.toolbar_sizes:
            size = self.toolbar_sizes.get(self.toolbar_icons_size)

            # Avoid to change icon size if there is no change
            if not size == self.__toolbar_cache.get("size"):
                self.__toolbar_cache["size"] = size

                for widget, icon in self.__images_storage.items():
                    widget.set_from_icon_name(icon, size)

        # ------------------------------------
        #   Toolbar view switcher
        # ------------------------------------

        if self.view_mode == Columns.Key.Grid:
            self.headerbar.set_active(True, widget="grid")
            self.menubar_view.set_active(True, widget="grid")
            self.toolbar_games.get_widget("views").switch_to("grid")

            self.views_games.set_view(GeodeGEM.Views.Name.GRID)

        else:
            self.headerbar.set_active(True, widget="list")
            self.menubar_view.set_active(True, widget="list")
            self.toolbar_games.get_widget("views").switch_to("list")

            self.views_games.set_view(GeodeGEM.Views.Name.LIST)

        # ------------------------------------
        #   Toolbar design
        # ------------------------------------

        # Update design colorscheme
        ui_utils.on_prefer_dark_theme(self.use_dark_theme)

        self.headerbar.set_active(self.use_dark_theme, widget="dark_theme")
        self.menubar_view.set_active(self.use_dark_theme, widget="dark_theme")

        if self.use_dark_theme:
            self.logger.debug("Use dark variant for GTK+ theme")

        else:
            self.logger.debug("Use light variant for GTK+ theme")

        # Update design template
        if not self.use_classic_theme:
            self.logger.debug("Use default theme for GTK+ interface")
            self.set_titlebar(self.headerbar)

        else:
            self.logger.debug("Use classic theme for GTK+ interface")

        # ------------------------------------
        #   Treeview columns order
        # ------------------------------------

        self.views_games.treeview.set_columns_order(*self.columns_order)

        # ------------------------------------
        #   Treeview columns sorting
        # ------------------------------------

        column, order = (Columns.List.NAME, Gtk.SortType.ASCENDING)

        if self.load_sort_column_at_startup:
            column = getattr(Columns.List, self.load_last_column.upper(), None)

            # Cannot found a column, use the default one
            if column is None:
                column = Columns.List.NAME

            if self.load_sort_column_order == "desc":
                order = Gtk.SortType.DESCENDING

        self.views_games.treeview.sorted_model.set_sort_column_id(
            column, order)

        # ------------------------------------
        #   Window size
        # ------------------------------------

        try:
            width, height = self.main_window_size

            self.window_size.base_width = int(width)
            self.window_size.base_height = int(height)

            self.resize(int(width), int(height))

        except ValueError as error:
            self.logger.error("Cannot resize main window: %s" % str(error))

        self.set_geometry_hints(
            self,
            self.window_size,
            Gdk.WindowHints.MIN_SIZE | Gdk.WindowHints.BASE_SIZE)

        self.set_position(Gtk.WindowPosition.CENTER)

        # ------------------------------------
        #   Sidebars position
        # ------------------------------------

        if self.sidebar_console_position is not None \
           and self.sidebar_console_position > -1:
            self.hpaned_consoles.set_position(self.sidebar_console_position)

        if self.sidebar_game_position is not None \
           and self.sidebar_game_position > -1:

            if self.sidebar_orientation == "horizontal":
                self.hpaned_games.set_position(self.sidebar_game_position)

            else:
                self.vpaned_games.set_position(self.sidebar_game_position)

    def __show_interface(self):
        """ Show main interface widgets
        """

        self.hide()
        self.unrealize()
        self.show_all()

        self.infobar.show_all()
        self.menu_consoles.show_all()
        self.menu_game.show_all()
        self.menubar_edit.show_all()
        self.menubar_game.show_all()
        self.menubar_help.show_all()
        self.menubar_main.show_all()
        self.menubar_view.show_all()
        self.scroll_sidebar.show_all()
        self.toolbar_consoles.show_all()

        # Manage window template
        if self.use_classic_theme:
            self.menubar.show_all()
            self.headerbar.hide()
        else:
            self.headerbar.show_all()
            self.menubar.hide()

        self.set_infobar_visibility(False)
        self.set_sidebar_visibility(
            self.show_sidebar, register_modification=False)
        self.set_statusbar_visibility(
            self.show_statusbar, register_modification=False)
        self.statusbar_progressbar.hide()

    def __start_interface(self):
        """ Load data and start interface
        """

        self.logger.info("Use Python interpreter version %d.%d.%d" % (
            version_info.major,
            version_info.minor,
            version_info.micro))

        self.logger.info("Use GTK+ library version %d.%d.%d" % (
            Gtk.get_major_version(),
            Gtk.get_minor_version(),
            Gtk.get_micro_version()))

        self.logger.info("Use Geode-GEM version %s (%s)" % (
            self.__version, Metadata.CODE_NAME))

        # ------------------------------------
        #   Load informations
        # ------------------------------------

        self.load_interface(True)

        # Check welcome message status in gem.conf
        if self.config.getboolean("gem", "welcome", fallback=True):
            dialog = GeodeDialog.Message(
                self,
                _("Welcome!"),
                _("Welcome and thanks for choosing Geode-GEM as emulator "
                  "manager. Start using Geode-GEM by dropping some files into "
                  "the interface.\n\nEnjoy and have fun :D"),
                Icons.Symbolic.SMILE_BIG,
                False)

            dialog.set_size_request(500, -1)

            dialog.run()
            dialog.destroy()

            # Disable welcome message for next launch
            self.config.modify("gem", "welcome", False)
            self.config.update()

        # Set default filters flag
        self.clear_game_filters()

        # Initialize main loop instance
        try:
            self.main_loop = GLib.MainLoop()
            self.main_loop.run()

        except KeyboardInterrupt:
            self.logger.warning("Terminate by keyboard interrupt")

            self.__stop_interface()

    def __stop_interface(self, *args):
        """ Save data and stop interface
        """

        self.logger.info("Close interface")

        # ------------------------------------
        #   Threads
        # ------------------------------------

        self.logger.debug("Terminate remaining threaded processus")

        # Remove games listing thread
        list_thread = self.threads.get("listing")
        if not list_thread == 0:
            self.logger.debug(f"Remove thread ID {list_thread}")
            GLib.source_remove(list_thread)

        # Remove game and script threads
        for thread in thread_enumerate().copy():

            # Avoid to remove the main thread
            if thread is not thread_main_thread():
                self.logger.debug(f"Remove thread {thread.name}")

                if isinstance(thread, GameThread):
                    thread.proc.terminate()
                    thread.join()
                    self.emit_game_terminated(None, thread)

                elif isinstance(thread, GamesLoadingThread):
                    thread.join()

        # Close open notes dialog
        if len(self.threads["notes"]) > 0:
            self.logger.debug("Terminate openning notes")

            notes = self.threads["notes"].copy()
            for identifier, thread in notes.items():
                thread.emit_response(None, Gtk.ResponseType.APPLY)

        # ------------------------------------
        #   Last console
        # ------------------------------------

        # Save current console as last_console in gem.conf
        row = self.listbox_consoles.get_selected_row()
        if row is not None:
            last_console = self.config.item("gem", "last_console", None)

            # Avoid to modify gem.conf if console is already in conf
            if last_console is None or not last_console == row.console.id:
                self.config.modify("gem", "last_console", row.console.id)

                self.logger.info(
                    f"Save {row.console.name} console for next startup")

        # ------------------------------------
        #   Last sorted column
        # ------------------------------------

        column, order = \
            self.views_games.treeview.sorted_model.get_sort_column_id()

        if column is not None and order is not None:

            for key, value in Columns.List.__dict__.items():
                if not key.startswith("__") and not key.endswith("__"):

                    if column == value:
                        self.config.modify("gem", "last_sort_column", key)

            if order == Gtk.SortType.ASCENDING:
                self.config.modify("gem", "last_sort_column_order", "asc")

            elif order == Gtk.SortType.DESCENDING:
                self.config.modify("gem", "last_sort_column_order", "desc")

        # ------------------------------------
        #   Columns order
        # ------------------------------------

        columns = [column.identifier
                   for column in self.views_games.treeview.get_columns()]

        self.config.modify("columns", "order", ':'.join(columns))

        # ------------------------------------
        #   Games view mode
        # ------------------------------------

        if self.toolbar_games.get_active("list"):
            self.config.modify("gem", "games_view_mode", Columns.Key.List)

        elif self.toolbar_games.get_active("grid"):
            self.config.modify("gem", "games_view_mode", Columns.Key.Grid)

        # ------------------------------------
        #   Windows size
        # ------------------------------------

        self.config.modify("windows", "main", "%dx%d" % self.get_size())

        # ------------------------------------
        #   Sidebars position
        # ------------------------------------

        self.config.modify("gem",
                           "sidebar_console_position",
                           self.hpaned_consoles.get_position())

        if self.sidebar_orientation == "horizontal":
            position = self.hpaned_games.get_position()

        else:
            position = self.vpaned_games.get_position()

        self.config.modify("gem", "sidebar_game_position", position)

        self.config.update()

        if self.main_loop.is_running():
            self.logger.debug("Close main loop")
            self.__block_signals()
            self.main_loop.quit()

    def __block_signals(self):
        """ Block check button signals to avoid stack overflow when toggled
        """

        for signal, widget in self.__geode_cache.get("signals").items():
            widget.handler_block(signal)

    def __unblock_signals(self):
        """ Unblock check button signals
        """

        for signal, widget in self.__geode_cache.get("signals").items():
            widget.handler_unblock(signal)

    def block_signals(function):
        """ Decorator to manage signals blocking behavior
        """

        def __function__(self, *args, **kwargs):
            self.__block_signals()
            results = function(self, *args, **kwargs)
            self.__unblock_signals()

            return results

        return __function__

    def use_sensitivity(function):
        """ Decorator to manage main interface sensitivity
        """

        def __function__(self, *args, **kwargs):
            self.set_sensitive(False)
            results = function(self, *args, **kwargs)
            self.set_sensitive(True)

            return results

        return __function__

    def check_console_is_ready(self, row):
        """ Check if selected console can be used properly by the user

        Parameters
        ----------
        row : gem.gtk.widgets.ListBoxSelectorItem
            Activated row
        """

        if row.console.path is None:
            self.logger.warning(f"No games directory for '{row.console.id}'")

            self.set_infobar_content(
                _("There is no games directory for this console"),
                icon=Gtk.MessageType.WARNING)

        elif not row.console.path.exists():
            self.logger.warning(
                f"Cannot open '{row.console.path}' for '{row.console.id}'")

            self.set_infobar_content(
                _("Specified games directory do not exists on filesystem"),
                icon=Gtk.MessageType.WARNING)

        elif not access(row.console.path, R_OK):
            self.logger.warning(
                f"Cannot read '{row.console.path}' for '{row.console.id}'")

            self.set_infobar_content(
                _("The games directory cannot not read"),
                icon=Gtk.MessageType.WARNING)

        elif row.console.emulator is None:
            self.logger.warning(f"Cannot find emulator for {row.console.name}")

            self.set_infobar_content(
                _("There is no default emulator set for this console"),
                icon=Gtk.MessageType.WARNING)

        elif not row.console.emulator.exists:
            self.logger.warning(
                f"{row.console.emulator.name} is not available")

            self.set_infobar_content(
                _("%s emulator cannot been found on your system") % (
                    f"<b>{row.console.emulator.name}</b>"),
                icon=Gtk.MessageType.ERROR)

        else:
            self.set_infobar_visibility(False)

    def check_console_is_visible(self, row, *args):
        """ Filter list with consoles searchentry text

        Parameters
        ----------
        row : gem.gtk.widgets.ListBoxSelectorItem
            Activated row
        """

        if self.hide_empty_console and len(row.console) == 0:
            return False

        widget = self.toolbar_consoles.get_widget("entry")
        if widget is None:
            return False

        filter_text = widget.get_text().strip().lower()
        if not len(filter_text):
            return True

        return filter_text in row.console.name.lower()

    def check_game_is_visible(self, model, row, *args):
        """ Check if a game is visible in both views based on user filters

        Parameters
        ----------
        model : Gtk.TreeModel
            Treeview model which receive signal
        row : Gtk.TreeModelRow
            Treeview current row
        """

        # Get game object from treeview
        if model == self.views_games.treeview.list_model:
            game = model.get_value(row, Columns.List.OBJECT)

        elif model == self.views_games.iconview.list_model:
            game = model.get_value(row, Columns.Grid.OBJECT)

        if game is None:
            return False

        # ------------------------------------
        #   Check filter
        # ------------------------------------

        tags = [game.name.lower()]
        if len(game.tags) > 0:
            tags.extend(game.tags)

        text = self.toolbar_games.get_widget("entry").get_text().lower()

        found = any(match(fr"{text}$", element) or text in element
                    for element in tags)

        # ------------------------------------
        #   Set status
        # ------------------------------------

        flags = [
            ("favorite", "unfavorite", game.favorite),
            ("multiplayer", "singleplayer", game.multiplayer),
            ("finish", "unfinish", game.finish)
        ]

        for first, second, status in flags:
            first = self.popover_filters.get_active(f"{first}_switch")
            second = self.popover_filters.get_active(f"{second}_switch")

            # Avoid to check both activated filters
            if first and second:
                continue

            found = found and ((status and first) or (not status and second))

        return found

    def check_game_selection(self):
        """ Check selected game

        This function check if the selected game in the games treeview is the
        same as the one stock in self.selection["game"]. If this is not the
        case, the self.selection is reset

        Returns
        -------
        bool
            Check status
        """

        name = None

        if self.selection["game"] is not None:
            name = self.selection["game"].name

        if name is not None:
            model, treeiter = self.get_selected_treeiter_from_container(
                self.views_games.treeview)

            if treeiter is not None:
                treeview_name = model.get_value(treeiter, Columns.List.NAME)

                if not treeview_name == name:
                    selection = self.views_games.treeview.get_selection()
                    if selection is not None:
                        selection.unselect_iter(treeiter)

                    self.selection["game"] = None

                    self.set_sensitive_interface()
                    self.set_game_information()

                    return False

        return True

    def check_gba_game_use_mednafen(self, game):
        """ Check if specified game is a GBA rom which use Mednafen

        Parameters
        ----------
        game : geode_gem.engine.game.Game
            Game instance

        Returns
        -------
        bool
            True if game is a GBA rom using Mednafen, False otherwise
        """

        if not self.__mednafen_status or game is None:
            return False

        emulator = game.emulator
        return game.extension == ".gba" and "mednafen" in emulator.binary.name

    def check_version(self):
        """ Check development version when debug mode is activate

        This function allow the developper to know which hash version is
        currently using

        Returns
        -------
        str
            Application version
        """

        version = Metadata.VERSION

        if self.api.debug and Path(".git").exists():
            output = ui_utils.call_external_application(
                "git", "rev-parse", "--short", "HEAD")

            if output is not None and match(r'^[\d\w]+$', output):
                return f"{version}-{output}"

        return version

    def clear_game_filters(self, widget=None, events=None):
        """ Reset game filters

        Parameters
        ----------
        widget : Gtk.Widget, optional
            Object which receive signal (Default: None)
        event : Gdk.EventButton or Gdk.EventKey, optional
            Event which triggered this signal (Default: None)
        """

        for widget in self.filters:
            self.popover_filters.set_active(True, widget=widget)

        self.toolbar_games.set_style(widget="filters")

    def emit(self, *args):
        """ Override emit function

        This override allow to use Interface function from another thread in
        MainThread
        """

        GLib.idle_add(GObject.GObject.emit, self, *args)

    def emit_game_note_response(self, widget, response, dialog, title, path):
        """ Close notes dialog

        This function close current notes dialog and save his textview buffer
        to the game notes file

        Parameters
        ----------
        widget : Gtk.Dialog
            Dialog object
        response : Gtk.ResponseType
            Dialog object user response
        dialog : Gtk.Dialog
            Dialog editor object
        title : str
            Dialog title, it's game name by default
        path : pathlib.Path
            Notes path
        """

        self.config.modify("windows", "notes", "%dx%d" % dialog.get_size())
        self.config.update()

        self.save_editor_options(dialog)

        dialog.destroy()

        if str(path) in self.threads["notes"]:
            del self.threads["notes"][str(path)]

    def emit_game_started(self, widget, game):
        """ The game processus has been started

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        game : gem.engine.game.Game
            Game object
        """

        self.on_execute_script_thread("ongamestarted", game)

    def emit_game_terminated(self, widget, thread):
        """ Terminate the game processus and update data

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        thread : gem.widgets.game.GameThread
            Game thread
        """

        game = thread.game

        if not thread.error:
            game.played += 1
            game.play_time = thread.game.play_time + thread.delta
            game.last_launch_time = thread.delta
            game.last_launch_date = date.today()

            # Update game from database
            self.api.update_game(game)

            # Update games views
            treeiter, griditer = self.views_games.get_iter_from_key(game.id)

            self.views_games.treeview.set_value(
                treeiter, Columns.List.PLAYED, game.played)
            self.views_games.treeview.set_value(
                treeiter,
                Columns.List.LAST_PLAY,
                ui_utils.string_from_date(game.last_launch_date))
            self.views_games.treeview.set_value(
                treeiter,
                Columns.List.LAST_TIME_PLAY,
                ui_utils.string_from_time(game.last_launch_time))
            self.views_games.treeview.set_value(
                treeiter,
                Columns.List.TIME_PLAY,
                ui_utils.string_from_time(game.play_time))
            self.views_games.treeview.set_value(
                treeiter,
                Columns.List.SCREENSHOT,
                self.get_ui_icon(
                    Columns.List.SCREENSHOT, game.screenshots))
            self.views_games.treeview.set_value(
                treeiter,
                Columns.List.SAVESTATE,
                self.get_ui_icon(
                    Columns.List.SAVESTATE, game.savestates))

            self.set_game_information()

        # ----------------------------------------
        #   Refresh widgets
        # ----------------------------------------

        select_console = self.selection.get("console", None)
        select_game = self.views_games.get_selected_game()

        if select_console is None:
            self.logger.debug(f"Restore widgets status for {game.name}")
            self.set_sensitive_interface()

        # Check if current selected file is the same as thread file
        elif select_game is not None and select_game.id == game.id:
            self.logger.debug(f"Restore widgets status for {game.name}")
            self.__tooltip_cache["instance"] = None

            if self.check_gba_game_use_mednafen(game):
                self.menu_game.set_sensitive(True, widget="memory_type")
                self.menubar_edit.set_sensitive(True, widget="memory_type")

        # ----------------------------------------
        #   Manage thread
        # ----------------------------------------

        # Remove this game from threads list
        if game.id in self.threads["playing"]:
            self.logger.debug(f"Remove {game.name} from process cache")
            del self.threads["playing"][game.id]

        if not len(self.threads["playing"]):
            self.headerbar.set_sensitive(True, widget="quit")
            self.menubar_main.set_sensitive(True, widget="quit")

        self.set_game_playing_status(game)

        # ----------------------------------------
        #   Manage script
        # ----------------------------------------

        # Remove this script from threads list
        if game.id in self.threads["scripts"]:
            self.logger.debug(f"Remove {game.name} from scripts cache")
            del self.threads["scripts"][game.id]

        self.on_execute_script_thread("ongamestopped", game)

    def emit_games_loading_terminated(self, widget, thread):
        """ Terminate the game processus and update data

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        thread : gem.widgets.game.GamesLoadingThread
            GamesLoadingThread thread instance
        """

        if self.selection["console"] is None \
           or not thread.console.id == self.selection["console"].id:
            return

        if thread.error_message is not None:
            self.logger.error(thread.error_message)
            self.set_infobar_content(thread.error_message,
                                     icon=Gtk.MessageType.ERROR)

        else:
            self.views_games.set_sensitive(True)
            self.views_overlay.get_widget("revealer").set_reveal_child(False)
            self.views_overlay.get_widget("spinner").stop()

            self.threads["listing"] = GLib.idle_add(
                self.on_append_games(thread.console).__next__)

        del self.threads["loading"][thread.console.id]

    def emit_game_script_terminated(self, widget, thread):
        """ Terminate the script processus

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        thread : gem.widgets.script.ScriptThread
            Game thread
        """

        # Remove this script from threads list
        if thread.game.id in self.threads["scripts"]:
            self.logger.debug(f"Remove {thread.game.name} from scripts cache")
            del self.threads["scripts"][thread.game.id]

    def get_game_desktop_file(self, game):
        """ Check user applications folder for specific desktop file

        Parameters
        ----------
        game : geode_gem.engine.game.Game
            Game instance

        Returns
        -------
        bool
            Desktop file status

        Examples
        --------
        >>> MainWindow.get_game_desktop_file("unavailable_file")
        False

        Notes
        -----
        In GNU/Linux desktop, the default folder for user applications is:

            ~/.local/share/applications/
        """

        return Folders.APPLICATIONS.joinpath(f"{game.path.stem}.desktop")

    def get_game_log_file(self, game):
        """ Check if a game has an output file available

        Parameters
        ----------
        game : geode_gem.engine.game.Game
            Game instance

        Returns
        -------
        str or None
            Output file path
        """

        if game is not None:
            log_path = self.api.get_local("logs", f"{game.id}.log")
            if log_path.exists():
                return log_path

        return None

    def get_icon_from_cache(self, *args):
        """ Retrieve icon from cache folder

        Returns
        -------
        str
            Cached icon path
        """

        return self.__cache.joinpath(*args)

    def get_pixbuf_from_cache(self,
                              key, size, identifier, path, use_cache=True,
                              use_blank=True):
        """ Retrieve an icon from cache or generate it

        Parameters
        ----------
        key : str
            Cache category folder
        size : int
            Pixbuf size in pixels
        identifier : str
            Icon identifier
        path : pathlib.Path
            Icon path
        use_cache : bool, optional
            Use cache directory and save new generated icons into cache
        use_blank : bool, optional
            Use a blank icon when specified path do not exists

        Returns
        -------
        Gdk.Pixbuf or None
            New cached icon or None if no icon has been generated
        """

        cache_path = self.get_icon_from_cache(
            key, f"{size}x{size}", f"{identifier}.png")

        # Retrieve icon from cache folder
        if use_cache and cache_path.exists() and cache_path.is_file():
            return GdkPixbuf.Pixbuf.new_from_file(str(cache_path))

        if path is None:
            return None

        # Check if icon exists in Gtk icons theme
        if not path.exists():
            filename = ui_utils.get_filename_from_icon_theme(
                self.icons_theme, str(path), size)

            if filename is not None:
                path = Path(filename).expanduser()

        icon, need_save = None, False

        # Generate a new cache icon
        if path.exists() and path.is_file():

            # Check the file mime-type to avoid non-image file
            if ui_utils.magic_from_file(path, mime=True).startswith("image/"):
                icon = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    str(path), size, size, True)

                need_save = True

        # Save generated icon to cache
        if use_cache and need_save:
            try:
                self.logger.debug(f"Save generated icon to {cache_path}")

                if not cache_path.parent.exists():
                    cache_path.parent.mkdir(mode=0o755, parents=True)

                icon.savev(str(cache_path), "png", list(), list())

            except GLib.Error:
                self.logger.exception("An error occur during cache generation")

        if icon is None and use_blank:
            return self.icons_blank.get(size)

        return icon

    def get_mednafen_memory_type_file(self, game):
        """ Retrieve a memory type file for a specific game

        Parameters
        ----------
        game : geode_gem.engine.game.Game
            Game instance

        Returns
        -------
        pathlib.Path
            Memory type file path
        """

        return \
            Path.home().joinpath(".mednafen", "sav", f"{game.path.stem}.type")

    def get_new_console_row(self, console):
        """ Append console row in consoles list

        Parameters
        ----------
        console : gem.engine.console.Console
            Console instance

        Returns
        -------
        Gtk.ListBoxRow
            New console row
        """

        grid = GeodeGtk.Box(
            GeodeGtk.Image(
                identifier="icon",
            ),
            GeodeGtk.Label(
                identifier="title",
                set_ellipsize=Pango.EllipsizeMode.END,
                set_halign=Gtk.Align.START,
            ),
            set_border_width=6,
            set_orientation=Gtk.Orientation.HORIZONTAL,
            set_spacing=8,
        )

        row = Gtk.ListBoxRow()
        row.add(grid)
        row.show_all()

        # Add an alias to quickly retrieve object instances
        setattr(row, "grid", grid)
        setattr(row, "console", console)

        self.listbox_consoles.add(row)

        self.set_console_row_information(row, console)

        return row

    def get_screenshot_from_game(self, game):
        """ Retrieve a screenshot from specified game

        Parameters
        ----------
        game : geode_gem.engine.game.Game
            Game instance

        Returns
        -------
        pathlib.Path
            Latest screenshot if found, None otherwise
        """

        if not len(game.screenshots):
            return None

        # Ordered game screenshots
        if not self.use_random_screenshot:
            screenshots = sorted(game.screenshots)

        # Get a random file from game screenshots
        else:
            screenshots = game.screenshots
            shuffle(screenshots)

        return Path(screenshots[-1])

    def get_selected_treeiter_from_container(self, widget):
        """ Retrieve treeiter from container widget

        Parameters
        ----------
        widget : Gtk.Container
            Container widget

        Returns
        -------
        Gtk.TreeStore, Gtk.TreeIter
            Selected treeiter
        """

        return widget.get_model(), widget.get_selected_treeiter()

    def get_window_size_from_configuration(self, window, width, height):
        """ Retrieve size for a specific window from configuration

        Parameters
        ----------
        window : str
            Window name
        width : int
            Window width size
        height : int
            Window width height

        Returns
        -------
        tuple
            Window size as integer tuple
        """

        try:
            size = self.config.get(
                "windows", window, fallback=f"{width}x{height}").split('x')

        except ValueError:
            size = (width, height)

        return tuple(map(int, size))

    def get_ui_icon(self, column, status):
        """ Retrieve an icon for a specific treeview column based on his status

        Parameters
        ----------
        column : str
            Column name based on Columns metadata class
        status : bool
            Activate status for icon

        Returns
        -------
        str
            Icon name if found in treeview_icons storage, None otherwise
        """

        if column not in self.treeview_icons:
            return None

        activate, unactivate = self.treeview_icons.get(column)

        icon_name = activate if status else unactivate
        if icon_name is None:
            return None

        if self.use_symbolic_icon:
            return getattr(Icons.Symbolic, icon_name.upper(), None)

        return getattr(Icons, icon_name.upper(), None)

    def load_configuration(self):
        """ Load main configuration file and store values
        """

        if getattr(self, "config", None) is None:
            self.config = Configuration(
                self.api.get_config("gem.conf"),
                interpolation=ExtendedInterpolation(),
                strict=False)

            # Get missing keys from config/gem.conf
            self.config.add_missing_data(
                engine_utils.get_data("data", "config", "gem.conf"))

        else:
            self.logger.debug("Reload configuration file")

            self.config.reload()

        # ------------------------------------
        #   Configuration values
        # ------------------------------------

        self.toolbar_icons_size = self.config.get(
            "gem", "toolbar_icons_size", fallback="small-toolbar")

        self.view_mode = self.config.get(
            "gem", "games_view_mode", fallback=Columns.Key.List)

        self.columns_order = self.config.get(
            "columns", "order", fallback=Columns.ORDER).split(':')

        self.load_last_column = self.config.get(
            "gem", "last_sort_column", fallback="Name")

        self.load_sort_column_at_startup = self.config.getboolean(
            "gem", "load_sort_column_startup", fallback=True)

        self.load_sort_column_order = self.config.get(
            "gem", "last_sort_column_order", fallback="asc")

        self.load_console_at_startup = self.config.getboolean(
            "gem", "load_console_startup", fallback=True)

        self.load_last_console = self.config.get(
            "gem", "last_console", fallback=None)

        self.hide_empty_console = self.config.getboolean(
            "gem", "hide_empty_console", fallback=False)

        self.use_dark_theme = self.config.getboolean(
            "gem", "dark_theme", fallback=False)

        self.use_classic_theme = self.config.getboolean(
            "gem", "use_classic_theme", fallback=False)

        self.use_ellipsize_title = self.config.getboolean(
            "gem", "sidebar_title_ellipsize", fallback=True)

        self.use_random_screenshot = self.config.getboolean(
            "gem", "show_random_screenshot", fallback=True)

        self.show_headerbar_buttons = self.config.getboolean(
            "gem", "show_header", fallback=True)

        self.show_sidebar = self.config.getboolean(
            "gem", "show_sidebar", fallback=True)

        self.show_statusbar = self.config.getboolean(
            "gem", "show_statusbar", fallback=True)

        self.sidebar_orientation = self.config.get(
            "gem", "sidebar_orientation", fallback="vertical")

        self.sidebar_console_position = self.config.getint(
            "gem", "sidebar_console_position", fallback=None)

        self.sidebar_game_position = self.config.getint(
            "gem", "sidebar_game_position", fallback=None)

        self.treeview_lines = self.config.get(
            "gem", "games_treeview_lines", fallback="none")

        self.main_window_size = self.config.get(
            "windows", "main", fallback="1024x768").split('x')

        self.use_symbolic_icon = self.config.getboolean(
            "treeview", "use_symbolic_icon", fallback=False)

        self.date_format = self.config.get(
            "date", "date_format", fallback="%%x").replace("%%", '%')

        self.datetime_format = self.config.get(
            "date", "datetime_format", fallback="%%x %%X").replace("%%", '%')

        # ------------------------------------
        #   Configuration operations
        # ------------------------------------

        # Avoid to have an empty string for last console value
        if not len(self.load_last_console):
            self.load_last_console = None

    def load_consoles(self, init_interface):
        """ Load consoles into interface ListBox

        Parameters
        ----------
        init_interface : bool
            Interface first initialization
        """

        consoles = self.api.get_consoles()

        previous_selection = None

        last_console = self.selection.get("console")
        if init_interface:
            last_console = self.load_last_console
        elif last_console is not None:
            last_console = last_console.id

        # Ensure to load at first the previous selected console
        if self.load_console_at_startup and last_console is not None:
            sorted_consoles = list()
            for console in consoles:
                if console.id == last_console:
                    sorted_consoles.insert(0, console)
                    previous_selection = console
                else:
                    sorted_consoles.append(console)

            consoles = sorted_consoles

        # Reset consoles caches
        self.consoles_iter.clear()
        # Remove previous consoles objects
        for child in self.listbox_consoles.get_children():
            self.listbox_consoles.remove(child)

        # Reset games view content
        self.views_games.clear()
        # Reset games view widgets
        self.views_games.set_placeholder_visibility(True)
        self.set_sidebar_visibility(False, register_modification=False)

        self.logger.debug("Load consoles into main interface")
        for row in self.on_append_consoles(consoles):
            # Store console iter
            self.consoles_iter[row.console.id] = row

            if previous_selection is not None and \
               row.console.id == previous_selection.id:
                self.on_select_console_from_list(
                    self.listbox_consoles, row, force=not init_interface)

        self.on_reload_consoles()

        self.logger.info(
            f"{len(self.listbox_consoles)} console(s) has been added")

    @block_signals
    def load_interface(self, init_interface=False):
        """ Load main interface

        Parameters
        ----------
        init_interface : bool, optional
            Interface first initialization (Default: False)
        """

        self.logger.debug(
            "%s main interface" % ("Load" if init_interface else "Reload"))

        self.api.init()

        # Retrieve user configuration
        self.load_configuration()

        # Retrieve user shortcuts
        self.__init_shortcuts()

        # Initialize main widgets
        if init_interface:
            self.__init_interface()

            self.__show_interface()

        # ------------------------------------
        #   Widgets
        # ------------------------------------

        self.set_infobar_visibility(False)

        self.set_sensitive_interface()

        # Show window buttons into headerbar
        self.headerbar.set_show_close_button(self.show_headerbar_buttons)

        # Show sidebar visibility buttons
        self.headerbar.set_active(self.show_sidebar, widget="show_sidebar")
        self.menubar_view.set_active(self.show_sidebar, widget="show_sidebar")

        # Show statusbar visibility buttons
        self.headerbar.set_active(self.show_statusbar, widget="show_statusbar")
        self.menubar_view.set_active(
            self.show_statusbar, widget="show_statusbar")

        # ------------------------------------
        #   Sidebar
        # ------------------------------------

        label_sidebar_title = self.scroll_sidebar.get_widget("title")

        if self.use_ellipsize_title:
            label_sidebar_title.set_line_wrap(False)
            label_sidebar_title.set_single_line_mode(True)
            label_sidebar_title.set_ellipsize(Pango.EllipsizeMode.END)
            label_sidebar_title.set_line_wrap_mode(Pango.WrapMode.WORD)

        else:
            label_sidebar_title.set_line_wrap(True)
            label_sidebar_title.set_single_line_mode(False)
            label_sidebar_title.set_ellipsize(Pango.EllipsizeMode.NONE)
            label_sidebar_title.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)

        self.set_sidebar_position(init_interface=init_interface)

        # ------------------------------------
        #   Treeview
        # ------------------------------------

        # Games - Treeview lines
        self.views_games.treeview.set_grid_lines(
            self.treeview_grid_lines.get(
                self.treeview_lines, Gtk.TreeViewGridLines.NONE))

        # Games - Treeview columns
        for key in self.__columns_storage:
            visibility = self.config.getboolean("columns", key, fallback=True)

            self.views_games.treeview.get_widget(key).set_visible(visibility)

            if key in self.menubar_view.inner_widgets.keys():
                self.headerbar.set_active(visibility, widget=key)
                self.menubar_view.set_active(visibility, widget=key)

        self.views_games.treeview.columns_autosize()

        # ------------------------------------
        #   Consoles
        # ------------------------------------

        self.toolbar_consoles.set_active(
            self.hide_empty_console, widget="hide_empty")

        self.load_consoles(init_interface)

    def load_signals(self, signals):
        """ Load and connect signals from a dictionnary

        Parameters
        ----------
        signals : dict
            Interface signals to connect

        Returns
        -------
        dict
            Connected signals references
        """

        signals_storage = dict()

        for instance, actions_dict in signals.items():
            for action, storage in actions_dict.items():
                for metadata in storage:
                    try:
                        # Use standard widget from Gtk
                        widget = instance
                        # Retrieve subwidget from GeodeGtk objects
                        if "widget" in metadata:
                            widget = instance.get_widget(metadata["widget"])

                        signal = widget.connect(
                            action,
                            metadata.get("method"),
                            *metadata.get("args", list()))

                        if metadata.get("allow_block_signal", False):
                            signals_storage[signal] = widget

                            if not hasattr(widget, 'identifier'):
                                continue

                            self.logger.debug(
                                f"Associate signal identifier '{signal}' to "
                                f"{instance.identifier}/{widget.identifier}")

                    except Exception:
                        self.logger.exception(
                            f"Cannot connect signal for {widget}: "
                            f"{list(metadata.values())}")

        return signals_storage

    def on_append_consoles(self, consoles):
        """ Append to consoles lisbox all available consoles

        This function add every consoles into consoles listbox and inform user
        when an emulator binary is missing
        """

        for console in consoles:
            self.logger.debug(f"Append console '{console.id}'")

            try:
                # Load console games files cache
                console.list_files()

            except Exception as error:
                self.logger.error(error)

            yield self.get_new_console_row(console)

    def on_append_games(self, console):
        """ Append to games treeview all games from console

        This function add every games which match console extensions to games
        treeview

        Parameters
        ----------
        console : gem.engine.console.Console
            Console object

        Notes
        -----
        Using yield avoid an UI freeze when append a lot of games
        """

        # Get current thread id
        current_thread_id = self.threads.get("listing")

        # Start a timer for debug purpose
        started = datetime.now()

        self.set_sidebar_visibility(len(console) > 0 and self.show_sidebar,
                                    register_modification=False)

        self.set_games_filter_completion_from_console(console)

        column, order = \
            self.views_games.treeview.sorted_model.get_sort_column_id()

        games = console.get_games()
        self.set_games_order_from_column(
            games, column, reverse=(order == Gtk.SortType.DESCENDING))

        # Append games
        self.statusbar_progressbar.show()

        for index, game in self.views_games.append_games(console, games):

            # Another thread has been called by user, close this one
            if not current_thread_id == self.threads.get("listing"):
                yield False

            self.set_statusbar_content()

            self.statusbar.set_widget_value(
                "progressbar", index=index, length=len(games))

            yield True

        self.set_statusbar_content()

        # End the timer
        delta = (datetime.now() - started).total_seconds()

        self.logger.debug(f"Append {len(console)} game(s) for '{console.id}' "
                          f"in {delta} second(s)")

        self.statusbar_progressbar.hide()

        # Close thread
        self.threads["listing"] = int()

        yield False

    def on_copy_file_path(self, widget):
        """ Copy path to clipboard

        Parameters
        ----------
        widget : Gtk.Widget
            object which received the signal
        """

        path = None

        if widget == self.menu_consoles.get_widget("copy_path"):
            if self.__geode_cache.get("row") is not None:
                path = self.__geode_cache.get("row").console.path

        elif widget.identifier == "copy_path":
            game = self.views_games.get_selected_game()
            if game and game.path.exists():
                path = game.path

        if path is not None:
            self.clipboard.set_text(str(path), -1)

    def on_drag_data_to_external_application(self, widget,
                                             context, data, info, time):
        """ Set rom file path uri

        This function send rom file path uri when user drag a game from gem and
        drop it to extern application

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        context : Gdk.DragContext
            Drag context
        data : Gtk.SelectionData
            Received data
        info : int
            Info that has been registered with the target in the Gtk.TargetList
        time : int
            Timestamp at which the data was received
        """

        if isinstance(widget, Gtk.TreeView) or isinstance(widget, Gtk.IconView):
            game = self.views_games.get_selected_game()
            if game is not None:
                data.set_uris([f"file://{game.path}"])

        elif (isinstance(widget, Gtk.Viewport)
              and self.__sidebar_cache.get("image") is not None):
            data.set_uris([f"file://{self.__sidebar_cache.get('image')}"])

    def on_drag_data_to_main_interface(self, widget,
                                       context, x, y, data, info, delta):
        """ Manage drag & drop acquisition

        This function receive drag files and install them into the correct
        games folder. If a file extension can be find in multiple consoles,
        a dialog appear to ask user where he want to put it.

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        context : Gdk.DragContext
            Drag context
        x : int
            X coordinate where the drop happened
        y : int
            Y coordinate where the drop happened
        data : Gtk.SelectionData
            Received data
        info : int
            Info that has been registered with the target in the Gtk.TargetList
        delta : int
            Timestamp at which the data was received
        """

        GObject.signal_stop_emission_by_name(widget, "drag_data_received")

        if not info == 0:
            return

        # Avoid to read data dropped from main interface
        if Gtk.drag_get_source_widget(context) is not None:
            return

        self.logger.debug("Received data from drag & drop")

        # ----------------------------------------
        #   Check received URIs
        # ----------------------------------------

        filepaths = dict()

        for uri in data.get_uris():
            result = urlparse(uri)
            if not result.scheme == "file":
                continue

            path = Path(url2pathname(result.path)).expanduser()
            if path and path.exists():
                filepaths[path] = list()

        # ----------------------------------------
        #   Retrieve consoles for every file
        # ----------------------------------------

        consoles = self.api.get_consoles()

        for path in filepaths:
            self.logger.debug(f"Receive {path.name}")

            # Lowercase extension
            extension = str()
            # Only retrieve extensions and not part of the name
            for subextension in path.suffixes:
                if subextension not in path.stem:
                    extension += subextension.lower()

            # Remove the first dot to match console extensions system
            if extension and extension[0] == '.':
                extension = extension[1:]

            # Check consoles which
            for console in consoles:
                if extension in console.extensions:
                    filepaths[path].append(console)

            # Move favorite console on first position
            filepaths[path].sort(key=lambda console: console.favorite)

        # ----------------------------------------
        #   Drag and drop dialog
        # ----------------------------------------

        if len(filepaths) > 0:
            self.on_show_drag_and_drop_dialog(filepaths)

    def on_events_manager(self, widget, event):
        """ Manage widgets for specific keymaps

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        event : Gdk.EventButton or Gdk.EventKey
            Event which triggered this signal
        """

        # Give me more lifes, powerups or cookies konami code, I need more
        konami_code = [Gdk.KEY_Up, Gdk.KEY_Up,
                       Gdk.KEY_Down, Gdk.KEY_Down,
                       Gdk.KEY_Left, Gdk.KEY_Right,
                       Gdk.KEY_Left, Gdk.KEY_Right]

        if event.keyval in konami_code:
            self.__geode_cache["keys"].append(event.keyval)

            if self.__geode_cache.get("keys") == konami_code:
                dialog = GeodeDialog.Message(
                    self,
                    "Someone wrote the KONAMI CODE !",
                    "Nice catch ! You have discover an easter-egg ! But, this "
                    "kind of code is usefull in a game, not in an emulators "
                    "manager !",
                    Icons.Symbolic.MONKEY)

                dialog.set_size_request(500, -1)

                dialog.run()
                dialog.destroy()

                self.__geode_cache["keys"] = list()

            if not self.__geode_cache.get("keys") == \
               konami_code[0:len(self.__geode_cache.get("keys"))]:
                self.__geode_cache["keys"] = list()

    def on_execute_script_thread(self, script, game):
        """ Execute a script in a dedicated thread for a specific game

        Paremeters
        ----------
        script : str
            Script name
        game : geode_gem.engine.game.Game
            Game instance
        """

        path = self.api.get_local(script)
        if not path.exists() or not access(path, X_OK):
            return

        self.threads["scripts"][game.id] = ScriptThread(self, path, game)
        self.threads["scripts"][game.id].start()

    def on_generate_console_header(self, row, before, *args):
        """ Update consoles listboxrow header based on console favorite status

        Parameters
        ----------
        row : Gtk.ListBoxRow
            Row to update
        before : Gtk.ListBoxRow
            Previous row, None if row is the first one
        """

        header = None

        if before is None and row.console.favorite:
            header = GeodeGtk.Label("label_favorite",
                                    set_markup=f"<b>{_('Favorite')}</b>")

        elif (not row.console.favorite and (
              not before or before.console.favorite)):
            header = GeodeGtk.Label("label_consoles",
                                    set_markup=f"<b>{_('Consoles')}</b>")

        if header is not None:
            header.set_margin_top(6)
            header.set_margin_bottom(6)
            header.set_style(Gtk.STYLE_CLASS_DIM_LABEL)

        row.set_header(header)

    @use_sensitivity
    def on_generate_game_desktop_file(self, *args):
        """ Generate application desktop file

        This function generate a .desktop file to allow user to launch the game
        from his favorite applications launcher
        """

        model, treeiter = self.get_selected_treeiter_from_container(
            self.views_games.treeview)

        console = self.selection.get("console", None)
        game = self.views_games.get_selected_game()

        if not all((treeiter, game, console)):
            return

        if game.emulator is None or game.emulator.id not in self.api.emulators:
            return

        icon = str()
        if game.cover is not None and game.cover.exists():
            icon = game.cover
        elif console.icon is not None:
            if console.icon.exists():
                icon = console.icon
            else:
                icon = self.api.get_local("icons", f"{console.icon}.png")

        # Fill template
        values = {
            "%name%": game.name,
            "%icon%": icon,
            "%path%": game.path.parent,
            "%command%": ' '.join(game.command())
        }

        # Put game path between quotes
        values["%command%"] = \
            values["%command%"].replace(str(game.path), f"\"{game.path}\"")

        try:
            # Read default template
            template = engine_utils.get_data(
                "data", "config", "template.desktop").read_text()

            # Replace custom variables
            for key, value in values.items():
                template = template.replace(key, str(value))

            # Check ~/.local/share/applications
            if not Folders.APPLICATIONS.exists():
                Folders.APPLICATIONS.mkdir(mode=0o755, parents=True)

            # Write the new desktop file
            file = self.get_game_desktop_file(game)
            file.write_text(template)

            self.set_message(
                _("Generate menu entry"),
                _("%s was generated successfully") % file.name,
                Icons.INFORMATION)

        except OSError:
            self.set_message(
                _("Generate menu entry for %s") % game.name,
                _("An error occur during generation, consult log for "
                  "further details."),
                Icons.ERROR)

    def on_generate_game_tooltip(self, treeview, x, y, keyboard, tooltip):
        """ Show game informations tooltip

        Parameters
        ----------
        treeview : Gtk.TreeView
            Widget which received the signal
        x : int
            X coordinate for mouse cursor position
        y : int
            Y coordinate for mouse cursor position
        keyboard : bool
            Set as True if the tooltip has been trigged by keyboard
        tooltip : Gtk.Tooltip
            Tooltip widget

        Returns
        -------
        bool
            Tooltip visible status
        """

        # Show a tooltip when the show_tooltip option is activate
        if not self.config.getboolean("gem", "show_tooltip", fallback=True):
            return False

        # Show a tooltip when the main window is sentitive only
        if not self.get_sensitive():
            return False

        # Get relative treerow position based on absolute cursor
        # coordinates
        x, y = treeview.convert_widget_to_bin_window_coords(x, y)

        selection = treeview.get_path_at_pos(x, y)
        # Using a tuple to mimic Gtk.TreeView behavior
        if treeview == self.views_games.iconview and selection is not None:
            selection = (selection)

        if not selection:
            return False

        model = treeview.get_model()
        treeiter = model.get_iter(selection[0])

        column_id = Columns.Grid.OBJECT
        if treeview == self.views_games.treeview:
            column_id = Columns.List.OBJECT

        game = model.get_value(treeiter, column_id)

        # Reload tooltip when another game is hovered
        if not self.__tooltip_cache.get("instance") == game:
            self.__tooltip_cache = {
                "data": list(),
                "instance": game,
                "pixbuf": None,
            }

            return False

        # Get new data from hovered game
        if len(self.__tooltip_cache.get("data")) == 0:
            data = [
                f"<big><b>{ui_utils.replace_for_markup(game.name)}</b></big>"]

            if not game.play_time == timedelta():
                data.append(": ".join(
                    [f"<b>{_('Play time')}</b>",
                     engine_utils.parse_timedelta(game.play_time)]))

            if not game.last_launch_time == timedelta():
                data.append(": ".join(
                    [f"<b>{_('Last launch')}</b>",
                     engine_utils.parse_timedelta(game.last_launch_time)]))

            # Fancy new line
            if len(data) > 1:
                data.insert(1, str())

            self.__tooltip_cache["data"] = data

        console = self.selection["console"]

        # Get new screenshots from hovered game
        if console is not None and self.__tooltip_cache.get("pixbuf") is None:
            image = None

            # Retrieve user choice for tooltip image
            tooltip_image = self.config.get(
                "gem", "tooltip_image_type", fallback="screenshot")

            if tooltip_image in ["both", "screenshot"]:
                image = self.get_screenshot_from_game(game)

            if not image and tooltip_image in ["both", "cover"]:
                if game.cover:
                    image = game.cover
                    if not game.cover.exists():
                        image = ui_utils.get_filename_from_icon_theme(
                            self.icons_theme, str(image), 96)

            # Check if image exists and is not a directory
            if image is not None:
                try:
                    image = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        str(image), -1, 96, True)

                except GLib.Error:
                    self.logger.exception(
                        "An error occur during tooltip generation")

            else:
                image = None

            self.__tooltip_cache["pixbuf"] = image

        # Only show tooltip when data are available
        if len(self.__tooltip_cache.get("data")) == 0:
            return False

        tooltip.set_markup('\n'.join(self.__tooltip_cache.get("data")))
        if self.__tooltip_cache.get("pixbuf") is not None:
            tooltip.set_icon(self.__tooltip_cache.get("pixbuf"))

        self.__tooltip_cache["instance"] = game

        return True

    def on_open_file_path(self, widget):
        """ Open directory into files manager

        Parameters
        ----------
        widget : Gtk.Widget
            object which received the signal
        """

        path = None

        if widget == self.menu_consoles.get_widget("open_path"):
            if self.__geode_cache.get("row") is not None:
                path = self.__geode_cache.get("row").console.path

        elif widget.identifier == "open_path":
            game = self.views_games.get_selected_game()
            if game is not None and game.path.parent.exists():
                path = game.path.parent

        if path is not None and path.exists():
            self.logger.debug(f"Open '{path}' directory in files manager")

            try:
                self.__xdg_open_instance.launch_uris([f"file://{path}"], None)

            except GLib.Error:
                self.logger.exception("Cannot open files manager")

    def on_prepare_game_launch(self, widget=None, *args):
        """ Prepare the game launch

        This function prepare the game launch and start a thread when
        everything are done

        Parameters
        ----------
        widget : Gtk.Widget, optional
            Object which receive signal (Default: None)
        """

        game = self.views_games.get_selected_game()
        if game is None or game.emulator is None \
           or not self.check_game_selection():
            return False

        # This game was already started
        if game.id in self.threads["playing"]:

            # Double-click shortcut is only use to launch game, not stop it
            if not isinstance(widget, Gtk.TreeView) and \
               not isinstance(widget, Gtk.IconView):
                self.threads["playing"][game.id].proc.terminate()

            return False

        console = self.selection.get("console", None)
        if console is None or game.emulator is None:
            return False

        if game.emulator.id not in self.api.emulators:
            return False

        self.logger.info(f"Initialize {game.name}")

        # Run game
        try:
            thread = GameThread(
                self,
                game,
                fullscreen=self.toolbar_games.get_active("fullscreen"))

            # Save thread references
            self.threads["playing"][game.id] = thread
            # Launch thread
            thread.start()

            self.set_game_playing_status(game)

        except FileNotFoundError:
            self.set_message(
                _("Cannot launch game"),
                _("%s binary cannot be found") % game.emulator.name)
            return False

        return True

    @block_signals
    def on_prepare_drag_and_drop_installation(self, data, options):
        """ Install received file in user system

        Parameters
        ----------
        data : dict
            Received files
        option : dict
            User options from DND dialog

        Notes
        -----
        Using yield to show a progressbar whitout freeze
        """

        # Update mouse cursor
        self.get_window().set_cursor(
            Gdk.Cursor.new_from_name(self.window_display, "wait"))

        self.statusbar.set_widget_value("progressbar")
        self.statusbar_progressbar.show()

        yield True

        validate_index = int()

        # Manage files
        for index, (path, console) in enumerate(data.items()):
            self.statusbar.set_widget_value(
                "progressbar", index=index, length=len(data))

            yield True

            # Lowercase extension
            extension = str()
            # Only retrieve extensions and not part of the name
            for subextension in path.suffixes:
                if subextension not in path.stem:
                    extension += subextension.lower()

            # Destination path
            new_path = console.path.joinpath(
                ''.join([path.stem, extension])).expanduser()

            # Check consoles games subdirectory
            if not new_path.parent.exists():

                if options["create"]:
                    new_path.parent.mkdir(mode=0o755, parents=True)

                else:
                    self.logger.warning(
                        "%s directory not exists" % new_path.parent)

            # Replace an existing file
            if new_path.exists():
                if new_path.is_file() and options["replace"]:
                    new_path.unlink()

            # Move or copy file to the correct location
            if new_path.parent.exists() \
               and new_path.parent.is_dir() \
               and not new_path.exists():
                validate_index += 1

                engine_utils.copy(path, new_path)

                if not options["copy"]:
                    path.unlink()

                game = console.get_game(
                    engine_utils.generate_identifier(new_path))

                # Add a new game to console storage if not exists
                if game is None:
                    game = console.add_game(new_path)

                # Update installed time
                else:
                    game.installed = datetime.fromtimestamp(
                        getctime(new_path)).date()

                # Update console tooltip
                if console.id in self.consoles_iter:
                    self.set_console_row_information(
                        self.consoles_iter[console.id], console)

                # This file is owned by current selected console
                if self.selection["console"] is not None \
                   and console.id == self.selection["console"].id:

                    # Remove an old entry in views
                    self.views_games.remove_game(game.id)

                    # Add a new item to views
                    self.views_games.append_game(console, game)

                    if self.views_games.view_placeholder.get_visible():
                        self.set_statusbar_content()

                        self.views_games.set_placeholder_visibility(False)

                        self.set_sidebar_visibility(
                            self.show_sidebar, register_modification=False)

        # Reset mouse cursor
        self.get_window().set_cursor(
            Gdk.Cursor.new_from_name(self.window_display, "default"))

        # Update consoles filters
        self.on_reload_consoles()

        self.statusbar_progressbar.hide()

        # Show an informative dialog
        text = _("No game has been added")
        if validate_index > 0:
            text = ngettext(
                _("1 game has been added"),
                _("%d games have been added") % validate_index,
                validate_index)

        self.set_message(_("Games installation"),
                         text,
                         Icons.Symbolic.INFORMATION)

        yield False

    def on_redirect_to_external_link(self, widget, *args):
        """ Open an external link

        Parameters
        ----------
        widget : Gtk.MenuItem
            object which received the signal
        """

        try:
            if widget.identifier == "website":
                link = Metadata.WEBSITE
            elif widget.identifier == "report":
                link = Metadata.BUG_TRACKER

            self.logger.debug(f"Open {link} in web navigator")
            self.__xdg_open_instance.launch_uris([link], None)

        except GLib.Error:
            self.logger.exception("Cannot open external link")

    def on_reload_consoles(self, *args):
        """ Reload consoles list when user set a filter
        """

        self.listbox_consoles.invalidate_sort()
        self.listbox_consoles.invalidate_filter()

    def on_reload_console_games(self, *args):
        """ Reload games list from selected console
        """

        row = self.listbox_consoles.get_selected_row()
        if row is not None:
            self.on_select_console_from_list(None, row, force=True)

    @block_signals
    def on_select_console_from_list(self, widget, row, force=False):
        """ Select a console

        This function occurs when the user select a console in the consoles
        listbox

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        row : gem.gtk.widgets.ListBoxSelectorItem
            Activated row
        force : bool
            Force console selection even if this is the same console
        """

        # Avoid to reload the same console
        selected_console = self.selection.get("console")
        if selected_console is not None \
           and selected_console.id == row.console.id and not force:
            return

        self.logger.debug(f"Select {row.console.name} console")

        self.selection = {
            "game": None,
            "console": row.console,
        }

        self.__console_icon = self.get_pixbuf_from_cache(
            "consoles", 96, row.console.id, row.console.icon)

        self.__console_thumbnail = self.get_pixbuf_from_cache(
            "consoles", 22, row.console.id, row.console.icon)

        self.icons_games_views = {
            "treeview": self.__console_thumbnail,
            "iconview": self.__console_icon,
        }

        # Manage previous threads
        if not self.threads["listing"] == 0:
            GLib.source_remove(self.threads["listing"])

        if row.console.id in self.threads["loading"]:
            self.threads["loading"][row.console.id].join()

        # Set console combobox active iter
        self.listbox_consoles.select_row(row)

        # Check console and emulator
        self.check_console_is_ready(row)

        # Ensure to reload files list if necessary
        if row.console.path is not None and row.console.path.exists():
            row.console.init_games(reload_files=force)

        self.set_statusbar_content()
        self.set_sensitive_interface()

        has_games = len(row.console) > 0

        self.set_sidebar_visibility(has_games and self.show_sidebar,
                                    register_modification=False)

        self.views_games.set_placeholder_visibility(not has_games)
        self.views_games.set_sensitive(True)
        self.views_games.clear()

        self.set_game_information()

        if has_games:
            self.logger.info(
                f"Found {len(row.console)} game(s) for {row.console.name}")

            self.views_overlay.get_widget("revealer").set_reveal_child(True)
            self.views_overlay.get_widget("spinner").start()

            self.views_games.set_sensitive(False)

            games_loading_thread = GamesLoadingThread(self, row.console)
            games_loading_thread.start()

            self.threads["loading"][row.console.id] = games_loading_thread

        else:
            self.logger.info(f"No game available for {row.console.name}")

    @block_signals
    def on_select_game_from_list(self, widget):
        """ Select a game

        This function occurs when the user select a game in the games treeview

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        # Current selected game
        game = self.views_games.get_selected_game()

        # No game has been choosen (when the user click in the empty view area)
        if game is None:
            # Unselect both games views
            self.views_games.unselect_all()

            # Reset sidebar widgets and menus entries
            self.set_sensitive_interface()
            self.set_game_information()

        # A new game has been selected
        elif not self.selection["game"] == game:
            self.logger.debug(f"Select game '{game.id}'")

            # Synchronize selection between both games views
            self.on_synchronize_game_selection(widget, game)

            # Update game informations and widgets
            self.set_sensitive_interface()
            self.set_game_information()

        # Store game instance
        self.selection["game"] = game

    @use_sensitivity
    def on_show_about_dialog(self, *args):
        """ Show about dialog
        """

        about = Gtk.AboutDialog(use_header_bar=not self.use_classic_theme)
        about.set_transient_for(self)
        about.set_program_name(Metadata.NAME)
        about.set_version(f"{self.__version} - {Metadata.CODE_NAME}")
        about.set_comments(Metadata.DESCRIPTION)
        about.set_copyright(Metadata.COPYLEFT)
        about.set_website(Metadata.WEBSITE)
        about.set_authors([
            "Ellena Lubert (PacMiam)"
        ])
        about.set_artists([
            f"Evan-Amos {Metadata.EVAN_AMOS} - Public Domain"
        ])
        about.set_translator_credits('\n'.join([
            "Anthony Jorion (Pingax)",
            "José Luis Lopez Castillo (DarkNekros)",
        ]))
        about.add_credit_section(_("Tested by"), [
            "Bruno Visse (atralfalgar)",
            "Jérôme Vigneron (Herlief)",
        ])
        about.set_license_type(Gtk.License.GPL_3_0)

        # Strange case... With an headerbar, the AboutDialog got some useless
        # buttons whitout any reasons. To avoid this, I remove any widget from
        # headerbar which is not a Gtk.StackSwitcher.
        if not self.use_classic_theme:
            children = about.get_header_bar().get_children()

            for child in children:
                if type(child) is not Gtk.StackSwitcher:
                    about.get_header_bar().remove(child)

        about.run()
        about.destroy()

    @use_sensitivity
    def on_show_application_log_dialog(self, *args):
        """ Show gem log

        This function show the gem log content in a non-editable dialog
        """

        if not self.api.log.exists():
            return

        dialog = GeodeDialog.Editor(
            self,
            _("Application log"),
            self.api.log,
            self.get_window_size_from_configuration("log", 800, 600),
            Icons.Symbolic.TERMINAL,
            editable=False)

        dialog.run()

        self.config.modify("windows", "log", "%dx%d" % dialog.get_size())
        self.config.update()

        self.save_editor_options(dialog)

        dialog.destroy()

    @use_sensitivity
    def on_show_clean_cache_dialog(self, *args):
        """ Rebuild icons cache directory
        """

        if not Folders.CACHE.exists():
            return

        success = False

        dialog = GeodeDialog.CleanCache(self)

        if dialog.run() == Gtk.ResponseType.YES:
            # Remove cache directory
            rmtree(str(Folders.CACHE))
            # Generate directories
            Folders.CACHE.mkdir(mode=0o755, parents=True)

            for name in ("consoles", "emulators", "games"):
                for size in getattr(Icons.Size, name.upper(), list()):
                    path = Folders.CACHE.joinpath(name, f"{size}x{size}")
                    if path.exists():
                        continue

                    self.logger.debug(f"Generate {path}")
                    path.mkdir(mode=0o755, parents=True)

            success = True

        dialog.destroy()

        if success:
            self.set_message(
                _("Rebuild icons cache"),
                _("Icons cache directory has been succesfully cleaned."),
                Icons.INFORMATION)

    @block_signals
    @use_sensitivity
    def on_show_console_editor_dialog(self, widget, *args):
        """ Open console editor dialog

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        selected_row = self.listbox_consoles.get_selected_row()

        if widget == self.toolbar_consoles.get_widget("add_console"):
            console = Console(self.api)
            previous_id = None
            previous_path = None
            previous_extensions = None

        elif self.__geode_cache.get("row") is not None:
            console = self.__geode_cache.get("row").console
            previous_id = console.id
            previous_path = console.path
            previous_extensions = console.extensions
            # Retrieve the correct console instance from api
            console = deepcopy(self.api.get_console(previous_id))

        dialog = GeodeDialog.Console(
            self,
            console,
            self.api.consoles,
            self.api.emulators,
            self.get_window_size_from_configuration("console", 800, 600))

        if dialog.run() == Gtk.ResponseType.APPLY:
            console = dialog.save()
        else:
            console = None

        self.config.modify("windows", "console", "%dx%d" % dialog.get_size())
        self.config.update()

        dialog.destroy()

        if console is None:
            return

        if previous_id is None:
            self.logger.info(f"Add '{console.id}' to consoles collection")
            self.api.add_console(console.name, console.as_dict().items())

        elif not console.id == previous_id:
            self.logger.info(
                f"Replace '{previous_id}' console with '{console.id}'")
            self.api.replace_console(previous_id, console)

        else:
            self.logger.info(f"Update '{console.id}' console")
            self.api.update_console(console)

        # Write console data
        self.api.write_data(GEM.Consoles)

        # Reload console cached game files if path or extensions is not the
        # same as previously
        reload_needed = (
            previous_id is None or
            (previous_path is not None and console.path is not None
             and not previous_path == console.path)
            or (previous_extensions is None
                and not set(previous_extensions) == set(console.extensions)))

        if console.path is not None and console.path.exists():
            try:
                if reload_needed:
                    console.init_games()
                else:
                    console.list_files()

            except OSError as error:
                self.logger.warning(error)

        # Remove previous console storage
        if previous_id in self.consoles_iter:
            del self.consoles_iter[previous_id]

        # Store row with the new identifier
        self.consoles_iter[console.id] = self.__geode_cache.get("row")

        # Remove thumbnails from cache
        for size in ("22x22", "24x24", "48x48", "64x64", "96x96"):
            cache_path = self.get_icon_from_cache(
                "consoles", size, f"{console.id}.png")
            if cache_path.exists():
                self.logger.debug(f"Remove '{cache_path}' from filesystem")
                remove(cache_path)

        # Update console row
        if widget.identifier == "add_console":
            row = self.get_new_console_row(console)

            # Store console iter
            self.consoles_iter[row.console.id] = row

            self.set_message(
                _("New console"),
                _("%s has been correctly added to your configuration.") % (
                    console.name),
                Icons.Symbolic.INFORMATION)

        else:
            self.set_console_row_information(
                self.__geode_cache.get("row"), console)

        # Refilter consoles list
        self.on_reload_consoles()

        # Reload games list
        if selected_row is not None \
           and selected_row == self.__geode_cache.get("row"):
            self.selection["console"] = self.__geode_cache.get("row").console

            # Update flag checkboxes from console submenu
            self.menu_consoles.set_active(console.favorite, widget="favorite")
            self.menu_consoles.set_active(console.recursive, widget="recursive")

            self.on_reload_console_games()

    @block_signals
    def on_show_console_menu_popup(self, widget, event):
        """ Open context menu

        This function open context-menu when user right-click or use context
        key on games treeview

        Parameters
        ----------
        widget : Gtk.ListBox
            Object which receive signal
        event : Gdk.EventButton or Gdk.EventKey
            Event which triggered this signal

        Returns
        -------
        bool
            Context menu popup status
        """

        row = None

        # Mouse
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == Gdk.BUTTON_SECONDARY:
                row = widget.get_row_at_y(int(event.y))
        # Keyboard
        elif event.type == Gdk.EventType.KEY_RELEASE:
            if event.keyval == Gdk.KEY_Menu:
                row = widget.get_selected_row()

        self.__geode_cache["row"] = row

        if row is None:
            return False

        self.menu_consoles.set_active(
            row.console.favorite, widget="favorite")
        self.menu_consoles.set_active(
            row.console.recursive, widget="recursive")

        # Allow to reload games list only for the current viewed console
        current_console = self.selection.get("console", None)
        self.menu_consoles.set_sensitive(
            current_console and current_console.id == row.console.id,
            widget="reload")

        # Check console emulator
        if row.console.emulator:
            configuration = row.console.emulator.configuration

            # Check emulator configurator
            self.menu_consoles.set_sensitive(
                configuration and configuration.exists(),
                widget="edit_file")

        else:
            self.menu_consoles.set_sensitive(False, widget="edit_file")

        self.menu_consoles.set_sensitive(
            row.console.emulator is not None, widget="edit_emulator")

        # Check console paths
        if row.console.path:
            self.menu_consoles.set_sensitive(
                row.console.path.exists(), widget="copy_path")
            self.menu_consoles.set_sensitive(
                row.console.path.exists(), widget="open_path")
            self.menu_consoles.set_sensitive(
                row.console.path.exists(), widget="reload")

        # Popup menu
        if event.type == Gdk.EventType.BUTTON_PRESS:
            self.menu_consoles.popup_at_pointer(event)
        elif event.type == Gdk.EventType.KEY_RELEASE:
            self.menu_consoles.popup_at_widget(
                row, Gdk.Gravity.CENTER, Gdk.Gravity.NORTH, event)

        return True

    @block_signals
    @use_sensitivity
    def on_show_console_remove_dialog(self, *args):
        """ Remove a console from user configuration
        """

        if self.__geode_cache.get("row") is None:
            return

        console = self.__geode_cache.get("row").console

        dialog = GeodeDialog.Question(
            self,
            _("Remove a console"),
            _("Are you sure you want to remove %s ?") % (
                f"<b>{console.name}</b>"))

        if dialog.run() == Gtk.ResponseType.YES:
            # Remove console
            self.api.delete_console(console.id)
            # Write consoles data
            self.api.write_data(GEM.Consoles)

            selected_row = self.listbox_consoles.get_selected_row()

            # Remove the current selected console
            if selected_row == self.__geode_cache.get("row"):
                self.selection["console"] = None

                self.views_games.clear()

                self.set_infobar_visibility(False)
                self.set_sidebar_visibility(False, register_modification=False)

                self.views_games.set_placeholder_visibility(True)

                self.set_game_information()

            # Remove row from listbox
            self.listbox_consoles.remove(self.__geode_cache.get("row"))

        dialog.destroy()

    @use_sensitivity
    def on_show_drag_and_drop_dialog(self, filepaths):
        """ Open drag and drop dialog

        Parameters
        ----------
        filepaths : list
            Dropped files as Path object list
        """

        data, options = None, None

        dialog = GeodeDialog.DNDConsole(self, filepaths)
        if dialog.run() == Gtk.ResponseType.APPLY:
            data, options = dialog.get_data(), dialog.get_options()

        dialog.destroy()

        # Manage validate files
        if data is None or len(data) == 0:
            return

        GLib.idle_add(
            self.on_prepare_drag_and_drop_installation(data, options).__next__)

    @block_signals
    @use_sensitivity
    def on_show_emulator_editor_dialog(self, widget, *args):
        """ Open console editor dialog

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        selected_row = self.listbox_consoles.get_selected_row()

        if widget == self.toolbar_consoles.get_widget("add_emulator"):
            emulator = Emulator()
            previous_id = None

        elif self.__geode_cache.get("row") is not None:
            emulator = self.__geode_cache.get("row").console.emulator
            previous_id = emulator.id
            # Retrieve the correct emulator instance from api
            emulator = deepcopy(self.api.get_emulator(previous_id))

        dialog = GeodeDialog.Emulator(
            self,
            emulator,
            self.api.emulators,
            self.get_window_size_from_configuration("emulator", 800, 600))

        if dialog.run() == Gtk.ResponseType.APPLY:
            emulator = dialog.save()
        else:
            emulator = None

        self.config.modify("windows", "emulator", "%dx%d" % dialog.get_size())
        self.config.update()

        dialog.destroy()

        if emulator is None:
            return

        if previous_id is None:
            self.logger.info(f"Add '{emulator.id}' to emulators collection")
            self.api.add_emulator(emulator.name, emulator.as_dict().items())

        elif not emulator.id == previous_id:
            self.logger.info(
                f"Replace '{previous_id}' emulator with '{emulator.id}'")
            self.api.replace_emulator(previous_id, emulator)

        else:
            self.logger.info(f"Update '{emulator.id}' emulator")
            self.api.update_emulator(emulator)

        # Write console data
        self.api.write_data(GEM.Emulators)

        # Remove thumbnails from cache
        for size in ("22x22", "48x48", "64x64"):
            cache_path = self.get_icon_from_cache(
                "emulators", size, f"{emulator.id}.png")
            if cache_path.exists():
                self.logger.debug(f"Remove '{cache_path}' from filesystem")
                remove(cache_path)

        # Update console row
        if widget == self.toolbar_consoles.get_widget("add_emulator"):
            self.set_message(
                _("New emulator"),
                _("%s has been correctly added to your configuration.") % (
                    emulator.name),
                Icons.Symbolic.INFORMATION)
            return

        self.__geode_cache.get("row").console.emulator = emulator

        status = False
        if emulator is not None and emulator.configuration:
            status = emulator.configuration.exists()

        self.menu_consoles.set_sensitive(status, widget="edit_file")

        # Reload games list
        same_emulator = False

        if selected_row is not None:
            identifier = selected_row.console.emulator.id
            # Reload games list if selected console has the same
            # emulator to avoid missing references
            same_emulator = identifier == emulator.id

        if selected_row == self.__geode_cache.get("row"):
            self.selection["console"] = self.__geode_cache.get("row").console
            self.on_reload_console_games()

        elif same_emulator:
            self.on_reload_console_games()

    @use_sensitivity
    def on_show_emulator_file_dialog(self, *args):
        """ Edit emulator configuration file
        """

        console = None
        if self.__geode_cache.get("row") is not None:
            console = self.__geode_cache.get("row").console

        if console is None:
            return

        emulator = console.emulator
        if emulator.configuration is None \
           or not emulator.configuration.exists():
            return

        dialog = GeodeDialog.Editor(
            self,
            _("Edit %s configuration") % emulator.name,
            emulator.configuration,
            self.get_window_size_from_configuration("editor", 800, 600),
            Icons.Symbolic.DOCUMENT)
        dialog.run()

        self.config.modify("windows", "editor", "%dx%d" % dialog.get_size())
        self.config.update()

        self.save_editor_options(dialog)

        dialog.destroy()

    @use_sensitivity
    def on_show_game_backup_memory_dialog(self, *args):
        """ Manage game backup memory

        This function can only be used with a GBA game and Mednafen emulator.
        """

        if not self.menu_game.get_sensitive(widget="memory_type"):
            return

        console = self.selection.get("console", None)
        game = self.views_games.get_selected_game()

        if not console or not game:
            return

        content = dict()

        # Check if a type file already exist in mednafen sav folder
        filepath = self.get_mednafen_memory_type_file(game)
        if filepath.exists():

            with filepath.open('r') as pipe:
                for line in pipe.readlines():
                    data = line.split()
                    if len(data) == 2:
                        content[data[0]] = int(data[1])

        dialog = GeodeDialog.Mednafen(self, game.name, content)

        data = None
        if dialog.run() == Gtk.ResponseType.APPLY:
            data = dialog.save()

        dialog.destroy()

        if data is None:
            return

        # Write data into type file
        if len(data) > 0:
            with filepath.open('w') as pipe:
                pipe.write('\n'.join(data))

        # Remove type file when no data are available
        elif filepath.exists():
            filepath.unlink()

    @use_sensitivity
    def on_show_game_duplication_dialog(self, *args):
        """ Duplicate a game

        This function allow the user to duplicate a game and his associate
        data
        """

        console = self.selection.get("console", None)
        if console is None:
            raise SystemError("There is a problem, since this method can only "
                              "be used when a console was selected, but there "
                              "is no console currently selected...")

        game = self.views_games.get_selected_game()

        if game is None:
            return

        dialog = GeodeDialog.Duplicate(self, game)

        data = None
        if dialog.run() == Gtk.ResponseType.APPLY:
            data = dialog.data

        dialog.destroy()

        if data is None:
            return

        # Generate the new destination path for the duplicated game
        dest_path = game.path.parent.joinpath(data.get("filename"))
        self.logger.info(f"Duplicate '{game.id}' to {dest_path}")

        # Retrieve game related files from user selection
        files = [(game.path, dest_path)]

        if data.get("memory"):
            path = self.get_mednafen_memory_type_file(game)
            files.append((path,
                          str(path).replace(game.path.stem, dest_path.stem)))

        if data.get("note"):
            identifier = engine_utils.generate_identifier(dest_path)
            files.append((self.api.get_local("notes", f"{game.id}.txt"),
                          self.api.get_local("notes", f"{identifier}.txt")))

        if data.get("savestates"):
            for path in game.savestates:
                destination = str(path).replace(game.path.stem, dest_path.stem)
                files.append((path, Path(destination)))

        if data.get("screenshots"):
            for path in game.screenshots:
                destination = str(path).replace(game.path.stem, dest_path.stem)
                files.append((path, Path(destination)))

        # Duplicate game files
        for source, destination in files:
            if not source.exists():
                continue

            if not access(destination.parent, W_OK):
                self.logger.error(
                    f"Cannot write in '{destination.parent}' directory")
                continue

            try:
                self.logger.debug(
                    f"Duplicate '{source.name}' to {destination.parent.name}")
                engine_utils.copy(source, destination)

            except Exception:
                self.logger.exception("An error occur during duplication")
                continue

        # Update game from database
        if data.get("database"):
            self.api.update_game(game.copy(dest_path))

        game = console.add_game(dest_path)

        # Update console tooltip
        if console.id in self.consoles_iter:
            self.set_console_row_information(
                self.consoles_iter[console.id], console, only_tooltip=True)

        self.views_games.append_game(console, game)

        self.set_message(
            _("Duplicate a game"),
            _("This game was duplicated successfully"),
            Icons.INFORMATION)

    @use_sensitivity
    def on_show_game_editor_dialog(self, *args):
        """ Edit game file

        This function check if the game file mime type is text/
        """

        game = self.views_games.get_selected_game()
        if game is None:
            return

        if not ui_utils.check_game_is_editable(game):
            return

        current_installation_date = game.get_installation_date()

        dialog = GeodeDialog.Editor(
            self,
            game.name,
            game.path,
            self.get_window_size_from_configuration("game", 800, 600),
            Icons.Symbolic.EDIT)
        dialog.run()

        new_installation_date = game.get_installation_date()

        if new_installation_date > current_installation_date:
            self.views_games.treeview.set_value(
                self.views_games.get_iter_from_key(game.id)[0],
                Columns.List.INSTALLED,
                ui_utils.string_from_date(new_installation_date ))

            label_installed = self.scroll_sidebar.get_widget("installed")
            label_installed.set_label(
                ui_utils.string_from_date(new_installation_date))
            label_installed.set_tooltip_text(
                new_installation_date.strftime(self.datetime_format))

        self.config.modify("windows", "game", "%dx%d" % dialog.get_size())
        self.config.update()

        self.save_editor_options(dialog)

        dialog.destroy()

    @use_sensitivity
    def on_show_game_log_dialog(self, *args):
        """ Show game log

        This function show the gem log content in a non-editable dialog
        """

        game = self.views_games.get_selected_game()
        if game is None:
            return

        path = self.get_game_log_file(game)
        if path is None or not path.exists():
            return

        dialog = GeodeDialog.Editor(
            self,
            game.name,
            path,
            self.get_window_size_from_configuration("log", 800, 600),
            Icons.Symbolic.TERMINAL,
            editable=False)

        dialog.run()

        self.config.modify("windows", "log", "%dx%d" % dialog.get_size())
        self.config.update()

        self.save_editor_options(dialog)

        dialog.destroy()

    @block_signals
    @use_sensitivity
    def on_show_game_maintenance_dialog(self, *args):
        """ Set some maintenance for selected game
        """

        console = self.selection.get("console", None)
        if console is None:
            raise SystemError("There is a problem, since this method can only "
                              "be used when a console was selected, but there "
                              "is no console currently selected...")

        game = self.views_games.get_selected_game()

        # Avoid trying to remove an executed game
        if game is None or game.id in self.threads["playing"]:
            return

        dialog = GeodeDialog.Maintenance(self, game)

        data = None
        if dialog.run() == Gtk.ResponseType.APPLY:
            data = dialog.data

        dialog.destroy()

        if data is None:
            return

        self.logger.info(f"Start '{game.id}' maintenance actions")

        # Retrieve game related files from user selection
        files = []

        need_to_update = False

        if data.get("cache"):
            for size in ("22x22", "96x96"):
                files.append(self.get_icon_from_cache(
                    "games", size, f"{game.id}.png"))

        if data.get("database"):
            game.reset()
            game.emulator = console.emulator

            need_to_update = True

        if data.get("environment"):
            game.environment.clear()

            need_to_update = True

        if data.get("log"):
            files.append(self.api.get_local("logs", f"{game.id}.log"))

        if data.get("note"):
            files.append(self.api.get_local("notes", f"{game.id}.txt"))

        if data.get("savestates"):
            files.extend(game.savestates)

        if data.get("screenshots"):
            files.extend(game.screenshots)

        # Remove specified game files
        for element in files:
            if not element.exists():
                continue

            if not access(element, W_OK):
                self.logger.error(
                    f"Cannot write in '{element.parent}' directory")
                continue

            try:
                self.logger.debug(f"Remove {element}")
                remove(element)

            except Exception:
                self.logger.exception("An error occur during removing")
                continue

        if need_to_update:
            # Update game from database
            self.api.update_game(game)
            # Store modified game
            self.selection["game"] = game
            self.__tooltip_cache["instance"] = None
            # Reset game view information
            self.views_games.reset_game(console, game)

        self.set_game_information()

    def on_show_game_menu_popup(self, widget, event):
        """ Open context menu

        This function open context-menu when user right-click or use context
        key on games views

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        event : Gdk.EventButton or Gdk.EventKey
            Event which triggered this signal

        Returns
        -------
        bool
            Context menu popup status
        """

        treeiter = None

        # Gdk.EventButton - Mouse
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if not event.button == Gdk.BUTTON_SECONDARY:
                return False

            x, y = int(event.x), int(event.y)

            # List view
            if widget == self.views_games.treeview:
                # Avoid to click on treeview header
                if not event.window == widget.get_bin_window():
                    return False

                treeiter = widget.get_path_at_pos(x, y)
                if treeiter is None:
                    return False

                widget.set_cursor(treeiter[0], treeiter[1], False)

            # Grid icons view
            elif widget == self.views_games.iconview:
                treeiter = widget.get_path_at_pos(x, y)
                if treeiter is None:
                    return False

                widget.select_path(treeiter)

            widget.grab_focus()

            self.menu_game.popup_at_pointer(event)
            return True

        # Gdk.EventKey - Keyboard
        elif event.type == Gdk.EventType.KEY_RELEASE:
            if not event.keyval == Gdk.KEY_Menu:
                return False

            model, treeiter = self.get_selected_treeiter_from_container(widget)
            if treeiter is not None:
                self.menu_game.popup_at_pointer(event)
                return True

        return False

    def on_show_game_note_dialog(self, *args):
        """ Edit game notes

        This function allow user to write some notes for a specific game. The
        user can open as many notes he wants but cannot open a note already
        open
        """

        game = self.views_games.get_selected_game()
        if game is None:
            return

        path = self.api.get_local("notes", f"{game.id}.txt")
        if path is not None and str(path) not in self.threads["notes"]:
            dialog = GeodeDialog.Editor(
                self,
                game.name,
                path,
                self.get_window_size_from_configuration("notes", 800, 600),
                Icons.Symbolic.DOCUMENT)

            # Allow to launch games with open notes
            dialog.set_modal(False)

            dialog.window.connect(
                "response",
                self.emit_game_note_response,
                dialog,
                game.name,
                path)

            dialog.show_all()

            # Save dialogs to close it properly when gem terminate and
            # avoid to reopen existing one
            self.threads["notes"][str(path)] = dialog

        elif str(path) in self.threads["notes"]:
            self.threads["notes"][str(path)].grab_focus()

    @use_sensitivity
    def on_show_game_properties_dialog(self, *args):
        """ Manage game default parameters

        This function allow the user to specify default emulator and default
        emulator arguments for the selected game
        """

        console = self.selection.get("console", None)
        game = self.views_games.get_selected_game()

        if game is None or console is None:
            return

        dialog = GeodeDialog.Properties(
            self,
            game,
            self.get_window_size_from_configuration("properties", 800, 600))

        if dialog.run() == Gtk.ResponseType.APPLY:
            self.logger.info(f"Update {game.name} parameters")
            game = dialog.save()

            # Update tags
            self.set_games_filter_completion_from_console(console)

            # ----------------------------------------
            #   Update games views
            # ----------------------------------------

            treeiter, griditer = self.views_games.get_iter_from_key(game.id)

            # Custom properties
            has_custom = game.has_custom_parameters(console)

            self.views_games.treeview.set_value(
                treeiter,
                Columns.List.PARAMETER,
                Icons.Symbolic.PROPERTIES if has_custom else None)

            # Name
            self.views_games.treeview.set_value(
                treeiter, Columns.List.NAME, game.name)
            self.views_games.iconview.set_value(
                griditer, Columns.Grid.NAME, game.name)

            # Tags
            self.toolbar_games.set_sensitive(len(game.tags) > 0, widget="tags")

            # Remove previous cache icons
            for size in (22, 96):
                path = self.get_icon_from_cache(
                    "games", f"{size}x{size}", f"{game.id}.png")
                if path.exists():
                    self.logger.debug(f"Remove {path} file")
                    remove(path)

            # Thumbnail
            self.on_update_game_icon_thumbnails(game)

            # Flags
            for flag in ("favorite", "multiplayer", "finish"):
                flag_column = getattr(Columns.List, flag.upper(), None)
                if flag_column is None:
                    continue

                self.views_games.treeview.set_value(
                    treeiter,
                    flag_column,
                    self.get_ui_icon(flag_column, getattr(game, flag)))

            # Screenshots
            has_screenshots = len(game.screenshots) > 0

            self.views_games.treeview.set_value(
                treeiter,
                Columns.List.SCREENSHOT,
                Icons.Symbolic.CAMERA if has_screenshots else None)

            self.menubar_game.set_sensitive(
                has_screenshots, widget="screenshots")
            self.toolbar_games.set_sensitive(
                has_screenshots, widget="screenshots")

            # Savestates
            self.views_games.treeview.set_value(
                treeiter,
                Columns.List.SAVESTATE,
                Icons.Symbolic.FLOPPY if len(game.savestates) > 0 else None)

            # Objects
            self.views_games.treeview.set_value(
                treeiter, Columns.List.OBJECT, game)
            self.views_games.iconview.set_value(
                griditer, Columns.Grid.OBJECT, game)

            # Update game from database
            self.api.update_game(game)

            self.set_game_information()

        self.config.modify("windows", "properties", "%dx%d" % dialog.get_size())
        self.config.update()

        dialog.destroy()

    @use_sensitivity
    def on_show_game_renaming_dialog(self, *args):
        """ Set a custom name for a specific game

        Parameters
        ----------
        widget : Gtk.CellRendererText
            object which received the signal
        path : str
            path identifying the edited cell
        new_name : str
            new name
        """

        console = self.selection.get("console", None)
        if console is None:
            raise SystemError("There is a problem, since this method can only "
                              "be used when a console was selected, but there "
                              "is no console currently selected...")

        game = self.views_games.get_selected_game()
        if game is None:
            return

        dialog = GeodeDialog.Rename(self, game)

        data = None
        if dialog.run() == Gtk.ResponseType.APPLY:
            data = dialog.data

        dialog.destroy()

        # Check if game name has been changed
        if data is None or data.get("name") == game.name:
            return

        new_name = data.get("name")

        self.logger.info(f"Rename '{game.name}' to '{new_name}'")
        game.name = new_name

        # Update game from database
        self.api.update_game(game)
        # Store modified game
        self.selection["game"] = game
        self.__tooltip_cache["instance"] = None
        # Reset game view information
        self.views_games.reset_game(console, game)

        # Restore focus to current game view
        if self.toolbar_games.get_active("grid"):
            self.views_games.iconview.grab_focus()
        elif self.toolbar_games.get_active("list"):
            self.views_games.treeview.grab_focus()

        self.set_game_information()

    @use_sensitivity
    def on_show_game_removing_dialog(self, *args):
        """ Remove a game

        This function also remove files from user disk as screenshots,
        savestates and game file.
        """

        console = self.selection.get("console", None)
        if console is None:
            raise SystemError("There is a problem, since this method can only "
                              "be used when a console was selected, but there "
                              "is no console currently selected...")

        game = self.views_games.get_selected_game()

        # Avoid trying to remove an executed game
        if game is None or game.id in self.threads["playing"]:
            return

        dialog = GeodeDialog.Delete(self, game)

        data = None
        if dialog.run() == Gtk.ResponseType.YES:
            data = dialog.data

        dialog.destroy()

        if data is None:
            return

        self.logger.info(f"Remove '{game.id}' and related data from filesystem")
        need_to_reload = False

        # Retrieve game related files from user selection
        files = [game.path]

        if data.get("cache"):
            for size in ("22x22", "96x96"):
                files.append(self.get_icon_from_cache(
                    "games", size, f"{game.id}.png"))

        if data.get("desktop"):
            files.append(self.get_game_desktop_file(game))

        if data.get("memory"):
            files.append(self.get_mednafen_memory_type_file(game))

        if data.get("savestates"):
            files.extend(game.savestates)

        if data.get("screenshots"):
            files.extend(game.screenshots)

        # Remove specified game files
        for element in files:
            if not element.exists():
                continue

            if not access(element, W_OK):
                self.logger.error(
                    f"Cannot write in '{element.parent}' directory")
                continue

            try:
                self.logger.debug(f"Remove {element}")
                remove(element)

            except Exception:
                self.logger.exception("An error occur during removing")
                continue

            need_to_reload = True

        # Remove game from database
        if data.get("database"):
            self.api.delete_game(game)
            need_to_reload = True

        # Save identifier for later
        identifier = game.id
        # Remove game from console storage
        console.delete_game(game)

        # Update console tooltip
        if console.id in self.consoles_iter:
            self.set_console_row_information(
                self.consoles_iter[console.id], console, only_tooltip=True)

        if need_to_reload:
            # Remove an old entry in views
            self.views_games.remove_game(identifier)
            # Remove view selections
            self.views_games.unselect_all()
            # And reset current selection
            self.selection["game"] = None

            self.set_game_information()

            self.set_message(
                _("Remove a game"),
                _("This game was removed successfully"),
                Icons.INFORMATION)

    @use_sensitivity
    def on_show_preferences_dialog(self, *args):
        """ Show preferences window
        """

        dialog = GeodeDialog.Preferences(self.api, self)

        if dialog.run() == Gtk.ResponseType.APPLY:
            dialog.save_configuration()

            self.logger.debug("Main interface need to be reload")
            self.load_interface()

        dialog.destroy()

    @use_sensitivity
    def on_show_screenshots_viewer_dialog(self, *args):
        """ Show game screenshots

        This function open game screenshots in a viewer. This viewer can be a
        custom one or the gem native viewer. This choice can be do in gem
        configuration file
        """

        console = self.selection.get("console", None)
        game = self.views_games.get_selected_game()

        if console is None or game is None or not game.screenshots:
            return

        # Get external viewer
        viewer = Path(self.config.get("viewer", "binary")).expanduser()

        screenshots_list = sorted(game.screenshots)

        # Native viewer
        if self.config.getboolean("viewer", "native", fallback=True):
            dialog = GeodeDialog.Viewer(
                self,
                f"{game.name} ({console.name})",
                self.get_window_size_from_configuration("viewer", 1024, 768),
                screenshots_list)
            dialog.run()

            self.config.modify(
                "windows", "viewer", "%dx%d" % dialog.get_size())
            self.config.update()

            dialog.destroy()

        # External viewer
        elif viewer.exists():
            # Retrieve viewer binary
            command = shlex_split(str(viewer))

            # Add arguments if available
            parameters = self.config.item("viewer", "options")
            if len(parameters) > 0:
                command.append(parameters)

            # Add game screenshot files
            command.extend([str(path) for path in screenshots_list])

            # Launch external viewer
            try:
                instance = Gio.AppInfo.create_from_commandline(
                    ' '.join(command), None,
                    Gio.AppInfoCreateFlags.SUPPORTS_URIS)
                instance.launch(None, None)

            except GLib.Error:
                self.logger.exception(f"Cannot generate {viewer} instance")

        # No available viewer
        else:
            self.set_message(_("Cannot open screenshots viewer"),
                             _("Cannot find %s") % f"<b>{viewer.name}</b>",
                             Icons.WARNING)

        # External viewer can remove file, so we need to check again
        if not len(game.screenshots):
            self.views_games.treeview.set_value(
                self.views_games.get_iter_from_key(game.id)[0],
                Columns.List.SCREENSHOT,
                None)

    def on_sort_consoles_list(self, first, second, *args):
        """ Sort consoles to reorganize them

        Parameters
        ----------
        first : gem.gtk.widgets.ListBoxSelectorItem
            First row to compare
        second : gem.gtk.widgets.ListBoxSelectorItem
            Second row to compare
        """

        if not first.console.favorite == second.console.favorite:
            return first.console.favorite < second.console.favorite

        return first.console.name.lower() > second.console.name.lower()

    def on_sort_games_iconview(self, model, row1, row2, column):
        """ Sort games list for specific columns

        Parameters
        ----------
        model : Gtk.TreeModel
            Treeview model which receive signal
        row1 : Gtk.TreeIter
            First treeiter to compare with second one
        row2 : Gtk.TreeIter
            Second treeiter to compare with first one
        column : int
            Sorting column index

        Returns
        -------
        int
            Sorting comparaison result
        """

        data1 = model.get_value(row1, Columns.Grid.OBJECT)
        data2 = model.get_value(row2, Columns.Grid.OBJECT)

        return data1.name.lower() > data2.name.lower()

    def on_sort_games_treeview(self, model, row1, row2, column):
        """ Sort games list for specific columns

        Parameters
        ----------
        model : Gtk.TreeModel
            Treeview model which receive signal
        row1 : Gtk.TreeIter
            First treeiter to compare with second one
        row2 : Gtk.TreeIter
            Second treeiter to compare with first one
        column : int
            Sorting column index

        Returns
        -------
        int
            Sorting comparaison result
        """

        data1 = model.get_value(row1, Columns.List.OBJECT)
        data2 = model.get_value(row2, Columns.List.OBJECT)

        # Column order
        order = Gtk.SortType.ASCENDING
        if column.identifier not in ("last_play", "time_play", "installed"):
            order = self.views_games.treeview.get_widget(
                column.identifier).get_sort_order()

        # Object sorting references
        first, second = None, None

        if column.identifier == "favorite":
            first, second = data1.favorite, data2.favorite

        elif column.identifier == "multiplayer":
            first, second = data1.multiplayer, data2.multiplayer

        elif column.identifier == "finish":
            first, second = data1.finish, data2.finish

        elif column.identifier == "play":
            first, second = data1.played, data2.played

        elif column.identifier == "last_play":
            first, second = data1.last_launch_date, data2.last_launch_date

        elif column.identifier == "play_time":
            first, second = data1.play_time, data2.play_time

        elif column.identifier == "score":
            first, second = data1.score, data2.score

        elif column.identifier == "installed":
            first, second = data1.installed, data2.installed

        # ----------------------------------------
        #   Compare
        # ----------------------------------------

        # Sort by name in the case where this games are never been launched
        if not first and not second:

            if data1.name.lower() < data2.name.lower():
                return -1

            elif data1.name.lower() == data2.name.lower():
                return 0

        # The second has been launched instead of first one
        elif not first:
            return -1

        # The first has been launched instead of second one
        elif not second:
            return 1

        elif first < second:
            return -1

        elif first == second:

            if data1.name.lower() < data2.name.lower():

                if order == Gtk.SortType.ASCENDING:
                    return -1

                elif order == Gtk.SortType.DESCENDING:
                    return 1

            elif data1.name.lower() == data2.name.lower():
                return 0

        return 1

    @block_signals
    def on_switch_games_view(self, widget):
        """ Switch between the available games list view mode

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        games_view = GeodeGEM.Views.Name.GRID
        if widget.identifier == "list":
            games_view = GeodeGEM.Views.Name.LIST

        # Update widgets status based on selected games view
        self.headerbar.set_active(True, widget=games_view.value)
        self.menubar_view.set_active(True, widget=games_view.value)
        self.toolbar_games.get_widget("views").switch_to(games_view.value)

        # Show activated games view when there are games available
        self.views_games.set_view(
            games_view, show=not self.views_games.placeholder.get_visible())

    def on_synchronize_game_selection(self, widget, game):
        """ Synchronize grid and list views selection

        Parameters
        ----------
        widget : Gtk.Widget
            Games view currently selected
        game : gem.engine.game.Game
            Game instance
        """

        if game is None or not self.views_games.has_game(game.id):
            return

        # Select the view to synchronise
        if widget == self.views_games.iconview:
            index, view = 0, self.views_games.treeview
        elif widget == self.views_games.treeview:
            index, view = 1, self.views_games.iconview

        path = view.get_path_from_treeiter(
            self.views_games.get_iter_from_key(game.id)[index])

        if path is not None:
            view.select_path_and_scroll(path)
        else:
            view.unselect_all()

        self.logger.debug(f"Synchronize selection for game '{game.id}'")

    @block_signals
    def on_update_consoles_filters(self, widget, *args):
        """ Change a console option switch

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        if widget.identifier == "hide_empty":
            self.hide_empty_console = not self.hide_empty_console

            self.config.modify(
                "gem", "hide_empty_console", self.hide_empty_console)
            self.config.update()

            self.toolbar_consoles.set_active(
                self.hide_empty_console, widget="hide_empty")

            self.on_reload_consoles()

        elif self.__geode_cache.get("row") is not None:
            console = self.__geode_cache.get("row").console

            if widget.identifier == "recursive":
                console.recursive = not console.recursive
                self.api.write_object(console)

            elif widget.identifier == "favorite":
                console.favorite = not console.favorite
                self.api.write_object(console)

                self.on_reload_consoles()

    @block_signals
    def on_update_games_filters(self, widget=None, status=None):
        """ Reload packages filter when user change filters from menu

        Parameters
        ----------
        widget : Gtk.Widget, optional
            Object which receive signal
        status : bool or None, optional
            New status for current widget (Default: None)

        Notes
        -----
        Check widget utility in this function
        """

        # Update status for Switch widgets
        if type(status) is bool and isinstance(widget, Gtk.Switch):
            widget.set_active(status)

        # Check if some filters has been disabled
        no_filters = all([self.popover_filters.get_active(key)
                          for key in self.filters])

        # Add a style to menu button when a filter was enabled
        self.toolbar_games.set_style(
            None if no_filters else Gtk.STYLE_CLASS_SUGGESTED_ACTION,
            widget="filters")

        # Refilter games views to update visible rows
        self.views_games.refilter()

        self.check_game_selection()

        # Update games length in headerbar subtitle
        self.set_statusbar_content()

    def on_update_game_icon_thumbnails(self, game):
        """ Update game icon thumbnails on tree and grid views

        Parameters
        ----------
        game : geode_gem.engine.game.Game
            Game object
        """

        large = self.__console_icon
        thumbnail = self.__console_thumbnail

        if game.cover is not None:
            large = self.get_pixbuf_from_cache(
                "games", 96, game.id, game.cover)
            thumbnail = self.get_pixbuf_from_cache(
                "games", 22, game.id, game.cover)

        treeiter, griditer = self.views_games.get_iter_from_key(game.id)

        self.views_games.iconview.set_value(
            griditer, Columns.Grid.THUMBNAIL, large)
        self.views_games.treeview.set_value(
            treeiter, Columns.List.THUMBNAIL, thumbnail)

        self.set_sidebar_image(game)

        # Reset tooltip pixbuf
        self.__tooltip_cache["pixbuf"] = None

    @block_signals
    def on_update_game_tag_filter(self, widget):
        """ Refilter games list with a new tag

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        entry_widget = self.toolbar_games.get_widget("entry")

        text = str()
        if not entry_widget.get_text() == widget.get_label():
            text = widget.get_label()

        entry_widget.set_text(text)

        # Refilter games views to update visible rows
        self.views_games.refilter()

    def save_editor_options(self, dialog: Gtk.Dialog):
        """ Save the selected editor options in the configuration file

        Parameters
        ----------
        dialog : gi.repository.Gtk.Dialog
            Editor dialog instance
        """

        for key, value in dialog.options.items():

            if isinstance(value, bool):
                value = "yes" if value else "no"

            self.config.set("editor", key, value)

        self.config.update()

    def set_console_row_information(self, row, console, only_tooltip=False):
        """ Set information from console for a specific listbox row

        Parameters
        ----------
        row : Gtk.ListBoxRow
            Row instance from consoles listbox
        console : gem.engine.console.Console
            Console instance
        only_tooltip : bool
            Avoid to reload all console information (Default: False)
        """

        if not only_tooltip:
            setattr(row, "console", console)

            icon = self.get_pixbuf_from_cache(
                "consoles", 24, console.id, console.icon)
            if icon is None:
                icon = self.icons_blank.get(24)

            row.grid.get_widget("icon").set_from_pixbuf(icon)

            row.grid.get_widget("title").set_text(console.name)

        text = _("No game")
        if len(console):
            text = ngettext(
                _("1 game"), _("%d games") % len(console), len(console))

        row.set_tooltip_text(text)

    def set_infobar_content(self, message, icon=Gtk.MessageType.INFO):
        """ Fill infobar informations

        Parameters
        ----------
        """

        self.infobar.set_message(icon, message)

        self.set_infobar_visibility(len(message) > 0)

    def set_infobar_visibility(self, status):
        """ Update infobar status

        Parameters
        ----------
        status : bool
            New status value
        """

        self.infobar.set_visible(status)

    @block_signals
    def set_interface_theme(self, widget, status=False, *args):
        """ Update dark theme status

        This function alternate between dark and light theme when user use
        dark theme entry in main menu

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        status : bool, optional
            New switch status (Default: False)
        """

        dark_theme_status = \
            not self.config.getboolean("gem", "dark_theme", fallback=False)

        ui_utils.on_prefer_dark_theme(dark_theme_status)

        self.config.modify("gem", "dark_theme", dark_theme_status)
        self.config.update()

        self.menubar_view.set_active(dark_theme_status, widget="dark_theme")

    @block_signals
    def set_game_flag(self, widget, flag_name):
        """ Update a specific flag for the selected game

        Parameters
        ----------
        widget : Gtk.Widget
            object which received the signal
        flag_name : str
            flag label name used to retrieve current status from game object
        """

        game, status = self.views_games.get_selected_game(), False

        if game is not None:
            treeiter, griditer = self.views_games.get_iter_from_key(game.id)

            # Reverse current game status
            status = not getattr(game, flag_name, False)

            # Update treeview icon
            flag_column = getattr(Columns.List, flag_name.upper(), None)
            if flag_column is not None:
                self.views_games.treeview.set_value(
                    treeiter,
                    flag_column,
                    self.get_ui_icon(flag_column, status))

            # Update game object in both games views storages
            self.views_games.treeview.set_value(
                treeiter, Columns.List.OBJECT, game)
            self.views_games.iconview.set_value(
                griditer, Columns.Grid.OBJECT, game)

            self.logger.debug(
                f"Set {flag_name} status for '{game.id}' to {status}")

            # Update game from database
            setattr(game, flag_name, status)
            self.api.update_game(game)

            self.check_game_selection()

        self.menubar_game.set_active(status, widget=flag_name)
        self.menu_game.set_active(status, widget=flag_name)

        self.on_update_games_filters()

    @block_signals
    def set_game_fullscreen(self, widget, *args):
        """ Update fullscreen button

        This function alternate fullscreen status between active and inactive
        state when user use fullscreen button in toolbar

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        # Switch fullscreen status
        self.__geode_cache["fullscreen"] = \
            not self.__geode_cache.get("fullscreen")

        fullscreen_button = self.toolbar_games.get_widget("fullscreen")
        fullscreen_image = self.toolbar_games.get_widget("fullscreen_image")

        if not self.__geode_cache.get("fullscreen"):
            self.logger.debug("Switch game launch to windowed mode")

            fullscreen_image.set_from_icon_name(Icons.Symbolic.RESTORE,
                                                Gtk.IconSize.SMALL_TOOLBAR)
            fullscreen_button.set_style()

        else:
            self.logger.debug("Switch game launch to fullscreen mode")

            fullscreen_image.set_from_icon_name(Icons.Symbolic.FULLSCREEN,
                                                Gtk.IconSize.SMALL_TOOLBAR)
            fullscreen_button.set_style(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

        fullscreen_button.set_active(self.__geode_cache.get("fullscreen"))
        self.menubar_game.set_active(
            self.__geode_cache.get("fullscreen"), widget="fullscreen")

    @block_signals
    def set_game_information(self):
        """ Update headerbar title and subtitle
        """

        self.__sidebar_cache["image"] = None

        console = self.selection.get("console", None)
        game = self.views_games.get_selected_game()

        # Update headerbar and statusbar informations
        self.set_statusbar_content()

        # Remove tags list
        self.menu_tags.clear()

        # Hide sidebar widgets
        self.scroll_sidebar.get_widget("score").set_visible(False)
        self.scroll_sidebar.get_widget("information").set_visible(False)
        self.scroll_sidebar.get_widget("frame").set_visible(False)

        # Reset sidebar informations
        self.scroll_sidebar.get_widget("title").set_label(str())
        self.scroll_sidebar.get_widget("image").set_from_pixbuf(None)

        # ----------------------------------------
        #   Update informations
        # ----------------------------------------

        if game is None:
            self.set_sensitive_interface(False)

            for widget_key in self.statusbar.pixbuf_widgets:
                self.statusbar.set_widget_value(
                    widget_key, image=None, set_tooltip_text=str())

        else:
            self.logger.debug(
                f"Update informations on main interface for '{game.id}'")

            self.set_sensitive_interface(True)
            self.set_game_playing_status(game)

            # Game editable file
            if not ui_utils.check_game_is_editable(game):
                self.menu_game.set_sensitive(False, widget="game_file")
                self.menubar_edit.set_sensitive(False, widget="game_file")

            # Check extension and emulator for GBA game on mednafen
            if not self.check_gba_game_use_mednafen(game):
                self.menu_game.set_sensitive(False, widget="memory_type")
                self.menubar_edit.set_sensitive(False, widget="memory_type")

            # Check game log file
            if self.get_game_log_file(game) is not None:
                self.menu_game.set_sensitive(True, widget="game_log")
                self.menubar_game.set_sensitive(True, widget="game_log")
                self.toolbar_games.set_sensitive(True, widget="game_log")

            # Game flags
            for name in ("favorite", "multiplayer", "finish"):
                self.menu_game.set_active(getattr(game, name), widget=name)
                self.menubar_game.set_active(getattr(game, name), widget=name)

            # Game tags
            self.toolbar_games.get_widget("tags").set_sensitive(game.tags)

            if len(game.tags) > 0:
                for tag in sorted(game.tags):
                    item = GeodeGtk.MenuItem(tag, identifier=tag)
                    item.connect("activate", self.on_update_game_tag_filter)

                    self.menu_tags.append(item)

                self.menu_tags.show_all()

            # Sidebar
            self.scroll_sidebar.get_widget("score").set_visible(True)
            self.scroll_sidebar.get_widget("information").set_visible(True)

            # Game log and screenshots
            for name in ("menu_game", "menubar_game", "toolbar_games"):
                getattr(self, name).set_sensitive(
                    self.get_game_log_file(game), widget="game_log")
                getattr(self, name).set_sensitive(
                    game.screenshots, widget="screenshots")

            # Statusbar icons
            for name in ("properties", "savestates", "screenshots"):
                self.set_statusbar_icon_for_widget(name, console, game)

            # Sidebar informations
            self.set_sidebar_content(console, game)

    def set_game_playing_status(self, game):
        """ Update game launch button

        Parameters
        ----------
        game : geode_gem.engine.game.Game
            Game instance
        """

        if game is not None:
            launch_button = self.toolbar_games.get_widget("launch")

            is_played = game.id in self.threads["playing"]
            if not is_played:
                label, tooltip_text = _("Play"), _("Launch selected game")
                launch_button.set_style(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
            else:
                label, tooltip_text = _("Stop"), _("Stop selected game")
                launch_button.set_style(Gtk.STYLE_CLASS_DESTRUCTIVE_ACTION)

            for name in ("menu_game", "menubar_game", "toolbar_games"):
                widget = getattr(self, name).get_widget("launch")
                widget.set_label(label)
                widget.set_tooltip_text(tooltip_text)
                widget.set_sensitive(True)

                getattr(self, name).set_sensitive(True, widget="game_log")

            if game.path.exists() and access(game.path, W_OK):
                self.menu_game.set_sensitive(not is_played, widget="remove")
                self.menubar_edit.set_sensitive(not is_played, widget="remove")

    def set_game_score(self, widget, score=None):
        """ Manage selected game score

        Parameters
        ----------
        widget : Gtk.MenuItem
            object which received the signal
        """

        game = self.views_games.get_selected_game()
        if game is None:
            return

        modification = False
        if widget.identifier == "increase" and game.score < 5:
            game.score += 1
            modification = True

        elif widget.identifier == "decrease" and game.score > 0:
            game.score -= 1
            modification = True

        elif score is not None:
            game.score = score
            modification = True

        if modification:
            treeiter, griditer = self.views_games.get_iter_from_key(game.id)

            self.views_games.treeview.set_value(
                treeiter, Columns.List.SCORE, game.score)
            self.views_games.treeview.set_value(
                treeiter, Columns.List.OBJECT, game)
            self.views_games.iconview.set_value(
                griditer, Columns.Grid.OBJECT, game)

            self.api.update_game(game)

            self.set_game_information()

    @block_signals
    def set_games_column_visibility(self, widget, key):
        """ Manage games treeview columns visibility

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        key : str
            Column key
        """

        if not self.config.has_option("columns", key):
            return

        self.config.modify("columns", key, widget.get_active())
        if not self.views_games.treeview.has_widget(key):
            return

        column = self.views_games.treeview.get_widget(key)
        column.set_visible(widget.get_active())

        self.views_games.treeview.columns_autosize()

        self.logger.debug(
            f"Switch visibility for '{key}' column to {column.get_visible()}")

    def set_games_order_from_column(self, games, column, reverse=False):
        """ Sort the games list based on the current sorted treeview column

        Parameters
        ----------
        games : list
            Game instances list
        column : int
            Column index from treeview
        reverse : bool, optional
            Sorted reverse status
        """

        if column == Columns.List.FAVORITE:
            games.sort(key=lambda game: game.favorite, reverse=reverse)

        elif column == Columns.List.MULTIPLAYER:
            games.sort(key=lambda game: game.multiplayer, reverse=reverse)

        elif column == Columns.List.FINISH:
            games.sort(key=lambda game: game.finish, reverse=reverse)

        elif column == Columns.List.PLAYED:
            games.sort(key=lambda game: game.played, reverse=reverse)

        elif column == Columns.List.LAST_PLAY:
            games.sort(key=lambda game: game.last_launch_date, reverse=reverse)

        elif column == Columns.List.TIME_PLAY:
            games.sort(key=lambda game: game.play_time, reverse=reverse)

        elif column == Columns.List.SCORE:
            games.sort(key=lambda game: game.score, reverse=reverse)

        elif column == Columns.List.INSTALLED:
            games.sort(key=lambda game: game.installed, reverse=reverse)

        else:
            games.sort(key=lambda game: game.name.lower(), reverse=reverse)

    def set_games_filter_completion_from_console(self, console):
        """ Add games tags from a specific console into entry completion model

        Parameters
        ----------
        console : gem.engine.console.Console
            Console instance
        """

        self.__toolbar_cache["tags"] = \
            set([tag for game in console.get_games() for tag in game.tags])

        self.toolbar_games.get_widget("entry").set_completion_data(
            "completion", *sorted(self.__toolbar_cache.get("tags")))

    def set_message(self, title, message, icon=Icons.ERROR, popup=True):
        """ Open a message dialog

        This function open a dialog to inform user and write message to logger
        output.

        Parameters
        ----------
        title : str
            Dialog title
        message : str
            Dialog message
        icon : str, optional
            Dialog icon, set also the logging mode (Default: Icons.ERROR)
        popup : bool, optional
            Show a popup dialog with specified message (Default: True)
        """

        if icon.startswith(Icons.ERROR):
            self.logger.error(message)
        elif icon.startswith(Icons.WARNING):
            self.logger.warning(message)
        else:
            self.logger.info(message)

        if popup:
            dialog = GeodeDialog.Message(self, title, message, icon)
            dialog.run()
            dialog.destroy()

    def set_sensitive_interface(self, status=False):
        """ Update sensitive status for main widgets

        Parameters
        ----------
        status : bool, optional
            Sensitive status (Default: False)
        """

        self.logger.debug(f"Reset widgets sensitivity status to {status}")

        for widget in self.__widgets_storage:
            widget.set_sensitive(status)

        self.set_game_playing_status(self.views_games.get_selected_game())

    def set_sidebar_content(self, console, game):
        """ Fill sidebar informations

        Parameters
        ----------
        console : geode_gem.engine.console.Console
            Console instance
        game : geode_gem.engine.game.Game
            Game instance
        """

        label_title = self.scroll_sidebar.get_widget("title")
        label_title.set_label(
            f"<span weight='bold' size='large'>"
            f"{ui_utils.replace_for_markup(game.name)}</span>")
        if self.use_ellipsize_title:
            label_title.set_tooltip_text(game.name)
        else:
            label_title.set_tooltip_text(str())

        self.set_sidebar_image(game)

        widgets = [
            {
                "widget": "played",
                "condition": game.played > 0,
                "markup": str(game.played),
                "default": '0',
            },
            {
                "widget": "play_time",
                "condition": not game.play_time == timedelta(),
                "markup": ui_utils.string_from_time(game.play_time),
                "tooltip": engine_utils.parse_timedelta(game.play_time)
            },
            {
                "widget": "last_play",
                "condition": not game.last_launch_date.strftime(
                    "%d%m%y") == "010101",
                "markup": ui_utils.string_from_date(game.last_launch_date),
                "tooltip": game.last_launch_date.strftime(self.date_format)
            },
            {
                "widget": "last_time",
                "condition": not game.last_launch_time == timedelta(),
                "markup": ui_utils.string_from_time(game.last_launch_time),
                "tooltip": engine_utils.parse_timedelta(game.last_launch_time)
            },
            {
                "widget": "installed",
                "condition": game.installed is not None,
                "markup": ui_utils.string_from_date(game.installed),
                "tooltip": game.installed.strftime(self.datetime_format)
            },
            {
                "widget": "score",
                "markup": str(game.score)
            },
            {
                "widget": "emulator",
                "condition": game.emulator is not None,
                "markup": getattr(game.emulator, "name", None)
            }
        ]

        for data in widgets:

            # Default label value widget
            if "condition" in data:
                widget = self.scroll_sidebar.get_widget(data["widget"])

                if data["condition"]:
                    widget.set_style(None)

                    if data["markup"] is not None:
                        widget.set_label(data["markup"])

                    # Set tooltip for current widget
                    if "tooltip" in data:
                        widget.set_tooltip_text(data["tooltip"])

                else:
                    widget.set_label(data.get("default", _("n/a")))
                    widget.set_style(Gtk.STYLE_CLASS_DIM_LABEL)
                    widget.set_tooltip_text(str())

            # Score case
            elif data["widget"] == "score":
                # Append star icons to sidebar
                for index in range(1, 6):
                    child = self.scroll_sidebar.get_widget(f"score_{index}")

                    is_starred = game.score >= index

                    child.set_from_icon_name(
                        self.get_ui_icon(
                            Columns.List.SCORE, is_starred),
                        Gtk.IconSize.LARGE_TOOLBAR)

                    child.set_sensitive(is_starred)

                # Show game score as tooltip
                self.scroll_sidebar.get_widget("score").set_tooltip_text(
                    "%d/5" % game.score)

    def set_sidebar_image(self, game):
        """ Define the game image shown in sidebar

        Parameters
        ----------
        game : geode_gem.engine.game.Game
            Game instance
        """

        frame_sidebar_screenshot = self.scroll_sidebar.get_widget("frame")

        if len(game.screenshots) > 0:
            self.__sidebar_cache["image"] = self.get_screenshot_from_game(game)
            width, height = 300, 200

            if self.__sidebar_cache.get("orientation") == \
               Gtk.Orientation.HORIZONTAL:
                height = 250

            frame_sidebar_screenshot.set_shadow_type(Gtk.ShadowType.IN)

        elif game.cover is not None:
            width, height = 128, 128

            image = game.cover
            if not image.exists():
                image = ui_utils.get_filename_from_icon_theme(
                    self.icons_theme, str(image), width)

            self.__sidebar_cache["image"] = image

            frame_sidebar_screenshot.set_shadow_type(Gtk.ShadowType.NONE)

        else:
            self.__sidebar_cache["image"] = None
            return

        try:
            path = self.__sidebar_cache.get("image")
            if ui_utils.magic_from_file(path, mime=True).startswith("image/"):
                self.scroll_sidebar.get_widget("image").set_from_pixbuf(
                    GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        str(path), width, height, True))

                frame_sidebar_screenshot.set_visible(True)

        except GLib.Error:
            self.__sidebar_cache["image"] = None
            frame_sidebar_screenshot.set_visible(False)

    @block_signals
    def set_sidebar_position(self, widget=None, init_interface=False):
        """ Move sidebar based on user configuration value

        Parameters
        ----------
        widget : Gtk.Widget, optional
            Object which receive signal
        init_interface : bool, optional
            Interface first initialization (Default: False)
        """

        self.__sidebar_cache["image"] = None

        # Retrieve current position and update configuration file
        if widget is not None:
            self.sidebar_orientation = "vertical"
            if widget in (self.headerbar.get_widget("right"),
                          self.menubar_view.get_widget("right")):
                self.sidebar_orientation = "horizontal"

            self.config.modify(
                "gem", "sidebar_orientation", self.sidebar_orientation)
            self.config.update()

        grid = self.scroll_sidebar.get_widget("grid")
        grid_content = self.scroll_sidebar.get_widget("content")
        grid_information = self.scroll_sidebar.get_widget("information")
        label_title = self.scroll_sidebar.get_widget("title")

        # Right-side sidebar
        if self.sidebar_orientation == "horizontal" \
           and (not self.__sidebar_cache.get("orientation") ==
                Gtk.Orientation.HORIZONTAL):

            label_title.set_justify(Gtk.Justification.CENTER)
            label_title.set_halign(Gtk.Align.CENTER)
            label_title.set_xalign(0.5)

            # Change game screenshot and score placement
            grid.remove(grid_content)
            grid.attach(grid_content, 0, 1, 1, 1)

            grid_content.set_orientation(Gtk.Orientation.VERTICAL)
            grid_content.set_margin_bottom(12)

            grid_information.set_halign(Gtk.Align.FILL)
            grid_information.set_column_homogeneous(True)
            grid_information.set_orientation(Gtk.Orientation.VERTICAL)

            if not init_interface:
                self.vpaned_games.remove(self.scroll_sidebar)

            self.hpaned_games.pack2(self.scroll_sidebar, False, True)

            self.scroll_sidebar.set_min_content_width(350)
            self.scroll_sidebar.set_min_content_height(-1)

            self.__sidebar_cache["orientation"] = Gtk.Orientation.HORIZONTAL

        # Bottom-side sidebar
        elif (self.sidebar_orientation == "vertical"
              and not (self.__sidebar_cache.get("orientation") ==
                       Gtk.Orientation.VERTICAL)):

            label_title.set_justify(Gtk.Justification.LEFT)
            label_title.set_halign(Gtk.Align.START)
            label_title.set_xalign(0.0)

            # Change game screenshot and score placement
            grid.remove(grid_content)
            grid.attach(grid_content, 1, 0, 1, 3)

            grid_content.set_margin_bottom(0)

            grid_information.set_halign(Gtk.Align.START)
            grid_information.set_column_homogeneous(False)
            grid_information.set_orientation(Gtk.Orientation.HORIZONTAL)

            if not init_interface:
                self.hpaned_games.remove(self.scroll_sidebar)

            self.vpaned_games.pack2(self.scroll_sidebar, False, True)

            self.scroll_sidebar.set_min_content_width(-1)
            self.scroll_sidebar.set_min_content_height(260)

            self.__sidebar_cache["orientation"] = Gtk.Orientation.VERTICAL

        # Update menu radio widgets
        position = "right"
        if self.__sidebar_cache.get("orientation") == Gtk.Orientation.VERTICAL:
            position = "bottom"

        self.headerbar.set_active(True, widget=position)
        self.menubar_view.set_active(True, widget=position)

        self.logger.debug(f"Mode sidebar to {position} side")

        if widget is not None:
            self.set_game_information()

    @block_signals
    def set_sidebar_visibility(self, status, register_modification=True):
        """ Update sidebar status

        Parameters
        ----------
        status : bool or Gtk.Widget
            New status value, emited widget otherwise
        register_modification : bool, optional
            Register sidebar visibility changes into main configuration file
        """

        if not isinstance(status, bool):
            status = status.get_active()

        if register_modification:
            self.show_sidebar = status

            self.config.modify("gem", "show_sidebar", self.show_sidebar)
            self.config.update()

            self.menubar_view.set_active(status, widget="show_sidebar")

        self.scroll_sidebar.set_visible(
            status and not self.views_games.placeholder.get_visible())

    def set_statusbar_content(self):
        """ Update headerbar and statusbar informations from games list
        """

        texts = list()

        console = self.selection.get("console", None)
        game = self.views_games.get_selected_game()

        # Console
        self.statusbar.set_visible(console is not None, widget="console")
        if self.statusbar.get_visible(widget="console"):
            text = self.set_statusbar_text_for_widget("console", console)
            texts.append(text)

        # Emulator
        self.statusbar.set_visible(
            console is not None and console.emulator is not None,
            widget="emulator")
        if self.statusbar.get_visible(widget="emulator"):
            self.set_statusbar_text_for_widget("emulator", console, game)

        # Game
        self.statusbar.set_visible(
            console is not None and game is not None, widget="game")
        if self.statusbar.get_visible(widget="game"):
            text = self.set_statusbar_text_for_widget("game", console, game)
            texts.append(text)

        # Headerbar
        if not self.use_classic_theme:
            self.headerbar.set_subtitle(" - ".join(texts))

    def set_statusbar_icon_for_widget(self, widget_key, console, game):
        """ Define the statusbar icon for a specific widget

        Parameters
        ----------
        widget_key : str
            Statusbar internal widget key
        console : geode_gem.engine.console.Console
            Console instance
        game : geode_gem.engine.game.Game
            Game instance
        """

        if widget_key == "screenshots":
            image = self.get_ui_icon(Columns.List.SCREENSHOT, game.screenshots)

            tooltip = _("No screenshot")
            if len(game.screenshots) > 0:
                tooltip = ngettext(_("1 screenshot"),
                                   _("%d screenshots") % len(game.screenshots),
                                   len(game.screenshots))

        elif widget_key == "savestates":
            image = self.get_ui_icon(Columns.List.SAVESTATE, game.savestates)

            tooltip = _("No savestate")
            if len(game.savestates) > 0:
                tooltip = ngettext(_("1 savestate"),
                                   _("%d savestates") % len(game.savestates),
                                   len(game.savestates))

        elif widget_key == "properties":
            use_parameters = game.has_custom_parameters(console)

            image = self.get_ui_icon(Columns.List.PARAMETER, use_parameters)

            tooltip = str()
            if game.default is not None:
                tooltip = _("Use alternative arguments")
            elif game.emulator == console.emulator:
                tooltip = _("Use alternative emulator")

        if self.statusbar.has_widget(widget_key):
            self.statusbar.set_widget_value(
                widget_key,
                image=(image, Gtk.IconSize.MENU),
                tooltip=tooltip)

    def set_statusbar_text_for_widget(self, widget_key, console, game=None):
        """ Define the statusbar text for a specific widget

        Parameters
        ----------
        widget_key : str
            Statusbar internal widget key
        console : geode_gem.engine.console.Console
            Console instance
        game : geode_gem.engine.game.Game, optional
            Game instance

        Returns
        -------
        str
            Dedicated text for specified widget
        """

        text = str()

        # Console
        if widget_key == "console":

            if self.views_games.treeview.is_filterable:
                games_length = len(self.views_games.treeview.filtered_model)
            else:
                games_length = len(self.views_games.treeview.list_model)

            text = _("N/A")
            if games_length > 0:
                text = ngettext(
                    _("1 game available"),
                    _("%d games available") % games_length,
                    games_length)

            text = ui_utils.replace_for_markup(text)

            self.statusbar.set_widget_value(
                "console", text=f"<b>{_('Console')}</b>: {text}")

        # Emulator
        elif widget_key == "emulator" and console.emulator is not None:
            emulator_name = ui_utils.replace_for_markup(console.emulator.name)

            if game is not None and game.emulator is not None \
               and console.emulator is not None \
               and not game.emulator.id == console.emulator.id:
                text = (f"<s>{emulator_name}</s> "
                        f"{ui_utils.replace_for_markup(game.emulator.name)}")
            else:
                text = emulator_name

            self.statusbar.set_widget_value(
                "emulator", text=f"<b>{_('Emulator')}</b>: {text}")

        # Game
        elif widget_key == "game" and game is not None:
            text = ui_utils.replace_for_markup(game.name)

            self.statusbar.set_widget_value("game", text=text)

        return text

    @block_signals
    def set_statusbar_visibility(self, status, register_modification=True):
        """ Update statusbar status

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        status : bool, optional
            New switch status (Default: False)
        """

        if not isinstance(status, bool):
            status = status.get_active()

        if register_modification:
            self.show_statusbar = status

            self.config.modify("gem", "show_statusbar", self.show_statusbar)
            self.config.update()

            self.menubar_view.set_active(
                self.show_statusbar, widget="show_statusbar")

        self.statusbar.set_visible(self.show_statusbar)
