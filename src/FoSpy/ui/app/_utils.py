import sys
import os
import platform
import importlib.metadata
import urllib.request
from urllib.error import URLError, HTTPError

SUPPORTED_EXTENSIONS = [".fos"]

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


def register_file_extensions() -> bool:
    """
    Registers this application as the default handler for the global list 
    of FoSpy extensions across Windows and Linux.
    
    Returns True if registration succeeded for all extensions, False otherwise.
    """
    # Determine the FoSpy version
    fospy_version = _get_version()

    # Define the required static properties
    app_id = f"FoSpy GUI {fospy_version}"
    description = "FoS-style viewer using the FoSpy framework"

    # Determine the system executable path
    python_exe = sys.executable

    # Build the OS execution command (OS specific injection handled inside loops)
    win_command = f'{python_exe} -m FoSpy.ui.app "%1"'
    linux_command = f'{python_exe} -m FoSpy.ui.app "%f"'

    # --- Windows Registry Mapping ---
    if platform.system() == "Windows":
        import winreg
        try:
            # First, register the App ID properties and its open command
            cmd_key_path = f"Software\\Classes\\{app_id}\\shell\\open\\command"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, cmd_key_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, win_command)
            
            desc_key_path = f"Software\\Classes\\{app_id}"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, desc_key_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, description)

            # Map every extension in the global list to this App ID
            for ext in SUPPORTED_EXTENSIONS:
                if not ext.startswith('.'):
                    ext = f".{ext}"
                ext_key_path = f"Software\\Classes\\{ext}"
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, ext_key_path) as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, app_id)

            # Broadcast change to system shell
            import ctypes
            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
            return True
            
        except Exception as e:
            print(f"Windows extension registration failed: {e}")
            return False

    # --- Linux MIME Handling ---
    elif platform.system() == "Linux":
        import subprocess
        try:
            apps_dir = os.path.expanduser("~/.local/share/applications")
            os.makedirs(apps_dir, exist_ok=True)
            
            desktop_filename = f"{app_id.lower().replace(' ', '_')}.desktop"
            desktop_file_path = os.path.join(apps_dir, desktop_filename)
            
            mime_type = f"application/x-{app_id.lower().replace(' ', '-')}"
            
            with open(desktop_file_path, "w") as f:
                f.write("[Desktop Entry]\n")
                f.write("Type=Application\n")
                f.write(f"Name={description}\n")
                f.write(f"Exec={linux_command}\n")
                f.write(f"MimeType={mime_type};\n")
                f.write("NoDisplay=true\n")


            for ext in SUPPORTED_EXTENSIONS:
                subprocess.run(["xdg-mime", "default", desktop_filename, mime_type], check=True)
                
            return True
            
        except Exception as e:
            print(f"Linux extension registration failed: {e}")
            return False

    return False