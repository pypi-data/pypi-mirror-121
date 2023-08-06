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

# Geode
from geode_gem.widgets.common import GeodeGtkCommon

# GObject
from gi.repository import Gtk


class GeodeGtkGrid(GeodeGtkCommon, Gtk.Grid):

    def __init__(self, *args, **kwargs):
        """ Constructor
        """

        GeodeGtkCommon.__init__(self, Gtk.Grid, **kwargs)

        for element in args:
            if isinstance(element, GeodeGtkGridItem):
                self.attach(element.widget,
                            element.left,
                            element.top,
                            element.width,
                            element.height)
                self.append_widget(element.widget)


class GeodeGtkGridItem:

    def __init__(self, widget, **kwargs):
        """ Constructor
        """

        self.widget = widget

        self.left = kwargs.get("left", 0)
        self.top = kwargs.get("top", 0)
        self.width = kwargs.get("width", 0)
        self.height = kwargs.get("height", 0)
