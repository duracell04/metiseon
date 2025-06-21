from __future__ import annotations

import argparse
import yaml


def load_config(path: str) -> dict:
    with open(path, "r") as fh:
        return yaml.safe_load(fh)


def cmd_backtest(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    print(f"Backtest {args.start} -> {args.end} for {cfg['tickers']}")


def cmd_trade(args: argparse.Namespace) -> None:
    cfg = load_config(args.config)
    cash = args.budget if args.budget is not None else f"{args.pct * 100}% NAV"
    print(f"Trade {cash} for tickers {cfg['tickers']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yml")
    sub = parser.add_subparsers(dest="command", required=True)

    b = sub.add_parser("backtest")
    b.add_argument("--start", required=True)
    b.add_argument("--end", required=True)
    b.set_defaults(func=cmd_backtest)

    t = sub.add_parser("trade")
    t.add_argument("--budget", type=float)
    t.add_argument("--pct", type=float)
    t.set_defaults(func=cmd_trade)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
