import { Header } from "@/components/Header";
import { KPIBar } from "@/components/KPIBar";
import { ChartCard } from "@/components/ChartCard";

const Reports = () => {
  const sampleEquities = [
    {
      ticker: "AAPL",
      name: "Apple Inc.",
      gina: "+4.2%",
      sigma: "18.3%",
      cvar: "-12.1%",
      slipcap: "28bp"
    },
    {
      ticker: "MSFT",
      name: "Microsoft Corp.",
      gina: "+3.8%",
      sigma: "16.7%",
      cvar: "-10.8%",
      slipcap: "25bp"
    },
    {
      ticker: "GOOGL",
      name: "Alphabet Inc.",
      gina: "+5.1%",
      sigma: "21.2%",
      cvar: "-14.3%",
      slipcap: "31bp"
    },
    {
      ticker: "NVDA",
      name: "NVIDIA Corp.",
      gina: "+7.6%",
      sigma: "34.5%",
      cvar: "-23.7%",
      slipcap: "42bp"
    },
    {
      ticker: "JPM",
      name: "JPMorgan Chase",
      gina: "+2.1%",
      sigma: "22.1%",
      cvar: "-15.2%",
      slipcap: "33bp"
    },
    {
      ticker: "V",
      name: "Visa Inc.",
      gina: "+3.4%",
      sigma: "17.9%",
      cvar: "-11.5%",
      slipcap: "27bp"
    }
  ];

  const portfolioMetrics = [
    { label: "GINα", value: "+4.3%", variant: "focus" as const },
    { label: "σ₆₃", value: "19.2%", variant: "default" as const },
    { label: "CVaR₉₅", value: "-13.4%", variant: "warning" as const },
    { label: "SlipCap", value: "29bp", variant: "default" as const }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl font-bold text-foreground mb-4">Reports</h1>
          <p className="text-lg text-muted-foreground mb-8">
            Portfolio performance in MEΩ. All metrics are currency-neutral and inflation-aware.
          </p>

          {/* Portfolio KPIs */}
          <div className="mb-12">
            <h2 className="text-xl font-semibold text-foreground mb-4">Portfolio Overview</h2>
            <KPIBar metrics={portfolioMetrics} />
          </div>

          {/* Portfolio Chart */}
          <div className="mb-12">
            <ChartCard 
              title="NAV Performance" 
              subtitle="MEΩ-denominated net asset value (2015-2025)"
            >
              <div className="w-full h-full flex items-end px-4 pb-8">
                <svg className="w-full h-full" viewBox="0 0 400 200" preserveAspectRatio="none">
                  {/* Platinum band (40% alpha) */}
                  <path
                    d="M 0 180 Q 100 160 200 120 T 400 60 L 400 200 L 0 200 Z"
                    fill="hsl(var(--platinum))"
                    opacity="0.2"
                  />
                  {/* Auric line */}
                  <path
                    d="M 0 180 Q 100 160 200 120 T 400 50"
                    fill="none"
                    stroke="hsl(var(--auric))"
                    strokeWidth="2"
                  />
                </svg>
              </div>
            </ChartCard>
          </div>

          {/* Equity Cards */}
          <div>
            <h2 className="text-xl font-semibold text-foreground mb-4">Individual Equities</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {sampleEquities.map((equity, idx) => (
                <div key={idx} className="border border-border rounded-lg p-6 bg-card">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="font-mono font-semibold text-foreground">{equity.ticker}</h3>
                      <p className="text-sm text-muted-foreground mt-1">{equity.name}</p>
                    </div>
                  </div>
                  
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-muted-foreground">GINα</span>
                      <span className="font-mono text-sm font-semibold text-auric">{equity.gina}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-muted-foreground">σ₆₃</span>
                      <span className="font-mono text-sm">{equity.sigma}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-muted-foreground">CVaR₉₅</span>
                      <span className="font-mono text-sm text-signal">{equity.cvar}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-muted-foreground">SlipCap</span>
                      <span className="font-mono text-sm">{equity.slipcap}</span>
                    </div>
                  </div>

                  {/* Mini chart */}
                  <div className="mt-4 h-16 border border-border/50 rounded bg-background/50">
                    <svg className="w-full h-full" viewBox="0 0 100 30" preserveAspectRatio="none">
                      <path
                        d={`M 0 ${20 + Math.random() * 5} ${Array.from({ length: 9 }, (_, i) => 
                          `L ${(i + 1) * 10} ${20 + Math.random() * 10}`
                        ).join(' ')}`}
                        fill="none"
                        stroke="hsl(var(--auric))"
                        strokeWidth="1"
                      />
                    </svg>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Footnote */}
          <div className="mt-12 border-t border-border pt-8">
            <p className="text-xs text-muted-foreground">
              All performance metrics are MEΩ-denominated. GINα isolates skill from currency effects. 
              σ₆₃ is 63-day realized volatility. CVaR₉₅ is 95% conditional value at risk. 
              SlipCap is the maximum allowable trading cost per position change.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Reports;
