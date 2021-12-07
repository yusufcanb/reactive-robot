import logging

import click

from reactive_robot import PKG_DIR, PYTHON_VERSION, __version__
from reactive_robot.config.base import load_config
from reactive_robot.log import Log
from reactive_robot.serve import serve


def add_options(opts):
    def inner(f):
        for i in reversed(opts):
            f = i(f)
        return f

    return inner


def verbose_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(Log)
        if value:
            state.stream.setLevel(logging.DEBUG)

    return click.option('-v', '--verbose',
                        is_flag=True,
                        expose_value=False,
                        help='Enable verbose output',
                        callback=callback)(f)


def quiet_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(Log)
        if value:
            state.stream.setLevel(logging.ERROR)

    return click.option('-q', '--quiet',
                        is_flag=True,
                        expose_value=False,
                        help='Silence warnings',
                        callback=callback)(f)


common_options = add_options([quiet_option, verbose_option])
common_config_options = add_options([
    click.option('-f', '--config-file', type=click.File('rb'), help="Please provide a rx-robot config file."),
])


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(
    __version__,
    '-V', '--version',
    message=f'%(prog)s, version %(version)s from {PKG_DIR} (Python {PYTHON_VERSION})'
)
@common_options
def cli():
    """
    Reactive Robot - Fastest way to turn your robot workflows into event driven service.
    """


@cli.command(name="serve")
@common_config_options
@common_options
def serve_robots(**kwargs):
    """Starts rx-robot event loop"""
    config = load_config(**kwargs)
    serve(config)
