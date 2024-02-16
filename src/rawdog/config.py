import yaml

from rawdog import __version__
from rawdog.utils import rawdog_dir

config_path = rawdog_dir / "config.yaml"


default_config = {
    "llm_api_key": None,
    "llm_base_url": None,
    "llm_model": "gpt-4-turbo-preview",
    "llm_custom_provider": None,
    "llm_temperature": 1.0,
    "retries": 2,
    "leash": False,
}
# NOTE: dry-run was replaced with leash on v0.1.4. There is code below to handle
# the transition, which should be removed eventually.

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
            missing_fields = {
                k: v
                for k, v in default_config.items()
                if k not in _config or (v is not None and _config[k] is None)
            }
            if missing_fields:
                print(f"Updating config file {config_path} for version {__version__}:")
                if "leash" in missing_fields and _config.get("dry_run"):
                    missing_fields["leash"] = True
                    del _config["dry_run"]
                    print(
                        "  - dry_run: deprecated on v0.1.4, setting leash=True instead"
                    )
                for k, v in missing_fields.items():
                    print(f"  + {k}: {v}")
                    _config[k] = v
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
        if k in setting_descriptions:
            help_text = setting_descriptions[k]
        else:
            help_text = f"Set the {normalized} config value"
        if default_config[k] is False:
            parser.add_argument(f"--{normalized}", action="store_true", help=help_text)
        else:
            parser.add_argument(f"--{normalized}", default=None, help=help_text)
    parser.add_argument(
        "--dry-run", action="store_true", help="Deprecated, use --leash instead)"
    )


def get_config(args=None):
    config = read_config_file()
    if args:
        config_args = {
            k.replace("-", "_"): v
            for k, v in vars(args).items()
            if k in default_config and v is not None and v is not False
        }
        config = {**config, **config_args}
    if config.get("dry_run"):
        del config["dry_run"]
        print("Warning: --dry-run is deprecated, use --leash instead")
    return config
