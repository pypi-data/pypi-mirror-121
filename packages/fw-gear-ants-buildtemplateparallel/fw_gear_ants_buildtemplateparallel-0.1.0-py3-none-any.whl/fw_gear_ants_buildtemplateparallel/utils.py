import fnmatch
import logging
import re
import sys
import typing as t
from functools import partial
from pathlib import Path

import backoff
import flywheel
from flywheel_gear_toolkit.utils.curator import HierarchyCurator
from flywheel_gear_toolkit.utils.datatypes import Container, PathLike
from flywheel_gear_toolkit.utils.walker import Walker
from joblib import Parallel, delayed

log = logging.getLogger(__name__)


class FileMatcher:
    def __init__(
        self,
        tags: t.List = None,
        regex_pattern: str = None,
        glob_pattern: str = None,
        filetype: str = None,
    ):
        """A Class to match flywheel.FileEntry by tags, filename or filetype."""
        self.tags = tags if tags else []
        if not isinstance(self.tags, list):
            raise TypeError(f"Tags must be of type list, {type(self.tags)} found.")

        self.regex_pattern = regex_pattern if regex_pattern else ""
        self.glob_pattern = glob_pattern if glob_pattern else ""
        self.filetype = filetype
        self.reg = None  # regex compiled
        self._preprocess_regex()

    def _preprocess_regex(self):
        """Build regex from `regex_pattern` and `glob_pattern`"""
        regex = self.regex_pattern
        if self.glob_pattern:
            try:
                regex_glob = fnmatch.translate(self.glob_pattern)
            except SyntaxError:
                log.error(f"Glob Pattern syntax is incorrect: {self.glob_pattern}")
                sys.exit(1)
            except Exception:
                log.exception(
                    f"Glob Pattern was not able to be translated to regex: "
                    f"{self.glob_pattern}"
                )
                sys.exit(1)

            if self.regex_pattern:
                regex = "|".join([regex, regex_glob])
            else:
                regex = regex_glob
        try:
            self.reg = re.compile(regex)
        except re.error:
            log.error(f"Invalid regular expression {regex}")
            sys.exit(1)

    def match(self, file: flywheel.FileEntry):
        """Returns True if file matches, False otherwise."""
        if self.filetype and file.type != self.filetype:
            return False

        if self.tags and not all([t in file.tags for t in self.tags]):
            return False

        if self.reg and not self.reg.match(file.name):
            return False
        return True


class FileFinder(HierarchyCurator):
    """A curator to find files matching regex filename and tags."""

    def __init__(
        self,
        *args,
        regex_pattern: str = None,
        glob_pattern: str = None,
        tags: t.List = None,
        filetype: str = None,
        **kwargs,
    ):
        super(FileFinder, self).__init__(*args, **kwargs)
        self.files = []
        self.file_matcher = FileMatcher(
            tags=tags,
            regex_pattern=regex_pattern,
            glob_pattern=glob_pattern,
            filetype=filetype,
        )

    def curate_acquisition(self, acquisition: flywheel.Acquisition):
        for f in acquisition.files:
            if self.file_matcher.match(f):
                self.files.append(f)


def find_matching_files(
    root: Container,
    tags: t.List = None,
    regex: str = None,
    glob_pattern: str = None,
    filetype: str = None,
):
    """Returns files matching tags/regex"""
    my_walker = Walker(root)
    finder = FileFinder(
        regex_pattern=regex, glob_pattern=glob_pattern, tags=tags, filetype=filetype
    )
    for container in my_walker.walk():
        finder.curate_container(container)
    return finder.files


def is_error_in(exc, errors=None):
    """Return True if exception status is in errors."""
    if errors is None:
        errors = []
    if hasattr(exc, "status"):
        if exc.status in errors:
            return True
    return False


def is_error_not_in(exc, errors=None):
    """Return True if exception status is NOT in errors."""
    return not is_error_in(exc, errors=errors)


@backoff.on_exception(
    backoff.expo,
    flywheel.rest.ApiException,
    max_tries=5,
    giveup=partial(is_error_not_in, errors=[500, 502, 504]),
)
def download_file(f: flywheel.FileEntry, dst_path: PathLike = None):
    """Download file robustly to dst_path

    Args:
        f (flywheel.FileEntry): A Flywheel file.
        dst_path (PathLike): A Path-like.

    Returns:
        (Path-like): Returns the destination path.
    """
    dst_path = Path(dst_path)
    if dst_path.exists():
        raise ValueError(f"Destination path already exists {f}")
    if not dst_path.parent.exists():
        dst_path.parent.mkdir(parents=True, exist_ok=True)
    log.info(
        f"Downloading  {f.name} from {f.parent_ref['type']} {f.parent_ref['id']}..."
    )
    f.download(dst_path)
    return dst_path


def download_files(files: t.List[flywheel.FileEntry], dest_dir: PathLike = None):
    """Download files to output_dir under file.id / file.name.

    Args:
        files (list): List of flywheel.FileEntry.
        dest_dir (PathLike): The folder where to download the files.

    Returns:
        list: A list containing all file paths.
    """
    dest_dir = Path(dest_dir)
    if not dest_dir.exists():
        log.debug(f"Creating output folder {dest_dir}")
        dest_dir.mkdir(parents=True)

    # buildtemplateparallel seems to require all the nifti to be in the same
    # location and being passed with a wildcard character. Building mapping here
    file_mapping = []
    for f in files:
        file_mapping.append((f, Path(dest_dir) / f"{f.id}-{f.name}"))

    res = Parallel(n_jobs=-1, prefer="threads")(
        delayed(download_file)(f, Path(dest_dir) / f"{f.id}-{f.name}") for f in files
    )
    return res
