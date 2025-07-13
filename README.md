# Metiseon MVP — Quant-Native Robo-Allocator (v0.2)

*“Wisdom without mathematics is guesswork;  
mathematics without liquidity is theory.”*

The Metiseon prototype is a **one-script**, self-verifiable robo-allocator that lives entirely on free data, a DuckDB file, and ~80 MB of open-source libraries.  
It is not a toy factor screen; it is a **closed-form capital-engine** that:

* represents your portfolio as a **quantum-state currency vector**  
* scores issuers on **economic durability** & **under-pricing**  
* sizes orders under an explicit **risk–liquidity budget**  
* prints performance as **real carry-clean α** across six markets.

Copy → paste → run. No cloud, no secrets, no vendor lock-in.

---

## 0 ▐  Table of Contents
1. Scope & Guard-Rails  
2. Quick Start  
3. Data Lineage & Schema  
4. Economic Engine
   - 4.1 Quantum-State Currency
   - 4.2 Durability & Value Factor
   - 4.3 Dynamic Risk Surface
   - 4.4 Liquidity & Slippage
   - 4.5 Allocator & Capital Flow
5. Performance Accounting
   - 5.1 Global Interest-Rate Neutral Alpha (GINα)
6. Repository Blueprint
7. config.yaml Cheatsheet
8. Dependencies
9. Extensibility Hooks
10. Mathematical Appendix
11. Disclaimer

---

## 1 ▐  Scope & Guard-Rails

| **Included** (MVP)                               | **Excluded** (v0.2)               |
|--------------------------------------------------|-----------------------------------|
| 6 liquid markets (VTI, IEFA, GLD, VNQ, BND, BTC) | Options, leverage, shorting       |
| Free data: Yahoo OHLCV, FRED, AlphaVantage demo  | Paid feeds (Refinitiv, FMP)       |
| Weekly cron; fixed or %-of-NAV cash injection    | Intraday fills, latency arbitrage |
| GARCH(1,1) σ + CVaR₉₉ tail risk                  | EVT, Student-t GARCH (hook)       |
| WAL-mode DuckDB ledger + HTML equity curve       | UI dashboards, on-chain notarisation |
| MEΩ default; CHF optional                        |                                    |

---

## 2 ▐  Quick Start ≈ 12 min

```bash
git clone https://github.com/<YOU>/metiseon.git
cd metiseon
conda env create -f environment.yml -n metiseon
conda activate metiseon

# 10-year vectorised back-test  (<40 s on GH runner)
python run.py backtest --start 2015-01-01 --end today

# One live paper trade (CHF 100 injection)
python run.py trade --budget 100          # or --pct 0.01
```

Artifacts

* `portfolio.db` — immutable ledger (DuckDB WAL)  
* `reports/latest.html` — equity curve + attribution  

---

## 3 ▐  Data Lineage & Schema

All tables co-habit **one** DuckDB file; nightly snapshots are DVC-pinned (SHA-256).

| table          | key cols                                          | feed & lag        | QA rule               |
|----------------|---------------------------------------------------|-------------------|-----------------------|
| `prices`       | date, ticker, adj_close, volume                   | Yahoo EOD (+0 d)  | linear fill ≤ 1 day   |
| `fundamentals` | date, ticker, roe, debt_eq, margin, rd%, insider  | AV demo (+3–7 d)  | drop any NaN          |
| `benchmarks`   | date, cpi, sofr, vix, chfusd                      | FRED monthly/daily| fwd-fill CPI ≤ 30 d   |
| `trades`       | ts, ticker, qty, price, fee_bps                   | internal          | PK (ts,ticker)        |
| `positions`    | ts, ticker, qty, cost, nav                        | derived           | DUCKDB CHECKs         |

**Async ingestion**: `asyncio.gather` + `run_in_executor` → 5× speed-up vs serial HTTP.

Current MEΩ weights:

```sql
SELECT symbol, weight
FROM benchmarks
WHERE date = (SELECT max(date) FROM benchmarks)
ORDER BY weight DESC
LIMIT 10;
```

---

## 4 ▐  Economic Engine

### 4.1 Quantum-State Currency

```
V_t = (CHF_t, USD_t, EUR_t, BTC_t, XAU_t …)
```

Collapsed to a reporting numéraire via

```
NAV_t = Σ_i  V_{i,t} · FX_{i→CHF,t}
```

All sizing rules are `%·NAV`; the code scales from CHF 500 to CHF 500 M **unchanged**.

### 4.2 Durability & Value Factor

```
D_i = 25
    +20·1{ROE>12%}
    +15·1{D/E<1}
    +15·1{Margin>10%}
    +10·1{InsiderOwn>2%}
    +15·1{R&D/Rev>5%}
    −10·1{D/E>1 ∧ InsiderOwn<1%}
```

*Score clamp*: `D_i ∈ [0,100]`

*Under-pricing overlay*:  
Dividend-yield percentile > 70 → +5 bonus pts.

### 4.3 Dynamic Risk Surface

* **σᵢ,t** — GARCH(1,1) conditional vol (252 d), `arch` pkg  
* **Crisis overlay**: if **VIX > 30** ⇒ σ × 1.25  
* **CVaR₉₉** — empirical tail (report only)  
* **Risk gate**: keep assets with σ ≤ median(σ_universe)

