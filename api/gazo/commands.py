import os
import click
from flask import current_app
from flask.cli import with_appcontext

CURRENT_DIR=os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT=os.path.join(CURRENT_DIR, os.pardir)
TESTS_PATH=os.path.join(PROJECT_ROOT, 'tests')


@click.command()
def test():
    """Run the tests."""
    import pytest
    rv = pytest.main(['-s',TESTS_PATH, '--verbose'])
    exit(rv)

@click.command()
def clean():
    for dirpath, _, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)
