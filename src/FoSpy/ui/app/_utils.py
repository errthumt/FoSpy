import sys
import os
import platform
import subprocess
import importlib.metadata
import urllib.request
from urllib.error import URLError, HTTPError
from ...blocks.files import EXT_MAP

SUPPORTED_EXTENSIONS = ["." + ext for ext in EXT_MAP]

def _get_label(blk, i=None):        
    id_key, id_txt = blk.get_id()
    label = f"{i} - " if i is not None else ""
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
    
    from FoSpy.config import values as cfg, save_all as cfg_save
    cfg.APP.registered = True
    cfg_save(prompt=False)
    return True

def register_dlg():
    from ...config import values as cfg, save_all as cfg_save
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
            "Help > Add to Apps",

            ("Yes", True),
            ("No", False),
            ("No, and don't ask again", DLG_ESCAPE),
            default=1,
            cancel=False
        )

        if response is DLG_ESCAPE:
            cfg.APP.registered = True
            cfg_save(prompt=False)

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


def _main_registration():
    print("Registering FoSpy GUI as a handler for the following extensions...")
    for ext in SUPPORTED_EXTENSIONS:
        print("*"+ext)

    fospy_version = _get_version()

    app_id = f"FoSpy-App_{fospy_version.replace(' ', '_')}"
    description = "FoS-style viewer using the FoSpy framework"
    current_os = platform.system()

    # --- 1. Find the target executable platform-agnostically ---
    # If frozen via PyInstaller, sys.executable is the compiled binary wrapper.
    # If running via pip entry points, it will point to an executable entry script wrapper.
    executable_path = _get_executable()


    # --- 2. Windows Implementation ---
    if current_os == "Windows":
        import winreg
        try:
            # Format command directly targeting the executable path wrapper
            win_command = f'"{executable_path}" "%1"'
            
            app_key_path = f"Software\\Classes\\{app_id}"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, app_key_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, description)
                
            # Set FriendlyAppName so Windows displays "FoSpy GUI X.X.X" in "Open With"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, app_key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, "FriendlyAppName", 0, winreg.REG_SZ, app_id)

            cmd_key_path = f"{app_key_path}\\shell\\open\\command"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_key_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, win_command)

            for ext in SUPPORTED_EXTENSIONS:
                if not ext.startswith('.'):
                    ext = f".{ext}"
                ext_key_path = f"Software\\Classes\\{ext}"
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, ext_key_path) as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, app_id)

            import ctypes
            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
            print("Windows extension registration complete.")
            return True
            
        except Exception as e:
            print(f"Windows extension registration failed: {e}")
            return False

    # --- 3. Linux Implementation ---
    elif current_os == "Linux":
        try:
            apps_dir = os.path.expanduser("~/.local/share/applications")
            os.makedirs(apps_dir, exist_ok=True)
            
            desktop_filename = f"{app_id.lower()}.desktop"
            desktop_file_path = os.path.join(apps_dir, desktop_filename)
            mime_type = f"application/x-{app_id.lower().replace('_', '-')}"
            
            with open(desktop_file_path, "w") as f:
                f.write("[Desktop Entry]\n")
                f.write("Type=Application\n")
                f.write(f"Name={description}\n")
                f.write(f"Exec=\"{executable_path}\" %f\n")
                f.write(f"MimeType={mime_type};\n")
                f.write("NoDisplay=true\n")

            for ext in SUPPORTED_EXTENSIONS:
                subprocess.run(["xdg-mime", "default", desktop_filename, mime_type], check=True)
            
            print("Linux extension registration complete.")
            return True
        except Exception as e:
            print(f"Linux extension registration failed: {e}")
            return False

    # --- 4. macOS (Darwin) Implementation ---
    elif current_os == "Darwin":
        try:
            # On macOS, associations are handled natively by Launch Services via App Bundles.
            # If the app path contains '.app', we trigger the core registry system.
            if ".app" in executable_path:
                # Isolate the outer absolute folder path to the actual MyApp.app directory
                app_bundle_path = executable_path.split(".app")[0] + ".app"
                
                # Use macOS built-in Launch Services tool to dynamically register the App bundle
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