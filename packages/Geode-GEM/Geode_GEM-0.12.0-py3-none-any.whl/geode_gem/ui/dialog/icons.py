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
from geode_gem.engine.utils import get_data

from geode_gem.ui.data import Icons
from geode_gem.ui.widgets.window import CommonWindow
from geode_gem.widgets import GeodeGtk

# GObject
from gi.repository import GdkPixbuf, GLib, Gtk

# Translation
from gettext import gettext as _


class IconsDialog(CommonWindow):

    def __init__(self, parent):
        """ Constructor

        Parameters
        ----------
        parent : gi.repository.Gtk.Window
            Parent object
        """

        CommonWindow.__init__(self,
                              parent,
                              _("Icons browser"),
                              Icons.Symbolic.IMAGE,
                              parent.use_classic_theme)

        # Application objects instances
        self.api = parent.api

        # Cache storage
        self.icons = dict()
        self.selected_icon = None
        # Listbox rows storage
        self.rows = dict()
        # Threading process
        self.thread = int()

        # Initialize interface
        self.__init_widgets()
        self.__init_packing()
        self.__init_signals()
        self.__init_interface()

    def __init_widgets(self):
        """ Initialize interface widgets
        """

        self.set_size(800, 600)
        self.set_spacing(6)
        self.set_resizable(True)

        # ----------------------------------------
        #   Parameters
        # ----------------------------------------

        self.listbox_categories = GeodeGtk.ListBox(
            set_selection_mode=Gtk.SelectionMode.SINGLE,
        )

        self.iconview_category = GeodeGtk.IconView(
            Gtk.ListStore(
                GdkPixbuf.Pixbuf,       # Icon pixbuf
                str,                    # Icon name
            ),
            is_expandable=True,
            is_fillable=True,
            set_pixbuf_column=0,
            set_tooltip_column=1,
            set_item_width=64,
            set_spacing=6,
            set_has_tooltip=True,
        )

        # ----------------------------------------
        #   Paned view
        # ----------------------------------------

        self.box = GeodeGtk.Box(
            GeodeGtk.Frame(
                GeodeGtk.ScrolledWindow(
                    self.listbox_categories,
                ),
                set_size_request=(150, -1),
            ),
            GeodeGtk.Frame(
                GeodeGtk.ScrolledWindow(
                    self.iconview_category,
                ),
                is_expandable=True,
                is_fillable=True,
            ),
            set_orientation=Gtk.Orientation.HORIZONTAL,
        )

    def __init_packing(self):
        """ Initialize widgets packing in main window
        """

        self.add_button(_("Close"), Gtk.ResponseType.CLOSE)
        self.add_button(_("Accept"), Gtk.ResponseType.APPLY, Gtk.Align.END)

        self.pack_start(self.box)

    def __init_signals(self):
        """ Initialize widgets signals
        """

        signals = {
            self.iconview_category: {
                "item-activated": [
                    {"method": self.on_activate_icon_selection}
                ],
                "selection-changed": [
                    {"method": self.on_update_icon_selection}
                ],
            },
            self.listbox_categories: {
                "row-selected": [
                    {"method": self.on_load_icons}
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

        self.set_response_sensitive(Gtk.ResponseType.APPLY, False)

        # Ensure to translate available contexts from default icons theme
        contexts = [_(context)
                    for context in self.main_parent.icons_theme.list_contexts()
                    if context not in ("Animations", "Legacy", "UI")]
        # Add also the Geode-GEM console icons collection
        contexts.append(_("Consoles"))

        for context in sorted(contexts):
            self.rows[context] = GeodeGtk.ListBoxItem(context)

            self.listbox_categories.add(self.rows[context])

            if context == _("Consoles"):
                path = get_data("data", "icons").resolve()
                icons = [icon.stem for icon in path.glob("*.png")]

            else:
                icons = self.main_parent.icons_theme.list_icons(context)

            self.icons[context] = icons

        self.listbox_categories.select_row(self.rows[_("Consoles")])

    def on_activate_icon_selection(self, widget, row):
        """ Send apply response when double-click on icon item

        Parameters
        ----------
        widget : gi.repository.Gtk.ListBox
            Object which received the signal
        path : gi.repository.Gtk.TreePath
            Tree path for the activated item
        """

        self.emit_response(None, Gtk.ResponseType.APPLY)

    def on_append_icons(self, context):
        """ Appends icons for a specific context as GLib thread

        Parameters
        ----------
        context : str
            Icon context category string
        """

        model = self.iconview_category.get_model()
        model.clear()

        for icon in sorted(self.icons[context]):
            row = self.on_append_icon(model, icon)
            if row is None:
                continue

            yield True

        self.thread = int()

        yield False

    def on_append_icon(self, model, icon_name):
        """ Add an icon to icon view

        Parameters
        ----------
        model : gi.repository.Gtk.TreeStore
            Icon view model storage
        icon_name : str
            Icon name as defined in icon theme

        Returns
        -------
        gi.repository.Gtk.TreeIter or None
            Inserted tree storage iter
        """

        icon_info = self.main_parent.icons_theme.lookup_icon_for_scale(
            icon_name, 64, 1, Gtk.IconLookupFlags.FORCE_SVG)

        if icon_info.is_symbolic():
            return None

        # Avoid duplicate icons. It's slower, but it's better for user
        if Path(icon_info.get_filename()).is_symlink():
            return None

        try:
            pixbuf = icon_info.load_icon()

            width, height = pixbuf.get_width(), pixbuf.get_height()
            if width > 64 or height > 64:
                pixbuf = pixbuf.scale_simple(64, 64, True)

            return model.append([pixbuf, icon_name])

        except GLib.Error:
            return None

    def on_load_icons(self, widget, row):
        """ Load icons for the current selected icon context

        Parameters
        ----------
        widget : gi.repository.Gtk.ListBox
            Object which received the signal
        row : gi.repository.Gtk.ListBoxRow
            Selected listbox row
        """

        self.selected_icon = None
        self.set_response_sensitive(Gtk.ResponseType.APPLY, False)

        context = row.label_title.get_text()

        if not self.thread == 0:
            GLib.source_remove(self.thread)

        self.thread = GLib.idle_add(self.on_append_icons(context).__next__)

    def on_update_icon_selection(self, widget):
        """ Store selected icon when a new selection occurs

        Parameters
        ----------
        widget : gi.repository.Gtk.IconView
            Object which received the signal
        """

        selections = widget.get_selected_items()

        if len(selections) > 0:
            model = self.iconview_category.get_model()

            treeiter = model.get_iter(selections[0])
            if treeiter is not None:
                self.selected_icon = model.get_value(treeiter, 1)

                self.set_response_sensitive(Gtk.ResponseType.APPLY, True)
