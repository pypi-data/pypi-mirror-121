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
from geode_gem.ui.data import Icons
from geode_gem.ui.utils import PixbufSize
from geode_gem.ui.widgets.window import CommonWindow
from geode_gem.widgets import GeodeGtk

# GObject
from gi.repository import Gdk, GdkPixbuf, GLib, Gtk

# Translation
from gettext import gettext as _

# Typing
from typing import Tuple


class ViewerDialog(CommonWindow):
    """ Geode-GEM screenshot files viewer dialog class

    Attributes
    ----------
    config :
    screenshots : list

    See Also
    --------
    geode_gem.ui.widgets.window.CommonWindow
    """

    DEFAULT_IMAGE_SIZE = 800

    STARTING_ZOOM = 200
    MAXIMAL_ZOOM = 400
    MINIMAL_ZOOM = 10

    PAGE_INCREMENT = 10
    STEP_INCREMENT = 5

    def __init__(self, parent: Gtk.Window, title: str, size: [int, int],
                 screenshots_path: list):
        """ Constructor

        Parameters
        ----------
        parent : gi.repository.Gtk.Window
            Parent object
        title : str
            Dialog title
        size : (int, int)
            Dialog size as (width, height) tuple
        screenshots_path : list
            Screnshots path list
        """

        CommonWindow.__init__(self,
                              parent,
                              title,
                              Icons.IMAGE,
                              parent.use_classic_theme)

        self.config = parent.config

        # Dialog window size
        self.__size = size

        # Screenshot files path
        self.screenshots = screenshots_path

        # Screenshot related variables
        self.__index = int()
        self.__path = None
        self.__pixbuf = None

        # Zoom related variables
        self.__actual_zoom = 100
        self.__actual_mode = "fit"

        # Initialize interface
        self.__init_widgets()
        self.__init_packing()
        self.__init_signals()
        self.__init_interface()

    def __init_widgets(self):
        """ Initialize interface widgets
        """

        self.set_size(*self.__size)
        self.set_spacing(0)
        self.set_resizable(True)

        self.grid_tools.set_border_width(6)

        # ------------------------------------
        #   Parameters
        # ------------------------------------

        # Get default display
        self.display = Gdk.Display.get_default()

        if self.display is not None:
            # Retrieve default display monitor
            self.monitor = self.display.get_primary_monitor()
            # Retrieve default monitor geometry
            self.geometry = self.monitor.get_geometry()

            self.__default_size = min(
                int(self.geometry.width / 2), int(self.geometry.height / 2))

        # ------------------------------------
        #   Overlay
        # ------------------------------------

        self.viewport = GeodeGtk.Viewport(
            GeodeGtk.Image(
                identifier="image",
            ),
        )
        self.viewport.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, list(),
                                      Gdk.DragAction.COPY)
        self.viewport.drag_source_add_uri_targets()

        self.overlay = GeodeGtk.Overlay(
            GeodeGtk.ScrolledWindow(
                self.viewport,
                identifier="scroll",
            ),
        )

        self.button_overlay_previous = GeodeGtk.Button(
            _("Previous screenshot"),
            icon_name=Icons.Symbolic.PREVIOUS,
            icon_size=Gtk.IconSize.BUTTON,
            identifier="overlay_previous",
            set_halign=Gtk.Align.START,
            set_margin_bottom=6,
            set_margin_end=6,
            set_margin_start=6,
            set_margin_top=6,
            set_no_show_all=True,
            set_style=Gtk.STYLE_CLASS_OSD,
            set_valign=Gtk.Align.CENTER,
        )

        self.button_overlay_next = GeodeGtk.Button(
            _("Next screenshot"),
            icon_name=Icons.Symbolic.NEXT,
            icon_size=Gtk.IconSize.BUTTON,
            identifier="overlay_next",
            set_halign=Gtk.Align.END,
            set_margin_bottom=6,
            set_margin_end=6,
            set_margin_start=6,
            set_margin_top=6,
            set_no_show_all=True,
            set_style=Gtk.STYLE_CLASS_OSD,
            set_valign=Gtk.Align.CENTER,
        )

        # ------------------------------------
        #   Toolbar
        # ------------------------------------

        self.toolbar_resize = GeodeGtk.Box(
            GeodeGtk.Button(
                _("Zoom fit"),
                icon_name=Icons.Symbolic.ZOOM_FIT,
                icon_size=Gtk.IconSize.BUTTON,
                identifier="fit",
            ),
            GeodeGtk.Button(
                _("Original size"),
                icon_name=Icons.Symbolic.ZOOM,
                icon_size=Gtk.IconSize.BUTTON,
                identifier="original",
            ),
            merge=True,
        )

        self.toolbar_move = GeodeGtk.Box(
            GeodeGtk.Button(
                _("First screenshot"),
                icon_name=Icons.Symbolic.FIRST,
                icon_size=Gtk.IconSize.BUTTON,
                identifier="first",
            ),
            GeodeGtk.Button(
                _("Previous screenshot"),
                icon_name=Icons.Symbolic.PREVIOUS,
                icon_size=Gtk.IconSize.BUTTON,
                identifier="previous",
            ),
            GeodeGtk.Button(
                _("Next screenshot"),
                icon_name=Icons.Symbolic.NEXT,
                icon_size=Gtk.IconSize.BUTTON,
                identifier="next",
            ),
            GeodeGtk.Button(
                _("Last screenshot"),
                icon_name=Icons.Symbolic.LAST,
                icon_size=Gtk.IconSize.BUTTON,
                identifier="last",
            ),
            merge=True,
        )

        self.scale_zoom = GeodeGtk.Scale(
            GeodeGtk.Adjustment(
                set_lower=self.MINIMAL_ZOOM,
                set_upper=self.MAXIMAL_ZOOM,
                set_step_increment=self.STEP_INCREMENT,
                set_page_increment=self.PAGE_INCREMENT,
            ),
            marks=[
                (self.MINIMAL_ZOOM, Gtk.PositionType.BOTTOM, None),
                (self.STARTING_ZOOM, Gtk.PositionType.BOTTOM, None),
                (self.MAXIMAL_ZOOM, Gtk.PositionType.BOTTOM, None),
            ],
            set_draw_value=False,
            set_size_request=(150, -1),
        )

    def __init_packing(self):
        """ Initialize widgets packing in main window
        """

        self.overlay.add_overlay(self.button_overlay_previous)
        self.overlay.add_overlay(self.button_overlay_next)

        self.pack_start(self.overlay, True, True, 0)

        self.add_widget(self.toolbar_move)
        self.add_widget(self.toolbar_resize, Gtk.Align.END)
        self.add_widget(self.scale_zoom, Gtk.Align.END)

    def __init_signals(self):
        """ Initialize widgets signals
        """

        signals = {
            self.button_overlay_next: {
                "clicked": [
                    {"method": self.on_button_click_event},
                ],
            },
            self.button_overlay_previous: {
                "clicked": [
                    {"method": self.on_button_click_event},
                ],
            },
            self.scale_zoom: {
                "change_value": [
                    {"method": self.on_update_adjustment},
                ],
            },
            self.toolbar_move: {
                "clicked": [
                    {
                        "method": self.on_button_click_event,
                        "widget": "first",
                    },
                    {
                        "method": self.on_button_click_event,
                        "widget": "previous",
                    },
                    {
                        "method": self.on_button_click_event,
                        "widget": "next",
                    },
                    {
                        "method": self.on_button_click_event,
                        "widget": "last",
                    },
                ],
            },
            self.toolbar_resize: {
                "clicked": [
                    {
                        "method": self.on_button_click_event,
                        "widget": "fit",
                    },
                    {
                        "method": self.on_button_click_event,
                        "widget": "original",
                    },
                ],
            },
            self.viewport: {
                "drag-data-get": [
                    {"method": self.on_dnd_send_data},
                ],
            },
            self.window: {
                "key-press-event": [
                    {"method": self.on_key_press_event},
                ],
            },
        }

        # Allow the picture to autosize (with zoom_fit) when resize dialog
        if self.config.getboolean("viewer", "auto_resize", fallback=False):
            signals[self.window]["size-allocate"] = {
                "method": self.update_screenshot
            }

        # Connect widgets
        self.main_parent.load_signals(signals)
        # Remove signals storage from memory
        del signals

    def __init_interface(self):
        """ Load data and start interface
        """

        self.show_all()

        self.on_update_screenshot()

    def generate_pixbuf_from_filename(self, path: Path) -> GdkPixbuf.Pixbuf:
        """ Generate a Pixbuf instance from a specific file path

        This method use a cache to avoid regenerating the same file each time
        the zoom level change.

        Parameters
        ----------
        path : pathlib.Path
            File path object on user filesystem

        Returns
        -------
        GdkPixbuf.Pixbuf
            Generated Pixbuf from specified file path
        """

        if str(path) == str(self.__path) and \
           isinstance(self.__pixbuf, GdkPixbuf.Pixbuf):
            return self.__pixbuf

        try:
            self.__pixbuf = GdkPixbuf.Pixbuf.new_from_file(str(path))
            self.__path = path

            self.set_subtitle(str(path))

        except GLib.Error:
            self.__pixbuf = None
            self.__path = None

            self.set_subtitle(str())

        return self.__pixbuf

    def on_button_click_event(self, widget: Gtk.Widget):
        """ Manage button events

        Parameters
        ----------
        widget : gi.repository.Gtk.Widget
            Object which receive signal
        """

        if widget.identifier == "original":
            self.__actual_mode = "original"

        elif widget.identifier == "fit":
            self.__actual_mode = "fit"

        elif widget.identifier == "first":
            self.__index = 0

        elif widget.identifier in ("overlay_previous", "previous"):
            self.__index -= 1

        elif widget.identifier in ("overlay_next", "next"):
            self.__index += 1

        elif widget.identifier == "last":
            self.__index = len(self.screenshots) - 1

        self.on_update_screenshot()

    def on_dnd_send_data(self, widget: Gtk.Widget, context: Gdk.DragContext,
                         data: Gtk.SelectionData, info: int, time: int):
        """ Set screenshot file path uri

        This function send rom file path uri when user drag a game from gem and
        drop it to extern application

        Parameters
        ----------
        widget : gi.repository.Gtk.Widget
            Object which receive signal
        context : gi.repository.Gdk.DragContext
            Drag context
        data : gi.repository.Gtk.SelectionData
            Received data
        info : int
            Info that has been registered with the target in the Gtk.TargetList
        time : int
            Timestamp at which the data was received
        """

        if self.__path is not None and self.__path.exists():
            data.set_uris(["file://%s" % str(self.__path)])

    def on_key_press_event(self, widget: Gtk.Widget, event: Gdk.EventKey):
        """ Manage user keys

        Parameters
        ----------
        widget : gi.repository.Gtk.Widget
            Object which receive signal
        event : gi.repository.Gdk.EventKey, default: None
            Event which triggered this signal
        """

        if event.keyval == Gdk.KEY_Left:
            self.__index -= 1

        elif event.keyval == Gdk.KEY_Right:
            self.__index += 1

        elif event.keyval == Gdk.KEY_KP_Subtract:
            self.__actual_mode = None
            self.__actual_zoom -= self.STEP_INCREMENT

        elif event.keyval == Gdk.KEY_KP_Add:
            self.__actual_mode = None
            self.__actual_zoom += self.STEP_INCREMENT

        self.on_update_screenshot()

    def on_update_adjustment(self, widget: Gtk.Widget, scroll: Gtk.ScrollType,
                             value: float):
        """ Change current screenshot size

        Parameters
        ----------
        widget : gi.repository.Gtk.Widget
            Object which receive signal
        scroll : gi.repository.Gtk.ScrollType
            Type of scroll action that was performed
        value : float
            New value resulting from the scroll action
        """

        self.__actual_mode = None
        self.__actual_zoom = int(value)

        self.on_update_screenshot()

    def on_update_screenshot(self):
        """ Clean index and actual_zoom attributes before showing screenshot
        """

        if self.__index < 0:
            self.__index = 0
        elif self.__index > len(self.screenshots) - 1:
            self.__index = len(self.screenshots) - 1

        if self.__actual_zoom < self.MINIMAL_ZOOM:
            self.__actual_zoom = self.MINIMAL_ZOOM
        elif self.__actual_zoom > self.MAXIMAL_ZOOM:
            self.__actual_zoom = self.MAXIMAL_ZOOM

        self.update_screenshot()
        self.set_widgets_sensitive()

    def set_widgets_sensitive(self):
        """ Refresh interface's widgets
        """

        max_size = len(self.screenshots) - 1

        self.toolbar_move.set_sensitive(self.__index > 0, widget="first")
        self.toolbar_move.set_sensitive(self.__index > 0, widget="previous")
        self.toolbar_move.set_sensitive(self.__index < max_size, widget="next")
        self.toolbar_move.set_sensitive(self.__index < max_size, widget="last")

        self.button_overlay_previous.set_visible(self.__index > 0)
        self.button_overlay_previous.image.set_visible(self.__index > 0)

        self.button_overlay_next.set_visible(self.__index < max_size)
        self.button_overlay_next.image.set_visible(self.__index < max_size)

    @property
    def scroll_allocation(self) -> Tuple[int, int]:
        """ Retrieve overlay scrolledwindow widget allocation size

        Returns
        -------
        tuple
            Overlay scrolledwindow allocation size as tuple of integer
        """

        allocation = self.overlay.get_widget("scroll").get_allocation()

        return (allocation.width, allocation.height)

    def update_screenshot(self):
        """ Change current screenshot size
        """

        path = self.screenshots[self.__index].expanduser()

        pixbuf = self.generate_pixbuf_from_filename(path)
        if pixbuf is None:
            return

        pixbuf_size = PixbufSize(pixbuf, self.DEFAULT_IMAGE_SIZE)

        if self.__actual_mode == "fit":
            ratio_x, ratio_y = pixbuf_size.get_ratio(*self.scroll_allocation)
            self.__actual_zoom = int(min(ratio_x, ratio_y) * 100)

        elif self.__actual_mode == "original":
            ratio_x, ratio_y = pixbuf_size.get_ratio(*pixbuf_size.size)
            self.__actual_zoom = int(min(ratio_x, ratio_y) * 100)

        zoomed_width, zoomed_height = (
            int((self.__actual_zoom * pixbuf_size.default_width) / 100),
            int((self.__actual_zoom * pixbuf_size.default_height) / 100))

        self.scale_zoom.get_adjustment().set_value(float(self.__actual_zoom))

        self.viewport.get_widget("image").set_from_pixbuf(pixbuf.scale_simple(
            zoomed_width, zoomed_height, GdkPixbuf.InterpType.TILES))
