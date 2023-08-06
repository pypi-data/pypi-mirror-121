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
from geode_gem.ui.widgets.window import CommonWindow
from geode_gem.widgets import GeodeGtk

# GObject
from gi.repository import Gtk, Pango

# Translation
from gettext import gettext as _


class MessageDialog(CommonWindow):

    def __init__(self, parent, title, message, icon, center=True):
        """ Constructor

        Parameters
        ----------
        parent : Gtk.Window
            Parent object
        title : str
            Dialog title
        message : str
            Dialog message
        icon : str
            Default icon name
        center : bool, optional
            If False, use justify text insted of center (Default: True)
        """

        CommonWindow.__init__(self,
                              parent,
                              title,
                              icon,
                              parent.use_classic_theme)

        # Message variables
        self.message = message
        self.center = center

        # Initialize interface
        self.__init_widgets()
        self.__init_packing()

    def __init_widgets(self):
        """ Initialize interface widgets
        """

        self.set_size(480, -1)
        self.set_spacing(6)
        self.set_resizable(True)

        self.grid.set_border_width(18)

        # ------------------------------------
        #   Label
        # ------------------------------------

        self.label = GeodeGtk.Label(
            set_justify=(Gtk.Justification.CENTER if self.center
                         else Gtk.Justification.FILL),
            set_label=self.message,
            set_line_wrap=True,
            set_line_wrap_mode=Pango.WrapMode.WORD,
        )

    def __init_packing(self):
        """ Initialize widgets packing in main window
        """

        self.pack_start(self.label, True, True)

        self.add_button(_("Close"), Gtk.ResponseType.CLOSE, Gtk.Align.END)
