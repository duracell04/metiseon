# Metiseon 🚀

> **open-source robo allocator**  
> Durability-score ranking • inverse-vol basket • zero-cost data • SQLite ledger

| 🔧 Stack | 📈 Signals | 🛡️ Risk |
|----------|-----------|--------|
| Python 3.10 • pandas • yfinance • GitHub Actions | Durability-Lite (industry z-scores of ROE, D/E, R&D) | inverse-vol sizing, cost model, stop-loss on score-decay |

## Quick start

```bash
git clone https://github.com/<you>/metiseon.git
conda env create -f environment.yml
python src/trade_loop.py  --paper
