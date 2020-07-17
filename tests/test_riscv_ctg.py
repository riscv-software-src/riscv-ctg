from click.testing import CliRunner
from riscv_ctg.main import cli
import pytest

@pytest.fixture
def runner():
    return CliRunner()

def test_version(runner):
    '''Testing version option'''
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0

