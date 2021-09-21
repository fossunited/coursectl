"""
coursectl
~~~~~~~~~

Script to manage courses on Community LMS.
"""

import os
import click
from . import config

@click.group()
def cli():
    """The CLI tool to manage courses on Community LMS.
    """
    pass

@cli.command()
@click.option("--profile", help="name of the profile to create/update", default="default")
def configure(profile):
    """Configure coursectl.

    This command will prompt for FRAPPE_API_KEY, FRAPPE_API_SECRET and
    FRAPPE_SITE_URL and saves them in the config file.
    """

    values = config.read_config(profile)
    def prompt(key):
        values[key] = click.prompt(key, default=os.getenv(key.upper()) or values.get(key))

    prompt("frappe_site_url")
    prompt("frappe_api_key")
    prompt("frappe_api_secret")

    config.write_config(profile, values)


def main():
    cli()

if __name__ == "__main__":
    main()