import re
from pathlib import Path

import typer

VERSION_FILE = "__version__.py"
PATTERN = r'VERSION\s*=\s*"([^"]+)"'


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

    version_file_path = Path(package_dir) / VERSION_FILE
    with open(version_file_path, "r") as f:
        content = f.read()
        match = re.search(PATTERN, content)
        if match:
            version = match.group(1)
            typer.echo(f"Version: {version}", color=typer.colors.BLUE)
        else:
            raise ValueError("Version not found")

    new_version = new_version.replace("v", "").replace("V", "")
    with open(version_file_path, "w") as f:
        f.write(content.replace(version, new_version))

    typer.echo(f"New version -> {new_version}", color=typer.colors.BRIGHT_CYAN)


if __name__ == "__main__":
    typer.run(set_version)
