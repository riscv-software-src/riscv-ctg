from click.testing import CliRunner
from riscv_ctg.main import cli
import pytest 

@pytest.fixture
def runner():
    return CliRunner()

def test_clean(runner):
    '''Testing clean option'''
    result = runner.invoke(cli, ['--clean'])
    assert result.exit_code == 0

def test_version(runner):
    '''Testing version option'''
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0

