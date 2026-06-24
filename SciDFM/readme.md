Scripts in this folder are intended to be run with a uv venv

```bash
python -m pip install uv
uv venv .env
.env/Scripts/activate
pip install -U transformers datasets evaluate accelerate timm torch
```