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
from os import R_OK, W_OK, access

# Geode
from geode_gem.widgets.common import GeodeGtkCommon

# GObject
from gi.repository import Gtk, GtkSource, Pango

# Typing
from typing import Union


TEXTVIEW_CSS = """
textview {
    font-family: %(family)s;
    font-size: %(size)dpt;
    font-style: %(style)s;
    font-variant: %(variant)s;
    font-weight: %(weight)d;
}
"""


class CommonEditor(GeodeGtkCommon):
    """ Common class to manage editor widgets

    Attributes
    ----------
    path : pathlib.Path or None
        The current opened file path if available, None otherwise
    font : str
        The current specified font as string representation
    css_provider : gi.repository.Gtk.CssProvider
        The widget CSS provider instance
    style_context : gi.repository.Gtk.StyleContext
        The widget style context instance

    See Also
    --------
    geode_gem.widgets.common.GeodeGtkCommon
    """

    __setters__ = {
        "set_bottom_margin": 4,
        "set_left_margin": 4,
        "set_right_margin": 4,
        "set_top_margin": 4,
    }

    DEFAULT_FONT = "Monospace 12"

    TAG_SEARCH_BACKGROUND = "yellow"
    TAG_SEARCH_FOREGROUND = "black"

    def __init__(self, subclass: Gtk.Widget, *args, **kwargs):
        """ Constructor

        Parameters
        ----------
        subclass : Gtk.TextView
            Subclass widget type

        See Also
        --------
        geode_gem.widgets.common.GeodeGtkCommon
        """

        GeodeGtkCommon.__init__(self, subclass, **kwargs)

        # Editor variables
        self.path = None
        self.font = kwargs.get("font", self.DEFAULT_FONT)

        # Widget style instances
        self.css_provider = Gtk.CssProvider.new()
        self.style_context = self.get_style_context()

        # Search related variables
        self.__search_iters = list()
        self.__current_iter_index = int()

        # Generate a tag used to show current iter in search mode
        self.inner_buffer.create_tag("search",
                                     background=self.TAG_SEARCH_BACKGROUND,
                                     foreground=self.TAG_SEARCH_FOREGROUND)

        self.set_buffer(self.inner_buffer)
        self.set_font(self.font)

    def clear_buffer(self):
        """ Clear the buffer content

        See Also
        --------
        gi.repository.Gtk.TextBuffer.delete
        """

        self.inner_buffer.delete(self.start_iter, self.end_iter)

    @property
    def end_iter(self) -> Gtk.TextIter:
        """ Retrieve the latest text iter from current buffer

        Returns
        -------
        Gtk.TextIter
            Latest text iter
        """

        return self.inner_buffer.get_end_iter()

    def get_content(self) -> str:
        """ Retrieve the content of the current buffer

        Returns
        -------
        str
            Buffer content as string

        Examples
        --------
        >>> CommonEditor.get_content()
        "Hello World!"
        """

        return self.inner_buffer.get_text(self.start_iter, self.end_iter, True)

    def get_font(self) -> str:
        """ Retrieve the font currently used by the editor

        Returns
        -------
        str
            Font representation as string

        Examples
        --------
        >>> CommonEditor.get_font()
        "Monospace 12"
        """

        return self.font

    @property
    def is_modified(self) -> bool:
        """ Check the modified bit state for current buffer

        Returns
        -------
        bool
            Buffer modified bit state

        See Also
        --------
        gi.repository.Gtk.TextBuffer.get_modified
        """

        return self.inner_buffer.get_modified()

    def on_search_iters(self, current_index: int, next_index: int):
        """ Switch to the next founded iter in search mode

        This method will do nothing if the search returns no result

        Parameters
        ----------
        current_index : int
            Current iter index from ``self.__search_iters`` list
        next_index : int
            Next iter index from ``self.__search_iters`` list

        Notes
        -----
        The last step set by this method is to scroll to the founded iter. To
        work properly, this widget must be contains in a scrolled container
        like Gtk.ScrolledWindow
        """

        if len(self.__search_iters) == 0:
            return

        if next_index < 0:
            next_index = len(self.__search_iters) - 1

        elif next_index >= len(self.__search_iters):
            next_index = 0

        start, end = self.__search_iters[current_index]
        self.inner_buffer.remove_tag_by_name("search", start, end)

        start, end = self.__search_iters[next_index]
        self.inner_buffer.apply_tag_by_name("search", start, end)
        self.inner_buffer.place_cursor(start)

        self.__current_iter_index = next_index

        self.scroll_to_iter(start, 0.25, False, 0.0, 0.0)

    def open_file(self, file_path: Path):
        """ Open the specified file path in current buffer

        Parameters
        ----------
        file_path : pathlib.Path
            File path on filesystem
        """

        if file_path.exists():
            if not access(file_path, R_OK):
                raise PermissionError(f"No read access for file '{file_path}'")

            self.inner_buffer.begin_not_undoable_action()
            self.inner_buffer.set_text(file_path.read_text(errors="replace"))
            self.inner_buffer.end_not_undoable_action()
            self.inner_buffer.set_modified(False)

        self.path = file_path

    def save_file(self):
        """ Save the current buffer in opened file path

        Raises
        ------
        ValueError
            If the ``self.path`` attribute is None
        """

        if self.path is None:
            raise ValueError("Cannot save a buffer without opened file")

        self.save_file_as(self.path)

    def save_file_as(self, file_path: Path):
        """ Save the current at the specified file path

        Parameters
        ----------
        file_path : pathlib.Path
            The file path which will be used to save current buffer

        Raises
        ------
        PermissionError
            If the file path exists but cannot be writed by the user
        """

        if file_path.exists() and not access(file_path, W_OK):
            raise PermissionError(f"No write access for file '{file_path}'")

        file_path.write_text(self.get_content())

        self.inner_buffer.set_modified(False)

    def search(self, pattern: str):
        """ Search a specific pattern string in current buffer

        Parameters
        ----------
        pattern : str
            String pattern to find in current buffer
        """

        self.search_reset()

        if len(pattern) == 0:
            return

        match = self.start_iter.forward_search(
            pattern, Gtk.TextSearchFlags.CASE_INSENSITIVE, self.end_iter)

        while match is not None:
            self.__search_iters.append(match)

            start, end = match
            match = end.forward_search(
                pattern, Gtk.TextSearchFlags.CASE_INSENSITIVE, self.end_iter)

    def search_next(self, *args):
        """ Go to the next founded iter

        See Also
        --------
        geode_gem.widgets.editor.CommonEditor.on_search_iters
        """

        self.on_search_iters(self.__current_iter_index,
                             self.__current_iter_index + 1)

    def search_previous(self, *args):
        """ Go to the previous founded iter

        See Also
        --------
        geode_gem.widgets.editor.CommonEditor.on_search_iters
        """

        self.on_search_iters(self.__current_iter_index,
                             self.__current_iter_index - 1)

    def search_reset(self):
        """ Reset current search and remove previous founded tag iter
        """

        self.__search_iters.clear()

        self.inner_buffer.remove_tag_by_name(
            "search", self.start_iter, self.end_iter)

    def set_font(self, font: Union[str, Pango.FontDescription]):
        """ Define a specific font for current TextView

        Parameters
        ----------
        font : str or Pango.FontDescription
            Font representation

        Raises
        ------
        TypeError
            If the specified font is not a string or a Pango.FontDescription

        See Also
        --------
        gi.repository.Gtk.StyleContext
        gi.repository.Pango.FontDescription

        Examples
        --------
        >>> CommonEditor.set_font("Sans 12")

        >>> from gi.repository import Pango
        >>> description = Pango.FontDescription.from_string("Monospace 10")
        >>> CommonEditor.set_font(description)
        """

        if isinstance(font, str):
            font = Pango.FontDescription.from_string(font)

        elif not isinstance(font, Pango.FontDescription):
            raise TypeError(
                "font parameter must be a string or Pango.FontDescription")

        font_size = int(font.get_size() / Pango.SCALE)
        font_style = font.get_style()
        font_variant = font.get_variant()
        font_weight = font.get_weight()

        style = "normal"
        if font_style == Pango.Style.OBLIQUE:
            style = "oblique"
        elif font_style == Pango.Style.ITALIC:
            style = "italic"

        variant = "normal"
        if font_variant == Pango.Variant.SMALL_CAPS:
            variant = "small-caps"

        weight = 400
        if font_weight in range(100, 1000):
            # Values like 350 or 380, which are availables in Pango.Weight, are
            # not valid with Gtk CSS processor. So the module will round the
            # weight to have a valid value for the Gtk CSS processor.
            weight = font_weight - (font_weight % 100)

        css = TEXTVIEW_CSS % {
            "family": font.get_family(),
            "size": font_size,
            "style": style,
            "variant": variant,
            "weight": weight,
        }

        self.css_provider.load_from_data(bytes(css, "UTF-8"))

        self.style_context.remove_provider(self.css_provider)
        self.style_context.add_provider(
            self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.font = font.to_string()

    @property
    def start_iter(self) -> Gtk.TextIter:
        """ Retrieve the first text iter from current buffer

        Returns
        -------
        Gtk.TextIter
            First text iter
        """

        return self.inner_buffer.get_start_iter()


class GeodeGtkSourceView(CommonEditor, GtkSource.View):
    """ Geode representation of GtkSource.View widget

    Attributes
    ----------
    inner_buffer : gi.repository.GtkSource.Buffer
        The widget text buffer instance
    inner_language : gi.repository.GtkSource.LanguageManager
        The widget language manager instance
    inner_style : geode_gem.widgets.editor.GeodeGtkStyleSchemeManager
        The widget style scheme manager instance

    See Also
    --------
    geode_gem.widgets.editor.CommonEditor
    gi.repository.GtkSource.View
    """

    __setters__ = {
        "set_insert_spaces_instead_of_tabs": True,
        "set_show_line_numbers": False,
        "set_tab_width": 4,
    }

    def __init__(self, *args, **kwargs):
        """ Constructor

        See Also
        --------
        geode_gem.widgets.editor.CommonEditor
        """

        self.inner_buffer = GtkSource.Buffer()
        self.inner_language = GtkSource.LanguageManager()
        self.inner_style = GeodeGtkStyleSchemeManager()

        CommonEditor.__init__(self, GtkSource.View, **kwargs)

    def get_style_scheme(self) -> str:
        """ Retrieve the current style scheme used by current buffer

        Returns
        -------
        str
            Style scheme name
        """

        style_scheme = self.inner_buffer.get_style_scheme()
        if style_scheme is None:
            return "none"

        return style_scheme.get_id()

    def open_file(self, file_path: Path):
        """ Open the specified file path in current buffer

        This method inherit from CommonEditor.open_file and try to guess the
        file language to setup source highlighting

        See Also
        --------
        geode_gem.widgets.editor.CommonEditor.open_file
        """

        super().open_file(file_path)

        self.inner_buffer.set_language(
            self.inner_language.guess_language(str(file_path)))

        self.inner_buffer.set_undo_manager(None)

    def set_style_scheme(self, style: str):
        """ Define the style scheme used by current buffer

        Parameters
        ----------
        style : str
            Style scheme name
        """

        scheme = self.inner_style.get_scheme(style)

        self.inner_buffer.set_style_scheme(scheme)


class GeodeGtkStyleSchemeManager(GeodeGtkCommon, GtkSource.StyleSchemeManager):

    def __init__(self, *args, **kwargs):
        """ Constructor

        See Also
        --------
        geode_gem.widgets.common.GeodeGtkCommon
        gi.repository.GtkSource.StyleSchemeManager
        """

        GeodeGtkCommon.__init__(self, GtkSource.StyleSchemeManager, **kwargs)

    def iter_style_schemes(self):
        """ Iterate trought available style schemes

        Yields
        ------
        pathlib.Path
            Style scheme file path
        """

        for path in self.get_search_path():
            scheme_path = Path(path).expanduser().resolve()

            for element in scheme_path.glob("*.xml"):
                yield element


class GeodeGtkTextView(CommonEditor, Gtk.TextView):
    """ Geode representation of GtkSource.View widget

    Attributes
    ----------
    inner_buffer : gi.repository.GtkSource.Buffer
        The widget text buffer instance

    See Also
    --------
    geode_gem.widgets.editor.CommonEditor
    gi.repository.Gtk.TextView
    """

    def __init__(self, *args, **kwargs):
        """ Constructor

        See Also
        --------
        geode_gem.widgets.editor.CommonEditor
        """

        self.inner_buffer = Gtk.TextBuffer()

        CommonEditor.__init__(self, Gtk.TextView, **kwargs)
