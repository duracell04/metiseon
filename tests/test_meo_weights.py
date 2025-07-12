import pandas as pd
from datetime import date
import importlib.util
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "meo.py"
spec = importlib.util.spec_from_file_location("meo", SRC)
meo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(meo)


def test_meo_weights(monkeypatch):
    def fake_fred(code, as_of):
        return 100.0

    def fake_fx(sym, as_of):
        return 1.0

    def fake_crypto(as_of):
        return {"BTC": 50.0, "ETH": 30.0}

    monkeypatch.setattr(meo, "_fred_series", fake_fred)
    monkeypatch.setattr(meo, "_fx_rate", fake_fx)
    monkeypatch.setattr(meo, "_crypto_caps", fake_crypto)

    df, m_world = meo.fetch_meo_components(date(2024, 1, 1))
    assert abs(df["weight"].sum() - 1) < 1e-9
    assert meo.meo_price_usd(m_world) == m_world * 1e-6


def test_cross_price():
    result = meo.meo_cross_price(10.0, 2.0)
    assert result == 5.0
    assert pd.isna(meo.meo_cross_price(10.0, 0.0))
