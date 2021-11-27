import toml
from reactive_robot import __version__


def test_package_version():
    with open("pyproject.toml") as f:
        package_definition = toml.load(f)
        assert __version__ == package_definition["tool"]["poetry"]["version"]
