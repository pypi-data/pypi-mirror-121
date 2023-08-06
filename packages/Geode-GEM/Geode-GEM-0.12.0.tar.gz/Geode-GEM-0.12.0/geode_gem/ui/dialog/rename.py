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
from gi.repository import Gtk

# Translation
from gettext import gettext as _


class RenameDialog(CommonWindow):

    def __init__(self, parent, game):
        """ Constructor

        Parameters
        ----------
        parent : Gtk.Window
            Parent object
        game : gem.api.Game
            Game object
        """

        CommonWindow.__init__(self,
                              parent,
                              _("Rename a game"),
                              Icons.Symbolic.EDITOR,
                              parent.use_classic_theme)

        # Application objects instances
        self.game = game

        # Initialize interface
        self.__init_widgets()
        self.__init_packing()
        self.__init_signals()
        self.__init_interface()

    def __init_widgets(self):
        """ Initialize interface widgets
        """

        self.set_size(520, -1)
        self.set_spacing(6)
        self.set_resizable(True)

        self.grid.set_border_width(18)

        # ------------------------------------
        #   Entry
        # ------------------------------------

        self.entry_name = GeodeGtk.SearchEntry(
            set_text=self.game.name,
            set_placeholder_text=self.game.name,
        )

    def __init_packing(self):
        """ Initialize widgets packing in main window
        """

        self.pack_start(self.entry_name, False, False)

        self.add_button(_("Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("Apply"), Gtk.ResponseType.APPLY, Gtk.Align.END)

    def __init_signals(self):
        """ Initialize widgets signals
        """

        signals = {
            self.entry_name: {
                "activate": [
                    {"method": self.validate_name},
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

        self.set_default_response(Gtk.ResponseType.APPLY)

    @property
    def data(self):
        """ Retrieve user selections

        Returns
        -------
        dict
            User selections from switchs status
        """

        name = self.entry_name.get_text().strip()

        return {
            "name": name if len(name) > 0 else self.game.path.name,
        }

    def validate_name(self, *args):
        """ Validate the new name by using the Return key
        """

        self.emit_response(None, Gtk.ResponseType.APPLY)
