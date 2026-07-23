import tomllib
import subprocess
from pathlib import Path

pyproject = tomllib.loads(Path("pyproject.toml").read_text())
project = pyproject["project"]

all_deps = project.get("optional-dependencies", {})
all_deps["_base"] = project.get("dependencies", [])

freeze_dir = Path("requirements")
freeze_dir.mkdir(exist_ok=True)

app_compatible = Path("src/FoSpy/ui/app/assets/compatible_packages.txt")

for extra, deps in all_deps.items():
    in_file = freeze_dir / f"{extra}.in"
    out_file = freeze_dir / f"{extra}.txt"

    in_file.write_text("\n".join(deps))

    subprocess.run([
        "pip-compile",
        "--no-strip-extras",
        "--output-file",
        str(out_file),
        str(in_file)
    ], check=True)

    print(f"Generated {out_file}")

    if extra == "DEV":
        with open(app_compatible, "w") as f:
            f.write(out_file.read_text())

