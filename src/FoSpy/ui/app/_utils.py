import sys
import os
import platform
import subprocess
import importlib.metadata
import urllib.request
import argparse
import inspect
import pathlib

import types
from typing import Any, Union, get_args, get_origin
from urllib.error import URLError, HTTPError
from ...blocks.files import EXT_READ_MAP, EXT_DESC_MAP

from PySide6.QtWidgets import(
    QDialog,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QDialogButtonBox,
    QLineEdit,
    QComboBox,
)

asset_dir = pathlib.Path(__file__).parent / "assets"

ASSETS = {
    "splash": asset_dir / "splash.png",
    "compatible packages": asset_dir / "compatible_packages.txt"
}

SKIP_ARG = object()

SUPPORTED_EXTENSIONS = ["." + ext for ext in EXT_READ_MAP]

class TextInputDialog(QDialog):
    def __init__(self, title, prompt, *labels, parent=None, **dropdowns:list[str]|dict[str, Any]):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.dropdowns = dropdowns

        layout = QVBoxLayout(self)

        prompt_label = QLabel(prompt)
        prompt_label.setWordWrap(True)
        layout.addWidget(prompt_label)

        self.edits = {}

        for lb in labels:
            if lb in self.edits:
                raise ValueError("Text/Dropdown labels must be unique")

            row_layout = QHBoxLayout()

            label = QLabel(lb)
            row_layout.addWidget(label)

            edit = QLineEdit()
            row_layout.addWidget(edit)
            self.edits[lb] = edit

            layout.addLayout(row_layout)

        for lb, options in dropdowns.items():
            if lb in labels:
                raise ValueError("Text/Dropdown labels must be unique")
            
            row_layout = QHBoxLayout()

            label = QLabel(lb)
            row_layout.addWidget(label)

            if isinstance(options, dict):
                drop_options = list(options.keys())
            else:
                drop_options = options

            drop = QComboBox()
            drop.addItems(drop_options)
            row_layout.addWidget(drop)
            self.edits[lb] = drop

            layout.addLayout(row_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _get_result(self, label):
        edit = self.edits[label]

        if isinstance(edit, QLineEdit):
            return edit.text()

        options = self.dropdowns[label]

        if isinstance(options, list):
            return edit.currentText()

        return options[edit.currentText()]

    def get_results(self):
        results = {k: self._get_result(k) for k in self.edits}

        if len(results) == 1:
            return results[next(iter(results))]

        return results

def _resolve_param_type(annotation: Any) -> Any:
    """Extracts a callable scalar type from Unions or standard type hints."""
    if annotation == inspect.Parameter.empty:
        return str

    origin = get_origin(annotation)
    
    # Check for Union types (e.g., Union[int, str] or int | str)
    if origin is Union or (hasattr(types, "UnionType") and origin is types.UnionType):
        args = get_args(annotation)
        # Filter out NoneType to handle Optional types gracefully (e.g., int | None)
        non_none_args = [arg for arg in args if arg is not type(None)]
        
        if non_none_args:
            # Take the first available type in the Union
            first_type = non_none_args[0]
            # Handle nested generics if necessary (like list[int] or PathLike[str])
            nested_origin = get_origin(first_type)
            return nested_origin if nested_origin is not None else first_type
            
        return str

    # Handle standard single types with generics (like os.PathLike[str])
    if origin is not None:
        return origin

    return annotation


def _get_parser(desc, func:Any, *shortcuts:tuple[str, str]):
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)

    shortcut_map = {long: short for long, short in shortcuts}

    signature = inspect.signature(func)

    req_in_front = {name: param for name, param in signature.parameters.items() if param.default == inspect.Parameter.empty}
    req_in_front.update(signature.parameters)

    for name, param in req_in_front.items():
        is_required = param.default == inspect.Parameter.empty

        if name in ("self", "cls"):
            continue

        param_type = _resolve_param_type(param.annotation) if param.annotation != inspect.Parameter.empty else str

        cli_name = name.lstrip("_").replace("_", "-")
        flags = ["--" + cli_name]
        if name in shortcut_map:
            flags.insert(0, "-" + shortcut_map[name])

        if param_type is bool:
            default_val = param.default if param.default != inspect.Parameter.empty else False
            parser.set_defaults(**{name: default_val})

            group = parser.add_mutually_exclusive_group(required=is_required)
            group.add_argument(
                *flags,
                action="store_true",
                dest=name,
                help=f"Enable {name} (Default: {default_val})"
            )

            group.add_argument(
                f"--no-{cli_name}" if not cli_name.startswith("no") else f"--{cli_name[2:].lstrip('-')}",
                action="store_false",
                dest=name,
                help=f"Disable {name} (Default: {default_val})"
            )

        else:
            pos_dest = f"__pos__{name}"
            flag_dest = f"__flag_{name}"

            group = parser.add_mutually_exclusive_group(
                required=is_required
            )

            if not is_required:
                group.add_argument(
                    *flags,
                    action="store",
                    type=param_type,
                    dest=flag_dest,
                    metavar=cli_name,
                    help=f"Set {name} (Default: {param.default})",
                    default=SKIP_ARG
                )

            group.add_argument(
                pos_dest,
                metavar=cli_name,
                nargs=1 if is_required else "?",
                action="store",
                type=param_type,
                help=f"Positional arg for {name}"
            )


    return parser

