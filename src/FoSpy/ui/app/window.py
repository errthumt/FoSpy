from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QAction, QStandardItemModel, QStandardItem, QActionGroup, QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSplitter,
    QTreeView,
    QStackedWidget,
    QWidget,
    QLabel,
    QVBoxLayout,
    QFileDialog,
    QMessageBox
)
import qdarktheme
import os
from typing import Any

from ...blocks import FileBlock, Block, SingleBlock, ListBlock
from ._utils import _get_label, register_dlg

WINDOW_TITLE = "FoSpy - FoS File Viewer"
WINDOW_DIMENSIONS = (1000, 700)
WIDGET_DATA_ROLE = Qt.ItemDataRole.UserRole + 1

AVAILABLE_THEMES = ["auto"] if hasattr(qdarktheme, "setup_theme") else []
AVAILABLE_THEMES.extend(["light", "dark"])
DEFAULT_THEME = AVAILABLE_THEMES[0]

class EscapeFlag:
    def __bool__(self):
        return False
    def __repr__(self):
        if hasattr(self, "__name__") and self.__name__ is not None:
            return f"<{self.__name__} escape flag>"
        else:
            return "<escape flag>"

DLG_ESCAPE = EscapeFlag()

class TextContentWidget(QWidget):
    """A simple content widget to display a title and description."""
    def __init__(self, title, description, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel(f"<h2>{title}</h2>")
        desc = QLabel(description)

        layout.addWidget(label)
        layout.addWidget(desc)

        self.layout = layout


class MainWindow(QMainWindow):
    def __init__(self, open_path=None):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)
        self.resize(*WINDOW_DIMENSIONS)

        # map of block -> tree item
        self.tree_items = {}

        # build dropdown ribbon
        self._create_menu_bar()

        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(main_splitter)
        self.splitter = main_splitter

        self._build_tree()

        # content area
        self.content_stack = QStackedWidget()
        main_splitter.addWidget(self.content_stack)

        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 4)

        copy = self._startup_copy_dlg(open_path)
        if copy is DLG_ESCAPE:
            open_path = None
            copy = False

        self._open_file(open_path=open_path, copy=copy)

        register_dlg()

    def _startup_copy_dlg(self, open_path):
        if open_path is None:
            return False
        
        path_str = os.path.abspath(open_path)

        return self._custom_popup(
            "FoSpy GUI -File Opened on Startup",
            "You are opening the file below on startup. "
            "Do you want to edit the file directly or make a copy?\n\n"
            + path_str,
            ("Edit A Copy", True),
            ("Edit Original File", False),
            cancel=True
        )

    def _open_file(self, open_path=None, copy=False):
        if open_path is not None:
            fb = FileBlock.fromFile(open_path)
            if copy:
                fb = fb.copy()
        else:
            fb = None

        self.root_block = fb
        self.refresh_tree()
        self._initialize_views()

        if fb is None:
            return

        if fb._sourceFile is None:
            self._flag_edited(fb)


    def _build_tree(self):
        """Builds the tree view with the given file block."""
        # tree sidebar
        self.tree_view = QTreeView()
        self.tree_view.setHeaderHidden(True)

        self.tree_model = QStandardItemModel()
        self.tree_view.setModel(self.tree_model)

        # wiring
        self.tree_view.clicked.connect(self._on_tree_selection)
        self.splitter.addWidget(self.tree_view)


    def refresh_tree(self, blk:Block=None):
        """Refreshes or builds tree nodes.
        If target_item is given, only that sub-tree branch is cleared and rebuilt"""
        print("Debug: refreshing tree...")
        if blk is None:
            blk = self.root_block
            if blk is None:
                return
            target_item = None
        else:
            target_item = self.tree_items.get(blk, None)
        
        if target_item is None:
            self._clear_views(self.tree_model.invisibleRootItem())
            self.tree_model.clear()

            target_item = QStandardItem(_get_label(blk))

            self.tree_model.appendRow(target_item)
        
        else:
            self._clear_views(target_item)
            target_item.removeRows(0, target_item.rowCount())

        self.tree_items[blk] = target_item
        self._register_view(target_item, blk)
        self._populate_tree_nodes(target_item, blk)
    
    def _populate_tree_nodes(self, parent_item:QStandardItem, blk:Block):
        """Recursively adds child nodes to a QStandardItem."""

        if not isinstance(blk, Block):
            return
        
        if not hasattr(blk, "__GUI_FLAGS__"):
            blk.__GUI_FLAGS__ = {}


        if isinstance(blk, ListBlock):
            for i, blk_i in enumerate(blk._objs):
                label = _get_label(blk_i, i)

                child_item = QStandardItem(label)
                self._add_tree_item(child_item, parent_item, blk_i)
        
        elif isinstance(blk, SingleBlock):
            # get dict of property name -> live object
            prop_dict = blk.get_prop_dict()

            for prop, obj in prop_dict.items():
                # only Block instances get added to tree. Primitives are edited
                # in the SingleBlock's own widget
                if isinstance(obj, Block):
                    child_item = QStandardItem(prop)
                    self._add_tree_item(child_item, parent_item, obj)
        self._set_flag(blk, "refresh", False)

    def _set_flag(self, blk:Block, flag:str, value:bool):
        blk.__GUI_FLAGS__[flag] = value
        item = self.tree_items.get(blk, None)
        if item is None:
            return

        if flag == "edited":
            txt = item.text()
            if value and "*" not in txt:
                item.setText(f"*{txt}")
            elif not value:
                txt = txt.replace("*", "")
                item.setText(txt)

    def _get_flag(self, blk:Block, flag:str):
        return blk.__GUI_FLAGS__.get(flag, False)    

    def _flag_edited(self, blk):
        self._set_flag(blk, "edited", True)
        self._set_flag(blk, "refresh", True)

        if hasattr(blk, "_parent_block") and blk._parent_block is not None:
            self._flag_edited(blk._parent_block)


    def _add_tree_item(self, child_item:QStandardItem, parent_item:QStandardItem, blk:Block):
        """Adds a single child item with corresponding block to a parent."""
        parent_item.appendRow(child_item)
        self._register_view(child_item, blk)
        self._populate_tree_nodes(child_item, blk)

        self.tree_items[blk] = child_item
        for flag, value in blk.__GUI_FLAGS__.items():
            self._set_flag(blk, flag, value)

    def _register_view(self, item:QStandardItem, blk:Block):

        label = item.text()

        view_data = {
            "builder": lambda lbl=label,b=blk: self._build_widget(lbl,b),
            "widget": None,
            "block": blk
        }

        item.setData(view_data, WIDGET_DATA_ROLE)

    def _clear_views(self, parent_item:QStandardItem):
        for row in range(parent_item.rowCount()):
            child = parent_item.child(row)

            if child:
                self._clear_views(child)
                
                widget_data = child.data(WIDGET_DATA_ROLE)
                if widget_data and widget_data.get("widget", None) is not None:
                    widget = widget_data.get("widget", None)
                    if widget:
                        self.content_stack.removeWidget(widget)
                        widget.deleteLater()

    def _create_file_menu(self, menu_bar):
        file_menu = menu_bar.addMenu("&File")

        # Open
        open_action = QAction("&Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_dlg)
        file_menu.addAction(open_action)

        # Open A Copy
        open_copy_action = QAction("&Open A Copy...", self)
        open_copy_action.setShortcut("Ctrl+Shift+O")
        open_copy_action.triggered.connect(lambda *_: self._open_dlg(copy=True))
        file_menu.addAction(open_copy_action)

        # Edit A Copy
        edit_copy_action = QAction("&Edit A Copy", self)
        edit_copy_action.setShortcut("Ctrl+Shift+E")
        edit_copy_action.triggered.connect(self._edit_copy)
        file_menu.addAction(edit_copy_action)

        # Save
        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save)
        file_menu.addAction(save_action)

        # Save As
        save_as_action = QAction("&Save As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_dlg)
        file_menu.addAction(save_as_action)

        # Exit
        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def _create_view_menu(self, menu_bar):
        view_menu = menu_bar.addMenu("&View")
        self.menus["view"] = view_menu

        theme_submenu = view_menu.addMenu("Theme")

        theme_group = QActionGroup(self)
        theme_group.setExclusive(True)

        for theme_id in AVAILABLE_THEMES:
            label = theme_id.capitalize()

            action = QAction(label, self)
            action.setCheckable(True)

            if theme_id == DEFAULT_THEME:
                self._choose_theme(theme_id)
                action.setChecked(True)
            
            action.triggered.connect(lambda *args, t=theme_id: self._choose_theme(t))

            theme_submenu.addAction(action)
            theme_group.addAction(action)
    
    def _create_help_menu(self, menu_bar):
        from ._utils import register_app
        help_menu = menu_bar.addMenu("&Help")
        self.menus["help"] = help_menu

        doc_menu = help_menu.addMenu("&Documentation")

        doc_site_action = QAction("&Docs Site", self)
        doc_site_action.triggered.connect(self._open_docs_site)
        doc_menu.addAction(doc_site_action)

        doc_gh_action = QAction("&Github", self)
        doc_gh_action.triggered.connect(lambda *_:
            QDesktopServices.openUrl(QUrl("https://github.com/errthumt/FoSpy")))
        doc_menu.addAction(doc_gh_action)
        
        register_action = QAction("&Add to Apps", self)
        register_action.triggered.connect(register_app)
        help_menu.addAction(register_action)

    def _open_docs_site(self):
        from ._utils import _get_version, _find_docs_url

        version = _get_version()
        url = _find_docs_url(version)

        if url.endswith("latest/"):
            if not self._custom_popup(
                "Documentation for version not found",
                f"A documentation URL for version {version} could not be found.\n\n"
                "Redirecting to the latest version instead:\n"
                + url,
                cancel=True
            ):
                return

        QDesktopServices.openUrl(QUrl(url))

    def _choose_theme(self, theme_id):
        app = QApplication.instance()
        app.setQuitOnLastWindowClosed(True)
        if not app:
            return
        
        try:
            qdarktheme.setup_theme(theme_id)
        except AttributeError:
            app.setStyleSheet(qdarktheme.load_stylesheet(theme_id))


    def _create_menu_bar(self):
        """Dropdown menu ribbon."""
        self.menus = {}

        menu_bar = self.menuBar()

        self._create_file_menu(menu_bar)

        self._create_view_menu(menu_bar)

        self._create_help_menu(menu_bar)
    
    def _open_dlg(self, copy=False):
        from ...blocks.files import EXT_READ_MAP

        if not self._unsaved_dlg("opening a new file"):
            return

        ext_list = [f"*.{ext}" for ext in EXT_READ_MAP]
        ext_str = f'({" ".join(ext_list)})'


        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open FoS-style file",
            "",
            f"FoS Style {ext_str};;All Files (*)"
        )

        if file_path:
            self._open_file(open_path=file_path, copy=copy)

    @classmethod
    def _custom_popup(cls, title, text, *btns:str|tuple[str, Any], default=0, cancel=True):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)

        if len(btns) == 0:
            btns = [("OK", True)]

        results = {}

        if not (
            (default>=0 and default<len(btns)) or 
            (default is DLG_ESCAPE and cancel)
        ):
            default = 0

        for i, btn in enumerate(btns):
            if isinstance(btn, tuple):
                btn_txt = btn[0]
                result = btn[1]
            else:
                btn_txt = btn
                result = i

            btn = msg_box.addButton(btn_txt, QMessageBox.ActionRole)
            if i == default:
                msg_box.setDefaultButton(btn)
                default = btn
            results[btn] = result
        
        if cancel:
            btn = msg_box.addButton("Cancel", QMessageBox.ActionRole)
            results[btn] = DLG_ESCAPE
            if default is DLG_ESCAPE:
                msg_box.setDefaultButton(btn)
                default = btn

        msg_box.exec()

        clicked = msg_box.clickedButton() or default

        return results[clicked]


    def _unsaved_dlg(self, pending_action="exiting"):
        if not self._get_flag(self.root_block, "edited"):
            return True
        
        options = [
            ("Save", self.save),
            ("Save As...", self.save_dlg),
            ("Discard", lambda: True)
        ]

        result = self._custom_popup(
            "Unsaved Changes",
            f"You have unsaved changes. What would you like to do before {pending_action}?",
            *options,
            default=1,
            cancel=True
        )

        if result is DLG_ESCAPE:
            return result
        
        return result()
        

    def _edit_copy(self):
        if (self.root_block is None or
            not self._unsaved_dlg("switching to a copy")):
            return
        
        self._open_file(open_path=self.root_block._sourceFile, copy=True)
        

    def _initialize_views(self):
        if self.root_block is not None:
            return self.go_to_block(self.root_block)
        
        self.no_file = TextContentWidget(
            "No File Selected",
            "Open a FoS file to view its contents.\n"
            "File > Open..."
        )

        empty_idx = self.content_stack.addWidget(self.no_file)
        self.content_stack.setCurrentIndex(empty_idx)

    def _on_tree_selection(self, idx):
        """Triggers when clicking within the tree layout."""

        item = self.tree_model.itemFromIndex(idx)
        if not item:
            return
        

                
        widget_data = item.data(WIDGET_DATA_ROLE)
        if widget_data is None:
            return
        
        blk = widget_data.get("block", None)
        if self._get_flag(blk, "refresh"):
            self._set_flag(blk, "refresh", False)
            self.refresh_tree(blk)

        if widget_data.get("widget", None) is None:
            widget = widget_data.get("builder", lambda: None)()
            if widget is None:
                return
            widget_data["widget"] = widget
            self.content_stack.addWidget(widget_data["widget"])
        
        item.setData(widget_data, WIDGET_DATA_ROLE)
        self.content_stack.setCurrentWidget(widget_data["widget"])
    
    def go_to_block(self, blk:Block):
        """Programmatically select a block in the tree."""

        item = self.tree_items.get(blk, None)

        if item is None:
            raise ValueError(f"Block {blk} not found in tree.")
        
        idx = self.tree_model.indexFromItem(item)
        if not idx.isValid():
            raise ValueError(f"Item {item} not found in tree model.")
        
        self.tree_view.setCurrentIndex(idx)
        self.tree_view.scrollTo(idx)
        self._on_tree_selection(idx)


    def _build_widget(self, label, blk:Block):
        """Build a widget for the given block or navigate to tab in parent's widget.

        Default behavior: Build widget for block and return it.

        If block's parent is a ListBlock: switch to block's tab and return None instead."""
        from .block_widgets import widget_map

        if hasattr(blk, "_parent_block") and isinstance(blk._parent_block, ListBlock):
            self.go_to_block(blk._parent_block)

            parent_item = self.tree_items[blk._parent_block]
            parent_widget = parent_item.data(WIDGET_DATA_ROLE)["widget"]
            parent_widget.go_to_tab(blk)

            blk_item = self.tree_items[blk]
            idx = self.tree_model.indexFromItem(blk_item)
            self.tree_view.setCurrentIndex(idx)
            self.tree_view.scrollTo(idx)

            return None

        for typ, widget in widget_map.items():
            if isinstance(blk, typ):
                return widget(label, blk, self)
        
        return QLabel("ERROR: No Widget Found")
    
    def _get_item_path(self, item:QStandardItem):
        path = []

        while item is not None:
            path.append(item.row())
            item = item.parent()
        
        return list(reversed(path))
    
    def _get_item_from_path(self, path:list[int]):
        if not path:
            return None
        
        item = self.tree_model.item(path[0])

        for row in path[1:]:
            if item is None:
                return None
            
            item = item.child(row)
        
        return item

    def save(self, *args,path:str=None):
        if not self.root_block:
            return
        
        if path is None and self.root_block._sourceFile is None:
            return self.save_dlg()

        self.root_block.save(filepath=path)

        # cache current tree selection
        current_idx = self.tree_view.currentIndex()
        cached_path = None
        if current_idx.isValid():
            current_item = self.tree_model.itemFromIndex(current_idx)
            if current_item is not None:
                cached_path = self._get_item_path(current_item)

        self._open_file(path)

        # restore tree selection
        if cached_path:
            new_item = self._get_item_from_path(cached_path)
            if new_item:
                new_idx = self.tree_model.indexFromItem(new_item)
                if new_idx.isValid():
                    self.tree_view.setCurrentIndex(new_idx)
                    self.tree_view.scrollTo(new_idx)
                    self._on_tree_selection(new_idx)
        return True
    
    def save_dlg(self, *args):
        from ...blocks.files import EXT_READ_MAP

        ext_list = [f"*.{ext}" for ext in EXT_READ_MAP]
        ext_str = f'({" ".join(ext_list)})'

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save FoS-style file",
            "",
            f"FoS Files {ext_str};;All Files (*)"
        )

        if path:
            self.save(path=path)
            return True

        return False





