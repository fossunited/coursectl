"""
coursectl
~~~~~~~~~

Script to manage courses on Community LMS.
"""

import os
import click

@click.group()
def cli():
    """The CLI tool to manage courses on Community LMS.
    """
    pass

def main():
    cli()

if __name__ == "__main__":
    main()