def _find_doc(func):
    if isinstance(func, type):
        return inspect.getdoc(func.__init__)
    return inspect.getdoc(func)

def add_parser(*shortcuts:tuple[str, str], desc:str="CLI Parser for FoSpy function.", args_to:callable=None) -> callable:
    def decorator(func, shortcuts=shortcuts, desc=desc, args_to=args_to):
        func_doc = _find_doc(func)
        args_to_doc = _find_doc(args_to) or ""

        if func_doc is None:
            func_doc = ""

        if args_to is None:
            args_to = func
        elif func_doc != "":
            func_doc += "\n\n===== Arguments sent to: =====\n\n"

        func_doc += args_to_doc

        if desc != "":
            desc += "\n\n" + func_doc


        parser = _get_parser(desc, args_to, *shortcuts)

        def decorated(*args, __parser__=parser, **kwargs):
            if args or kwargs:
                return func(*args, **kwargs)
            
            args = __parser__.parse_args()
            args = vars(args)

            cleaned = {}
            for k, v in args.items():
                if k.startswith(("__pos__", "__flag_")):
                    k = k[7:]
                cleaned[k] = v

            return func(**cleaned)

        return decorated
    return decorator






def _get_label(blk, i=None):        
    id_key, id_txt = blk.get_id()
    label = f"{i} - " if i is not None else ""
    label += id_txt

    if id_key is None:
        label += " Object"

    return label

def _get_template_label(blk):
    id_key, id_txt = blk.get_id()

    label = "🏷️"
    label += id_txt

    if id_key is None:
        label += " Object"

    return label

def _get_version():
    try:
        vers = importlib.metadata.version("FoSpy")
    except importlib.metadata.PackageNotFoundError:
        vers = "v?"
    if "+" in vers:
        vers = vers.split("+")[0] + " (unstable)"

    return vers

