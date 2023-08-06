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

# Filesystem
from pathlib import Path

# Geode-GEM
from geode_gem.ui.data import Icons
from geode_gem.ui.dialog.question import QuestionDialog
from geode_gem.ui.widgets.window import CommonWindow
from geode_gem.widgets import GeodeGtk

# GObject
from gi.repository import Gdk, GLib, Gtk

# Translation
from gettext import gettext as _

# Typing
from typing import Union


class EditorDialog(CommonWindow):
    """ Geode-GEM editor dialog class

    Attributes
    ----------
    config : geode_gem.engine.lib.configuration.Configuration
        Main application configuration manager instance
    logger : logging.Logger
        Main application logging manager instance
    path : pathlib.Path
        Current opened file path object instance

    See Also
    --------
    geode_gem.ui.widgets.window.CommonWindow
    """

    def __init__(self, parent: Gtk.Window, title: str, file_path: Path,
                 size: [int, int], icon: Union[str, Icons],
                 editable: bool = True):
        """ Constructor

        Parameters
        ----------
        parent : gi.repository.Gtk.Window
            Parent object
        title : str
            Dialog title
        file_path : str
            File path to edit
        size : (int, int)
            Dialog size as (width, height) tuple
        icon : str or geode_gem.ui.data.Icons
            Default icon name as string
        editable : bool, default: True
            If True, allow to modify and save text buffer to file_path
        """

        CommonWindow.__init__(self,
                              parent,
                              title,
                              icon,
                              parent.use_classic_theme)

        # Application objects instances
        self.config = parent.config
        self.logger = parent.logger
        self.path = file_path

        # Dialog window size
        self.__size = size

        # Buffer variables
        self.__buffer_thread = int()
        self.__editable = editable

        # Colorscheme variables
        self.__colorscheme_was_loaded = False

        # User editor config
        self.__editor_config = {
            "auto_indent": self.config.getboolean(
                "editor", "auto_indent", fallback=False),
            "colorscheme": self.config.get(
                "editor", "colorscheme", fallback="none"),
            "font": self.config.get(
                "editor", "font", fallback="Sans 12"),
            "highlight_current_line": self.config.getboolean(
                "editor", "highlight_current_line", fallback=True),
            "indent_on_tab": self.config.getboolean(
                "editor", "indent_on_tab", fallback=True),
            "line_numbers": self.config.getboolean(
                "editor", "lines", fallback=True),
            "right_margin": self.config.getboolean(
                "editor", "right_margin", fallback=False),
            "right_margin_position": self.config.getint(
                "editor", "right_margin_position", fallback=80),
            "space_instead_of_tab": self.config.getboolean(
                "editor", "space_instead_of_tab", fallback=True),
            "tab_width": self.config.getint(
                "editor", "tab", fallback=4),
            "wrap_mode": self.config.getboolean(
                "editor", "wrap_mode", fallback=False),
        }

        # Initialize interface
        self.__init_widgets()
        self.__init_packing()
        self.__init_signals()
        self.__init_interface()

    def __init_widgets(self):
        """ Initialize interface widgets
        """

        self.set_size(*self.__size)
        self.set_spacing(6)
        self.set_resizable(True)

        self.grid.set_border_width(6)

        # ------------------------------------
        #   Widgets
        # ------------------------------------

        self.file_filter = Gtk.FileFilter.new()
        self.file_filter.add_mime_type("text/*")

        self.popover = GeodeGtk.Popover(
            set_modal=True,
        )

        self.toolbar = GeodeGtk.Box(
            GeodeGtk.Button(
                _("Save file"),
                icon_name=Icons.Symbolic.SAVE,
                identifier="save",
            ),
            GeodeGtk.Button(
                _("Save a copy of this file as"),
                icon_name=Icons.Symbolic.SAVE_AS,
                identifier="save_as",
            ),
            GeodeGtk.Button(
                _("Reload file"),
                icon_name=Icons.Symbolic.REFRESH,
                identifier="refresh",
            ),
            None,
            GeodeGtk.MenuButton(
                _("Open contextual menu"),
                GeodeGtk.MenuItem(_("Set _font..."), identifier="font"),
                None,
                GeodeGtk.CheckMenuItem(
                    _("Automatic line _wrapping"),
                    identifier="wrap_mode",
                    set_active=self.__editor_config.get("wrap_mode"),
                ),
                GeodeGtk.CheckMenuItem(
                    _("_Highlight current line"),
                    identifier="highlight_current_line",
                    set_active=self.__editor_config.get(
                        "highlight_current_line"),
                ),
                None,
                GeodeGtk.CheckMenuItem(
                    _("Automatic _indentation"),
                    identifier="auto_indent",
                    set_active=self.__editor_config.get("auto_indent"),
                ),
                GeodeGtk.CheckMenuItem(
                    _("_Indent line on tab"),
                    identifier="indent_on_tab",
                    set_active=self.__editor_config.get("indent_on_tab"),
                ),
                GeodeGtk.CheckMenuItem(
                    _("Use _space instead of tab"),
                    identifier="space_instead_of_tab",
                    set_active=self.__editor_config.get("space_instead_of_tab"),
                ),
                None,
                GeodeGtk.CheckMenuItem(
                    _("Show line _number"),
                    identifier="line_numbers",
                    set_active=self.__editor_config.get("line_numbers"),
                ),
                GeodeGtk.CheckMenuItem(
                    _("Show _right line"),
                    identifier="right_margin",
                    set_active=self.__editor_config.get("right_margin"),
                ),
                None,
                GeodeGtk.MenuItem(
                    _("_Colorschemes"),
                    GeodeGtk.RadioMenuItem(
                        _("None"), identifier="none", set_active=True),
                    None,
                    identifier="colorschemes",
                ),
                icon_name=Icons.Symbolic.MENU,
                set_use_popover=True,
            ),
            GeodeGtk.ToggleButton(
                _("Search a string pattern in file"),
                icon_name=Icons.Symbolic.FIND,
                identifier="search",
                set_active=False,
            ),
            set_spacing=6,
        )

        self.search_entry = GeodeGtk.SearchEntry(
            set_placeholder_text=_("Search...")
        )

        self.searchbar = GeodeGtk.SearchBar(
            GeodeGtk.Box(
                self.search_entry,
                GeodeGtk.Button(
                    _("Previous"),
                    icon_name=Icons.Symbolic.UP,
                    identifier="previous",
                ),
                GeodeGtk.Button(
                    _("Next"),
                    icon_name=Icons.Symbolic.DOWN,
                    identifier="next",
                ),
                merge=True,
                set_orientation=Gtk.Orientation.HORIZONTAL,
            ),
            set_show_close_button=False,
        )
        self.searchbar.connect_entry(self.search_entry)

        self.text_editor = GeodeGtk.SourceView(
            identifier="textview",
            is_expandable=True,
            is_fillable=True,
            set_editable=self.__editable,
        )

        self.frame = GeodeGtk.Frame(
            GeodeGtk.Box(
                self.searchbar,
                GeodeGtk.ScrolledWindow(
                    self.text_editor,
                    is_expandable=True,
                    is_fillable=True,
                ),
                set_orientation=Gtk.Orientation.VERTICAL,
                set_spacing=0,
            ),
            set_shadow_type=Gtk.ShadowType.OUT,
        )

    def __init_packing(self):
        """ Initialize widgets packing in main window
        """

        self.pack_start(self.toolbar, False, False)
        self.pack_start(self.frame, True, True)

    def __init_signals(self):
        """ Initialize widgets signals
        """

        signals = {
            self.searchbar: {
                "clicked": [
                    {
                        "method": self.text_editor.search_next,
                        "widget": "next",
                    },
                    {
                        "method": self.text_editor.search_previous,
                        "widget": "previous",
                    },
                ],
            },
            self.search_entry: {
                "activate": [
                    {"method": self.on_search_pattern},
                ],
                "changed": [
                    {"method": self.on_change_search_entry},
                ],
            },
            self.text_editor.inner_buffer: {
                "modified-changed": [
                    {"method": self.on_modify_text_buffer},
                ],
            },
            self.toolbar: {
                "activate": [
                    {
                        "method": self.on_set_editor_font,
                        "widget": "font",
                    },
                ],
                "clicked": [
                    {
                        "method": self.on_refresh_file,
                        "widget": "refresh",
                    },
                    {
                        "method": self.on_save_file,
                        "widget": "save",
                    },
                    {
                        "method": self.on_save_file_as,
                        "widget": "save_as",
                    },
                ],
                "toggled": [
                    {
                        "method": self.on_set_editor_option,
                        "widget": "auto_indent",
                    },
                    {
                        "method": self.on_set_editor_option,
                        "widget": "highlight_current_line",
                    },
                    {
                        "method": self.on_set_editor_option,
                        "widget": "indent_on_tab",
                    },
                    {
                        "method": self.on_set_editor_option,
                        "widget": "line_numbers",
                    },
                    {
                        "method": self.on_select_colorscheme,
                        "widget": "none",
                    },
                    {
                        "method": self.on_set_editor_option,
                        "widget": "right_margin",
                    },
                    {
                        "method": self.on_switch_search_bar,
                        "widget": "search",
                    },
                    {
                        "method": self.on_set_editor_option,
                        "widget": "space_instead_of_tab",
                    },
                    {
                        "method": self.on_set_editor_option,
                        "widget": "wrap_mode",
                    },
                ],
            },
            self.window: {
                "key-press-event": [
                    {"method": self.on_key_press_event},
                ],
                "response": [
                    {"method": self.on_close_dialog},
                ],
            },
        }

        # Connect widgets
        self.main_parent.load_signals(signals)
        # Remove signals storage from memory
        del signals

    def __init_interface(self):
        """ Initialize and fill interface widgets
        """

        # Ensure to start without any style scheme
        self.text_editor.set_style_scheme("none")

        # Add available colorschemes for GtkSource
        colorschemes = self.toolbar.get_widget("colorschemes")

        submenu = colorschemes.get_submenu()
        for name in self.text_editor.inner_style.get_scheme_ids():
            colorscheme = self.text_editor.inner_style.get_scheme(name)

            menuitem = GeodeGtk.RadioMenuItem(colorscheme.get_name(),
                                              group="none",
                                              identifier=colorscheme.get_id())
            menuitem.connect("toggled", self.on_select_colorscheme)
            submenu.append(menuitem)

        self.__colorscheme_was_loaded = True

        # Check use colorscheme selection
        scheme = self.__editor_config.get("colorscheme")
        if scheme is not None and submenu.has_widget(scheme):
            submenu.get_widget(scheme).set_active(True)

        # Set editor options
        self.text_editor.set_auto_indent(
            self.__editor_config.get("auto_indent"))
        self.text_editor.set_font(
            self.__editor_config.get("font"))
        self.text_editor.set_highlight_current_line(
            self.__editor_config.get("highlight_current_line"))
        self.text_editor.set_indent_on_tab(
            self.__editor_config.get("indent_on_tab"))
        self.text_editor.set_right_margin_position(
            self.__editor_config.get("right_margin_position"))
        self.text_editor.set_show_line_numbers(
            self.__editor_config.get("line_numbers"))
        self.text_editor.set_show_right_margin(
            self.__editor_config.get("right_margin"))
        self.text_editor.set_insert_spaces_instead_of_tabs(
            self.__editor_config.get("space_instead_of_tab"))
        self.text_editor.set_tab_width(
            self.__editor_config.get("tab_width"))
        self.text_editor.set_wrap_mode(
            self.__editor_config.get("wrap_mode"))

        submenu.show_all()
        self.show_all()

        # Hide search bar by default
        self.searchbar.set_visible(False)
        # Enable save action only in editable mode
        self.toolbar.get_widget("save").set_sensitive(self.__editable)
        self.toolbar.get_widget("refresh").set_sensitive(self.path.exists())
        # Focus cursor in text editor
        self.text_editor.grab_focus()

        self.on_open_file()

    def on_change_search_entry(self, widget: Gtk.Widget):
        """ Check search entry changes

        Parameters
        ----------
        widget : gi.repository.Gtk.Widget
            Object which receive signal
        """

        search = self.search_entry.get_text()

        # Reset founded iters when the search entry was cleared
        if len(search) == 0:
            self.text_editor.search_reset()

    def on_close_dialog(self, widget: Gtk.Widget, response: Gtk.ResponseType):
        """ Manage editor dialog closing process

        Parameters
        ----------
        widget : gi.repository.Gtk.Widget
            Object which receive signal
        response : gi.repository.Gtk.ResponseType
            Response type sent by closing dialog
        """

        if self.path is not None and self.text_editor.is_modified:
            dialog = QuestionDialog(
                self.main_parent,
                _("Closing editor"),
                _("The current buffer was modified. Do you want to save "
                  "this modification?"))

            if dialog.run() == Gtk.ResponseType.YES:
                self.save_file(self.path)

            dialog.destroy()

    def on_key_press_event(self, widget: Gtk.Widget, event: Gdk.EventKey):
        """ Manage user keys

        Parameters
        ----------
        widget : gi.repository.Gtk.Widget
            Object which receive signal
        event : gi.repository.Gdk.EventKey
            Event which triggered this signal
        """

        if event.type == Gdk.EventType.KEY_PRESS:
            ctrl_mask = event.state & Gdk.ModifierType.CONTROL_MASK

            # Ctrl+f to open/hide search bar
            if ctrl_mask and event.keyval == Gdk.KEY_f:
                widget = self.toolbar.get_widget("search")
                widget.set_active(not widget.get_active())

            # Ctrl+r or F5 to reload current buffer
            elif ((ctrl_mask and event.keyval == Gdk.KEY_r)
                  or event.keyval == Gdk.KEY_F5):
                self.on_refresh_file()

            # Ctrl+s to save current buffer
            elif ctrl_mask and event.keyval == Gdk.KEY_s:
                self.on_save_file()

            # Ctrl+Shift+s to save current buffer into another file
            elif ctrl_mask and event.keyval == Gdk.KEY_S:
                self.on_save_file_as()

    def on_modify_text_buffer(self, text_buffer: Gtk.TextBuffer):
        """ Check the buffer modified bit flips to update toolbar

        Parameters
        ----------
        textbuffer : gi.repository.Gtk.TextBuffer
            Modified buffer
        """

        self.toolbar.get_widget("save").set_style(
            Gtk.STYLE_CLASS_SUGGESTED_ACTION if text_buffer.get_modified()
            else None)

    def on_open_file(self, *args):
        """ Open a new file in source buffer

        This method will use GLib to load file without freezing interface
        """

        if not self.__buffer_thread == 0:
            GLib.source_remove(self.__buffer_thread)

        loader = self.open_file()
        self.__buffer_thread = GLib.idle_add(loader.__next__)

    def on_refresh_file(self, *args):
        """ Reload the current file

        This method will ask the user to confirm the reloading if the buffer
        was modified
        """

        if self.text_editor.is_modified:
            dialog = QuestionDialog(self.main_parent,
                                    _("The file was not saved"),
                                    _("Do you realy want to reload this file?"))
            response = dialog.run()
            dialog.destroy()

            if response == Gtk.ResponseType.NO:
                return

        self.on_open_file()

    def on_save_file(self, *args):
        """ Save the current file
        """

        # Avoid to save the file if the current buffer was not modified
        if self.path is None or not self.text_editor.is_modified:
            return

        self.save_file(self.path)

        self.toolbar.get_widget("refresh").set_sensitive(self.path.exists())

    def on_save_file_as(self, *args):
        """ Save a copy of the current file
        """

        dialog = Gtk.FileChooserNative.new(_("Save current file as"),
                                           self.main_parent,
                                           Gtk.FileChooserAction.SAVE)
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_filter(self.file_filter)
        dialog.set_preview_widget_active(False)
        dialog.set_select_multiple(False)
        dialog.set_use_preview_label(False)

        # Ensure to start in user home directory
        dialog.set_current_folder(str(Path('~').expanduser()))

        if dialog.run() == Gtk.ResponseType.ACCEPT:
            self.save_file(Path(dialog.get_filename()).expanduser())

        dialog.destroy()

    def on_search_pattern(self, *args):
        """ Search a pattern in current buffer
        """

        search = self.search_entry.get_text()
        if len(search) > 0:
            self.text_editor.search(search)

        # Move to the first founded iter if available
        self.text_editor.search_next()

    def on_select_colorscheme(self, widget: Gtk.Widget):
        """ Active the selected colorscheme

        Parameters
        ----------
        widget : gi.repository.Gtk.Widget
            Object which receive signal
        """

        if not self.__colorscheme_was_loaded:
            return

        if widget.get_active():
            self.text_editor.set_style_scheme(widget.identifier)

    def on_set_editor_font(self, widget: Gtk.Widget):
        """ Define the editor font

        Parameters
        ----------
        widget : gi.repository.Gtk.Widget
            Object which receive signal
        """

        dialog = Gtk.FontChooserDialog.new(_("Choose font for editor"),
                                           self.main_parent)
        dialog.set_font(self.text_editor.get_font())

        if dialog.run() == Gtk.ResponseType.OK:
            self.text_editor.set_font(dialog.get_font_desc())
            self.text_editor.set_monospace(
                dialog.get_font_family().is_monospace())

        dialog.destroy()

    def on_set_editor_option(self, widget: Gtk.Widget):
        """ Set break line mode for textview

        Parameters
        ----------
        widget : gi.repository.Gtk.Widget
            Object which receive signal
        """

        if widget.identifier == "auto_indent":
            self.text_editor.set_auto_indent(widget.get_active())

        elif widget.identifier == "highlight_current_line":
            self.text_editor.set_highlight_current_line(widget.get_active())

        elif widget.identifier == "indent_on_tab":
            self.text_editor.set_indent_on_tab(widget.get_active())

        elif widget.identifier == "line_numbers":
            self.text_editor.set_show_line_numbers(widget.get_active())

        elif widget.identifier == "right_margin":
            self.text_editor.set_show_right_margin(widget.get_active())

        elif widget.identifier == "space_instead_of_tab":
            self.text_editor.set_insert_spaces_instead_of_tabs(
                widget.get_active())

        elif widget.identifier == "wrap_mode":
            self.text_editor.set_wrap_mode(
                Gtk.WrapMode.WORD_CHAR if widget.get_active()
                else Gtk.WrapMode.NONE)

    def on_switch_search_bar(self, widget: Gtk.Widget):
        """ Switch between visible status for the search bar

        Parameters
        ----------
        widget : gi.repository.Gtk.Widget
            Object which receive signal
        """

        status = widget.get_active()

        self.searchbar.set_visible(status)
        self.searchbar.set_search_mode(status)

    def open_file(self):
        """ Open a file and store his contents inside source buffer

        Yields
        ------
        bool
            True if opening process still going, False otherwise
        """

        self.set_subtitle(_("Loading..."))

        self.text_editor.set_sensitive(False)
        self.text_editor.clear_buffer()

        # Remove style from save button since this buffer become unmodified
        self.toolbar.get_widget("save").set_style(None)

        yield True
        self.text_editor.open_file(self.path)

        self.text_editor.set_sensitive(True)
        self.set_subtitle(str(self.path))

        self.__buffer_thread = int()

        yield False

    @property
    def options(self) -> dict:
        """ Retrieve selected editor options

        Returns
        -------
        dict
            Selected options as dictionary structure
        """

        return {
            "auto_indent": self.text_editor.get_auto_indent(),
            "colorscheme": self.text_editor.get_style_scheme(),
            "font": self.text_editor.get_font(),
            "highlight_current_line": (
                self.text_editor.get_highlight_current_line()),
            "indent_on_tab": self.text_editor.get_indent_on_tab(),
            "line_numbers": self.text_editor.get_show_line_numbers(),
            "right_margin": self.text_editor.get_show_right_margin(),
            "space_instead_of_tab": (
                self.text_editor.get_insert_spaces_instead_of_tabs()),
            "wrap_mode": (
                self.text_editor.get_wrap_mode() == Gtk.WrapMode.WORD_CHAR),
        }

    def save_file(self, file_path: Path):
        """ Save current buffer to a specific file path

        Parameters
        ----------
        file_path : pathlib.Path
            The file path which will be used to save current buffer
        """

        self.text_editor.save_file_as(file_path)
