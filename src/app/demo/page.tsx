import Image from "next/image";
import { Header } from "@/components/Header";
import { CodeBlock } from "@/components/CodeBlock";
import navStats from "../../../public/charts/nav_meo.json";
import decisionTrace from "../../../public/logic/decision_trace.json";

const cliCode = `python run.py backtest --start 2015-01-01 --end 2025-01-01 --denom MEΩ
open reports/latest.html`;

const ledgerCode = `SELECT ts, ticker, qty, price, fee
FROM trades
ORDER BY ts DESC
LIMIT 5;`;

const ledgerRows = [
  { ts: "2025-06-27T15:30Z", ticker: "VTI", qty: "+120", price: "$224.34", fee: "12 bp" },
  { ts: "2025-06-20T15:30Z", ticker: "IEFA", qty: "-110", price: "$70.12", fee: "12 bp" },
  { ts: "2025-06-13T15:30Z", ticker: "GLD", qty: "+40", price: "$188.10", fee: "12 bp" },
  { ts: "2025-06-06T15:30Z", ticker: "BND", qty: "+200", price: "$75.44", fee: "12 bp" },
  { ts: "2025-05-30T15:30Z", ticker: "BTC-USD", qty: "-0.45", price: "$62,350.00", fee: "12 bp" },
];

const formatPercent = (value: number | null, options?: { sign?: boolean }) => {
  if (value === null || value === undefined) return "—";
  const pct = (value * 100).toFixed(2);
  const prefix = options?.sign ? (Number(pct) >= 0 ? "+" : "") : "";
  return `${prefix}${pct}%`;
};

