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
from geode_gem.ui.utils import replace_for_markup
from geode_gem.ui.widgets.window import CommonWindow
from geode_gem.widgets import GeodeGtk

# GObject
from gi.repository import Gtk, Pango

# Translation
from gettext import gettext as _


class DeleteDialog(CommonWindow):

    def __init__(self, parent, game):
        """ Constructor

        Parameters
        ----------
        parent : gi.repository.Gtk.Window
            Parent object
        game : gem.engine.game.Game
            Game object
        """

        CommonWindow.__init__(self,
                              parent,
                              _("Remove a game"),
                              Icons.Symbolic.DELETE,
                              parent.use_classic_theme)

        # Application objects instances
        self.game = game

        # Initialize interface
        self.__init_widgets()
        self.__init_packing()

    def __init_widgets(self):
        """ Initialize interface widgets
        """

        self.set_size(640, 480)
        self.set_spacing(6)
        self.set_resizable(True)

        # ------------------------------------
        #   Parameters
        # ------------------------------------

        self.switch_cache = GeodeGtk.Switch()
        self.switch_database = GeodeGtk.Switch()
        self.switch_desktop = GeodeGtk.Switch()
        self.switch_memory = GeodeGtk.Switch(set_active=False)
        self.switch_savestates = GeodeGtk.Switch(set_active=False)
        self.switch_screenshots = GeodeGtk.Switch(set_active=False)

        # ------------------------------------
        #   View
        # ------------------------------------

        self.box = GeodeGtk.Box(
            GeodeGtk.Label(
                set_ellipsize=Pango.EllipsizeMode.END,
                set_halign=Gtk.Align.CENTER,
                set_markup="<span weight='bold' size='large'>%s</span>" % (
                    replace_for_markup(self.game.name)),
            ),
            GeodeGtk.Label(
                set_ellipsize=Pango.EllipsizeMode.END,
                set_justify=Gtk.Justification.CENTER,
                set_halign=Gtk.Align.CENTER,
                set_markup="%s\n%s" % (
                    _("The following game going to be removed from your "
                      "hard drive."),
                    _("This action is irreversible!")),
            ),
            GeodeGtk.StackSection(
                _("Optional data to remove"),
                GeodeGtk.Frame(
                    GeodeGtk.ScrolledWindow(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Database"),
                                self.switch_database,
                                description=_("Delete game data from database"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Menu entry"),
                                self.switch_desktop,
                                description=_("Delete desktop file"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Savestates"),
                                self.switch_savestates,
                                description=_("Delete savestates files"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Screenshots"),
                                self.switch_screenshots,
                                description=_("Delete screenshots files"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Icons cache"),
                                self.switch_cache,
                                description=_("Delete generated icons from "
                                              "cache"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Flash memory"),
                                self.switch_memory,
                                description=_("Delete flash memory file"),
                                identifier="mednafen_memory"
                            ),
                            identifier="listbox",
                        ),
                    ),
                ),
                is_expandable=True,
                is_fillable=True,
            ),
            set_border_width=18,
            set_orientation=Gtk.Orientation.VERTICAL,
            set_spacing=12,
        )

    def __init_packing(self):
        """ Initialize widgets packing in main window
        """

        self.pack_start(self.box)

        # Only show the memory section if this is a GBA game using Mednafen
        if not self.main_parent.check_gba_game_use_mednafen(self.game):
            self.box.get_widget("listbox").remove(
                self.box.get_widget("mednafen_memory"))

        self.add_button(_("No"), Gtk.ResponseType.NO)
        self.add_button(_("Yes"), Gtk.ResponseType.YES, Gtk.Align.END)

    @property
    def data(self):
        """ Retrieve user selections

        Returns
        -------
        dict
            User selections from switchs status
        """

        return {
            "cache": self.switch_cache.get_active(),
            "database": self.switch_database.get_active(),
            "desktop": self.switch_desktop.get_active(),
            "memory": self.switch_memory.get_active(),
            "savestates": self.switch_savestates.get_active(),
            "screenshots": self.switch_screenshots.get_active(),
        }
