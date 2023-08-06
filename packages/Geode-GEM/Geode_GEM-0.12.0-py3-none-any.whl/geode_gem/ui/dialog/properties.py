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
from geode_gem.ui.configurator import Configurator
from geode_gem.widgets import GeodeGtk

# GObject
from gi.repository import GdkPixbuf, Gtk, Pango

# System
from os import environ

# Translation
from gettext import gettext as _


class GamePropertiesDialog(Configurator):

    __help__ = {
        "order": [
            _("Description"),
            _("Parameters"),
        ],
        _("Description"): [
            _("Emulator default arguments can use custom parameters to "
              "facilitate file detection."),
            _("Nintendo console titles are identified by a 6 character "
              "identifier known as a GameID. This GameID is only used "
              "with some emulators like Dolphin-emu. For more "
              "informations, consult emulators documentation."),
            _("Tags are split by commas.")
        ],
        _("Parameters"): {
            "<key>": _("Use game key"),
            "<name>": _("Use ROM filename"),
            "<lname>": _("Use ROM lowercase filename"),
            "<rom_path>": _("Use ROM folder path"),
            "<rom_file>": _("Use ROM file path"),
            "<conf_path>": _("Use emulator configuration file path"),
        }
    }

    def __init__(self, parent, game, size):
        """ Constructor

        Parameters
        ----------
        parent : Gtk.Window
            Parent object
        game : geode_gem.engine.game.Game
            Game object
        size : (int, int)
            Dialog window size
        """

        Configurator.__init__(self,
                              parent,
                              _("Game properties"),
                              Icons.Symbolic.GAMING,
                              parent.use_classic_theme)

        # Application objects instances
        self.api = parent.api
        self.game = game

        # Dialog window size
        self.__size = size

        # Environment variables row storage
        self.__variables = {
            "counter": int(),
            "rows": dict(),
        }

        # Initialize interface
        self.__init_widgets()
        self.__init_signals()
        self.__init_packing()
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

        self.entry_name.set_tooltip_text(_("Game name"))

        self.model_tags = Gtk.ListStore(str)

        self.entry_tags = GeodeGtk.SearchEntry(
            GeodeGtk.EntryIcon(Gtk.EntryIconPosition.PRIMARY, None),
            GeodeGtk.EntryCompletion(
                self.model_tags,
                identifier="completion_tags",
                set_popup_single_match=True,
                set_popup_completion=True,
                set_text_column=0,
                set_match_func=self.on_entry_completion_match_tag,
            ),
            identifier="tags",
            set_hexpand=True,
            set_placeholder_text=_("Use comma to separate tags"),
            set_tooltip_text=_("Use comma to separate tags"),
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
            identifier="emulator_binary",
            is_expandable=True,
            is_fillable=True,
            set_id_column=2,
        )

        self.entry_arguments = GeodeGtk.SearchEntry(
            GeodeGtk.EntryIcon(
                Gtk.EntryIconPosition.PRIMARY,
                Icons.Symbolic.TERMINAL,
            ),
            identifier="emulator_arguments",
            is_expandable=True,
            is_fillable=True,
            set_placeholder_text=_("No default value"),
        )

        self.entry_game_id = GeodeGtk.SearchEntry(
            GeodeGtk.EntryIcon(
                Gtk.EntryIconPosition.PRIMARY,
                Icons.Symbolic.PASSWORD,
            ),
            identifier="game_id",
            is_expandable=True,
            is_fillable=True,
            set_placeholder_text=_("No default value"),
        )

        # ----------------------------------------
        #   Environment variables
        # ----------------------------------------

        self.model_cell_storage = Gtk.ListStore(str)

        self.treeview_environment = GeodeGtk.TreeView(
            Gtk.ListStore(str, str, int),
            GeodeGtk.TreeViewColumn(
                _("Name"),
                GeodeGtk.CellRendererCombo(
                    self.model_cell_storage,
                    attributes={
                        "text": 0,
                    },
                    properties={
                        "editable": True,
                        "ellipsize": Pango.EllipsizeMode.END,
                        "has-entry": True,
                        "placeholder-text": _("Variable name"),
                        "text-column": 0,
                    },
                    identifier="cell_environment_key",
                    is_expandable=True,
                    set_alignment=(0, 0.5),
                    set_padding=(12, 6),
                ),
                set_expand=True,
            ),
            GeodeGtk.TreeViewColumn(
                _("Value"),
                GeodeGtk.CellRendererText(
                    attributes={
                        "text": 1,
                    },
                    properties={
                        "editable": True,
                        "ellipsize": Pango.EllipsizeMode.END,
                        "placeholder-text": _("No value"),
                    },
                    identifier="cell_environment_value",
                    is_expandable=True,
                    set_alignment=(0, 0.5),
                    set_padding=(12, 6),
                ),
                set_expand=True,
            ),
            filterable=True,
            visible_func=self.check_item_is_visible,
        )

        self.button_add_variable = GeodeGtk.Button(
            label=_("Add a new variable"),
            icon_name=Icons.Symbolic.ADD,
            icon_size=Gtk.IconSize.BUTTON,
            identifier="add_variable",
        )

        self.button_remove_variable = GeodeGtk.Button(
            label=_("Remove the selected variable"),
            icon_name=Icons.Symbolic.REMOVE,
            icon_size=Gtk.IconSize.BUTTON,
            identifier="remove_variable",
        )

        self.entry_variables_filter = GeodeGtk.SearchEntry(
            identifier="variable_filter",
            set_placeholder_text=_("Filter..."),
        )

        # ----------------------------------------
        #   Stack sidebar
        # ----------------------------------------

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
                        GeodeGtk.Label(
                            set_halign=Gtk.Align.END,
                            set_style=Gtk.STYLE_CLASS_DIM_LABEL,
                            set_text=_("Tags"),
                        ),
                        left=0,
                        top=2,
                        width=1,
                        height=1,
                    ),
                    GeodeGtk.GridItem(
                        self.button_thumbnail, left=2, top=0, width=1, height=2,
                    ),
                    GeodeGtk.GridItem(
                        self.entry_tags, left=1, top=2, width=2, height=1,
                    ),
                    set_row_spacing=6,
                    set_column_spacing=12,
                    set_column_homogeneous=False,
                    set_margin_bottom=18,
                ),
                GeodeGtk.StackSection(
                    _("Alternative emulator"),
                    GeodeGtk.Frame(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Emulator"),
                                self.combobox_emulators,
                                description=_("Use an alternative emulator "
                                              "for this game"),
                                homogeneous=True,
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Arguments"),
                                self.entry_arguments,
                                homogeneous=True,
                            ),
                        ),
                    ),
                ),
                GeodeGtk.StackSection(
                    _("Flags"),
                    GeodeGtk.Frame(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Favorite"),
                                GeodeGtk.Switch(
                                    identifier="flag_favorite",
                                ),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Multiplayer"),
                                GeodeGtk.Switch(
                                    identifier="flag_multiplayer",
                                ),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Finish"),
                                GeodeGtk.Switch(
                                    identifier="flag_finish",
                                ),
                            ),
                        ),
                    ),
                ),
                GeodeGtk.StackSection(
                    _("Misc"),
                    GeodeGtk.Frame(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Game identifier"),
                                self.entry_game_id,
                                homogeneous=True,
                            ),
                        ),
                    ),
                ),
            ),
            GeodeGtk.StackView(
                _("Environment"),
                GeodeGtk.StackSection(
                    _("Environment variables"),
                    GeodeGtk.Box(
                        GeodeGtk.Label(
                            set_text=_(
                                "You can defined environment variables which "
                                "will be used during the game launching "
                                "process."),
                            set_halign=Gtk.Align.START,
                            set_valign=Gtk.Align.CENTER,
                            set_margin_bottom=12,
                            set_line_wrap=True,
                        ),
                        GeodeGtk.Box(
                            GeodeGtk.Box(
                                self.button_add_variable,
                                self.button_remove_variable,
                                merge=True,
                            ),
                            None,
                            self.entry_variables_filter,
                        ),
                        GeodeGtk.Frame(
                            GeodeGtk.ScrolledWindow(
                                self.treeview_environment,
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
            self.combobox_emulators: {
                "changed": [
                    {"method": self.on_select_emulator},
                ],
            },
            self.entry_tags: {
                "match-selected": [
                    {
                        "method": self.on_entry_completion_write_tag,
                        "widget": "completion_tags",
                    },
                ],
            },
            self.entry_variables_filter: {
                "changed": [
                    {"method": self.on_refilter_treeiters},
                ],
            },
            self.stack: {
                "clicked": [
                    {
                        "method": self.on_append_item,
                        "widget": "add_variable",
                    },
                    {
                        "method": self.on_remove_item,
                        "widget": "remove_variable",
                    },
                ],
            },
            self.treeview_environment: {
                "edited": [
                    {
                        "method": self.on_update_item,
                        "widget": "cell_environment_key",
                    },
                    {
                        "method": self.on_update_item,
                        "widget": "cell_environment_value",
                    },
                ],
            },
        }

        signals |= self.default_signals

        # Do not need to check if a name already exists in games collection
        del signals[self.entry_name]

        # Connect widgets
        self.main_parent.load_signals(signals)
        # Remove signals storage from memory
        del signals

    def __init_interface(self):
        """ Initialize and fill interface widgets
        """

        model = self.combobox_emulators.get_model()

        emulators = list()
        for emulator in self.main_parent.api.emulators.values():
            icon = self.main_parent.get_pixbuf_from_cache(
                "emulators", 22, emulator.id, emulator.icon)
            if icon is None:
                icon = self.main_parent.icons_blank.get(22)

            row = model.append([icon, emulator.name, emulator.id])
            if row is not None:
                emulators.append(emulator.id)

        self.entry_name.set_text(self.game.name)

        if self.game.cover is not None:
            self.entry_thumbnail.set_text(str(self.game.cover))

        # Game tags
        if len(self.game.tags) > 0:
            self.entry_tags.set_text(', '.join(self.game.tags))

        for tag in self.main_parent.api.get_game_tags():
            self.model_tags.append([tag])

        # Emulator
        emulator = self.game.emulator
        if emulator is not None and emulator.id in emulators:
            self.combobox_emulators.set_active_id(emulator.id)

        # Emulator parameters
        if len(self.game.default) > 0:
            self.entry_arguments.set_text(self.game.default)

        # Flags
        for identifier in ("favorite", "multiplayer", "finish"):
            widget = self.stack.get_widget(f"flag_{identifier}")
            widget.set_active(getattr(self.game, identifier))

        # Game ID
        if self.game.key is not None:
            self.entry_game_id.set_text(self.game.key)

        # Environment variables
        for index, key in enumerate(sorted(self.game.environment)):
            self.__variables["rows"][index] = self.treeview_environment.append(
                [key, self.game.environment[key], index])

        self.__variables["counter"] = len(self.treeview_environment.list_model)

        for key in sorted(environ.copy().keys()):
            self.model_cell_storage.append([key])

    def check_item_is_visible(self, model, row, *args):
        """ Check if a line is visible in ignores listview

        Parameters
        ----------
        model : Gtk.TreeModel
            Treeview model which receive signal
        row : Gtk.TreeModelRow
            Treeview current row
        """

        text = self.entry_variables_filter.get_text()
        if not len(text):
            return True

        return (text.upper() in model.get_value(row, 0)
                or text in model.get_value(row, 1))

    def on_entry_completion_match_tag(self, widget, key, treeiter):
        """ Check if current entry match an entry from completion

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        key : str
            String to match
        treeiter : Gtk.Treeiter
            Row to match

        Returns
        -------
        bool
            Match item status
        """

        text = self.entry_tags.get_text()

        # Retrieve tag from model
        tag = self.model_tags.get_value(treeiter, 0)

        if ',' in text:
            # Retrieve current cursor position
            position = self.entry_tags.get_position()

            # Retrieve commas position
            left_comma = text.rfind(',', 0, position)
            right_comma = text.find(',', position)

            if left_comma == -1 and right_comma == -1:
                text = text
            elif left_comma == -1:
                text = text[:right_comma]
            elif right_comma == -1:
                text = text[left_comma + 1:]
            else:
                text = text[left_comma + 1:right_comma]

        # Avoid to retrieve all the tag when the specified text is empty
        if len(text.strip()) == 0:
            return False

        # Avoid to show the tag when the user already complete it
        if text.strip() == tag:
            return False

        # Check if the tag start with the specified text
        return tag.startswith(text.strip())

    def on_entry_completion_write_tag(self, widget, model, treeiter):
        """ Write the specified completion item to entry

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        model : Gtk.TreeModel
            Model which contains data
        treeiter : Gtk.Treeiter
            Selected entry from model

        Returns
        -------
        bool
            Handled signal
        """

        text = self.entry_tags.get_text()

        # Retrieve tag from model
        tag = model.get_value(treeiter, 0)

        if len(text) > 0:
            # Retrieve current cursor position
            position = self.entry_tags.get_position()

            # Retrieve commas position
            left_comma = text.rfind(',', 0, position)
            right_comma = text.find(',', position)

            left_text = str()
            if not left_comma == -1:
                left_text = text[:left_comma + 1] + ' '

            right_text = str()
            if not right_comma == -1:
                right_text = text[right_comma:]

            self.entry_tags.set_text(left_text + tag + right_text)
            self.entry_tags.set_position(len(left_text + tag))

        return True

    def on_append_item(self, widget):
        """ Append a new row in treeview

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        counter = self.__variables["counter"]

        self.__variables["rows"][counter] = \
            self.treeview_environment.append([str(), str(), counter])
        self.__variables["counter"] += 1

    def on_refilter_treeiters(self, widget, *args):
        """ Refilter items list to update visible rows

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        self.treeview_environment.refilter()

    def on_remove_item(self, widget):
        """ Remove a row in treeview

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        selection = self.treeview_environment.get_selection()
        if selection is None:
            return

        model, treeiter = selection.get_selected()
        if treeiter is not None:
            index = self.treeview_environment.inner_model.get_value(treeiter, 2)
            self.treeview_environment.remove(self.__variables["rows"][index])

    def on_update_item(self, widget, path, text):
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

        if widget.identifier == "cell_environment_key":
            self.treeview_environment.inner_model[path][0] = str(text)

        elif widget.identifier == "cell_environment_value":
            self.treeview_environment.inner_model[path][1] = str(text)

    def on_select_emulator(self, widget=None):
        """ Select an emulator in combobox and update parameters placeholder

        Other Parameters
        ----------------
        widget : Gtk.Widget
            Object which receive signal (Default: None)
        """

        emulator = self.main_parent.api.get_emulator(
            self.combobox_emulators.get_active_id())

        self.entry_arguments.set_placeholder_text(_("No default value"))

        if emulator is not None and len(emulator.default) > 0:
            self.entry_arguments.set_placeholder_text(emulator.default)

    def save(self):
        """ Save information into game object

        Returns
        -------
        geode_gem.engine.game.Game
            Game object
        """

        name = self.entry_name.get_text().strip()
        if len(name) == 0:
            name = self.game.path.stem

        path = self.entry_thumbnail.get_text().strip()
        if len(path) > 0:
            path = Path(path).expanduser()
        else:
            path = None

        tags = self.entry_tags.get_text().strip()
        if len(tags) > 0:
            tags = [tag.strip() for tag in tags.split(',')]
        else:
            tags = list()

        self.game.name = name
        self.game.key = self.entry_game_id.get_text().strip()
        self.game.default = self.entry_arguments.get_text().strip()
        self.game.cover = path
        self.game.tags = tags

        self.game.emulator = self.api.get_emulator(
            self.combobox_emulators.get_active_id())

        for flag in ("favorite", "multiplayer", "finish"):
            setattr(self.game, flag,
                    self.stack.get_widget(f"flag_{flag}").get_active())

        self.game.environment.clear()

        model = self.treeview_environment.get_model()
        for row in model:
            key = model.get_value(row.iter, 0).strip()
            if len(key) == 0:
                continue

            value = model.get_value(row.iter, 1).strip()
            self.game.environment[key] = value

        return self.game
