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
from geode_gem.widgets import GeodeGtk

# GObject
from gi.repository import GdkPixbuf, Gtk


class FileChooserDialog:

    def __init__(self, *args):
        """ Constructor
        """

        # Related FileChooserNative arguments
        self.filechooser_arguments = args

        # Initialize interface
        self.__init_widgets()
        self.__init_signals()

    def __init_widgets(self):
        """ Initialize interface widgets
        """

        self.file_filter = Gtk.FileFilter.new()
        self.file_filter.add_mime_type("image/*")

        self.dialog = Gtk.FileChooserNative.new(*self.filechooser_arguments)

        self.dialog.set_filter(self.file_filter)
        self.dialog.set_preview_widget(
            GeodeGtk.Image(set_size_request=(256, 256)))
        self.dialog.set_preview_widget_active(False)
        self.dialog.set_select_multiple(False)
        self.dialog.set_use_preview_label(False)

    def __init_signals(self):
        """ Initialize widgets signals
        """

        self.dialog.connect(
            "update-preview", self.on_update_file_chooser_preview)

    def on_update_file_chooser_preview(self, widget):
        """ Update thumbnail image from entry text content

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        pixbuf = None

        filename = widget.get_preview_filename()
        if filename is not None:

            path = Path(filename).expanduser()
            if path.exists() and path.is_file():
                try:
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        str(path), 200, 200, True)

                except Exception:
                    pass

        widget.get_preview_widget().set_from_pixbuf(pixbuf)
        widget.set_preview_widget_active(pixbuf is not None)
