# Metiseon MVP — Technical Specification (v0.2)

A **single‑script**, deterministic robo‑allocator demonstrator.  
Public data only, zero infra cost, mathematically explicit.  
Everything here runs on a laptop and a free GitHub runner.

---

## 0  Table of Contents

1. Scope & Guard‑Rails  
2. Quick Start (copy–paste)  
3. Data Model & Lineage  
4. Quant Engine  
  4.1  Durability‑Lite Factor $D_i$  
  4.2  Risk Model $\sigma_i, \text{CVaR}_{95}$  
  4.3  Asset Filter & Tie‑Break  
  4.4  Capital‑Injection Model  
  4.5  Execution & Slippage  
5. Performance Accounting  
  5.1  Nominal NAV  
  5.2  Real Carry‑Adjusted $\alpha$  
  5.3  Attribution Layout  
6. Repository Topology  
7. YAML Config Reference  
8. Dependency Foot‑Print  
9. Extensibility Hooks  
10. Mathematical Glossary  
11. Disclaimer  

---

## 1  Scope & Boundaries

| Included in MVP                              | Explicitly **out‑of‑scope**             |
| -------------------------------------------- | --------------------------------------- |
| • 6 tickers (5 ETFs + BTC spot)              | Leverage, options, shorting             |
| • Free data (Yahoo, FRED, AlphaVantage demo) | Paid feeds, real‑time execution         |
| • Weekly cron, linear or %‑NAV inflow        | Minute bars, macro‑HMM regime switching |
| • DuckDB ledger + static HTML report         | Quantum CVaR, GUI dashboards, licences  |

---

## 2  Quick Start (15 min)

```bash
# 1 – clone & install (Conda ≤ 85 MB)
git clone https://github.com/<YOUR-USER>/metiseon.git
cd metiseon
conda env create -f environment.yml -n metiseon
conda activate metiseon

# 2 – 10‑year vectorised back‑test (< 40 s)
python run.py backtest --start 2015-01-01 --end today

# 3 – Simulate weekly CHF 100 buy
python run.py trade --budget 100   # or --pct 0.01
```

**Artifacts:**  
- `portfolio.db`  
- `reports/latest.html` (equity curve + attribution)

---

## 3  Data Model & Integrity

All tables live in a **single WAL‑mode DuckDB** file; nightly snapshots can be committed via DVC (SHA‑256 pin).

| Table          | Columns (types)                                                            | Source            | Update lag      | QC checks                   |
| -------------- | -------------------------------------------------------------------------- | ----------------- | --------------- | --------------------------- |
| `prices`       | date, ticker, adj\_close, volume                                           | Yahoo             | daily 00:05 UTC | missing → linear fill ≤ 1 d |
| `fundamentals` | date, ticker, roe, debt\_equity, profit\_margin, rd\_to\_rev, insider\_own | AlphaVantage demo | weekly          | drop rows with any NaN      |
| `benchmarks`   | date, cpi, sofr                                                            | FRED              | monthly/ daily  | NaN fwd‑fill ≤ 5 d          |
| `trades`       | ts, ticker, qty, price, fee                                                | internal          | on trade        | primary key (`ts`,`ticker`) |
| `positions`    | ts, ticker, qty, cost\_basis, nav                                          | derived           | on trade        | DUCKDB CHECKs               |

*Async pull*: tickers fetched concurrently via `asyncio` + `run_in_executor`; 5× speed‑up vs serial.

---

## 4  Quantitative Engine

### 4.1  Durability‑Lite Factor $D_i$

Piece‑wise deterministic with **interaction penalty**:

$$
\begin{aligned}
D_i &= 25 
  + 20\,\mathbb 1_{\text{ROE}>12\%}
  + 15\,\mathbb 1_{D/E<1}
  + 15\,\mathbb 1_{PM>10\%}
  + 10\,\mathbb 1_{\text{Insider}>2\%}
  + 15\,\mathbb 1_{R\&D/Rev>5\%} \\\\
  &\quad - 10\,\mathbb 1_{(D/E>1)\land(\text{Insider}<1\%)} \tag{Cross‑factor penalty}
\end{aligned}
$$

Clamped to $[0,100]$.

### 4.2  Risk Metrics

* **Dynamic volatility**: GARCH(1,1) with daily update  
  $\sigma_{i,t}^2 = \omega + \alpha\,\varepsilon_{i,t-1}^2 + \beta\,\sigma_{i,t-1}^2$  
  fitted over last 252 d (ARCH package, no display).  
  Crisis overlay: if VIX$_t>30$ multiply $\sigma_{i,t}$ by 1.25.

* **FX‑beta adjustment** (reporting currency CHF):  
  $\beta^{\text{FX}}_{i}=\frac{\operatorname{Cov}(r_i, r_{\text{CHFUSD}})}{\operatorname{Var}(r_{\text{CHFUSD}})}$  
  NAVs are re‑expressed: $\tilde r_i = r_i - \beta^{\text{FX}}_i r_{\text{CHFUSD}}$.

