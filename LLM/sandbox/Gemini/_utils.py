async def _get_key(env_var_name="FoSpy_Testing_API_key", fallback=True):
    import os
    from importlib.util import find_spec
    from pathlib import Path

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


    
    target_path = Path(os.path.abspath(__file__)).parent / "secrets.json"
    print(f"\nLooking for cached secrets at '{target_path}'...")
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if not target_path.exists():
        if fallback:
            print("Could not find secrets. Upload secrets.json")

            from ipywidgets import FileUpload
            from IPython.display import display
            import asyncio 

            upload = FileUpload(accept=".json", multiple=False)
            display(upload)

            while len(upload.value) == 0:
                await asyncio.sleep(1)
            
            with open(target_path, "wb") as f:
                f.write(upload.value[0]["content"])

            print(f"\nCached secrets to runtime at '{target_path}'")
    
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
            raise Exception("Could not get API key through cached secrets. Exception: {e}")
        else:
            print("Could not get API key through cached secrets. Exception:")
            print(e)
            print("\n Returning None.")
    
    return None
    

    
        
    
    
