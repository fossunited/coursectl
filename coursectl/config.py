import configparser
from pathlib import Path

CONFIG_FILE_PATH = "~/.config/frappe/config"

def write_config(profile, values):
    """Write the confiuration to config 
    """
    p = Path(CONFIG_FILE_PATH).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    config = configparser.ConfigParser()
    config.read(str(p))
    config[profile] = values
    with p.open("w") as f:
        config.write(f)
    print("write config to", p)


def read_config(profile):
    """Reads the confiuration from config file ~/.config/frappe/config 
    """
    p = Path(CONFIG_FILE_PATH).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    config = configparser.ConfigParser()
    config.read(str(p))

    if config.has_section(profile):
        return dict(config.items(profile))
    else:
        return {}