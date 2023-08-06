"""Module to resolve includes of various types."""
import logging
import os
import shutil
import subprocess
import tempfile
import typing as t
from pathlib import Path

log = logging.getLogger(__name__)


def get_profile(path: Path, include: str) -> Path:
    """Get a profile from an include string.

    Includes can be one of the following:
    - Absolute path to an include
    - Relative path to an include in the same
      directory as the provided path
    - A git include with the format [git_repo]$[path/to/file]

    Args:
        path (Path): current profile path. The parent directory
            of this path will be used to resolve relative include.
        include (str): include string

    Returns:
        Path: path to profile
    """
    if "$" in include:
        return get_git_profile(include)
    include_path = Path(include)
    if include_path.is_absolute():
        return include_path
    resolve_path = path.parents[0] / include_path
    return resolve_path


def get_git_profile(include: str) -> Path:
    """Get a profile from a git source.

    Consumes includes with the format [git_repo]$[path/to/file].

    Args:
        include (str): Git source with the proper format.

    Returns:
        Path: path to profile

    Notes:
        This repo must be public
    """
    # Check for git executable
    git = shutil.which("git")
    if git:
        log.debug(f"Found git at {git}")
    else:
        raise RuntimeError(f'Need to have "git" installed to use git include {include}')
    # Get repo and path to file in repo
    parts: t.List[str] = include.split("$")
    with tempfile.TemporaryDirectory() as tmpdir:
        dir_path = Path(tmpdir).resolve()
        args: t.List[str] = ["git", "clone", "--depth", "1"]
        if len(parts) == 3:
            args.extend(["--branch", parts[2]])
        if len(parts) > 1:
            args.append(parts[0])
            path = parts[1]
        else:
            raise ValueError(f"Include {include} is improperly formatted")
        args.append(str(dir_path))
        # Clone the repo
        try:
            subprocess.run(args, check=True)
        except subprocess.CalledProcessError as e:
            log.error(f"Could not clone git dependency {parts[0]}")
            raise RuntimeError from e
        # Return path
        repo_path = dir_path / os.listdir(tmpdir)[0]
        return repo_path / path
