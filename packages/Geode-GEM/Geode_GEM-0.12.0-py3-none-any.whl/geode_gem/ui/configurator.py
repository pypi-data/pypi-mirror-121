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
from geode_gem.engine.utils import generate_identifier

from geode_gem.ui.data import Icons
from geode_gem.ui.dialog.filechooser import FileChooserDialog
from geode_gem.ui.dialog.icons import IconsDialog
from geode_gem.ui.utils import get_filename_from_icon_theme, magic_from_file
from geode_gem.ui.widgets.window import CommonWindow
from geode_gem.widgets import GeodeGtk

# GObject
from gi.repository import Gdk, GdkPixbuf, GObject, Gtk

# Translation
from gettext import gettext as _

# URL
from urllib.parse import urlparse
from urllib.request import url2pathname


class Configurator(CommonWindow):

    __missing_icon__ = Icons.MISSING

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        CommonWindow.__init__(self, *args, **kwargs)

        # Store apply button status
        self.__status = False

    def init_common_widgets(self):
        """ Initialize common widgets
        """

        self.entry_name = GeodeGtk.SearchEntry(
            GeodeGtk.EntryIcon(Gtk.EntryIconPosition.PRIMARY, None),
            identifier="name",
            is_expandable=True,
            is_fillable=True,
            set_hexpand=True,
        )

        self.entry_thumbnail = GeodeGtk.SearchEntry(
            GeodeGtk.EntryIcon(Gtk.EntryIconPosition.PRIMARY, None),
            identifier="thumbnail",
            is_expandable=True,
            is_fillable=True,
            set_hexpand=True,
            set_placeholder_text=_("Absolute path to the icon thumbnail"),
            set_tooltip_text=_("Absolute path to the icon thumbnail"),
        )

        self.entry_thumbnail.drag_dest_set(
            Gtk.DestDefaults.ALL, list(), Gdk.DragAction.COPY)
        self.entry_thumbnail.drag_dest_add_uri_targets()

        self.button_filechooser = GeodeGtk.Button(
            label=_("Game icon thumbnail"),
            icon_name=Icons.Symbolic.FOLDER,
            icon_size=Gtk.IconSize.BUTTON,
        )

        self.button_filechooser.drag_dest_set(
            Gtk.DestDefaults.ALL, list(), Gdk.DragAction.COPY)
        self.button_filechooser.drag_dest_add_uri_targets()

        self.button_thumbnail = GeodeGtk.Button(
            label=_("Icons browser"),
            icon_name=self.__missing_icon__,
            icon_size=Gtk.IconSize.DND,
            set_size_request=(64, 64),
        )

        self.button_thumbnail.image.set_size_request(64, 64)

        self.button_thumbnail.drag_dest_set(
            Gtk.DestDefaults.ALL, list(), Gdk.DragAction.COPY)
        self.button_thumbnail.drag_dest_add_uri_targets()

        self.filechooser_thumbnail = FileChooserDialog(
            _("Choose a file path for icon thumbnail"),
            self.main_parent,
            Gtk.FileChooserAction.OPEN,
            _("Select"),
            _("Cancel"),
        )

    @property
    def default_signals(self):
        """ Define common signals
        """

        return {
            self.button_filechooser: {
                "clicked": [
                    {"method": self.on_show_thumbnail_file_chooser_dialog},
                ],
                "drag-data-received": [
                    {"method": self.on_drag_and_drop_filepath},
                ],
            },
            self.button_thumbnail: {
                "clicked": [
                    {"method": self.on_show_icons_browser_dialog},
                ],
                "drag-data-received": [
                    {"method": self.on_drag_and_drop_filepath},
                ],
            },
            self.entry_name: {
                "changed": [
                    {"method": self.on_update_name_entry},
                ],
            },
            self.entry_thumbnail: {
                "changed": [
                    {"method": self.on_update_thumbnail_entry},
                ],
                "drag-data-received": [
                    {"method": self.on_drag_and_drop_filepath},
                ],
            },
        }

    def get_filename_from_icon_theme(self, name, size=64):
        """ Retrieve filepath from a specific name in icon theme

        Parameters
        ----------
        name : str
            Icon name to search in icon theme
        size : int, optional
            Icon size in pixels (Default: 64)

        Returns
        -------
        str or None
            Icon filepath if found, None otherwise
        """

        return get_filename_from_icon_theme(
            self.main_parent.icons_theme, name, size)

    def on_drag_and_drop_filepath(self, widget,
                                  context, x, y, data, info, delta):
        """ Retrieve image file from an external application

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

        filepath = None
        for uri in data.get_uris():

            result = urlparse(uri)
            if not result.scheme == "file":
                continue

            path = Path(url2pathname(result.path)).expanduser()
            if path is not None and path.exists() and \
               magic_from_file(path, mime=True).startswith("image/"):
                # No needs to go futher, we have an image
                filepath = str(path)
                break

        if filepath is not None:
            self.entry_thumbnail.set_text(filepath)

    def on_show_icons_browser_dialog(self, *args):
        """ Show the icons theme collection dialog
        """

        self.window.set_sensitive(False)

        icon_name = self.entry_thumbnail.get_text()
        if len(icon_name) == 0:
            icon_name = None

        dialog = IconsDialog(self)

        selected_icon = None
        if dialog.run() == Gtk.ResponseType.APPLY:
            selected_icon = dialog.selected_icon

        dialog.destroy()

        if selected_icon is not None:
            self.entry_thumbnail.set_text(selected_icon)

        self.window.set_sensitive(True)

    def on_show_thumbnail_file_chooser_dialog(self, *args):
        """ Show the file chooser dialog when icon thumbnail button was clicked
        """

        icon = self.entry_thumbnail.get_text()

        # Check if icon is available in icons theme if filepath not exists
        if not Path(icon).expanduser().exists():
            icon = self.get_filename_from_icon_theme(icon)

        if icon is not None and len(icon) > 0:
            self.filechooser_thumbnail.dialog.set_filename(
                str(Path(icon).expanduser()))

        self.window.set_sensitive(False)

        if self.filechooser_thumbnail.dialog.run() == Gtk.ResponseType.ACCEPT:
            self.path = Path(
                self.filechooser_thumbnail.dialog.get_filename()).expanduser()

            self.entry_thumbnail.set_text(str(self.path))

        self.window.set_sensitive(True)

    def on_update_name_entry(self, widget, elements, element):
        """ Check if a value is not already used

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        elements : dict
            API objects as dictionary storage
        element : geode_gem.engine.console.Console or
                  geode_gem.engine.emulator.Emulator
            API object to check from elements storage
        """

        icon = None
        tooltip = None

        name = self.entry_name.get_text()

        self.__status = len(name) > 0

        if self.__status:
            name = generate_identifier(name)

            # Check if current object exists in database
            if name in elements:

                if element is None:
                    self.__status = False

                # Avoid to use a name which already exists in database
                elif not element.id == name:
                    self.__status = False

                if not self.__status:
                    icon = Icons.ERROR
                    tooltip = _("This name has already been taken")

        self.set_response_sensitive(Gtk.ResponseType.APPLY, self.__status)

        self.entry_name.set_icon_from_icon_name(
            Gtk.EntryIconPosition.PRIMARY, icon)
        self.entry_name.set_tooltip_text(tooltip)

    def on_update_thumbnail_entry(self, widget):
        """ Update thumbnail image from entry text content

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        text = widget.get_text()

        self.set_thumbnail_image_from_path(
            None if len(text) == 0 else Path(text).expanduser())

    def set_thumbnail_image_from_path(self, path):
        """ Define thumbnail button image from a specific path

        Parameters
        ----------
        path : pathlib.Path or None
            Image path object
        """

        if path is not None:

            # Check if icon is available in icons theme if filepath not exists
            if not path.exists():
                filename = self.get_filename_from_icon_theme(str(path))

                if filename is not None:
                    path = Path(filename).expanduser()

            if path.exists():
                try:
                    if magic_from_file(path, mime=True).startswith("image/"):
                        self.button_thumbnail.image.set_from_pixbuf(
                            GdkPixbuf.Pixbuf.new_from_file_at_scale(
                                str(path.expanduser()), 64, 64, True))
                        return True

                except Exception:
                    pass

        self.button_thumbnail.image.set_from_icon_name(
            self.__missing_icon__, Gtk.IconSize.DND)

        return False
