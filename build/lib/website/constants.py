import os


CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(CURRENT_FILE_PATH, "..", "Data")


ESSENTIAL_CONFIG_KEYS = [
    "ACCESS_CODE",
    "SECRET_KEY",
    "SECRET_KEY",
    "run",
    "ACCESS_CODE_HASH",
]
