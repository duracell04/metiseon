import { Header } from "@/components/Header";

const HowItWorks = () => {
  const sections = [
    {
      title: "Data",
      content: "Adj Close & Volume (Yahoo), fundamentals (AV demo), benchmarks (FRED), crypto caps (CoinGecko). 24h cache; ≤1-day forward fill."
    },
    {
      title: "Score (Durability-Lite)",
      content: "Binary, explainable rules: ROE > 12, D/E < 1, Margin > 10, Insider > 2, R&D/Rev > 5, penalty for levered/low-skin. Score 0–100."
    },
    {
      title: "Risk",
      content: "σ via GARCH(1,1) on MEΩ-relative returns. CVaR for reporting."
    },
    {
      title: "Allocation",
      content: "Drop last winner → σ ≤ median → arg-max score → tie → lower σ."
    },
    {
      title: "Cost gate",
      content: "Fee 12 bp + √impact; skip if > cap (default 35 bp)."
    },
    {
      title: "Numéraire & GINα",
      content: "Everything can be expressed in MEΩ; performance as GINα: ((1 + R) / (1 + r_IRS + π_MEΩ)) − 1 − carry.",
      formula: "GINα = ((1 + R) / (1 + r_IRS + π_MEΩ)) − 1 − carry"
    }
  ];

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
              <div key={idx} className="border border-border rounded-lg p-6 bg-card">
                <div className="flex gap-4">
                  <div className="flex-shrink-0">
                    <div className="w-10 h-10 rounded-full bg-auric/10 flex items-center justify-center">
                      <span className="font-mono font-semibold text-auric">{idx + 1}</span>
                    </div>
                  </div>
                  <div className="flex-1">
                    <h2 className="text-xl font-semibold text-foreground mb-3">
                      {section.title}
                    </h2>
                    <p className="text-muted-foreground leading-relaxed">
                      {section.content}
                    </p>
                    {section.formula && (
                      <div className="mt-4 bg-midnight text-snow p-4 rounded font-mono text-sm border border-border">
                        {section.formula}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-12 border-t border-border pt-8">
            <p className="text-sm text-muted-foreground">
              All steps are deterministic. Given identical inputs and timestamps, the system produces 
              identical outputs. No discretion, no optimization, no look-ahead bias.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default HowItWorks;
