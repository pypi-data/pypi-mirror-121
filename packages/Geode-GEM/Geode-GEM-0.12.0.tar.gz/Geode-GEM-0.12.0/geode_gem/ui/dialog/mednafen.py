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

# Geode-GEM
from geode_gem.ui.data import Icons
from geode_gem.ui.widgets.window import CommonWindow
from geode_gem.widgets import GeodeGtk

# GObject
from gi.repository import Gtk, Pango

# Translation
from gettext import gettext as _


class MednafenDialog(CommonWindow):

    memory_list = ["eeprom", "flash", "rtc", "sensor", "sram"]

    def __init__(self, parent, name, data):
        """ Constructor

        Parameters
        ----------
        parent : Gtk.Window
            Parent object
        name : str
            Game name
        data : dict
            Backup memory type dictionary (with type as key)
        """

        CommonWindow.__init__(self,
                              parent,
                              _("Backup Memory Type"),
                              Icons.Symbolic.SAVE,
                              parent.use_classic_theme)

        # Main information
        self.data = data
        self.name = name

        # Files row storage
        self.__variables = {
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

        self.set_size(640, 420)
        self.set_spacing(6)
        self.set_resizable(True)
        self.set_subtitle(self.name)

        # ------------------------------------
        #   Parameters
        # ------------------------------------

        self.button_add_file = GeodeGtk.Button(
            label=_("Add a new flash type file"),
            icon_name=Icons.Symbolic.ADD,
            icon_size=Gtk.IconSize.BUTTON,
            identifier="add_file",
        )

        self.button_remove_file = GeodeGtk.Button(
            label=_("Remove the selected file"),
            icon_name=Icons.Symbolic.REMOVE,
            icon_size=Gtk.IconSize.BUTTON,
            identifier="remove_file",
        )

        self.entry_files_filter = GeodeGtk.SearchEntry(
            identifier="file_filter",
            set_placeholder_text=_("Filter..."),
        )

        self.adjustment_value = GeodeGtk.Adjustment(
            set_lower=0,
            set_upper=2147483647,  # INT_MAX
            set_step_increment=16,
            set_page_increment=1024,
        )

        self.model_cell_storage = Gtk.ListStore(str)
        self.model_files = Gtk.ListStore(str, int, int)

        self.treeview_files = GeodeGtk.TreeView(
            self.model_files,
            GeodeGtk.TreeViewColumn(
                _("Type"),
                GeodeGtk.CellRendererCombo(
                    self.model_cell_storage,
                    attributes={
                        "text": 0,
                    },
                    properties={
                        "editable": True,
                        "ellipsize": Pango.EllipsizeMode.END,
                        "has-entry": True,
                        "placeholder-text": _("Select a flash type"),
                        "text-column": 0,
                    },
                    identifier="cell_file_key",
                    is_expandable=True,
                    set_alignment=(0, 0.5),
                    set_padding=(12, 6),
                ),
                set_expand=True,
            ),
            GeodeGtk.TreeViewColumn(
                _("Value"),
                GeodeGtk.CellRendererSpin(
                    attributes={
                        "text": 1,
                    },
                    properties={
                        "adjustment": self.adjustment_value,
                        "editable": True,
                        "placeholder-text": _("No value"),
                    },
                    identifier="cell_file_value",
                    is_expandable=True,
                    set_alignment=(0, 0.5),
                    set_padding=(12, 6),
                ),
                set_expand=True,
            ),
            filterable=True,
            visible_func=self.check_item_is_visible,
        )

        # ------------------------------------
        #   View
        # ------------------------------------

        self.box = GeodeGtk.Box(
            GeodeGtk.Label(
                set_justify=Gtk.Justification.FILL,
                set_line_wrap=True,
                set_line_wrap_mode=Pango.WrapMode.WORD,
                set_max_width_chars=8,
                set_single_line_mode=False,
                set_label=_("This dialog allows you to specify specific "
                            "backup memory type for this game. Check Mednafen "
                            "documentation link for futher information."),
            ),
            GeodeGtk.Box(
                GeodeGtk.Box(
                    GeodeGtk.Box(
                        self.button_add_file,
                        self.button_remove_file,
                        merge=True,
                    ),
                    None,
                    self.entry_files_filter,
                ),
                GeodeGtk.Frame(
                    GeodeGtk.ScrolledWindow(
                        self.treeview_files,
                    ),
                    is_expandable=True,
                    is_fillable=True,
                ),
                is_expandable=True,
                is_fillable=True,
                set_orientation=Gtk.Orientation.VERTICAL,
                set_spacing=12,
            ),
            set_border_width=18,
            set_orientation=Gtk.Orientation.VERTICAL,
            set_spacing=12,
        )

    def __init_packing(self):
        """ Initialize widgets packing in main window
        """

        self.pack_start(self.box)

        self.add_button(_("Cancel"), Gtk.ResponseType.CLOSE)
        self.add_button(_("Apply"), Gtk.ResponseType.APPLY, Gtk.Align.END)

        self.add_external_link_help(
            _("Mednafen documentation"),
            ("https://mednafen.github.io/documentation/gba.html"
             "#Section_backupmem_type"))

    def __init_signals(self):
        """ Initialize widgets signals
        """

        signals = {
            self.button_add_file: {
                "clicked": [
                    {"method": self.on_append_item},
                ],
            },
            self.button_remove_file: {
                "clicked": [
                    {"method": self.on_remove_item},
                ],
            },
            self.entry_files_filter: {
                "changed": [
                    {"method": self.on_refilter_treeiters},
                ],
            },
            self.treeview_files: {
                "edited": [
                    {
                        "method": self.on_update_cell,
                        "widget": "cell_file_key",
                    },
                    {
                        "method": self.on_update_cell,
                        "widget": "cell_file_value",
                    },
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

        for key in self.memory_list:
            self.model_cell_storage.append([key])

        for index, key in enumerate(self.data):
            self.__variables["rows"][index] = self.treeview_files.append(
                [key, self.data.get(key), index])

        self.__variables["counter"] = len(self.treeview_files.list_model)

    def check_item_is_visible(self, model, row, *args):
        """ Check if a line is visible in files type treeview

        Parameters
        ----------
        model : Gtk.TreeModel
            Treeview model which receive signal
        row : Gtk.TreeModelRow
            Treeview current row
        """

        text = self.entry_files_filter.get_text()
        if not len(text):
            return True

        return text.lower() in model.get_value(row, 0)

    def on_append_item(self, widget):
        """ Append a new row in treeview

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        counter = self.__variables["counter"]

        self.__variables["rows"][counter] = \
            self.treeview_files.append([self.memory_list[0], int(), counter])
        self.__variables["counter"] += 1

    def on_refilter_treeiters(self, widget, *args):
        """ Refilter items list to update visible rows

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        self.treeview_files.refilter()

    def on_remove_item(self, widget):
        """ Remove a row in treeview

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        selection = self.treeview_files.get_selection()
        if selection is None:
            return

        model, treeiter = selection.get_selected()
        if treeiter is not None:
            index = self.treeview_files.inner_model.get_value(treeiter, 2)
            self.treeview_files.remove(self.__variables["rows"][index])

    def on_update_cell(self, widget, path, text):
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

        if widget.identifier == "cell_file_key":
            self.treeview_files.inner_model[path][0] = str(text)

        elif widget.identifier == "cell_file_value":
            self.treeview_files.inner_model[path][1] = int(text)

    def save(self):
        """ Retrieve information from current dialog

        Returns
        -------
        list
            Flash type string list
        """

        return [f"{key} {value}"
                for key, value, index in self.treeview_files.inner_model]
