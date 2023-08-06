#!/usr/bin/env python
import logging

import click
import coloredlogs

from flask.cli import FlaskGroup, with_appcontext
from flask import current_app

# commands
from vogue.commands.load import load as load_command
from vogue.server import create_app, configure_app
from .load import load

# Get version and doc decorator
from vogue import __version__
from vogue.tools.cli_utils import add_doc as doc

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LOG = logging.getLogger(__name__)


@click.version_option(__version__)
@click.group(
    cls=FlaskGroup,
    create_app=create_app,
    add_default_commands=True,
    invoke_without_command=False,
    add_version_option=False,
)
@click.option("-c", "--config", type=click.File(), help="Path to config file")
@with_appcontext
def cli(config):
    """Main entry point"""
    if current_app.test:
        return
    configure_app(current_app, config)
    pass


@cli.command()
def test():
    """Test server using CLI"""
    click.echo("test")
    pass


@cli.command()
@with_appcontext
def name():
    """Returns the app name, for testing purposes, mostly"""
    click.echo(current_app.name)
    return current_app.name


cli.add_command(test)
cli.add_command(load)
cli.add_command(name)