const DemoPage = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="border border-border rounded-lg bg-card p-6 mb-8">
          <p className="text-lg text-foreground font-medium">Run Metiseon locally or in the cloud. No accounts, no API keys.</p>
        </div>

        <section className="grid md:grid-cols-2 gap-6 mb-12">
          <div className="border border-border rounded-lg bg-card p-6 flex flex-col gap-4">
            <div>
              <p className="text-sm uppercase tracking-wide text-muted-foreground">Run in Codespace / Colab</p>
              <p className="text-foreground font-semibold text-xl mt-1">Open in a preconfigured environment.</p>
            </div>
            <div className="flex gap-3">
              <a
                href="https://github.com/metiseon/landing#readme"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center justify-center rounded-md bg-auric px-4 py-2 text-midnight font-semibold hover:bg-auric/90"
              >
                Open in Codespaces
              </a>
              <a
                href="https://colab.research.google.com/"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center justify-center rounded-md border border-auric/40 px-4 py-2 text-auric font-semibold hover:bg-auric/10"
              >
                Open in Colab
              </a>
            </div>
          </div>

          <div className="border border-border rounded-lg bg-card p-6 flex flex-col gap-4">
            <div>
              <p className="text-sm uppercase tracking-wide text-muted-foreground">Run locally (CLI)</p>
              <p className="text-foreground font-semibold text-xl mt-1">Deterministic weekly loop, MEΩ denominated.</p>
            </div>
            <CodeBlock code={cliCode} />
          </div>
        </section>

        <section className="grid lg:grid-cols-3 gap-8 mb-12">
          <div className="lg:col-span-2 space-y-4">
            <div className="border border-border rounded-lg bg-card p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-2xl font-semibold text-foreground symbols">MEΩ Backtest (2015–2025)</h2>
                  <p className="text-sm text-muted-foreground">NAV (MEΩ); deterministic weekly loop</p>
                </div>
                <span className="inline-flex items-center gap-2 text-xs font-mono border border-auric/40 text-auric px-3 py-1 rounded symbols">
                  MEΩ-native
                </span>
              </div>
              <div className="border border-border rounded-lg overflow-hidden bg-background">
                <Image src="/charts/nav_meo.svg" alt="NAV (MEΩ), 2015–2025" width={1280} height={720} className="w-full h-auto" priority />
              </div>
              <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="border border-border rounded-lg p-3 bg-card/70">
                  <p className="text-xs text-muted-foreground symbols">GINα (YTD)</p>
                  <p className="text-lg font-mono font-semibold text-auric">{formatPercent(navStats.gin_alpha_ytd, { sign: true })}</p>
                </div>
                <div className="border border-border rounded-lg p-3 bg-card/70">
                  <p className="text-xs text-muted-foreground symbols">σ<sub>63</sub></p>
                  <p className="text-lg font-mono font-semibold">{formatPercent(navStats.sigma_63)}</p>
                </div>
                <div className="border border-border rounded-lg p-3 bg-card/70">
                  <p className="text-xs text-muted-foreground symbols">CVaR<sub>95</sub></p>
                  <p className="text-lg font-mono font-semibold text-signal">-{formatPercent(navStats.cvar_95)}</p>
                </div>
                <div className="border border-border rounded-lg p-3 bg-card/70">
                  <p className="text-xs text-muted-foreground">SlipCap</p>
                  <p className="text-lg font-mono font-semibold">{navStats.slipcap_bp} bp</p>
                </div>
              </div>
            </div>
          </div>

          <div className="border border-border rounded-lg bg-card p-6 space-y-4">
            <div>
              <h2 className="text-xl font-semibold text-foreground">Weekly decision trace</h2>
              <p className="text-sm text-muted-foreground">The last Friday in the backtest: scores → σ gate → cost cap → chosen</p>
            </div>

            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="font-mono text-muted-foreground">Date</div>
              <div className="font-mono text-foreground">{decisionTrace.date}</div>
              <div className="font-mono text-muted-foreground">Last winner excluded</div>
              <div className="font-mono text-foreground">{decisionTrace.last_winner_excluded ?? "—"}</div>
              <div className="font-mono text-muted-foreground">Candidates</div>
              <div className="font-mono text-foreground">{decisionTrace.candidates.join(", ")}</div>
              <div className="font-mono text-muted-foreground">Chosen</div>
              <div className="font-mono text-foreground symbols">{decisionTrace.chosen}</div>
            </div>

            <div className="border border-border rounded-lg bg-card/60 p-3">
              <p className="text-xs text-muted-foreground mb-2 font-semibold">Scores (Durability-Lite)</p>
              <div className="grid grid-cols-2 gap-2 font-mono text-sm">
                {Object.entries(decisionTrace.scores).map(([ticker, score]) => (
                  <div key={ticker} className="flex justify-between">
                    <span className="text-muted-foreground">{ticker}</span>
                    <span className="text-foreground">{score}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="border border-border rounded-lg bg-card/60 p-3">
              <p className="text-xs text-muted-foreground mb-2 font-semibold symbols">σ (MEΩ-relative)</p>
              <div className="grid grid-cols-2 gap-2 font-mono text-sm">
                {Object.entries(decisionTrace.sigma).map(([ticker, sigma]) => (
                  <div key={ticker} className="flex justify-between">
                    <span className="text-muted-foreground">{ticker}</span>
                    <span className="text-foreground">{formatPercent(sigma, { sign: false })}</span>
                  </div>
                ))}
                <div className="flex justify-between pt-2 border-t border-border/60 col-span-2">
                  <span className="text-muted-foreground">median σ</span>
                  <span className="text-foreground">{formatPercent(decisionTrace.sigma_median)}</span>
                </div>
              </div>
            </div>

            <div className="border border-border rounded-lg bg-card/60 p-3 font-mono text-sm space-y-1">
              <div className="flex justify-between"><span className="text-muted-foreground">Fee</span><span className="text-foreground">{decisionTrace.fee_bp} bp</span></div>
              <div className="flex justify-between"><span className="text-muted-foreground">√impact</span><span className="text-foreground">{decisionTrace.impact_bp} bp</span></div>
              <div className="flex justify-between"><span className="text-muted-foreground">Cap</span><span className="text-foreground">{decisionTrace.cap_bp} bp</span></div>
              <div className="flex justify-between"><span className="text-muted-foreground">Allowed?</span><span className="text-foreground">{decisionTrace.trade_allowed ? "yes" : "no"}</span></div>
            </div>
          </div>
        </section>

        <section className="grid lg:grid-cols-3 gap-8 mb-12">
          <div className="border border-border rounded-lg bg-card p-6 lg:col-span-2 space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xl font-semibold text-foreground">Audit visuals</h3>
                <p className="text-sm text-muted-foreground">Durability flags and σ gate, frozen to the demo week.</p>
              </div>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <figure className="border border-border rounded-lg bg-background overflow-hidden">
                <Image src="/logic/score_breakdown.svg" alt="Durability-Lite flags (base=25)" width={640} height={320} className="w-full h-auto" />
                <figcaption className="text-xs text-muted-foreground p-3">Durability-Lite flags (base=25)</figcaption>
              </figure>
              <figure className="border border-border rounded-lg bg-background overflow-hidden">
                <Image src="/logic/sigma_gate.svg" alt="σ histogram (median in orange, chosen in green)" width={640} height={320} className="w-full h-auto" />
                <figcaption className="text-xs text-muted-foreground p-3 symbols">σ histogram (median in orange, chosen in green)</figcaption>
              </figure>
            </div>
          </div>

          <div className="border border-border rounded-lg bg-card p-6 space-y-4">
            <div>
              <h3 className="text-xl font-semibold text-foreground symbols">MEΩ top-10 weights</h3>
              <p className="text-sm text-muted-foreground">
                Weights recomputed daily from open feeds; persisted as (date, symbol, weight, meo_usd, m_world_usd).
              </p>
            </div>
            <div className="border border-border rounded-lg overflow-hidden bg-background">
              <Image src="/logic/meo_weights.svg" alt="MEΩ top-10 weights" width={640} height={320} className="w-full h-auto" />
            </div>
          </div>
        </section>

        <section className="grid lg:grid-cols-2 gap-8 mb-12">
          <div className="border border-border rounded-lg bg-card p-6 space-y-4">
            <div>
              <h3 className="text-xl font-semibold text-foreground">Embedded DuckDB ledger</h3>
              <p className="text-sm text-muted-foreground">Every trade, fee, and position is on-ledger</p>
            </div>
            <CodeBlock code={ledgerCode} language="sql" />
            <div className="border border-border rounded-lg overflow-hidden bg-background">
              <Image src="/logic/ledger_card.svg" alt="Ledger rows preview" width={640} height={260} className="w-full h-auto" />
            </div>
          </div>

          <div className="border border-border rounded-lg bg-card p-6 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-semibold text-foreground">Live ledger snapshot</h3>
              <span className="text-xs font-mono px-2 py-1 rounded bg-auric/10 text-auric border border-auric/40">read-only</span>
            </div>
            <div className="overflow-auto border border-border rounded-lg">
              <table className="min-w-full text-sm font-mono">
                <thead className="bg-muted/20 text-muted-foreground">
                  <tr>
                    <th className="px-3 py-2 text-left">ts</th>
                    <th className="px-3 py-2 text-left">ticker</th>
                    <th className="px-3 py-2 text-left">qty</th>
                    <th className="px-3 py-2 text-left">price</th>
                    <th className="px-3 py-2 text-left">fee</th>
                  </tr>
                </thead>
                <tbody>
                  {ledgerRows.map((row) => (
                    <tr key={row.ts} className="border-t border-border/60">
                      <td className="px-3 py-2 text-foreground">{row.ts}</td>
                      <td className="px-3 py-2 text-foreground">{row.ticker}</td>
                      <td className="px-3 py-2 text-foreground">{row.qty}</td>
                      <td className="px-3 py-2 text-foreground">{row.price}</td>
                      <td className="px-3 py-2 text-foreground">{row.fee}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <footer className="border border-border rounded-lg bg-card p-6 flex flex-col md:flex-row gap-2 md:items-center md:justify-between">
          <span className="font-mono text-sm symbols">Powered by Mêtior (MEΩ)</span>
          <span className="text-sm text-muted-foreground">Public data: Yahoo, FRED, Alpha Vantage (demo), CoinGecko</span>
          <span className="text-sm text-muted-foreground">Prototype. Paper trading only. No investment advice.</span>
        </footer>
      </main>
    </div>
  );
};

export default DemoPage;
