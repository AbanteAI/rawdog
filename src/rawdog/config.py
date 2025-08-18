import yaml

from rawdog import __version__
from rawdog.utils import rawdog_dir

config_path = rawdog_dir / "config.yaml"


default_config = {
    "llm_api_key": None,
    "llm_base_url": None,
    "llm_model": "claude-sonnet-4-20250514",
    "llm_custom_provider": None,
    "llm_temperature": 1.0,
    "retries": 2,
    "leash": False,
}
setting_descriptions = {
    "retries": "If the script fails, retry this many times before giving up.",
    "leash": "Print the script before executing and prompt for confirmation.",
}


_config = None


def read_config_file():
    global _config
    if _config is None:
        if config_path.exists():
            with open(config_path, "r") as f:
                _config = yaml.safe_load(f)
            valid_fields = set(default_config.keys())
            present_fields = set(_config.keys())
            missing_fields = valid_fields - present_fields
            extra_fields = present_fields - valid_fields
            if missing_fields:
                print(f"Updating config file {config_path} for version {__version__}:")
                for k in missing_fields:
                    print(f"  + {k}: {default_config[k]}")
                    _config[k] = default_config[k]
            if extra_fields:
                print(f"Warning: {extra_fields} are not valid config fields. Ignoring.")
            if missing_fields or extra_fields:
                with open(config_path, "w") as f:
                    yaml.safe_dump(_config, f)
        else:
            _config = default_config.copy()
            with open(config_path, "w") as f:
                yaml.safe_dump(_config, f)
    return _config


def add_config_flags_to_argparser(parser):
    for k in default_config.keys():
        normalized = k.replace("_", "-")
        if normalized in ["dry-run", "pip-model"]:
            print(f"Warning: {normalized} is deprecated, ignoring")
        if normalized in setting_descriptions:
            help_text = setting_descriptions[k]
        else:
            help_text = f"Set the {normalized} config value"
        if default_config[k] is False:
            parser.add_argument(f"--{normalized}", action="store_true", help=help_text)
        else:
            parser.add_argument(f"--{normalized}", default=None, help=help_text)


def get_config(args=None):
    config = read_config_file()
    if args:
        config_args = {
            k.replace("-", "_"): v
            for k, v in vars(args).items()
            if k in default_config and v is not None and v is not False
        }
        config = {**config, **config_args}
    return config
