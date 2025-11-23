import { Header } from "@/components/Header";

const ginFormula = (
  <div className="space-y-2">
    <div className="font-mono text-sm symbols">
      GINα<sub>t</sub> = (1 + R<sub>t</sub><sup>P</sup>) / (1 + r<sub>t</sub><sup>IRS</sup> + π<sub>t</sub><sup>MEΩ</sup>) − 1 − C<sub>carry,t</sub>
    </div>
    <div className="text-xs text-muted-foreground symbols">
      r<sub>t</sub><sup>IRS</sup> = global interest-rate surface (polynomial fit, CIP-constrained)
      <br />
      π<sub>t</sub><sup>MEΩ</sup> = MEΩ-weighted global inflation
      <br />
      C<sub>carry,t</sub> = funding / storage / staking net costs
    </div>
  </div>
);

const asciiFallback = (
  <div className="space-y-1 font-mono text-xs">
    <div>GIN alpha = ((1 + R^P) / (1 + r_IRS + pi_MEO)) - 1 - carry</div>
    <div className="text-muted-foreground">
      Use MEO for environments that cannot render Ω; sigma_63 for σ&lt;sub&gt;63&lt;/sub&gt;.
    </div>
  </div>
);

const sections = [
  {
    title: "Data",
    content:
      "Adj Close & Volume (Yahoo), fundamentals (Alpha Vantage demo), benchmarks (FRED), crypto caps (CoinGecko). 24 h HTTP cache; ≤ 1-day forward fill for EOD gaps.",
  },
  {
    title: "Score (Durability-Lite)",
    content:
      "Binary, explainable rules: ROE > 12 %, D/E < 1, Margin > 10 %, Insider > 2 %, R&D/Rev > 5 %; penalty if (D/E > 1 ∧ Insider < 1 %). Score clamped to 0–100.",
  },
  {
    title: "Risk",
    content: "Volatility σ via GARCH(1,1) on MEΩ-relative returns; CVaR<sub>95</sub> reported for tails.",
  },
  {
    title: "Allocation",
    content: "Drop last winner → keep tickers with σ ≤ median(σ) → pick highest Durability score; tie → lower σ.",
  },
  {
    title: "Cost gate",
    content:
      "Fee 12 bp + slippage from √impact: impact_decimal = 0.001 × √(qty / ADV10); impact_bp = 10000 × impact_decimal. Skip trade if fee_bp + impact_bp > SlipCap (35 bp default).",
  },
  {
    title: "Numéraire & GINα",
    content: "Everything is expressed in MEΩ. Performance is reported as GINα, below.",
    formula: ginFormula,
    fallback: asciiFallback,
  },
];

const HowItWorksPage = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold text-foreground mb-4">How it works</h1>
          <p className="text-lg text-muted-foreground mb-12">
            Deterministic allocation in six steps. Each rule is fixed, testable, and reproducible.
          </p>

          <div className="space-y-8">
            {sections.map((section, idx) => (
              <div key={section.title} className="border border-border rounded-lg p-6 bg-card">
                <div className="flex gap-4">
                  <div className="flex-shrink-0">
                    <div className="w-10 h-10 rounded-full bg-auric/10 flex items-center justify-center">
                      <span className="font-mono font-semibold text-auric">{idx + 1}</span>
                    </div>
                  </div>
                  <div className="flex-1">
                    <h2 className="text-xl font-semibold text-foreground mb-3">{section.title}</h2>
                    <p className="text-muted-foreground leading-relaxed">{section.content}</p>
                    {section.formula && (
                      <div className="mt-4 bg-midnight text-snow p-4 rounded border border-border">{section.formula}</div>
                    )}
                    {section.fallback && (
                      <div className="mt-3 bg-muted/30 text-foreground p-3 rounded border border-border/60">{section.fallback}</div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-12 border-t border-border pt-8">
            <p className="text-sm text-muted-foreground">
              All steps are deterministic. Given identical inputs and timestamps, the system produces identical outputs. No discretion, no optimization, no
              look-ahead bias.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default HowItWorksPage;
