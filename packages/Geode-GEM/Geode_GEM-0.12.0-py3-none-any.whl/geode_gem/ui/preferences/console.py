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
from geode_gem.engine.console import Console
from geode_gem.engine.utils import generate_identifier

from geode_gem.ui.configurator import Configurator
from geode_gem.ui.data import Icons
from geode_gem.widgets import GeodeGtk

# GObject
from gi.repository import GdkPixbuf, Gtk, Pango

# Translation
from gettext import gettext as _


class ConsolePreferences(Configurator):

    __help__ = {
        "order": [
            "Description",
            "Extensions",
            _("Extensions examples"),
            "Expressions"
        ],
        "Description": [
            _("A console represent a games library. You can specify a "
              "default emulator which is used by this console and "
              "extensions which is readable by this emulator.")
        ],
        "Extensions": [
            _("Most of the time, extensions are common between differents "
              "emulators and represent the console acronym name (example: "
              "Nintendo NES -> nes)."),
            _("Extensions are split by spaces and must not have the first "
              "dot (using \"nes\" than \".nes\").")
        ],
        _("Extensions examples"): {
            "Nintendo NES": "nes",
            "Sega Megadrive": "md smd bin 32x md cue"
        },
        "Expressions": [
            _("It's possible to hide specific files from the games list "
              "with regular expressions.")
        ]
    }

    def __init__(self, parent, console, consoles, emulators, size):
        """ Constructor

        Parameters
        ----------
        parent : geode_gem.ui.interface.MainWindow
            Parent application object
        console : geode_gem.engine.console.Console
            Console object
        consoles : list
            Consoles object list
        emulators : list
            Emulators object list
        size : tuple
            Window dialog size as integer's tuple
        """

        Configurator.__init__(self,
                              parent,
                              _("Console"),
                              Icons.Symbolic.GAMING,
                              parent.use_classic_theme)

        # Application objects instances
        self.api = parent.api
        self.config = parent.config
        self.consoles = consoles
        self.emulators = emulators

        # Console object
        self.console = console

        # Dialog window size
        self.__size = size

        # Ignores row storage
        self.__ignores = {
            "counter": int(),
            "rows": dict(),
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

        # ----------------------------------------
        #   Parameters
        # ----------------------------------------

        self.init_common_widgets()

        self.entry_name.set_tooltip_text(_("Console name"))

        self.filechooser_games = GeodeGtk.FileChooserButton(
            _("Console games directory"),
            Gtk.FileChooserAction.SELECT_FOLDER,
            is_expandable=True,
            is_fillable=True,
        )

        self.button_reset_games = GeodeGtk.Button(
            label=_("Reset selected games directory"),
            icon_name=Icons.Symbolic.CLEAR,
            icon_size=Gtk.IconSize.BUTTON,
        )

        self.switch_recursive = GeodeGtk.Switch(
            set_active=False,
        )

        self.switch_favorite = GeodeGtk.Switch(
            set_active=False,
        )

        self.combobox_emulators = GeodeGtk.ComboBox(
            Gtk.ListStore(GdkPixbuf.Pixbuf, str, str),
            GeodeGtk.CellRendererPixbuf(
                attributes={
                    "pixbuf": 0,
                },
            ),
            GeodeGtk.CellRendererText(
                attributes={
                    "text": 1,
                },
                set_alignment=(0, 0.5),
                set_padding=(6, 0),
            ),
            is_expandable=True,
            is_fillable=True,
            set_id_column=2,
        )

        self.button_reset_emulator = GeodeGtk.Button(
            label=_("Reset selected emulator"),
            icon_name=Icons.Symbolic.CLEAR,
            icon_size=Gtk.IconSize.BUTTON,
        )

        self.entry_extensions = GeodeGtk.SearchEntry(
            GeodeGtk.EntryIcon(Gtk.EntryIconPosition.PRIMARY, None),
            identifier="extensions",
            is_expandable=True,
            is_fillable=True,
            set_hexpand=True,
            set_placeholder_text=_("Use space to separate extensions"),
        )

        self.treeview_ignores = GeodeGtk.TreeView(
            Gtk.ListStore(str, int),
            GeodeGtk.TreeViewColumn(
                "line",
                GeodeGtk.CellRendererText(
                    attributes={
                        "text": 0,
                    },
                    properties={
                        "editable": True,
                        "ellipsize": Pango.EllipsizeMode.END,
                        "placeholder_text": _("Write your regex here..."),
                    },
                    identifier="cell_ignores",
                    is_expandable=True,
                    set_alignment=(0, 0.5),
                    set_padding=(12, 6),
                ),
            ),
            filterable=True,
            set_headers_visible=False,
            visible_func=self.check_item_is_visible,
        )

        self.button_add_ignore = GeodeGtk.Button(
            _("Add a new line"),
            icon_name=Icons.Symbolic.ADD,
        )

        self.button_remove_ignore = GeodeGtk.Button(
            _("Remove selected line"),
            icon_name=Icons.Symbolic.REMOVE,
        )

        self.entry_ignores_filter = GeodeGtk.SearchEntry(
            identifier="console_filter",
            set_placeholder_text=_("Filter..."),
        )

        # ------------------------------------
        #   Stack sidebar
        # ------------------------------------

        self.stack = GeodeGtk.StackSidebar(
            GeodeGtk.StackView(
                _("Parameters"),
                GeodeGtk.Grid(
                    GeodeGtk.GridItem(
                        GeodeGtk.Label(
                            set_halign=Gtk.Align.END,
                            set_style=Gtk.STYLE_CLASS_DIM_LABEL,
                            set_text=_("Name"),
                        ),
                        left=0,
                        top=0,
                        width=1,
                        height=1,
                    ),
                    GeodeGtk.GridItem(
                        self.entry_name, left=1, top=0, width=1, height=1,
                    ),
                    GeodeGtk.GridItem(
                        GeodeGtk.Label(
                            set_halign=Gtk.Align.END,
                            set_style=Gtk.STYLE_CLASS_DIM_LABEL,
                            set_text=_("Icon"),
                        ),
                        left=0,
                        top=1,
                        width=1,
                        height=1,
                    ),
                    GeodeGtk.GridItem(
                        GeodeGtk.Box(
                            self.entry_thumbnail,
                            self.button_filechooser,
                            merge=True
                        ), left=1, top=1, width=1, height=1,
                    ),
                    GeodeGtk.GridItem(
                        self.button_thumbnail, left=2, top=0, width=1, height=2,
                    ),
                    set_row_spacing=6,
                    set_column_spacing=12,
                    set_column_homogeneous=False,
                    set_margin_bottom=18,
                ),
                GeodeGtk.StackSection(
                    _("Console"),
                    GeodeGtk.Frame(
                        GeodeGtk.ScrolledWindow(
                            GeodeGtk.ListBox(
                                GeodeGtk.ListBoxItem(
                                    _("Games directory"),
                                    GeodeGtk.Box(
                                        self.filechooser_games,
                                        self.button_reset_games,
                                        is_expandable=True,
                                        is_fillable=True,
                                        set_spacing=6,
                                    ),
                                    description=_("Directory used to retrieve "
                                                  "games files"),
                                ),
                                GeodeGtk.ListBoxItem(
                                    _("Use recursive mode"),
                                    self.switch_recursive,
                                    description=_("Retrieve files recursively. "
                                                  "This option must be used "
                                                  "carefully!"),
                                ),
                                GeodeGtk.ListBoxItem(
                                    _("Mark as favorite"),
                                    self.switch_favorite,
                                    description=_("Mark this console as one of "
                                                  "your favorite"),
                                ),
                            ),
                            set_policy=(
                                Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER),
                        ),
                    ),
                ),
                GeodeGtk.StackSection(
                    _("Launcher"),
                    GeodeGtk.Frame(
                        GeodeGtk.ScrolledWindow(
                            GeodeGtk.ListBox(
                                GeodeGtk.ListBoxItem(
                                    _("Emulator"),
                                    GeodeGtk.Box(
                                        self.combobox_emulators,
                                        self.button_reset_emulator,
                                        is_expandable=True,
                                        is_fillable=True,
                                        set_spacing=6,
                                    ),
                                    description=_("This emulator will be used "
                                                  "to launch games"),
                                    homogeneous=True,
                                ),
                                GeodeGtk.ListBoxItem(
                                    _("Extensions"),
                                    self.entry_extensions,
                                    description=_("File extensions associated "
                                                  "with this console"),
                                    homogeneous=True,
                                    set_tooltip_text=_(
                                        "Use space to separate extensions"),
                                ),
                            ),
                            set_policy=(
                                Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER),
                        ),
                    ),
                ),
            ),
            GeodeGtk.StackView(
                _("Files"),
                GeodeGtk.StackSection(
                    _("Ignore files"),
                    GeodeGtk.Box(
                        GeodeGtk.Label(
                            set_text=_(
                                "Files can be ignored during console loading "
                                "process. You can use Regular Expression to "
                                "define which files needs to be ignored."),
                            set_halign=Gtk.Align.START,
                            set_valign=Gtk.Align.CENTER,
                            set_margin_bottom=12,
                            set_line_wrap=True,
                        ),
                        GeodeGtk.Box(
                            GeodeGtk.Box(
                                self.button_add_ignore,
                                self.button_remove_ignore,
                                merge=True,
                            ),
                            None,
                            self.entry_ignores_filter,
                        ),
                        GeodeGtk.Frame(
                            GeodeGtk.ScrolledWindow(
                                self.treeview_ignores,
                            ),
                            is_expandable=True,
                            is_fillable=True,
                        ),
                        is_expandable=True,
                        is_fillable=True,
                        set_orientation=Gtk.Orientation.VERTICAL,
                        set_spacing=12,
                    ),
                    is_expandable=True,
                    is_fillable=True,
                ),
            ),
        )

    def __init_packing(self):
        """ Initialize widgets packing in main window
        """

        self.pack_start(self.stack)

        self.add_button(_("Close"), Gtk.ResponseType.CLOSE)
        self.add_button(_("Accept"), Gtk.ResponseType.APPLY, Gtk.Align.END)

        self.add_help(self.__help__)

    def __init_signals(self):
        """ Initialize widgets signals
        """

        signals = {
            self.button_add_ignore: {
                "clicked": [
                    {"method": self.on_append_item},
                ],
            },
            self.button_remove_ignore: {
                "clicked": [
                    {"method": self.on_remove_item},
                ],
            },
            self.button_reset_emulator: {
                "clicked": [
                    {"method": self.on_reset_widget},
                ],
            },
            self.button_reset_games: {
                "clicked": [
                    {"method": self.on_reset_widget},
                ],
            },
            self.entry_ignores_filter: {
                "changed": [
                    {"method": self.on_refilter_treeiters},
                ],
            },
            self.treeview_ignores: {
                "edited": [
                    {
                        "method": self.on_edited_cell,
                        "widget": "cell_ignores",
                    },
                ],
            },
        }

        signals |= self.default_signals

        # Connect widgets
        self.main_parent.load_signals(signals)
        # Remove signals storage from memory
        del signals

    def __init_interface(self):
        """ Initialize and fill interface widgets
        """

        model = self.combobox_emulators.get_model()

        emulators = list()
        for emulator in self.emulators.values():
            icon = self.main_parent.get_pixbuf_from_cache(
                "emulators",
                22,
                emulator.id,
                emulator.icon,
                use_cache=False)
            if icon is None:
                icon = self.main_parent.icons_blank.get(22)

            row = model.append([icon, emulator.name, emulator.id])
            if row is not None:
                emulators.append(emulator.id)

        # Filling not needed with new console
        if self.console is None or self.console.id is None:
            return

        self.entry_name.set_text(self.console.name)
        self.entry_name.set_placeholder_text(self.console.name)

        if self.console.icon is not None:
            self.entry_thumbnail.set_text(str(self.console.icon))

        if self.console.path is not None:
            self.filechooser_games.set_filename(str(self.console.path))

        self.switch_favorite.set_active(self.console.favorite)
        self.switch_recursive.set_active(self.console.recursive)

        self.entry_extensions.set_text(' '.join(self.console.extensions))

        # Ignores Regular Expressions
        for index, ignore in enumerate(self.console.ignores):
            self.__ignores["rows"][index] = self.treeview_ignores.append(
                [ignore, index])

        self.__ignores["counter"] = len(self.treeview_ignores.list_model)

        # Emulator
        emulator = self.console.emulator
        if emulator is not None and emulator.id in emulators:
            self.combobox_emulators.set_active_id(emulator.id)

    def check_item_is_visible(self, model, row, *args):
        """ Check if a line is visible in ignores listview

        Parameters
        ----------
        model : Gtk.TreeModel
            Treeview model which receive signal
        row : Gtk.TreeModelRow
            Treeview current row
        """

        text = self.entry_ignores_filter.get_text()
        if not len(text):
            return True

        return text in model.get_value(row, 0)

    def on_append_item(self, widget):
        """ Append a new row in treeview

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        counter = self.__ignores["counter"]

        self.__ignores["rows"][counter] = \
            self.treeview_ignores.append([str(), counter])
        self.__ignores["counter"] += 1

    def on_edited_cell(self, widget, path, text):
        """ Update treerow when a cell has been edited

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        path : str
            Path identifying the edited cell
        text : str
            New text
        """

        self.treeview_ignores.inner_model[path][0] = str(text)

    def on_refilter_treeiters(self, widget, *args):
        """ Refilter items list to update visible rows

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        self.treeview_ignores.refilter()

    def on_remove_item(self, widget):
        """ Remove a row in treeview

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        selection = self.treeview_ignores.get_selection()
        if selection is None:
            return

        model, treeiter = selection.get_selected()
        if treeiter is not None:
            index = self.treeview_ignores.inner_model.get_value(treeiter, 1)
            self.treeview_ignores.remove(self.__ignores["rows"][index])

            del self.__ignores["rows"][index]

    def on_reset_widget(self, widget):
        """ Reset a specific widget

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        if widget == self.button_reset_games:
            self.filechooser_games.set_filename(str())

        elif widget == self.button_reset_emulator:
            self.combobox_emulators.set_active_id(None)

    def on_update_name_entry(self, widget):
        """ Check if a value is not already used

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        Configurator.on_update_name_entry(
            self, widget, self.consoles, self.console)

    def save(self):
        """ Save modification
        """

        name = self.entry_name.get_text().strip()
        if len(name) == 0:
            raise ValueError("Cannot save a console with an empty name")

        console = Console(
            self.api,
            id=generate_identifier(name),
            name=name,
            path=self.filechooser_games.get_filename(),
            extensions=self.entry_extensions.get_text().strip().split(),
            favorite=self.switch_favorite.get_active(),
            recursive=self.switch_recursive.get_active(),
            emulator=self.emulators.get(self.combobox_emulators.get_active_id())
        )

        icon = self.entry_thumbnail.get_text().strip()
        if len(icon) > 0:
            console.icon = Path(icon).expanduser()

        model = self.treeview_ignores.get_model()
        for row in model:
            element = model.get_value(row.iter, 0)
            if element is not None and len(element) > 0:
                console.ignores.append(element)

        return console
