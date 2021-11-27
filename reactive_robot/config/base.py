import logging
import os
import yaml
from contextlib import contextmanager

from marshmallow.exceptions import ValidationError

from reactive_robot.config.schema import RxRobotConfigSchema
from reactive_robot.exceptions import InvalidConfigurationFileException, ConfigurationFileNotExists

log = logging.getLogger('reactive_robot.config')


@contextmanager
def _open_config_file(config_file):
    """
    A context manager which yields an open file descriptor ready to be read.

    Accepts a filename as a string, an open or closed file descriptor, or None.
    When None, it defaults to `reactive-robot.yml` in the CWD. If a closed file descriptor
    is received, a new file descriptor is opened for the same file.

    The file descriptor is automatically closed when the context manager block is existed.
    """

    # Default to the standard config filename.
    if config_file is None:
        paths_to_try = ['reactive-robot.yml', 'reactive-robot.yaml']
    # If it is a string, we can assume it is a path and attempt to open it.
    elif isinstance(config_file, str):
        paths_to_try = [config_file]
    # If closed file descriptor, get file path to reopen later.
    elif getattr(config_file, 'closed', False):
        paths_to_try = [config_file.name]
    else:
        paths_to_try = None

    if paths_to_try:
        # config_file is not a file descriptor, so open it as a path.
        for path in paths_to_try:
            path = os.path.abspath(path)
            log.debug(f"Trying to load configuration file: {path}")
            try:
                config_file = open(path, 'rb')
                break
            except FileNotFoundError:
                log.info(f"Config file '{path}' does not exist.")
                continue
        else:
            log.error(f"Config file '{paths_to_try[0]}' does not exist.")
            raise ConfigurationFileNotExists(f"Config file '{paths_to_try[0]}' does not exist.")
    else:
        log.debug(f"Trying to load configuration file: {config_file}")
        config_file.seek(0)

    try:
        yield config_file
    finally:
        if hasattr(config_file, 'close'):
            config_file.close()


def load_config(config_file=None, **kwargs):
    """
    Load the configuration for a given file object or name

    The config_file can either be a file object, string or None. If it is None
    the default `reactive-robot.yml` filename will loaded.

    Extra kwargs are passed to the configuration to replace any default values
    unless they themselves are None.
    """
    options = kwargs.copy()

    # Filter None values from the options. This usually happens with optional
    # parameters from Click.
    for key, value in options.copy().items():
        if value is None:
            options.pop(key)

    config_schema = RxRobotConfigSchema()
    with _open_config_file(config_file) as fd:
        data = yaml.safe_load(fd)
        log.debug("Reading YAML file, %s " % data)
        try:
            dump = config_schema.load(data, unknown=True)
        except ValidationError as e:
            raise InvalidConfigurationFileException(e.messages)

    log.debug("Using schema %s" % dump)
    return dump
