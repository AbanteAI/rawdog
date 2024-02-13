import yaml

from rawdog.utils import rawdog_dir


config_path = rawdog_dir / "config.yaml"


default_config = {
    "llm_api_key": None,
    "llm_base_url": "https://api.openai.com/v1",
    "llm_model": "gpt-4-turbo-preview",
    "llm_custom_provider": None,
    "llm_temperature": 1.0,
}


def load_config():
    if config_path.exists():
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    
    # create and new config
    config = default_config.copy()
    with open(config_path, "w") as f:
        yaml.safe_dump(config, f)
    return config


def update_config(**kwargs):
    config = load_config()
    for k, v in kwargs.items():
        if k not in default_config:
            print(f"Warning: {k} is not a valid config key")
        else:
            config[k] = v
    with open(config_path, "w") as f:
        yaml.safe_dump(config, f)