### 4.4 Liquidity & Slippage

```
fee_bps     = 12
impact_bps  = 100 * sqrt(q_notional / ADV10)
slippage_bp = max(10, impact_bps)        # 10 bp floor
trade_skip  = fee_bps + slippage_bp > cfg.slip_cap_bp
```

### 4.5 Allocator & Capital Flow

```python
if cfg.weekly_buy:
    cash = Decimal(cfg.weekly_buy)
else:                  # proportional mode
    cash = Decimal(cfg.weekly_pct) * nav

qty = round(cash / price, 4)    # 4 dp fractional ETFs
```

**Selection pipeline**

1. drop `last_ticker`  
2. drop σ > median(σ)  
3. arg-max `D_i`  
4. tie → lower σ  

---

## 5 ▐  Performance Accounting

| layer           | formula                                               | note                    |
|-----------------|-------------------------------------------------------|-------------------------|
| **nominal P/L** | `NAV_t = Σ q_i · P_i`                                 |                         |
| **real excess** | `α_real = ((1+R_T)/(1+π_T)) − 1 − R_f,T − C_carry`    | carry = 0 for ETFs/BTC  |
| CPI lag 1 m     | SOFR strip daily                                      |                         |

Weekly HTML shows NAV curve + table:

`| Ticker | D | Entry CHF | Exit CHF | Δ% | Fee bp | Slip bp | PnL CHF |`

Metiseon reports α_real^{MEΩ} – returns net of inflation, funding, and cross-currency drift.

### 5.1 Global Interest-Rate Neutral Alpha (GINα)

GINα measures performance relative to a global interest-rate and inflation baseline. It
adjusts nominal returns for worldwide yield differentials and carry costs so that
portfolio results reflect pure skill rather than macro conditions.

Mathematically,

```
GINα_t = ((1 + R_t^{Metiseon}) / (1 + r_t^{IRS} + π_t^{MEΩ})) - 1 - C_{carry,t}
```

where `R_t^{Metiseon}` is the portfolio return in MEΩ units, `r_t^{IRS}` is the
global interest-rate surface, `π_t^{MEΩ}` the aggregated global inflation rate and
`C_{carry,t}` explicit funding costs.

The interest-rate surface itself is fitted as a polynomial regression over global
monetary indicators,

```
r_t^{IRS}(x) = Σ_{k=0}^n α_k(t) · x^k
```

and carry-neutrality across currencies is enforced via covered interest-rate parity.

---

## 6 ▐  Repository Blueprint

| path                           | role                                |
|--------------------------------|-------------------------------------|
| `run.py`                       | CLI (`backtest`, `trade`)           |
| `src/async_data.py`            | concurrent Yahoo / AV / FRED fetch  |
| `src/score.py`                 | Durability + dividend bonus         |
| `src/risk.py`                  | GARCH σ, CVaR, FX-beta              |
| `src/allocator.py`             | pick + size + skip cost             |
| `src/ledger.py`                | DuckDB WAL, NAV calc                |
| `tests/`                       | pytest sanity (< 20 s)              |
| `.github/workflows/ci.yml`     | lint + tests                        |
| `.github/workflows/weekly.yml` | Fri 06:15 UTC auto-trade            |

---

## 7 ▐  config.yaml Cheatsheet

```yaml
tickers:        [VTI, IEFA, GLD, VNQ, BND, BTC-USD]

# choose ONE of the two cash-flow modes
weekly_buy:     100        # fixed CHF
#weekly_pct:    0.01       # 1 % of NAV

risk_window:    63
sigma_method:   garch      # or "std"
slip_cap_bp:    35
report_path:    reports/latest.html
db_path:        portfolio.db
currency:       CHF
```

---

## 8 ▐  Dependencies

```shell
python=3.11
duckdb>=0.10
pandas>=2.2
numpy
yfinance>=0.2
alpha_vantage
fredapi
arch
requests-cache
matplotlib
pytest
```

*Cold install < 85 MB • back-test < 40 s on GH-runner*

---

## 9 ▐  Extensibility Hooks

| where          | drop-in idea                   |
|----------------|-------------------------------|
| `risk.py`      | EVT-CVaR, Student-t GARCH     |
| `score.py`     | Bayesian ridge factor weight  |
| `allocator.py` | top-N basket, Kelly sizing    |
| `async_data`   | paid feed fallback (Refinitiv)|

---

## 10 ▐  Mathematical Appendix

| symbol  | meaning                                 |
|---------|-----------------------------------------|
| `V_t`   | currency-state vector at time t         |
| `NAV_t` | Σ state × FX → CHF                      |
| `D_i`   | durability-lite score 0-100             |
| `σᵢ,t`  | GARCH(1,1) conditional vol (annualised) |
| `CVaR₉₉`| mean of worst 1 % daily P/L             |
| `qᵢ,t`  | units of asset _i_ held after trade t   |
| `Pᵢ,t`  | total-return price (adj close)          |
| `R_T`   | cumulative nominal return of portfolio |
| `π_T`   | CPI inflation over [0,T]               |
| `α_real`| real carry-clean alpha                 |

---

## 11 ▐  Disclaimer

Prototype code released under **MIT Licence**.  
No warranty, no investment advice. Use entirely at your own risk.

<!-- END OF README -->
