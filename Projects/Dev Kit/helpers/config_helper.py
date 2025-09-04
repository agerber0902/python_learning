from pathlib import Path
from configparser import ConfigParser

from helpers.helper import setErrorMessage

# Set up path for config.ini
config_path = "config.ini"

# config error handling
if not Path(config_path).exists():
	raise FileNotFoundError(setErrorMessage(f"Config file not found at {config_path}"))
if not Path(config_path).is_file():
      raise FileNotFoundError(setErrorMessage(f"Config file not found at {config_path}"))

# Read the config file
config = ConfigParser(interpolation=None)
files_read = config.read(config_path)
if not files_read:
    raise FileNotFoundError(setErrorMessage(f"'{config_path}' not found or could not be read."))

# Read the config values
LICENSE_KEY = config['sdk']['LICENSE_KEY']
OUTPUT_PATH = config['sdk']['OUTPUT_PATH']
DB_PATH = config['sdk']['DB_PATH']

# Error handling
if not LICENSE_KEY or not OUTPUT_PATH or not DB_PATH:
      raise ValueError("One of LICENSE_KEY, OUTPUT_PATH, or DB_PATH does not exist")