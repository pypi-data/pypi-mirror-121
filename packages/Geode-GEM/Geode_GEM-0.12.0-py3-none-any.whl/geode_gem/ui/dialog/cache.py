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


class CleanCacheDialog(CommonWindow):

    def __init__(self, parent):
        """ Constructor

        Parameters
        ----------
        parent : Gtk.Window
            Parent object
        """

        CommonWindow.__init__(self,
                              parent,
                              _("Rebuild icons cache"),
                              Icons.Symbolic.FOLDER,
                              parent.use_classic_theme)

        # Initialize interface
        self.__init_widgets()
        self.__init_packing()

    def __init_widgets(self):
        """ Initialize interface widgets
        """

        self.set_size(640, -1)
        self.set_spacing(6)
        self.set_resizable(True)

        # ------------------------------------
        #   Labels
        # ------------------------------------

        self.box = GeodeGtk.Box(
            GeodeGtk.Label(
                set_ellipsize=Pango.EllipsizeMode.END,
                set_markup="<span weight='bold' size='large'>%s</span>" % (
                    _("Do you really want to rebuild the icons cache "
                      "directory?")),
            ),
            GeodeGtk.Label(
                set_ellipsize=Pango.EllipsizeMode.END,
                set_text=_("This action will ensure to remove icons which are "
                           "no longer used."),
                set_style=Gtk.STYLE_CLASS_DIM_LABEL,
            ),
            set_border_width=18,
            set_orientation=Gtk.Orientation.VERTICAL,
            set_spacing=12,
        )

    def __init_packing(self):
        """ Initialize widgets packing in main window
        """

        self.pack_start(self.box, False, False)

        self.add_button(_("No"), Gtk.ResponseType.NO)
        self.add_button(_("Yes"), Gtk.ResponseType.YES, Gtk.Align.END)
