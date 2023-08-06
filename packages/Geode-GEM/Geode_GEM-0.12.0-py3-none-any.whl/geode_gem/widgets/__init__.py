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

from geode_gem.widgets import (button, cellrenderer, combobox, editor, entry,
                               grid, iconview, infobar, listbox, menu, misc,
                               paned, stack, statusbar, toolbar, treeview)


# ------------------------------------------------------------------------------
#   Class
# ------------------------------------------------------------------------------

class GeodeGtk:
    """ Custom widgets for Geode-GEM applications
    """

    Adjustment = misc.GeodeGtkAdjustment
    Box = misc.GeodeGtkBox
    Button = button.GeodeGtkButton
    ButtonBox = misc.GeodeGtkButtonBox
    CellRendererAccel = cellrenderer.GeodeGtkCellRendererAccel
    CellRendererCombo = cellrenderer.GeodeGtkCellRendererCombo
    CellRendererPixbuf = cellrenderer.GeodeGtkCellRendererPixbuf
    CellRendererSpin = cellrenderer.GeodeGtkCellRendererSpin
    CellRendererText = cellrenderer.GeodeGtkCellRendererText
    CheckMenuItem = menu.GeodeGtkCheckMenuItem
    ComboBox = combobox.GeodeGtkComboBox
    ComboBoxText = combobox.GeodeGtkComboBoxText
    Entry = entry.GeodeGtkEntry
    EntryCompletion = entry.GeodeGtkEntryCompletion
    EntryIcon = entry.GeodeGtkEntryIcon
    FileChooserButton = button.GeodeGtkFileChooserButton
    FontButton = button.GeodeGtkFontButton
    Frame = misc.GeodeGtkFrame
    Grid = grid.GeodeGtkGrid
    GridItem = grid.GeodeGtkGridItem
    HPaned = paned.GeodeGtkHPaned
    HeaderBar = misc.GeodeGtkHeaderBar
    IconView = iconview.GeodeGtkIconView
    Image = misc.GeodeGtkImage
    InfoBar = infobar.GeodeGtkInfoBar
    Label = misc.GeodeGtkLabel
    LinkButton = button.GeodeGtkLinkButton
    ListBox = listbox.GeodeGtkListBox
    ListBoxButton = listbox.GeodeGtkListBoxButton
    ListBoxCheckItem = listbox.GeodeGtkListBoxCheckItem
    ListBoxItem = listbox.GeodeGtkListBoxItem
    Menu = menu.GeodeGtkMenu
    MenuButton = button.GeodeGtkMenuButton
    MenuItem = menu.GeodeGtkMenuItem
    Overlay = misc.GeodeGtkOverlay
    Paned = paned.GeodeGtkPaned
    Popover = misc.GeodeGtkPopover
    RadioMenuItem = menu.GeodeGtkRadioMenuItem
    Revealer = misc.GeodeGtkRevealer
    Scale = misc.GeodeGtkScale
    ScrolledWindow = misc.GeodeGtkScrolledWindow
    SearchBar = misc.GeodeGtkSearchBar
    SearchEntry = entry.GeodeGtkSearchEntry
    SpinButton = button.GeodeGtkSpinButton
    SourceView = editor.GeodeGtkSourceView
    Spinner = misc.GeodeGtkSpinner
    StackOption = stack.GeodeGtkStackOption
    StackSection = stack.GeodeGtkStackSection
    StackSidebar = stack.GeodeGtkStackSidebar
    StackView = stack.GeodeGtkStackView
    Statusbar = statusbar.GeodeGtkStatusbar
    StyleSchemeManager = editor.GeodeGtkStyleSchemeManager
    Switch = misc.GeodeGtkSwitch
    TextView = editor.GeodeGtkTextView
    ToggleButton = button.GeodeGtkToggleButton
    Toolbar = toolbar.GeodeGtkToolbar
    ToolbarBox = toolbar.GeodeGtkToolbarBox
    ToolbarSwitch = toolbar.GeodeGtkToolbarSwitch
    TreeView = treeview.GeodeGtkTreeView
    TreeViewColumn = treeview.GeodeGtkTreeViewColumn
    Viewport = misc.GeodeGtkViewport
    VPaned = paned.GeodeGtkVPaned
