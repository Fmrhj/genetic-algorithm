import re
from pathlib import Path

import typer

VERSION_FILE = "__version__.py"
PATTERN_VERSION = r'VERSION\s*=\s*"([^"]+)"'

PYPROJECT_TOML_FILE = "pyproject.toml"
PATTERN_PYPROJECT_TOML = r'version\s*=\s*"([^"]+)"'


def set_version(
    package_dir: str = typer.Argument(metavar="package_dir"),
    new_version: str = typer.Argument(metavar="new_version"),
) -> None:
    """Updates the version of a __version__.py file. This is used as the
    version of the pushed package to PyPI

    Args:
        package_dir (Annotated[str, typer.Argument], optional): where to find
          the __version__ file. Defaults to
          typer.Argument( metavar="package_dir" ).

        new_version (str, optional): New tagged vesion.
        Defaults to typer.Argument(metavar="new_version").

    Raises:
        ValueError: if version could not be read from __version__.py file
    """

    def _find_and_replace(file_path: Path, pattern_version: str) -> tuple[str, str]:
        with open(file_path, "r") as f:
            content = f.read()
            match = re.search(pattern_version, content)
            if match:
                version = match.group(1)
                typer.echo(f"Version: {version}", color=typer.colors.BLUE)
                return content, version
            else:
                raise ValueError("Version not found")

    version_file_path = Path(package_dir) / VERSION_FILE
    content, version = _find_and_replace(version_file_path, PATTERN_VERSION)

    new_version = new_version.replace("v", "").replace("V", "")

    with open(version_file_path, "w") as f:
        f.write(content.replace(version, new_version))

    pyproject_toml_file_path = Path(".") / PYPROJECT_TOML_FILE
    content_toml, version_toml = _find_and_replace(
        pyproject_toml_file_path, PATTERN_PYPROJECT_TOML
    )
    with open(pyproject_toml_file_path, "w") as f:
        f.write(content_toml.replace(version_toml, new_version))

    typer.echo(f"New version -> {new_version}", color=typer.colors.BRIGHT_CYAN)


if __name__ == "__main__":
    typer.run(set_version)
