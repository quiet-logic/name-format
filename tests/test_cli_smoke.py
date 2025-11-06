import sys, subprocess
def run_cli(*args):
    out = subprocess.check_output([sys.executable, "-m", "name_format.cli", *args], text=True)
    return out.strip()
def test_cli_basic():
    assert run_cli("ó", "brien") == "O'Brien"
