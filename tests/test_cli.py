from click.testing import CliRunner
from coursectl.cli import cli, config

def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, "--help")
    assert result.exit_code == 0

def test_configure(monkeypatch, tmp_path):
    config_path = tmp_path / "config"

    monkeypatch.setattr(config, "CONFIG_FILE_PATH", str(config_path))

    runner = CliRunner()
    result = runner.invoke(cli, "configure", input="https://example.com/\nABCD\nXYZ\n")
    assert result.exit_code == 0

    config_text = config_path.read_text()
    assert "frappe_site_url = https://example.com/" in config_text
    assert "frappe_api_key = ABCD" in config_text
    assert "frappe_api_secret = XYZ" in config_text

