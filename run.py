"""Command-line interface for the Metiseon robo allocator."""

from __future__ import annotations

import argparse
import asyncio
import base64
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from typing import Iterable
from decimal import Decimal

import matplotlib.pyplot as plt
import pandas as pd
import yaml

from src import allocator, async_data, ledger, risk, score

FEE_BP = 12.0  # fixed commission in basis points
PIT_LAG_DAYS = 45  # backtest point-in-time lag for fundamentals


def load_config(path: str = "config.yml") -> dict:
    cfg_path = Path(path)
    if not cfg_path.exists():
        return {}
    return yaml.safe_load(cfg_path.read_text())


async def pull_data(tickers: list[str], start: str, end: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    prices = await async_data.fetch_prices(tickers, start, end)
    fundamentals = await async_data.fetch_fundamentals(tickers)
    return prices, fundamentals


async def gather_meo_series(dates: Iterable[pd.Timestamp]) -> pd.Series:
    """Return MEΩ prices for each date."""
    async def _fetch(d: pd.Timestamp) -> float:
        s = await async_data.fetch_meo(d.date())
        return float(s.get("meo_usd", float("nan")))

    prices = await asyncio.gather(*[_fetch(d) for d in dates])
    return pd.Series(prices, index=pd.DatetimeIndex(dates))


def latest_sigma(price_df: pd.DataFrame, date: pd.Timestamp, method: str, window: int, denom: pd.Series) -> pd.Series:
    levels = price_df.columns.levels[0]
    sigmas: dict[str, float] = {}
    for t in levels:
        series = price_df[t]["adj_close"].loc[:date]
        if series.empty:
            sigmas[t] = float("nan")
            continue
        denom_series = denom.loc[series.index]
        if method == "garch":
            s = risk.garch_sigma(series, denom_series)
        else:
            s = risk.realised_sigma(series, window, denom_series)
        sigmas[t] = s.iloc[-1] if not s.empty else float("nan")
    return pd.Series(sigmas)


def size_cash(nav: float, cfg: dict, budget: float | None, pct: float | None) -> float:
    if budget is not None:
        return float(budget)
    if pct is not None:
        return nav * float(pct)
    if "weekly_pct" in cfg:
        return nav * float(cfg["weekly_pct"])
    return float(cfg.get("weekly_buy", 100))


def generate_report(dates: Iterable[datetime], navs: Iterable[float], path: str) -> None:
    fig, ax = plt.subplots()
    ax.plot(list(dates), list(navs))
    ax.set_xlabel("Date")
    ax.set_ylabel("NAV")
    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    img = base64.b64encode(buf.getvalue()).decode()
    html = f"<html><body><h1>Equity Curve</h1><img src='data:image/png;base64,{img}'/></body></html>"
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(html)


def run_backtest(args: argparse.Namespace, cfg: dict) -> None:
    start = args.start
    end = args.end
    tickers = cfg.get("tickers", [])
    prices, fundamentals = asyncio.run(pull_data(tickers, start, end))
    fundamentals = fundamentals.sort_values("date")
    adv10 = prices.xs("volume", level=1, axis=1).rolling(10).mean()
    if args.denom == "MEΩ":
        meo_series = asyncio.run(gather_meo_series(prices.index))
    else:
        meo_series = pd.Series(1.0, index=prices.index)
    book = ledger.Ledger(cfg.get("db_path", "portfolio.db"))
    nav_hist: list[tuple[datetime, float]] = []
    last = book.last_ticker()
    nav = book.nav()
    for date in prices.index:
        if date < pd.to_datetime(start) or date > pd.to_datetime(end):
            continue
        if date.weekday() != 4:  # weekly on Friday
            continue
        f = (
            fundamentals[fundamentals["date"] <= date - timedelta(days=PIT_LAG_DAYS)]
            .drop_duplicates("ticker", keep="last")
            .set_index("ticker")
        )
        if f.empty:
            continue
        scores = score.apply_scores(f)
        sigma = latest_sigma(prices, date, cfg.get("sigma_method", "garch"), int(cfg.get("risk_window", 63)), meo_series)
        best = allocator.pick_asset(scores, sigma, last)
        if not best:
            continue
        price = prices.at[date, (best, "adj_close")]
        adv = adv10.at[date, best]
        if args.denom == "MEΩ":
            nav = float(
                book.nav_meo(
                    prices.xs("adj_close", level=1, axis=1).loc[date],
                    meo_series.at[date],
                )
            )
        else:
            nav = book.nav()
        cash = size_cash(nav, cfg, args.budget, args.pct)
        budget_meo = Decimal(str(cash)) / Decimal(str(meo_series.at[date]))
        qty = allocator.size_trade(price, budget_meo, meo_series.at[date])
        if qty and allocator.decision_block(qty, adv, FEE_BP, float(cfg.get("slip_cap_bp", 35))):
            fee = price * float(qty) * FEE_BP / 10000
            book.book_trade(date.to_pydatetime(), best, qty, price, fee)
            if args.denom == "MEΩ":
                nav = float(
                    book.nav_meo(
                        prices.xs("adj_close", level=1, axis=1).loc[date],
                        meo_series.at[date],
                    )
                )
            else:
                nav = book.nav()
            nav_hist.append((date.to_pydatetime(), nav))
            last = best
    if nav_hist:
        dates, navs = zip(*nav_hist)
        generate_report(dates, navs, cfg.get("report_path", "reports/latest.html"))


def run_trade(args: argparse.Namespace, cfg: dict) -> None:
    end = datetime.utcnow().date().isoformat()
    start = (datetime.utcnow() - timedelta(days=365)).date().isoformat()
    tickers = cfg.get("tickers", [])
    prices, fundamentals = asyncio.run(pull_data(tickers, start, end))
    fundamentals = fundamentals.sort_values("date")
    adv10 = prices.xs("volume", level=1, axis=1).rolling(10).mean()
    if args.denom == "MEΩ":
        meo_series = asyncio.run(gather_meo_series(prices.index))
    else:
        meo_series = pd.Series(1.0, index=prices.index)
    book = ledger.Ledger(cfg.get("db_path", "portfolio.db"))
    today = prices.index[-1]
    if args.denom == "MEΩ":
        nav = float(
            book.nav_meo(
                prices.xs("adj_close", level=1, axis=1).loc[today],
                meo_series.at[today],
            )
        )
    else:
        nav = book.nav()
    last = book.last_ticker()
    f = (
        fundamentals[fundamentals["date"] <= today - timedelta(days=PIT_LAG_DAYS)]
        .drop_duplicates("ticker", keep="last")
        .set_index("ticker")
    )
    scores = score.apply_scores(f)
    sigma = latest_sigma(prices, today, cfg.get("sigma_method", "garch"), int(cfg.get("risk_window", 63)), meo_series)
    best = allocator.pick_asset(scores, sigma, last)
    if not best:
        print("No suitable asset to trade.")
        return
    price = prices.at[today, (best, "adj_close")]
    adv = adv10.at[today, best]
    cash = size_cash(nav, cfg, args.budget, args.pct)
    budget_meo = Decimal(str(cash)) / Decimal(str(meo_series.at[today]))
    qty = allocator.size_trade(price, budget_meo, meo_series.at[today])
    if qty and allocator.decision_block(qty, adv, FEE_BP, float(cfg.get("slip_cap_bp", 35))):
        fee = price * float(qty) * FEE_BP / 10000
        book.book_trade(today.to_pydatetime(), best, qty, price, fee)
    nav_df = book.con.execute("SELECT ts, nav FROM positions ORDER BY ts").df()
    if not nav_df.empty:
        if args.denom == "MEΩ":
            nav_df["nav"] = nav_df["nav"] / meo_series.reindex(pd.to_datetime(nav_df["ts"])).values
        generate_report(pd.to_datetime(nav_df["ts"]), nav_df["nav"], cfg.get("report_path", "reports/latest.html"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Metiseon robo allocator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    back = sub.add_parser("backtest", help="Run historical backtest")
    back.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    back.add_argument("--end", required=True, help="End date YYYY-MM-DD")
    back.add_argument("--budget", type=float, help="Weekly cash injection")
    back.add_argument("--pct", type=float, help="Weekly injection as fraction of NAV")
    back.add_argument("--denom", choices=["CHF", "MEΩ"], default="MEΩ", help="Reporting currency")

    trade = sub.add_parser("trade", help="Execute single trade step")
    trade.add_argument("--budget", type=float, help="Cash to deploy")
    trade.add_argument("--pct", type=float, help="Cash as fraction of NAV")
    trade.add_argument("--denom", choices=["CHF", "MEΩ"], default="MEΩ", help="Reporting currency")

    args = parser.parse_args()
    cfg = load_config()

    if args.cmd == "backtest":
        run_backtest(args, cfg)
    elif args.cmd == "trade":
        run_trade(args, cfg)


if __name__ == "__main__":
    main()
