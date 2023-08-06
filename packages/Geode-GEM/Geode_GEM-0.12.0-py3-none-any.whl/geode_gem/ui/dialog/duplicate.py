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


class DuplicateDialog(CommonWindow):

    def __init__(self, parent, game):
        """ Constructor

        Parameters
        ----------
        parent : Gtk.Window
            Parent object
        game : gem.engine.game.Game
            Game object instance
        """

        CommonWindow.__init__(self,
                              parent,
                              _("Duplicate a game"),
                              Icons.Symbolic.COPY,
                              parent.use_classic_theme)

        # Application objects instances
        self.api = parent.api
        self.game = game

        # Initialize interface
        self.__init_widgets()
        self.__init_packing()
        self.__init_signals()
        self.__init_interface()

    def __init_widgets(self):
        """ Initialize interface widgets
        """

        self.set_size(640, 480)
        self.set_spacing(6)
        self.set_resizable(True)

        # ------------------------------------
        #   Parameters
        # ------------------------------------

        self.entry_name = GeodeGtk.SearchEntry()

        self.switch_database = GeodeGtk.Switch(set_active=False)
        self.switch_savestates = GeodeGtk.Switch(set_active=False)
        self.switch_screenshots = GeodeGtk.Switch(set_active=False)
        self.switch_note = GeodeGtk.Switch(set_active=False)
        self.switch_memory = GeodeGtk.Switch(set_active=False)

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
            GeodeGtk.StackSection(
                _("New filename"),
                self.entry_name,
            ),
            GeodeGtk.StackSection(
                _("Optional data to duplicate"),
                GeodeGtk.Frame(
                    GeodeGtk.ScrolledWindow(
                        GeodeGtk.ListBox(
                            GeodeGtk.ListBoxItem(
                                _("Database"),
                                self.switch_database,
                                description=_(
                                    "Duplicate game data from database"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Savestates"),
                                self.switch_savestates,
                                description=_("Duplicate savestates files"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Screenshots"),
                                self.switch_screenshots,
                                description=_("Duplicate screenshots files"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Note"),
                                self.switch_note,
                                description=_("Duplicate game note files"),
                            ),
                            GeodeGtk.ListBoxItem(
                                _("Flash memory"),
                                self.switch_memory,
                                description=_("Duplicate flash memory files"),
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

        self.add_button(_("Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("Accept"), Gtk.ResponseType.APPLY, Gtk.Align.END)

    def __init_signals(self):
        """ Initialize widgets signals
        """

        signals = {
            self.entry_name: {
                "changed": [
                    {"method": self.on_check_filename},
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

        self.entry_name.set_text(self.game.path.stem)

    @property
    def data(self):
        """ Retrieve user selections

        Returns
        -------
        dict
            User selections from switchs status
        """

        return {
            "database": self.switch_database.get_active(),
            "memory": self.switch_memory.get_active(),
            "filename":
                f"{self.entry_name.get_text().strip()}{self.game.extension}",
            "note": self.switch_note.get_active(),
            "savestates": self.switch_savestates.get_active(),
            "screenshots": self.switch_screenshots.get_active(),
        }

    def on_check_filename(self, *args):
        """ Check filename in game folder to detect if a file already exists
        """

        icon = None
        status = True

        # Retrieve specified name
        name = self.entry_name.get_text().strip()

        if len(name) > 0:
            name += self.game.extension

            # Generate file path
            filepath = self.game.path.parent.joinpath(name)

            # Cannot replace an existing file
            if filepath.exists():
                icon = Icons.Symbolic.ERROR
                status = False

        self.entry_name.set_icon_from_icon_name(
            Gtk.EntryIconPosition.PRIMARY, icon)
        self.set_response_sensitive(Gtk.ResponseType.APPLY, status)