def _find_docs_url(version):
    docs_root = "https://errthumt.github.io/FoSpy/"
    if version.endswith("(unstable)"):
        return docs_root + "incoming/"
    
    try:
        url = docs_root + "v" + version + "/" 

        req = urllib.request.Request(
            url,
            method="HEAD",
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                return url
        

    except (URLError, HTTPError, TimeoutError):
        pass
    
    # fall back to latest release
    return docs_root + "latest/"

def register_app() -> bool:
    """
    Registers a compiled launcher executable or App Bundle as the default handler
    for FoSpy file extensions across Windows, Linux, and macOS.
    
    Returns True if registration succeeded, False otherwise.
    """

    success = _main_registration()
    if not success:
        return False
    
    from FoSpy.config import values as cfg
    cfg.APP.registered = True
    cfg.APP.save()
    return True

def add_to_start():
    success = _main_shortcut_registration()
    if not success:
        return False

    from FoSpy.config import values as cfg
    cfg.APP.start_menu = True
    cfg.APP.save()

    return success

def register_dlg():
    from ...config import values as cfg
    from .window import MainWindow, DLG_ESCAPE

    if not cfg.get("APP.registered", False):
        response = MainWindow._custom_popup(
            "FoSpy GUI - Registration Recommended",
            "This GUI is not registered as a handler for FoS-style file extensions. "
            "Would you like to register it now?\n\n"

            "After registration, supported files can be opened with\n"
            f"right-click > \"Open With\" > {_get_executable(full=False)}\n"
            "(Or similar)\n\n"

            "You can always register later with\n"
            "Help > Add as *.fos Editor",

            ("Yes", True),
            ("No", False),
            ("No, and don't ask again", DLG_ESCAPE),
            default=1,
            cancel=False
        )

        if response is DLG_ESCAPE:
            cfg.APP.registered = True
            cfg.APP.save()

        elif response:
            register_app()

def _get_executable(full=True):
    executable_path = sys.executable

    current_os = platform.system()
    # Fallback/Development environment handling for raw script invocation
    if executable_path.endswith(('python', 'python.exe', 'python3')):
        if current_os == "Windows":
            # Convert standard python.exe path to pip's console/gui script wrapper entry
            executable_path = executable_path.replace("python.exe", "fospy-app.exe")
        else:
            executable_path = executable_path.replace(os.path.basename(executable_path), "fospy-app")

    # Double check that our generated wrapper exists, fallback to standard pathing if not found
    if not os.path.exists(executable_path):
        executable_path = sys.executable

    if full:
        return executable_path
    
    return os.path.basename(executable_path)


import os
import platform
import subprocess

def _main_registration():
    print("Registering FoSpy GUI as a handler for the following extensions...")
    for ext in SUPPORTED_EXTENSIONS:
        print("*" + ext)

    fospy_version = _get_version()

    # 1. Non-unique app ID (Constant) so subsequent runs overwrite old keys/files
    app_id = "FoSpy_GUI"
    
    # 2. Display text for the UI / Open With menus (includes version)
    display_name = f"{app_id} {fospy_version}"

    current_os = platform.system()
    executable_path = _get_executable()

    # --- 1. Windows Implementation ---
    if current_os == "Windows":
        import winreg
        import ctypes
        try:
            win_command = f'"{executable_path}" "%1"'
            exe_basename = os.path.basename(executable_path) # e.g., "fospy-app.exe"
            
            # Explicitly map the literal .exe filename to the versioned display name
            exe_key_path = f"Software\\Classes\\Applications\\{exe_basename}"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, exe_key_path) as key:
                winreg.SetValueEx(key, "FriendlyAppName", 0, winreg.REG_SZ, display_name)
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{exe_key_path}\\shell\\open\\command") as key:
                winreg.SetValue(key, "", winreg.REG_SZ, win_command)

            # Map each extension to its own ProgID to support distinct filetype descriptions
            for ext in SUPPORTED_EXTENSIONS:
                ext_clean = ext.lstrip('.')
                prog_id = f"{app_id}.{ext_clean}"
                
                # Retrieve custom description from map
                description = EXT_DESC_MAP.get(ext_clean, "FoS-Style")
                
                # Register the Custom ProgID
                prog_key_path = f"Software\\Classes\\{prog_id}"
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, prog_key_path) as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, description)
                    winreg.SetValueEx(key, "FriendlyTypeName", 0, winreg.REG_SZ, description)

                # Shell command
                cmd_key_path = f"{prog_key_path}\\shell\\open\\command"
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_key_path) as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, win_command)
                
                # Modern Windows UI fallback for app name
                shell_key_path = f"{prog_key_path}\\shell"
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, shell_key_path, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, "AppName", 0, winreg.REG_SZ, display_name)

                # Link extension to the ProgID
                ext_key_path = f"Software\\Classes\\.{ext_clean}"
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, ext_key_path) as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, prog_id)

            # Clear shell caches
            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
            print("Windows extension registration complete.")
            return True
            
        except Exception as e:
            print(f"Windows extension registration failed: {e}")
            return False

    # --- 2. Linux Implementation ---
    elif current_os == "Linux":
        try:
            # Generate shared-mime-info XML to support custom filetype descriptions in file explorers
            mime_dir = os.path.expanduser("~/.local/share/mime/packages")
            os.makedirs(mime_dir, exist_ok=True)
            mime_xml_path = os.path.join(mime_dir, f"{app_id.lower()}.xml")
            
            mime_types = []
            with open(mime_xml_path, "w") as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">\n')
                for ext in SUPPORTED_EXTENSIONS:
                    ext_clean = ext.lstrip('.')
                    description = EXT_DESC_MAP.get(ext_clean, "FoS-Style")
                    mime_type = f"application/x-{app_id.lower()}-{ext_clean}"
                    mime_types.append(mime_type)
                    
                    f.write(f'  <mime-type type="{mime_type}">\n')
                    f.write(f'    <comment>{description}</comment>\n')
                    f.write(f'    <glob pattern="*.{ext_clean}"/>\n')
                    f.write('  </mime-type>\n')
                f.write('</mime-info>\n')
            
            subprocess.run(["update-mime-database", os.path.expanduser("~/.local/share/mime")], check=True)

            # Create the desktop entry using the versioned display name
            apps_dir = os.path.expanduser("~/.local/share/applications")
            os.makedirs(apps_dir, exist_ok=True)
            
            desktop_filename = f"{app_id.lower()}.desktop"
            desktop_file_path = os.path.join(apps_dir, desktop_filename)
            
            with open(desktop_file_path, "w") as f:
                f.write("[Desktop Entry]\n")
                f.write("Type=Application\n")
                f.write(f"Name={display_name}\n")
                f.write(f"Exec=\"{executable_path}\" %f\n")
                f.write(f"MimeType={';'.join(mime_types)};\n")
                f.write("NoDisplay=true\n")

            # Bind defaults
            for mime_type in mime_types:
                subprocess.run(["xdg-mime", "default", desktop_filename, mime_type], check=True)
            
            print("Linux extension registration complete.")
            return True
        except Exception as e:
            print(f"Linux extension registration failed: {e}")
            return False

    # --- 3. macOS (Darwin) Implementation ---
    elif current_os == "Darwin":
        try:
            if ".app" in executable_path:
                app_bundle_path = executable_path.split(".app")[0] + ".app"
                
                # macOS reads descriptions and app names strictly from Info.plist
                # We dynamically inject the mapped descriptions and versioned app name here.
                import plistlib
                plist_path = os.path.join(app_bundle_path, "Contents", "Info.plist")
                
                if os.path.exists(plist_path):
                    with open(plist_path, 'rb') as f:
                        plist = plistlib.load(f)
                        
                    # Inject display name with version
                    plist["CFBundleName"] = display_name
                    
                    # Inject filetype mappings and descriptions
                    doc_types = []
                    for ext in SUPPORTED_EXTENSIONS:
                        ext_clean = ext.lstrip('.')
                        description = EXT_DESC_MAP.get(ext_clean, "FoS-Style")
                        doc_types.append({
                            "CFBundleTypeName": description,
                            "CFBundleTypeRole": "Editor",
                            "LSHandlerRank": "Owner",
                            "LSItemContentTypes": [f"com.{app_id.lower()}.{ext_clean}"]
                        })
                    
                    plist["CFBundleDocumentTypes"] = doc_types
                    
                    with open(plist_path, 'wb') as f:
                        plistlib.dump(plist, f)
                        
                lsregister_path = "/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister"
                
                if os.path.exists(lsregister_path):
                    subprocess.run([lsregister_path, "-f", app_bundle_path], check=True)
                    print("macOS extension registration complete.")
                    return True
                else:
                    print("macOS lsregister tool path not found.")
                    return False
            else:
                print("macOS registration skipped: App must be built inside a native .app bundle framework.")
                return False
        except Exception as e:
            print(f"macOS extension registration failed: {e}")
            return False

    return False

