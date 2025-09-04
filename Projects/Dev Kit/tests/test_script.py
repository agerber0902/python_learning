# Test all the project imports
import sys
import platform
import requests
from pathlib import Path    # This is tested in config parser

# Test config parser
from configparser import ConfigParser
def test_config_parser():
    print("Testing ConfigParser from configparser...")
    try:
        here = Path(__file__).parent
        config_path = here / "test_config.ini"

        print(f"Testing config file: {config_path}")

        config = ConfigParser(interpolation=None)
        files_read = config.read(config_path)
        if not files_read:
            print(f"⚠️ Warning: '{config_path}' not found or could not be read.")

        print(config["test"]["TEST_CONFIG_VALUE"])

        print("✅ Testing ConfigParser from configparser complete.")
    except Exception as e:
        print(f"❌ Error reading test_config.ini: {e}")

def main():
    print("Python Test Script is running...")
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")

    try:
        print("Trying Request...")
        response = requests.get("https://api.github.com", timeout=5)
        print(f"✅ GitHub API status: {response.status_code}") # NOTE: we dont care about the status code, just want to see request import work
    except Exception as e:
        print("❌ Request failed: {e}")

    test_config_parser()

if __name__ == "__main__":
    main()