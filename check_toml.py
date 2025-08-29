import tomllib  # Python 3.11+ এ built-in

with open("droidbuilder.toml", "rb") as f:
    try:
        data = tomllib.load(f)
        print("✅ TOML parsed successfully!")
        print(data)
    except Exception as e:
        print("❌ TOML parse error:", e)
