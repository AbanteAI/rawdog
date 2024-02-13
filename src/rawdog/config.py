import yaml

from rawdog.utils import rawdog_dir

config_path = rawdog_dir / "config.yaml"


default_config = {
    "llm_api_key": None,
    "llm_base_url": None,
    "llm_model": "gpt-4-turbo-preview",
    "llm_custom_provider": None,
    "llm_temperature": 1.0,
}


_config = None


def read_config_file():
    global _config
    if _config is None:
        if config_path.exists():
            with open(config_path, "r") as f:
                _config = yaml.safe_load(f)
            # These fields may be null in older config files
            for field in ("llm_model", "llm_temperature"):
                if not _config.get(field):
                    _config[field] = default_config[field]
        else:
            _config = default_config.copy()
            with open(config_path, "w") as f:
                yaml.safe_dump(_config, f)
    return _config


def add_config_flags_to_argparser(parser):
    for k in default_config.keys():
        parser.add_argument(f"--{k}", default=None, help=f"Set the {k} config value")


def get_config(args=None):
    config = read_config_file()
    if args:
        config_args = {
            k: v for k, v in vars(args).items() if k in default_config and v is not None
        }
        config = {**config, **config_args}
    return config
