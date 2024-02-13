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


_config = None


def get_config():
    global _config
    if _config is None:
        if config_path.exists():
            with open(config_path, "r") as f:
                _config = yaml.safe_load(f)
        else:
            _config = default_config.copy()
            with open(config_path, "w") as f:
                yaml.safe_dump(_config, f)
    return _config
