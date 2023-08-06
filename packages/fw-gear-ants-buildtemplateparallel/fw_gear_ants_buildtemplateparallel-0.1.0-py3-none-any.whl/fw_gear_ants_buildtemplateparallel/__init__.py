"""The fw_gear_ants_buildtemplateparallel package."""
from importlib.metadata import version
from pathlib import Path

try:
    __version__ = version(__package__)
except:  # pragma: no cover
    pass

TEMPLATES_DIR = Path(__file__).parent / "templates"
