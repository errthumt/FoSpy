import code
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QLabel,
    QMenuBar,
    QScrollArea,
    QWidget
)
import sys
import io
import traceback
from typing import Any
import ast
from .window import MainWindow
from ._utils import _clear_layout

CONSOLE_DIM = (800, 600)
VARS_MAX_H = 150

VAR_NAME_W = 200

CONSOLE_FONT = QFont("Monospace")
CONSOLE_FONT.setStyleHint(QFont.TypeWriter)
CONSOLE_FONT.setPointSize(11)

CONSOLE_STYLE = "background-color: #1E1E1E; color: #ffffff;"

class ReadOnly:
    def __init__(self, **attrs):
        self._locked = True

        if "_registry" in attrs:
            raise ValueError("read_only._registry is reserved for internal use")

        self.override(_registry={},**attrs)
    
    def __setattr__(self, name, value):
        if name == "_locked":
            if not isinstance(value, bool):
                raise TypeError(f"Expected bool for '_locked', got {type(value)}")
            return super().__setattr__(name, value)
        
        if name == "_registry":
            if not isinstance(value, dict):
                raise TypeError(f"Expected dict for '_registry', got {type(value)}")
            return super().__setattr__(name, value)

        if self._locked:
            raise AttributeError(f"Attribute {name} is read-only")
        super().__setattr__(name, value)

    def override(self, **attrs):
        self._locked = False
        for k, v in attrs.items():
            setattr(self, k, v)
            if k != "_registry":
                self.get_registry()[k] = v
        self._locked = True

    def get_registry(self):
        return self.__getattribute__("_registry", override=True)

    def __getattribute__(self, name, override=False):
        if name == "_registry" and not override:
            raise AttributeError("You cannot access read_only._registry directly")
        
        return super().__getattribute__(name)

class ReadOnlyRedirect(dict):
    def __init__(self, read_only:ReadOnly, *args, **kwargs):

        super().__init__(*args, read_only=read_only, **kwargs)
        self.read_only = read_only

    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        
        if hasattr(self.read_only, key):
            return getattr(self.read_only, key)
        
        raise KeyError(key)

class ProtectedConsole(code.InteractiveConsole):
    def __init__(self, *protected_vars:str, **all_vars):
        if "read_only" in all_vars:
            raise ValueError("read_only is reserved for internal use")

        free_vars = all_vars.copy()
        protected = {}
        for v in protected_vars:
            if v in protected:
                raise ValueError(f"Duplicate protected variable '{v}'")
            if v not in free_vars:
                raise ValueError(f"Cannot protect variable '{v}', it does not exist")
            
            protected[v] = free_vars.pop(v)

        self.read_only = ReadOnly(**protected)

        local_vars = ReadOnlyRedirect(self.read_only, **free_vars)

        super().__init__(locals=local_vars)

    def push(self, line):
        try:
            tree = ast.parse(line)
        except SyntaxError:
            # delegate to base handling
            return super().push(line)
        
        assignments = (
            ast.Assign,
            ast.AugAssign,
            ast.AnnAssign,
            ast.NamedExpr
        )
        
        if any(
            isinstance(node, assignments)
            and (
                (
                    hasattr(node, "targets") and any(
                        self._is_protected(t)
                        for t in node.targets
                    )
                )
                or
                (
                    hasattr(node, "target") and
                    self._is_protected(node.target)
                )
            )
            for node in ast.walk(tree)
        ):
            return False

        return super().push(line)
    
    def _is_protected(self, target):
        if isinstance(target, ast.Name):
            return self._read_only(target.id)
        
        if isinstance(target, ast.Tuple):
            return any(self._is_protected(t) for t in target.elts)
        
        if isinstance(target, ast.Starred):
            return self._is_protected(target.value)
        
        return False

    def _read_only(self, name):
        if name == "read_only" or hasattr(self.read_only, name):
            self.log(f"Cannot assign to read-only variable '{name}'")
            return True
        return False
    
    def add_protected(self, **protected_vars):
        self.read_only.override(**protected_vars)
        self.log("Added/Updated Protected Variables:",
                 *[f"    {k}" for k in protected_vars])
    
    def get_protected(self):
        return self.read_only.get_registry()

    def log(self, *txt):
        if not txt:
            return
        
        if len(txt) == 1:
            return print("[console] " + txt[0])

        print("[console/]")
        for t in txt:
            print(t)
        print("[/console]")


