from click.testing import CliRunner
from coursectl.cli import cli

def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, "--help")
    assert result.exit_code == 0

def test_configure():
    pass