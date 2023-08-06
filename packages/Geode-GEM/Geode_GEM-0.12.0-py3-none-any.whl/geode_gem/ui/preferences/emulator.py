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

# GEM
from geode_gem.engine.emulator import Emulator
from geode_gem.engine.utils import get_binary_path, generate_identifier

from geode_gem.ui.data import Icons
from geode_gem.ui.configurator import Configurator
from geode_gem.widgets import GeodeGtk

# GObject
from gi.repository import Gtk

# Translation
from gettext import gettext as _


class EmulatorPreferences(Configurator):

    __help__ = {
        "order": [
            _("Description"),
            _("Parameters"),
        ],
        _("Description"): [
            _("To facilitate file detection with every emulators, some "
              "custom parameters have been created."),
            _("These parameters are used in \"Default options\", \"Save\" "
              "and \"Snapshots\" entries."),
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

    def __init__(self, parent, emulator, emulators, size):
        """ Constructor

        Parameters
        ----------
        parent : Gtk.Window
            Parent object
        emulator : geode_gem.engine.emulator.Emulator
            Selected Emulator object
        emulators : list
            Emulators object list
        size : tuple
            Window dialog size as integer's tuple
        """

        Configurator.__init__(self,
                              parent,
                              _("Emulator"),
                              Icons.Symbolic.PROPERTIES,
                              parent.use_classic_theme)

        # Application objects instances
        self.api = parent.api
        self.config = parent.config
        self.emulators = emulators

        # Emulator object
        self.emulator = emulator

        # Dialog window size
        self.__size = size

        # Initialize interface
        self.__init_widgets()
        self.__init_packing()
        self.__init_signals()
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

        self.entry_name.set_tooltip_text(_("Emulator name"))

        self.filechooser_binary = GeodeGtk.FileChooserButton(
            _("Emulator binary file"),
            Gtk.FileChooserAction.OPEN,
            is_expandable=True,
            is_fillable=True,
        )

        self.filefilter_binary = Gtk.FileFilter.new()
        self.filefilter_binary.add_mime_type("application/x-executable")
        self.filechooser_binary.set_filter(self.filefilter_binary)

        self.button_reset_binary = GeodeGtk.Button(
            label=_("Reset selected executable file"),
            icon_name=Icons.Symbolic.CLEAR,
            icon_size=Gtk.IconSize.BUTTON,
        )

        self.filechooser_configuation = GeodeGtk.FileChooserButton(
            _("Emulator configuration file"),
            Gtk.FileChooserAction.OPEN,
            is_expandable=True,
            is_fillable=True,
        )

        self.filefilter_configuation = Gtk.FileFilter.new()
        self.filefilter_configuation.add_mime_type("text/*")
        self.filechooser_configuation.set_filter(self.filefilter_configuation)

        self.button_reset_configuration = GeodeGtk.Button(
            label=_("Reset selected configuration file"),
            icon_name=Icons.Symbolic.CLEAR,
            icon_size=Gtk.IconSize.BUTTON,
        )

        self.entry_arguments_default = GeodeGtk.SearchEntry(
            GeodeGtk.EntryIcon(Gtk.EntryIconPosition.PRIMARY, None),
            identifier="default",
            is_expandable=True,
            is_fillable=True,
            set_hexpand=True,
            set_placeholder_text=_("No argument"),
        )

        self.entry_arguments_windowed = GeodeGtk.SearchEntry(
            GeodeGtk.EntryIcon(Gtk.EntryIconPosition.PRIMARY, None),
            identifier="windowed",
            is_expandable=True,
            is_fillable=True,
            set_hexpand=True,
            set_placeholder_text=_("No argument"),
        )

        self.entry_arguments_fullscreen = GeodeGtk.SearchEntry(
            GeodeGtk.EntryIcon(Gtk.EntryIconPosition.PRIMARY, None),
            identifier="fullscreen",
            is_expandable=True,
            is_fillable=True,
            set_hexpand=True,
            set_placeholder_text=_("No argument"),
        )

        # ----------------------------------------
        #   Files
        # ----------------------------------------

        self.entry_files_savestates = GeodeGtk.SearchEntry(
            GeodeGtk.EntryIcon(Gtk.EntryIconPosition.PRIMARY, None),
            identifier="savestates",
            is_expandable=True,
            is_fillable=True,
            set_hexpand=True,
            set_margin_bottom=12,
            set_placeholder_text=_("No pattern for savestate files detection"),
        )

        self.entry_files_screenshots = GeodeGtk.SearchEntry(
            GeodeGtk.EntryIcon(Gtk.EntryIconPosition.PRIMARY, None),
            identifier="screenshots",
            is_expandable=True,
            is_fillable=True,
            set_hexpand=True,
            set_margin_bottom=12,
            set_placeholder_text=_("No pattern for screenshot files detection"),
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
                        self.button_thumbnail, left=2, top=0, width=1, height=2,
                    ),
                    set_row_spacing=6,
                    set_column_spacing=12,
                    set_column_homogeneous=False,
                    set_margin_bottom=18,
                ),
                GeodeGtk.StackSection(
                    _("Emulator"),
                    GeodeGtk.Frame(
                        GeodeGtk.ScrolledWindow(
                            GeodeGtk.ListBox(
                                GeodeGtk.ListBoxItem(
                                    _("Executable"),
                                    GeodeGtk.Box(
                                        self.filechooser_binary,
                                        self.button_reset_binary,
                                        is_expandable=True,
                                        is_fillable=True,
                                        set_spacing=6,
                                    ),
                                    description=_(
                                        "Selected binary must be executable"),
                                    homogeneous=True,
                                ),
                                GeodeGtk.ListBoxItem(
                                    _("Configuration file"),
                                    GeodeGtk.Box(
                                        self.filechooser_configuation,
                                        self.button_reset_configuration,
                                        is_expandable=True,
                                        is_fillable=True,
                                        set_spacing=6,
                                    ),
                                    homogeneous=True,
                                ),
                            ),
                            set_policy=(
                                Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER),
                        ),
                    ),
                ),
                GeodeGtk.StackSection(
                    _("Arguments"),
                    GeodeGtk.Frame(
                        GeodeGtk.ScrolledWindow(
                            GeodeGtk.ListBox(
                                GeodeGtk.ListBoxItem(
                                    _("Default"),
                                    self.entry_arguments_default,
                                    description=_(
                                        "Add when launching emulator"),
                                    homogeneous=True,
                                ),
                                GeodeGtk.ListBoxItem(
                                    _("Windowed"),
                                    self.entry_arguments_windowed,
                                    description=_("Activate windowed mode"),
                                    homogeneous=True,
                                ),
                                GeodeGtk.ListBoxItem(
                                    _("Fullscreen"),
                                    self.entry_arguments_fullscreen,
                                    description=_("Activate fullscreen mode"),
                                    homogeneous=True,
                                ),
                            ),
                            set_policy=(
                                Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER),
                        ),
                    ),
                ),
            ),
            GeodeGtk.StackView(
                _("Files"),
                GeodeGtk.StackSection(
                    _("Patterns"),
                    GeodeGtk.Label(
                        set_text=_(
                            "These patterns are used to detect specific files "
                            "for a game. You can check the help button to "
                            "have more information about available pattern "
                            "helpers."),
                        set_halign=Gtk.Align.START,
                        set_valign=Gtk.Align.CENTER,
                        set_margin_bottom=12,
                        set_line_wrap=True,
                    ),
                    GeodeGtk.Box(
                        GeodeGtk.Image(
                            set_from_icon_name=(
                                Icons.FLOPPY, Gtk.IconSize.MENU),
                        ),
                        GeodeGtk.Label(
                            is_expandable=True,
                            is_fillable=True,
                            set_markup="<b>%s</b>" % _("Savestates"),
                            set_halign=Gtk.Align.START,
                            set_valign=Gtk.Align.CENTER,
                        ),
                        set_spacing=6,
                    ),
                    self.entry_files_savestates,
                    GeodeGtk.Box(
                        GeodeGtk.Image(
                            set_from_icon_name=(
                                Icons.IMAGE, Gtk.IconSize.MENU),
                        ),
                        GeodeGtk.Label(
                            set_markup="<b>%s</b>" % _("Screenshots"),
                            set_halign=Gtk.Align.START,
                            set_valign=Gtk.Align.CENTER,
                        ),
                        set_spacing=6,
                    ),
                    self.entry_files_screenshots,
                    GeodeGtk.Label(
                        set_markup="<i>%s</i>" % _("* can be used as joker"),
                        set_halign=Gtk.Align.END,
                        set_valign=Gtk.Align.CENTER,
                        set_style=Gtk.STYLE_CLASS_DIM_LABEL,
                        set_use_markup=True,
                    ),
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
            self.button_reset_binary: {
                "clicked": [
                    {"method": self.on_reset_filechooser},
                ],
            },
            self.button_reset_configuration: {
                "clicked": [
                    {"method": self.on_reset_filechooser},
                ],
            },
        }

        signals |= self.default_signals

        # Connect widgets
        self.main_parent.load_signals(signals)
        # Remove signals storage from memory
        del signals

    def __init_interface(self):
        """ Initialize and fill interface widgets
        """

        # Filling not needed with new emulator
        if self.emulator is None or self.emulator.id is None:
            return

        self.entry_name.set_text(self.emulator.name)
        self.entry_name.set_placeholder_text(self.emulator.name),

        # Binary
        binary = self.emulator.binary
        if binary is not None and not binary.exists():
            binary = next(
                (Path(item) for item in get_binary_path(str(binary))), None)

        if binary is not None:
            self.filechooser_binary.set_filename(str(binary))

        if self.emulator.configuration is not None:
            self.filechooser_configuation.set_filename(
                str(self.emulator.configuration))

        if self.emulator.icon is not None:
            self.entry_thumbnail.set_text(str(self.emulator.icon))

        # File detection patterns
        if self.emulator.savestates is not None:
            self.entry_files_savestates.set_text(
                str(self.emulator.savestates))
        if self.emulator.screenshots is not None:
            self.entry_files_screenshots.set_text(
                str(self.emulator.screenshots))

        # Emulator arguments
        if self.emulator.default is not None:
            self.entry_arguments_default.set_text(self.emulator.default)
        if self.emulator.windowed is not None:
            self.entry_arguments_windowed.set_text(self.emulator.windowed)
        if self.emulator.fullscreen is not None:
            self.entry_arguments_fullscreen.set_text(self.emulator.fullscreen)

    def on_reset_filechooser(self, widget):
        """ Reset a specific filechooser button widget

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        if widget == self.button_reset_binary:
            self.filechooser_binary.set_filename(str())

        elif widget == self.button_reset_configuration:
            self.filechooser_configuation.set_filename(str())

    def on_update_name_entry(self, widget):
        """ Check if a value is not already used

        Parameters
        ----------
        widget : Gtk.Widget
            Object which receive signal
        """

        Configurator.on_update_name_entry(
            self, widget, self.emulators, self.emulator)

    def save(self):
        """ Save modification
        """

        name = self.entry_name.get_text().strip()
        if len(name) == 0:
            raise ValueError("Cannot save an emulator with an empty name")

        emulator = Emulator(
            id=generate_identifier(name),
            name=name,
            binary=self.filechooser_binary.get_filename(),
            configuration=self.filechooser_configuation.get_filename(),
            default=self.entry_arguments_default.get_text().strip(),
            windowed=self.entry_arguments_windowed.get_text().strip(),
            fullscreen=self.entry_arguments_fullscreen.get_text().strip(),
        )

        icon = self.entry_thumbnail.get_text().strip()
        if len(icon) > 0:
            emulator.icon = Path(icon).expanduser()

        savestates = self.entry_files_savestates.get_text().strip()
        if len(savestates) > 0:
            emulator.savestates = Path(savestates).expanduser()

        screenshots = self.entry_files_screenshots.get_text().strip()
        if len(screenshots) > 0:
            emulator.screenshots = Path(screenshots).expanduser()

        return emulator