class PythonConsole(QDialog):
    def __init__(self, parent:MainWindow=None, persistent=True, **local_vars:Any|tuple[Any, str]):
        super().__init__(parent)
        self.persistent=persistent
        self.indent = 0

        # attach to parent
        if parent is not None and (
            not hasattr(parent, "__python_console__") or
            parent.__python_console__ is None
        ):
            parent.__python_console__ = self

        self.setWindowTitle("FoSpy GUI - Python Console")
        self.resize(*CONSOLE_DIM)

        layout = QVBoxLayout(self)

        menu_bar = QMenuBar(self)
        layout.setMenuBar(menu_bar)

        console_menu = menu_bar.addMenu("&Console")

        if persistent:
            hide_action = QAction("Hide", self)
            hide_action.triggered.connect(self.close)
            console_menu.addAction(hide_action)
        
        restart_action = QAction("Restart", self)
        restart_action.triggered.connect(self.restart)
        console_menu.addAction(restart_action)

        close_action = QAction("Close", self)
        close_action.triggered.connect(self.exit_dlg)
        console_menu.addAction(close_action)

        header = QLabel("<h2>FoSpy GUI - Live Python Console</h2>")
        layout.addWidget(header, stretch=0)

        subheader = QLabel("<h3>Available Variables:</h3>")
        layout.addWidget(subheader, stretch=0)

        var_header_layout = QHBoxLayout()
        var_name = QLabel("<h4>Variable Name</h4>")
        var_name.setMinimumWidth(VAR_NAME_W)
        var_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        var_desc = QLabel("<h4>Description</h4>")
        var_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        var_header_layout.addWidget(var_name, stretch=0)
        var_header_layout.addWidget(var_desc, stretch=1)
        layout.addLayout(var_header_layout, stretch=0)

        var_container = QWidget()
        self.var_layout = QVBoxLayout(var_container)
        self.var_layout.setContentsMargins(0, 0, 0, 0)

        var_scroll = QScrollArea(self)
        var_scroll.setWidgetResizable(True)
        var_scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        var_scroll.setContentsMargins(0, 0, 0, 0)
        var_scroll.setWidget(var_container)
        var_scroll.setMinimumHeight(VARS_MAX_H)
        layout.addWidget(var_scroll, stretch=0)

        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        self.output.setFont(CONSOLE_FONT)
        self.output.setStyleSheet(CONSOLE_STYLE)
        layout.addWidget(self.output, stretch=1)

        input_layout = QHBoxLayout()
        input_label = QLabel(">>>")
        self.input = QLineEdit()
        self.input.setFont(CONSOLE_FONT)
        self.input.setStyleSheet(CONSOLE_STYLE)
        self.input.returnPressed.connect(self.execute_line)

        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input, stretch=1)
        layout.addLayout(input_layout, stretch=0)

        self.console_vars = {
            "__console__": (self, "The Python Console"),
        }
        for key, value in local_vars.items():
            if (isinstance(value, tuple) and
                len(value) == 2 and
                isinstance(value[1], str)):
                value, desc = value
            else:
                desc = "Unknown"

            self.console_vars[key] = (value, desc)

        self.console = ProtectedConsole()
        self.console.run_command = self.output.append
        self.buffer = self._buffer()
        self.refresh_vars()

    def _buffer(self):
        while True:
            # cache excepttion hook
            cached_hook = sys.excepthook
            sys.excepthook = self.handle_exception

            buf = io.StringIO()
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = buf
            sys.stderr = buf

            yield buf

            sys.stdout = old_stdout
            sys.stderr = old_stderr
            sys.excepthook = cached_hook

            out = buf.getvalue()
            if out.strip():
                self.output.append(out)
            
            yield False

    def open_buffer(self):
        return next(b for b in self.buffer if b)
    
    def flush(self):
        return next(b for b in self.buffer if not b)
    
    @staticmethod
    def single_buffer(func):
        def decorated(self, *args, **kwargs):
            self.open_buffer()
            func(self, *args, **kwargs)
            self.flush()
        return decorated
    
    @single_buffer
    def add_protected(self, **protected_vars):
        self.console.add_protected(**protected_vars)

    def refresh_vars(self):
        self.flush()
        _clear_layout(self.var_layout)

        current_vars = {
            k: (v, "Unknown") for k, v in
            self.console.get_protected().items()
        }

        current_vars.update(self.console_vars)

        new_registry = {}
        for key, (val, desc) in current_vars.items():
            new_registry[key] = val

            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(0, 0, 0, 0)

            key_label = QLabel(key)
            key_label.setMinimumWidth(VAR_NAME_W)
            key_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            key_label.setFont(CONSOLE_FONT)
            row_layout.addWidget(key_label, stretch=0)

            desc_label = QLabel(desc)
            desc_label.setWordWrap(True)
            row_layout.addWidget(desc_label, stretch=1)
            self.var_layout.addLayout(row_layout)

        self.add_protected(**new_registry)
        self.var_layout.addStretch()

    @single_buffer
    def execute_line(self):
        src = self.input.text()
        self.input.clear()
        
        push = True
        if src.strip() == "":
            self.indent = self.indent - 1 if self.indent > 0 else 0

            if self.indent > 0:
                push=False
            
            src = src.strip()
        
        self.output.append(f">>>{' .' * self.indent} {src}")

        if not push:
            return
        
        src = "    " * self.indent + src.strip()
        if src.strip().endswith(":"):
            self.indent += 1
            self.output.append(f">>>{' .' * self.indent}")

        self.console.push(src)

    def handle_exception(self, exctype, value, tb):
        # format full traceback
        formatted = "".join(traceback.format_exception(exctype, value, tb))

        self.output.append(formatted)

    def restart(self):

        if not self.exit_dlg(title="Restart Python Console"):
            return

        self.exit_override()
        self.parent()._open_console()

    def exit_dlg(self, title="Exit Python Console"):
        options = [
            (title, self.exit_override),
        ]

        if self.persistent:
            options.append(("Keep Output and Hide", self.close))


        resp = self.parent()._custom_popup(
            title,
            f"{title}?\n\n"
            "All console output will be lost.",
            *options,
            cancel=True
        )

        if resp:
            resp()
            return resp == self.exit_override
        
        return False
        

    def exit_override(self):
        self.persistent = False
        self.close()

    def closeEvent(self, event):
        if self.persistent:
            event.ignore()
            self.hide()
        else:
            if (hasattr(self.parent(), "__python_console__") and
                self.parent().__python_console__ is self):
                self.parent().__python_console__ = None
            super().closeEvent(event)
        
        win = self.parent()
        file = win.root_block

        win._flag_edited(file)
        win.refresh_tree()
        

