"""
coursectl
~~~~~~~~~

Script to manage courses on Community LMS.
"""

import os
import click
from . import config
from .api import API

@click.group()
@click.option("--profile", help="name of the configuration profile to use", default="default", envvar="FRAPPE_PROFILE")
@click.pass_context
def cli(ctx, profile):
    """The CLI tool to manage courses on Community LMS.
    """
    ctx.ensure_object(dict)
    ctx.obj['profile'] = profile

@cli.command()
@click.pass_context
def configure(ctx):
    """Configure coursectl.

    This command will prompt for FRAPPE_API_KEY, FRAPPE_API_SECRET and
    FRAPPE_SITE_URL and saves them in the config file.
    """
    profile = ctx.obj['profile']
    values = config.read_config(profile)
    def prompt(key):
        values[key] = click.prompt(key, default=os.getenv(key.upper()) or values.get(key))

    prompt("frappe_site_url")
    prompt("frappe_api_key")
    prompt("frappe_api_secret")

    config.write_config(profile, values)

@cli.command()
@click.pass_context
def version(ctx):
    """Prints the version of the coursectl command and the server.
    """
    from . import __version__
    print(__version__)

@cli.command()
@click.pass_context
@click.argument("filenames", type=click.Path(exists=True), nargs=-1, required=True)
def push_lesson(ctx, filenames):
    """Pushes one or more lessons to the server.
    """
    api = API(profile=ctx.obj['profile'])
    for f in filenames:
        api.push_lesson(f)


@cli.command()
@click.pass_context
@click.argument("filenames", type=click.Path(exists=True), nargs=-1, required=True)
def push_exercise(ctx, filenames):
    """Pushes one or more exercises to the server.
    """
    api = API(profile=ctx.obj['profile'])
    for f in filenames:
        api.push_exercise(f)

@cli.command()
@click.pass_context
@click.argument("name")
def pull_lesson(ctx, name):
    """Pulls a lesson from the server and saves it locally.
    """
    api = API(profile=ctx.obj['profile'])
    api.pull_lesson(name)

@cli.command()
@click.pass_context
@click.argument("name")
def pull_exercise(ctx, name):
    """Pulls a exercise from the server and saves it locally.
    """
    api = API(profile=ctx.obj['profile'])
    api.pull_exercise(name)

@cli.command()
@click.pass_context
@click.argument("filename", type=click.Path(exists=True), default="course.yml")
def push_course(ctx, filename):
    """Pushes a course to the server.

    Also pushes the chapters.
    """
    api = API(profile=ctx.obj['profile'])
    api.push_course(filename)


@cli.command()
@click.pass_context
def whoami(ctx):
    """Prints the current user.
    """
    api = API(profile=ctx.obj['profile'])
    email = api.whoami()
    print(email)

def main():
    cli()

if __name__ == "__main__":
    main()