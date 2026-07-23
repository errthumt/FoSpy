from PySide6.QtGui import QAction, QActionGroup, QDesktopServices
from PySide6.QtCore import QUrl

MENU_BUILDERS = {}

def add_to_menus(name):
    def decorator(func, n=name):
        def builder(win, menu_bar, _n=n, _f=func):
            specs = _f(win)
            add_menu(win, menu_bar, _n, specs)
        MENU_BUILDERS[n] = builder
        return func
    return decorator

def add_menu(win, menu_bar, label, specs:dict|tuple[tuple], parent=None):
    label_txt = "&"+label.capitalize()
    if parent is None:
        menu = menu_bar.addMenu(label_txt)
        win.menus[label] = menu
        def add_action(action, *_, m=menu):
            return m.addAction(action)
    else:
        menu = parent.addMenu(label_txt)

        exclusive = isinstance(specs, tuple)

        if exclusive:
            group = QActionGroup(win)
            group.setExclusive(True)

            def add_action(action, i, *_, g=group, m=menu):
                g.addAction(action)
                if i == 0:
                    action.setChecked(True)
                return m.addAction(action)
        else:
            def add_action(action, *_, m=menu):
                return m.addAction(action)

    if isinstance(specs, dict):
        specs = specs.items()

    for i, (name, spec) in enumerate(specs):
        if isinstance(spec, (tuple,dict)):
            add_menu(win, menu, name, spec, parent=menu)
            continue

        action_func = spec
        if len(name) == 2:
            action_label, shortcut = name
        else:
            action_label = name
            shortcut = None

        action = QAction(action_label, win)
        if shortcut:
            action.setShortcut(shortcut)
        action.triggered.connect(action_func)
        add_action(action, i)

    return menu

@add_to_menus("file")
def file_menu(win):

    return {
        "Open...": win._open_dlg,
        "Open A Copy...": lambda *_: win._open_dlg(copy=True),
        "Edit A Copy": win._edit_copy,
        "Save": win.save,
        "Save As...": win.save_dlg
    }


    # file_menu = menu_bar.addMenu("&File")

    # # Open
    # open_action = QAction("&Open...", win)
    # open_action.setShortcut("Ctrl+O")
    # open_action.triggered.connect(win._open_dlg)
    # file_menu.addAction(open_action)

    # # Open A Copy
    # open_copy_action = QAction("&Open A Copy...", win)
    # open_copy_action.setShortcut("Ctrl+Shift+O")
    # open_copy_action.triggered.connect(lambda *_: win._open_dlg(copy=True))
    # file_menu.addAction(open_copy_action)

    # # Edit A Copy
    # edit_copy_action = QAction("&Edit A Copy", win)
    # edit_copy_action.setShortcut("Ctrl+Shift+E")
    # edit_copy_action.triggered.connect(win._edit_copy)
    # file_menu.addAction(edit_copy_action)

    # # Save
    # save_action = QAction("&Save", win)
    # save_action.setShortcut("Ctrl+S")
    # save_action.triggered.connect(win.save)
    # file_menu.addAction(save_action)

    # # Save As
    # save_as_action = QAction("&Save As...", win)
    # save_as_action.setShortcut("Ctrl+Shift+S")
    # save_as_action.triggered.connect(win.save_dlg)
    # file_menu.addAction(save_as_action)

    # # Exit
    # exit_action = QAction("&Exit", win)
    # exit_action.triggered.connect(win.close)
    # file_menu.addAction(exit_action)

    # return file_menu

@add_to_menus("view")
def view_menu(win):
    from .window import AVAILABLE_THEMES, DEFAULT_THEME

    theme_options = []

    available = [DEFAULT_THEME]
    available.extend(t for t in AVAILABLE_THEMES if t != DEFAULT_THEME)

    win._choose_theme(DEFAULT_THEME)

    for theme_id in available:
        label = theme_id.capitalize()

        def choose_theme(*_, t=theme_id):
            win._choose_theme(t)

        theme_options.append((label, choose_theme))

    theme_options = tuple(theme_options)

    return {
        "theme": theme_options
    }

    # view_menu = menu_bar.addMenu("&View")
    # win.menus["view"] = view_menu

    # theme_submenu = view_menu.addMenu("Theme")

    # theme_group = QActionGroup(win)
    # theme_group.setExclusive(True)

    # for theme_id in AVAILABLE_THEMES:
    #     label = theme_id.capitalize()

    #     action = QAction(label, win)
    #     action.setCheckable(True)

    #     if theme_id == DEFAULT_THEME:
    #         win._choose_theme(theme_id)
    #         action.setChecked(True)
        
    #     action.triggered.connect(lambda *args, t=theme_id: win._choose_theme(t))

    #     theme_submenu.addAction(action)
    #     theme_group.addAction(action)
    
    # return view_menu

@add_to_menus("window")
def window_menu(win):
    return {
        "Refresh Window": lambda *_: win.hard_refresh(to_blk=True)
    }

    # win_menu = menu_bar.addMenu("&Window")
    # win.menus["window"] = win_menu

    # refresh_action = QAction("Refresh Window", win)
    # refresh_action.triggered.connect(lambda *_: win.hard_refresh(to_blk=True))
    # win_menu.addAction(refresh_action)

    # return win_menu

@add_to_menus("help")
def help_menu(win):
    return {
        "Docs Site": win._open_docs_site,
        "Github": lambda *_: QDesktopServices.openUrl(QUrl("https://github.com/errthumt/FoSpy"))
    }


    # help_menu = menu_bar.addMenu("&Help")
    # win.menus["help"] = help_menu

    # doc_menu = help_menu.addMenu("&Documentation")

    # doc_site_action = QAction("&Docs Site", win)
    # doc_site_action.triggered.connect(win._open_docs_site)
    # doc_menu.addAction(doc_site_action)

    # doc_gh_action = QAction("&Github", win)
    # doc_gh_action.triggered.connect(lambda *_:
    #     QDesktopServices.openUrl(QUrl("https://github.com/errthumt/FoSpy")))
    # doc_menu.addAction(doc_gh_action)
    

    # return help_menu

@add_to_menus("app")
def app_menu(win):
    from ._utils import register_app, add_to_start
    from .setup.check_update import update_dlg
    import platform

    menu = {
        "Update FoSpy": {
            "From PyPI": lambda *_, w=win: update_dlg(w),
            "From GitHub": lambda *_, w=win: update_dlg(w,github=True)
        },
        "Add as *.fos Editor": register_app,
        "Add to Start Menu": add_to_start
    }

    current_os = platform.system()
    if current_os == "Windows":
        menu["Add to Start Menu"] = add_to_start

    return menu

    # app_menu = menu_bar.addMenu("&App")
    # win.menus["app"] = app_menu

    # register_action = QAction("&Add as *.fos Editor", win)
    # register_action.triggered.connect(register_app)
    # app_menu.addAction(register_action)

    # current_os = platform.system()
    # if current_os == "Windows":
    #     start_action = QAction("&Add to Start Menu", win)
    #     start_action.triggered.connect(add_to_start)
    #     app_menu.addAction(start_action)
    
    # update_action = QAction("&Update FoSpy", win)
    # update_action.triggered.connect(update_dlg)
    # app_menu.addAction(update_action)

    # return app_menu

@add_to_menus("tools")
def tools_menu(win):
    return {
        "Python Console": win._open_console
    }