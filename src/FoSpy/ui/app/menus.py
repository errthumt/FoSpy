from PySide6.QtGui import QAction, QActionGroup, QDesktopServices
from PySide6.QtCore import QUrl

MENU_BUILDERS = {}

def add_to_menus(name):
    def decorator(func):
        MENU_BUILDERS[name] = func
        return func
    return decorator


@add_to_menus("file")
def file_menu(win, menu_bar):
    file_menu = menu_bar.addMenu("&File")

    # Open
    open_action = QAction("&Open...", win)
    open_action.setShortcut("Ctrl+O")
    open_action.triggered.connect(win._open_dlg)
    file_menu.addAction(open_action)

    # Open A Copy
    open_copy_action = QAction("&Open A Copy...", win)
    open_copy_action.setShortcut("Ctrl+Shift+O")
    open_copy_action.triggered.connect(lambda *_: win._open_dlg(copy=True))
    file_menu.addAction(open_copy_action)

    # Edit A Copy
    edit_copy_action = QAction("&Edit A Copy", win)
    edit_copy_action.setShortcut("Ctrl+Shift+E")
    edit_copy_action.triggered.connect(win._edit_copy)
    file_menu.addAction(edit_copy_action)

    # Save
    save_action = QAction("&Save", win)
    save_action.setShortcut("Ctrl+S")
    save_action.triggered.connect(win.save)
    file_menu.addAction(save_action)

    # Save As
    save_as_action = QAction("&Save As...", win)
    save_as_action.setShortcut("Ctrl+Shift+S")
    save_as_action.triggered.connect(win.save_dlg)
    file_menu.addAction(save_as_action)

    # Exit
    exit_action = QAction("&Exit", win)
    exit_action.triggered.connect(win.close)
    file_menu.addAction(exit_action)

    return file_menu

@add_to_menus("view")
def view_menu(win, menu_bar):
    from .window import AVAILABLE_THEMES, DEFAULT_THEME

    view_menu = menu_bar.addMenu("&View")
    win.menus["view"] = view_menu

    theme_submenu = view_menu.addMenu("Theme")

    theme_group = QActionGroup(win)
    theme_group.setExclusive(True)

    for theme_id in AVAILABLE_THEMES:
        label = theme_id.capitalize()

        action = QAction(label, win)
        action.setCheckable(True)

        if theme_id == DEFAULT_THEME:
            win._choose_theme(theme_id)
            action.setChecked(True)
        
        action.triggered.connect(lambda *args, t=theme_id: win._choose_theme(t))

        theme_submenu.addAction(action)
        theme_group.addAction(action)
    
    return view_menu

@add_to_menus("window")
def window_menu(win, menu_bar):
    win_menu = menu_bar.addMenu("&Window")
    win.menus["window"] = win_menu

    refresh_action = QAction("Refresh Window", win)
    refresh_action.triggered.connect(lambda *_: win.hard_refresh(to_blk=True))
    win_menu.addAction(refresh_action)

    return win_menu

@add_to_menus("help")
def help_menu(win, menu_bar):
    from ._utils import register_app, add_to_start
    import platform
    help_menu = menu_bar.addMenu("&Help")
    win.menus["help"] = help_menu

    doc_menu = help_menu.addMenu("&Documentation")

    doc_site_action = QAction("&Docs Site", win)
    doc_site_action.triggered.connect(win._open_docs_site)
    doc_menu.addAction(doc_site_action)

    doc_gh_action = QAction("&Github", win)
    doc_gh_action.triggered.connect(lambda *_:
        QDesktopServices.openUrl(QUrl("https://github.com/errthumt/FoSpy")))
    doc_menu.addAction(doc_gh_action)
    
    register_action = QAction("&Add as *.fos Editor", win)
    register_action.triggered.connect(register_app)
    help_menu.addAction(register_action)

    current_os = platform.system()
    if current_os == "Windows":
        start_action = QAction("&Add to Start Menu", win)
        start_action.triggered.connect(add_to_start)
        help_menu.addAction(start_action)

    return help_menu

@add_to_menus("tools")
def tools_menu(win, menu_bar):
    tools_menu = menu_bar.addMenu("&Tools")

    console_action = QAction("Python Console", win)
    console_action.triggered.connect(win._open_console)
    tools_menu.addAction(console_action)

    return tools_menu