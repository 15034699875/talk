import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../db_config.json')

DEFAULT_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'talk'
}

def get_db_config():
    if not os.path.exists(CONFIG_PATH):
        return None
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_db_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f) 