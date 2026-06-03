import os
import zipfile

def zipdir(path, zipname):
    with zipfile.ZipFile(zipname, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, path)
                z.write(full_path, rel_path)

def pkg_all():
    from .._utils import ch2repo
    ch2repo()

    zipdir("internal/dev_build/windows", "mkdocs/docs/file_download/windows_dev_setup.zip")