def _main_shortcut_registration():
    """
    Create a Start Menu shortcut for the FoSpy GUI using the same metadata
    used for extension registration.
    """
    current_os = platform.system()
    if current_os != "Windows":
        print("Start Menu shortcut creation is only supported on Windows.")
        return False

    try:
        fospy_version = _get_version()
        app_id = f"FoSpy_GUI_{fospy_version.replace(' ', '_')}"
        description = "FoS-style viewer using the FoSpy framework"

        # Same executable path logic as extension registration
        executable_path = _get_executable()

        # --- Build Start Menu target folder ---
        start_menu_dir = os.path.join(
            os.environ["APPDATA"],
            r"Microsoft\Windows\Start Menu\Programs\FoSpy"
        )
        os.makedirs(start_menu_dir, exist_ok=True)

        shortcut_path = os.path.join(start_menu_dir, f"{app_id}.lnk")

        # --- Build PowerShell COM call ---
        ps_cmd = [
            "powershell", "-NoProfile", "-Command",
            (
                "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{}');"
                "$s.TargetPath='{}';"
                "$s.WorkingDirectory='{}';"
                "$s.Description='{}';"
                "$s.Save();"
            ).format(
                shortcut_path.replace("\\", "\\\\"),
                executable_path.replace("\\", "\\\\"),
                os.path.dirname(executable_path).replace("\\", "\\\\"),
                description.replace("'", "''")
            )
        ]

        subprocess.check_call(ps_cmd)
        print(f"Start Menu shortcut created at: {shortcut_path}")
        return True

    except Exception as e:
        print(f"Start Menu shortcut creation failed: {e}")
        return False


def _clear_layout(layout, delete=False):
    """Recursively delete all widgets, child layouts, and spacers inside a layout"""
    if layout is None:
        return

    while layout.count():
        item = layout.takeAt(0)

        # Case 1: widget
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
            widget.deleteLater()
            continue

        # Case 2: nested layout
        child_layout = item.layout()
        if child_layout is not None:
            _clear_layout(child_layout, delete=True)
            continue

    if delete:
        layout.setParent(None)
        layout.deleteLater()

