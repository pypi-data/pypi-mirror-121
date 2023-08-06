"""Parser module to parse gear config.json."""
import logging
import sys
import typing as t

from flywheel_gear_toolkit import GearToolkitContext
from flywheel_gear_toolkit.utils.datatypes import Container

log = logging.getLogger(__name__)


def parse_config(
    context: GearToolkitContext,
) -> t.Tuple[str, str, t.List[str], str, Container]:
    """Parse input context.

    Ars:
        GearToolkitContext: The gear toolkit context.

    Returns:
        str: A string representing a regular expression.
        str: A string representing a glob pattern expression.
        list: A list of string.
        Container: A Flywheel container.
    """
    regex_pattern = context.config.get("Input Regex")
    glob_pattern = context.config.get("Input Glob Pattern")
    tags = context.config.get("Input Tags")
    if not tags and not (regex_pattern or glob_pattern):
        log.error(
            "Input Regex or Input Glob or Input Tags must be defined. " "None found."
        )
        sys.exit(1)
    target = context.config.get("Target Template")
    destination_parent = context.get_destination_parent()
    if tags:
        tags = [tag.strip() for tag in tags.split(",")]
    return regex_pattern, glob_pattern, tags, target, destination_parent
