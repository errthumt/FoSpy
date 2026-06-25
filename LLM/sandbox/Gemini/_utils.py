def _get_key(env_var_name="FoSpy_Testing_API_key", fallback=True):
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
        except Exception as e:
            print("Could not get API key through Colab secrets. Exception:")
            print(e)


    
    target_path = Path(os.path.abspath(__file__)).parent / f"secrets/{env_var_name}.txt"
    print(f"\nLooking for cached key at '{target_path}'...")
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if not target_path.exists():
        if fallback:
            print("Could not find key file. Paste your API key when requested.")

            target_path.write_bytes(input("API key: ").encode("utf-8"))

            print(f"\nCached key file to runtime at '{target_path}'")
        else:
            print("Could not find key. Returning None.")
            return None
    
    print("API key read from cached file.")
    return target_path.read_text()
    

    
        
    
    
