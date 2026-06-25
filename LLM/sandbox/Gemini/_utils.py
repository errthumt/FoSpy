import asyncio
from pathlib import Path
import os

target_path = Path(os.path.abspath(__file__)).parent / "secrets.json"

def _get_key(env_var_name="FoSpy_Testing_API_key", fallback=True):
    from importlib.util import find_spec

    print(f"Looking for API key with variable name '{env_var_name}'.")

    print(f"\nLooking for os.environ['{env_var_name}']...")
    if os.environ.get(env_var_name, None) is not None:
        print("Found API Key through environment variable.")
        return os.environ[env_var_name]
    
    print("Could not find API key through environment variable.")

    if find_spec("google.colab") is not None:
        print(f"\nLooking in Colab secrets with google.colab.userdata.get('{env_var_name}')...")
        try:
            from google.colab import userdata
            key = userdata.get(env_var_name)
            print("Found API key in Colab secrets.")
            return key
        except Exception as e:
            print("Could not get API key through Colab secrets. Exception:")
            print(e)


    print(f"\nLooking for cached secrets at '{target_path}'...")
    

    if not target_path.exists() and fallback:
        print("Could not find secrets. Delegating to secrets.json upload.")

        return "upload"
    
    return _get_key_from_file(env_var_name, target_path, fallback)
    


def _get_key_from_file(env_var_name,filepath=target_path, fallback=True):
    print(f"\nLooking for '{env_var_name}' key in cached secrets...")
    try:
        import json
        with open(target_path, "r") as f:
            secrets = json.load(f)
            key = secrets[env_var_name]
            print("Found API key in cached secrets.")
            return key
    except Exception as e:
        if fallback:
            raise Exception(f"Could not get API key through cached secrets. Exception: {e}")
        else:
            print("Could not get API key through cached secrets. Exception:")
            print(e)
            print("\n Returning None.")
    
    return None

def _get_key_from_upload(env_var_name, upload):
    target_path.parent.mkdir(parents=True, exist_ok=True)
    value = upload.value
    if not value:
        raise Exception("No file uploaded.")
    if isinstance(value, tuple):
        # ipywidgets v8+ layout
        file_info = value[0]
        # In v8, 'content' is a memoryview object, cast it to bytes
        file_bytes = bytes(file_info["content"])
    else:
        # ipywidgets v7 layout (fallback)
        file_name = list(value.keys())[0]
        file_bytes = value[file_name]["content"]

    with open(target_path, "wb") as f:
        f.write(file_bytes)

    return _get_key_from_file(env_var_name, target_path)


        
    
    
