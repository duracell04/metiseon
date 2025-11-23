import { Header } from "@/components/Header";
import { ChartCard } from "@/components/ChartCard";
import { KPIBar } from "@/components/KPIBar";

const sampleEquities = [
  {
    ticker: "AAPL",
    name: "Apple Inc.",
    gina: "+4.2%",
    sigma: "18.3%",
    cvar: "-12.1%",
    slipcap: "28bp",
    spark: [18, 16, 15, 12, 14, 10, 9, 8, 6, 5],
  },
  {
    ticker: "MSFT",
    name: "Microsoft Corp.",
    gina: "+3.8%",
    sigma: "16.7%",
    cvar: "-10.8%",
    slipcap: "25bp",
    spark: [20, 19, 17, 15, 16, 14, 12, 13, 11, 10],
  },
  {
    ticker: "GOOGL",
    name: "Alphabet Inc.",
    gina: "+5.1%",
    sigma: "21.2%",
    cvar: "-14.3%",
    slipcap: "31bp",
    spark: [22, 20, 18, 15, 17, 16, 14, 12, 11, 9],
  },
  {
    ticker: "NVDA",
    name: "NVIDIA Corp.",
    gina: "+7.6%",
    sigma: "34.5%",
    cvar: "-23.7%",
    slipcap: "42bp",
    spark: [24, 25, 22, 20, 23, 21, 19, 18, 16, 15],
  },
  {
    ticker: "JPM",
    name: "JPMorgan Chase",
    gina: "+2.1%",
    sigma: "22.1%",
    cvar: "-15.2%",
    slipcap: "33bp",
    spark: [12, 11, 10, 9, 10, 8, 7, 8, 7, 6],
  },
  {
    ticker: "V",
    name: "Visa Inc.",
    gina: "+3.4%",
    sigma: "17.9%",
    cvar: "-11.5%",
    slipcap: "27bp",
    spark: [14, 15, 13, 12, 13, 11, 10, 11, 9, 8],
  },
];

const portfolioMetrics = [
  { label: "GINI�", value: "+4.3%", variant: "focus" as const },
  { label: "I��,+�,�", value: "19.2%", variant: "default" as const },
  { label: "CVaR�,%�,.", value: "-13.4%", variant: "warning" as const },
  { label: "SlipCap", value: "29bp", variant: "default" as const },
];

const sparkToPath = (points: number[]) => {
  const step = 100 / Math.max(points.length - 1, 1);
  return points.map((value, index) => `${index === 0 ? "M" : "L"} ${index * step} ${30 - value}`).join(" ");
};

const ReportsPage = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl font-bold text-foreground mb-4">Reports</h1>
          <p className="text-lg text-muted-foreground mb-8">Portfolio performance in MEIc. All metrics are currency-neutral and inflation-aware.</p>

          <div className="mb-12">
            <h2 className="text-xl font-semibold text-foreground mb-4">Portfolio Overview</h2>
            <KPIBar metrics={portfolioMetrics} />
          </div>

          <div className="mb-12">
            <ChartCard title="NAV Performance" subtitle="MEIc-denominated net asset value (2015-2025)">
              <div className="w-full h-full flex items-end px-4 pb-8">
                <svg className="w-full h-full" viewBox="0 0 400 200" preserveAspectRatio="none">
                  <path d="M 0 180 Q 100 160 200 120 T 400 60 L 400 200 L 0 200 Z" fill="hsl(var(--platinum))" opacity="0.2" />
                  <path d="M 0 180 Q 100 160 200 120 T 400 50" fill="none" stroke="hsl(var(--auric))" strokeWidth="2" />
                </svg>
              </div>
            </ChartCard>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-foreground mb-4">Individual Equities</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {sampleEquities.map((equity) => (
                <div key={equity.ticker} className="border border-border rounded-lg p-6 bg-card">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="font-mono font-semibold text-foreground">{equity.ticker}</h3>
                      <p className="text-sm text-muted-foreground mt-1">{equity.name}</p>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-muted-foreground">GINI�</span>
                      <span className="font-mono text-sm font-semibold text-auric">{equity.gina}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-muted-foreground">I��,+�,�</span>
                      <span className="font-mono text-sm">{equity.sigma}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-muted-foreground">CVaR�,%�,.</span>
                      <span className="font-mono text-sm text-signal">{equity.cvar}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-muted-foreground">SlipCap</span>
                      <span className="font-mono text-sm">{equity.slipcap}</span>
                    </div>
                  </div>

                  <div className="mt-4 h-16 border border-border/50 rounded bg-background/50">
                    <svg className="w-full h-full" viewBox="0 0 100 30" preserveAspectRatio="none">
                      <path d={sparkToPath(equity.spark)} fill="none" stroke="hsl(var(--auric))" strokeWidth="1" />
                    </svg>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-12 border-t border-border pt-8">
            <p className="text-xs text-muted-foreground">
              All performance metrics are MEIc-denominated. GINI� isolates skill from currency effects. I��,+�,� is 63-day realized volatility. CVaR�,%�,. is 95%
              conditional value at risk. SlipCap is the maximum allowable trading cost per position change.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ReportsPage;