* **Tail risk (optional)**: empirical $\text{CVaR}_{95}$ used only for reporting.

### 4.3  Asset Filter

1. Exclude last‑week winner.
2. Risk gate: $\sigma_{i,t} \le \operatorname{median}_j(\sigma_{j,t})$.
3. Select $ i^* = \arg\max D_i$.
4. Tie → minimal $\sigma_{i}$.

### 4.4  Capital‑Injection Model

Fixed or proportional cash flow

$$
\text{Cash}_t = \begin{cases}
B,& \text{fixed}\; (\text{default }B=100\,\text{CHF})\\[4pt]
p\,\text{NAV}_{t^-},& \text{percentage mode (e.g. }p=0.01)\end{cases}
$$

Quantity (Decimal, 4 dp):  
$q_t = \operatorname{round_{0.0001}}\!\Bigl(\tfrac{\text{Cash}_t}{P_{i^*,t}}\Bigr)$

### 4.5  Execution & Slippage

*Fee* ≈ 12 bp fixed.  *Market impact* (square‑root):  
$\text{Slip}_{i} = 0.001 \bigl( \tfrac{q_t}{\text{ADV}_{10,i}} \bigr)^{1/2}$  
Trade skipped if total cost > 35 bp.

---

## 5  Performance Accounting

### 5.1 Nominal NAV

$ \text{NAV}_t=\sum_i q_{i,t}\,P_{i,t}$  
Dividend‑adjusted total‑return prices used (Yahoo `AdjClose`).

### 5.2 Real, Carry‑Adjusted $\alpha$

$ \alpha^{\text{real}}_{T}=\frac{1+R_T}{1+\pi_T}-1- R_{f,T}-C^{\text{carry}}_{T}$

- ETFs & BTC → $C^{\text{carry}}=0$.
- CPI lag 1 month; SOFR daily.

### 5.3 Attribution Table (weekly)

|Ticker|$D$|Entry CHF|Exit CHF|Return %|Fee bp|Slip bp|PnL CHF|

---

## 6  Repository Topology (only real files)

| Path                           | Purpose                                  |
| ------------------------------ | ---------------------------------------- |
| `run.py`                       | CLI: `backtest`, `trade`                 |
| `src/data.py`                  | Async fetch + cache (requests‑cache)     |
| `src/score.py`                 | Durability calculations                  |
| `src/risk.py`                  | GARCH volatility, FX‑beta, CVaR          |
| `src/allocator.py`             | Select asset, size order, slippage check |
| `src/db.py`                    | DuckDB helper (WAL, .parquet)            |
| `tests/*`                      | Pytest quick sanity (~20 s)              |
| `.github/workflows/ci.yml`     | Lint + tests                             |
| `.github/workflows/weekly.yml` | Fri 06:15 UTC cron trade                 |

---

## 7  YAML Configuration

```yaml
tickers: [VTI, IEFA, GLD, VNQ, BND, BTC-USD]
weekly_buy: 100         # Fixed mode (CHF)
#weekly_pct: 0.01       # Proportional mode (1 % NAV) — uncomment to use
risk_window: 63
sigma_method: garch     # or "std"
slip_cap_bp: 35         # Skip order if cost > cap (basis points)
report_path: reports/latest.html
db_path: portfolio.db
currency: CHF
```

---

## 8  Dependency Foot‑Print (Conda)

```
python=3.11
duckdb>=0.10
pandas>=2.2
numpy
yfinance>=0.2
alpha_vantage
fredapi
matplotlib
arch                # GARCH
requests-cache
pytest
```

Cold install < 85 MB; back‑test < 40 s on GitHub runner.

---

## 9  Extensibility Hooks

- **risk.py** → swap in EVT‑CVaR or Student‑t GARCH.
- **score.py** → plug Bayesian regression (`sklearn`) weights.
- **allocator.py** → expand to top‑N basket, Kelly sizing.
- **data.py** → add paid feed fallback (FMP, Refinitiv).

---

## 10  Mathematical Glossary

| Symbol         | Definition                          |
| -------------- | ----------------------------------- |
| $r_{i,t}$      | Log return of asset $i$ on day $t$  |
| $\sigma_{i,t}$ | Conditional volatility from GARCH   |
| $D_i$          | Durability‑Lite score (0‑100)       |
| $q_{i,t}$      | Units held post‑trade               |
| $P_{i,t}$      | Total‑return price                  |
| $R_T$          | Cumulative nominal portfolio return |
| $\pi_T$        | CPI inflation over $[0,T]$          |

---

## 11  Disclaimer

Prototype code released under MIT licence.  
No warranty, no investment advice.

