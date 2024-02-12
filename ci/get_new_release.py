import subprocess
from enum import Enum

import typer
from git import Repo
from packaging import version


class BumpType(str, Enum):
    CHORE = "chore"
    PATCH = "patch"
    MINOR = "minor"
    MAJOR = "major"


class ReleaseType(str, Enum):
    RELEASE_CANDIDATE = "rc"
    FINAL = "final"


INITIAL_TAG = "v0.1.0"
INITIAL_RC_TAG = "v0.1.0rc0"


def get_git_root() -> str:
    raw = subprocess.Popen(
        ["git", "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE
    ).communicate()[0]
    return raw.rstrip().decode("utf-8")


def get_current_tag() -> str:
    """Gets current tag from list of repo tags

    Returns:
        str: current tag, e.g. "v0.1.0", "", "v0.1.0rc2"
    """
    repo = Repo(get_git_root(), search_parent_directories=True)
    tags = [str(tag) for tag in repo.tags]
    if len(tags) == 0:
        return ""
    tags.sort(key=lambda x: version.Version(x))
    return tags[-1]


def is_current_tag_rc(current_tag: str) -> bool:
    return "rc" in current_tag


def print_tag(tag: str, tag_type: str = "Current") -> str:
    print(f"{tag_type} tag:\n{tag}")


def bump_version(
    current_version: str, bump_type: BumpType, release_type: ReleaseType
) -> str:
    major, minor, patch = [int(x) for x in current_version.split(".")]

    match bump_type:
        case BumpType.MAJOR:
            major += 1
            minor = 0
        case BumpType.MINOR:
            minor += 1
            patch = 0
        case BumpType.PATCH:
            patch += 1
        case _:
            raise ValueError(f"Check the release type {release_type}")

    return f"v{major}.{minor}.{patch}"


def bump_tag(current_tag: str, bump_type: BumpType, release_type: ReleaseType) -> str:
    # Validate input
    if len(current_tag) <= 5 or "v" not in current_tag:
        raise ValueError(f"Error parsing current tag {current_tag}")

    current_version = current_tag.replace("v", "").split("rc")[0]
    if is_current_tag_rc(current_tag):
        rc_bit = int(current_tag.split("rc")[1])
    else:
        rc_bit = ""

    # if current tag is release candidate, no version bump is needed
    if is_current_tag_rc(current_tag) and release_type == ReleaseType.RELEASE_CANDIDATE:
        rc_bit += 1
        return f"v{current_version}rc{rc_bit}"
    elif is_current_tag_rc(current_tag) and release_type == ReleaseType.FINAL:
        return f"v{current_version}"

    new_version = bump_version(current_version, bump_type, release_type)

    if release_type == ReleaseType.RELEASE_CANDIDATE:
        new_version = f"{new_version}rc0"

    return new_version


"""
def main(
    bump_type: BumpType = typer.Argument(metavar="bump_type"),
    release_type: ReleaseType = typer.Argument(metavar="release_type"),
) -> None:
    current_tag = get_current_tag()
    print_tag(current_tag)

    # Initialize tags
    if current_tag == "":
        if release_type == ReleaseType.FINAL:
            new_tag = INITIAL_TAG
        else:
            new_tag = INITIAL_RC_TAG
        print_tag(new_tag, "New")
        return

    # If Chore -> skip
    if bump_type == BumpType.CHORE:
        print_tag(current_tag)
    else:
        new_tag = bump_tag(str(current_tag), bump_type, release_type)
        print_tag(new_tag, "New")
"""


def main() -> None:
    get_current_tag()


if __name__ == "__main__":
    typer.run(main)
