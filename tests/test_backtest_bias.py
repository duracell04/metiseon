from pathlib import Path
import re

def test_backtest_uses_pt_lag():
    src = Path('run.py').read_text()
    const = re.search(r'PIT_LAG_DAYS\s*=\s*(\d+)', src)
    assert const and int(const.group(1)) >= 45
    assert 'timedelta(days=PIT_LAG_DAYS)' in src
