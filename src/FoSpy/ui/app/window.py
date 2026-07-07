from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (
    QMainWindow,
    QSplitter,
    QTreeView,
    QStackedWidget,
    QWidget,
    QLabel,
    QVBoxLayout
    # QMenuBar
)

from ...blocks import FileBlock, Block, SingleBlock, ListBlock

WINDOW_TITLE = "FoSpy - FoS File Viewer"
WINDOW_DIMENSIONS = (1000, 700)
WIDGET_DATA_ROLE = Qt.ItemDataRole.UserRole + 1

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

        if open_path is not None:
            fb = FileBlock.fromFile(open_path)
        else:
            fb = None

        self.root_block = fb

        # build dropdown ribbon
        self._create_menu_bar()

        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(main_splitter)
        self.splitter = main_splitter

        self._build_tree()

        # content area
        self.content_stack = QStackedWidget()
        main_splitter.addWidget(self.content_stack)

        self._initialize_views()

        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 4)

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

        self.refresh_tree()

    def refresh_tree(self, blk:Block=None, target_item:QStandardItem=None):
        """Refreshes or builds tree nodes.
        If target_item is given, only that sub-tree branch is cleared and rebuilt"""

        if blk is None:
            blk = self.root_block
            if blk is None:
                return
        
        if target_item is None:
            self._clear_views(self.tree_model.invisibleRootItem())
            self.tree_model.clear()

            if isinstance(blk, FileBlock):
                text = blk._sourceFile or "<Not Saved>"
                target_item = QStandardItem(text)
            else:
                target_item = QStandardItem(f"{type(blk).__name__} Object")

            self.tree_model.appendRow(target_item)
        
        else:
            self._clear_views(target_item)
            target_item.removeRows(0, target_item.rowCount())

        self._register_view(target_item, blk)
        self._populate_tree_nodes(target_item, blk)
    
    def _populate_tree_nodes(self, parent_item:QStandardItem, blk:Block):
        """Recursively adds child nodes to a QStandardItem."""

        if isinstance(blk, ListBlock):
            for i, blk_i in enumerate(blk._objs):
                id_key, id_txt = blk_i.get_id()
                label = f"{i} - {id_txt}"
                if id_key is None:
                    label += " Object"

                child_item = QStandardItem(label)
                self._add_tree_item(child_item, parent_item, blk_i)
        
        elif isinstance(blk, SingleBlock):
            # serialize to property names only
            serial = blk.serialize(shallow=True, clean=True)

            for prop in serial:
                obj = getattr(blk, prop)
                # only Block instances get added to tree. Primitives are edited
                # in the SingleBlock's own widget
                if isinstance(obj, Block):
                    child_item = QStandardItem(prop)
                    self._add_tree_item(child_item, parent_item, obj)

    def _add_tree_item(self, child_item:QStandardItem, parent_item:QStandardItem, blk:Block):
        """Adds a single child item with corresponding block to a parent."""
        parent_item.appendRow(child_item)
        self._register_view(child_item, blk)
        self._populate_tree_nodes(child_item, blk)

    def _register_view(self, item:QStandardItem, blk:Block):
        view_data = {
            "builder": lambda: self._build_widget(blk),
            "widget": None
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



    def _create_menu_bar(self):
        """Dropdown menu ribbon."""
        self.menus = {}

        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("&File")
        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        self.menus["file"] = file_menu


        # View Menu
        view_menu = menu_bar.addMenu("&View")
        self.menus["view"] = view_menu

        # Help Menu
        help_menu = menu_bar.addMenu("&Help")
        self.menus["help"] = help_menu

    def _initialize_views(self):
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

        if widget_data.get("widget", None) is None:
            widget_data["widget"] = widget_data.get("builder", lambda: None)()
            self.content_stack.addWidget(widget_data["widget"])
        
        self.content_stack.setCurrentWidget(widget_data["widget"])

    def _build_widget(self, blk:Block):
        """Stub: Build a widget for the given block."""
        return QLabel(f"Editor View for {type(blk).__name__}")




