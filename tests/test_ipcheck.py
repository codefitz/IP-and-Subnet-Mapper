import subprocess
import sys
import os


def run_ipcheck(args):
    cmd = [sys.executable, os.path.join(os.path.dirname(__file__), '..', 'ipcheck.py')] + args
    return subprocess.run(cmd, capture_output=True, text=True)


def test_single_ip_match():
    result = run_ipcheck(['-i', '192.168.1.210', '-s', '192.168.1.0/24'])
    assert 'found in 192.168.1.0/24' in result.stdout
    assert result.returncode == 0


def test_ip_range():
    result = run_ipcheck(['-i', '192.168.1.208/30', '-s', '192.168.1.210'])
    assert 'found in 192.168.1.210/32' in result.stdout
    assert result.returncode == 0


def test_invalid_ip():
    result = run_ipcheck(['-i', 'invalid', '-s', '192.168.1.0/24'])
    assert 'not valid cidr syntax' in result.stdout.lower()
    assert result.returncode != 0
