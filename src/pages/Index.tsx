import { Header } from "@/components/Header";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Link } from "react-router-dom";
import { Check } from "lucide-react";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Hero Section */}
        <div className="max-w-4xl mx-auto text-center mb-24">
          <div className="mb-8 flex justify-center">
            <div className="w-20 h-20 bg-midnight rounded-lg flex items-center justify-center">
              <span className="text-auric font-bold text-4xl">ΣM</span>
            </div>
          </div>
          
          <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6 leading-tight">
            Open math. Deterministic capital. Benchmarked in MEΩ.
          </h1>
          
          <p className="text-lg md:text-xl text-muted-foreground mb-8 leading-relaxed max-w-3xl mx-auto">
            Metiseon is a deterministic, open-math robo-allocator. It thinks in Mêtior (MEΩ), 
            so performance is currency-neutral, inflation-aware, and reproducible. Same inputs → same trades.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <Button size="lg" className="bg-auric text-midnight hover:bg-auric/90">
              Run a 10-year backtest
            </Button>
            <Button size="lg" variant="link" className="text-auric">
              Show me the equations →
            </Button>
          </div>
          
          <div className="flex justify-center mb-8">
            <Badge variant="outline" className="border-auric/30 text-auric px-4 py-2">
              <span className="font-mono">Powered by Mêtior (MEΩ)</span>
            </Badge>
          </div>
        </div>

        {/* Proof Bullets */}
        <div className="max-w-5xl mx-auto mb-24">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="border border-border rounded-lg p-6 bg-card">
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-auric/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <Check className="w-4 h-4 text-auric" />
                </div>
                <div>
                  <h3 className="font-semibold text-foreground mb-2">Deterministic</h3>
                  <p className="text-sm text-muted-foreground">
                    Weekly rules, fixed costs, embedded DuckDB ledger.
                  </p>
                </div>
              </div>
            </div>

            <div className="border border-border rounded-lg p-6 bg-card">
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-auric/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <Check className="w-4 h-4 text-auric" />
                </div>
                <div>
                  <h3 className="font-semibold text-foreground mb-2">MEΩ-native</h3>
                  <p className="text-sm text-muted-foreground">
                    Global numéraire (fiat M2 + metals + crypto).
                  </p>
                </div>
              </div>
            </div>

            <div className="border border-border rounded-lg p-6 bg-card">
              <div className="flex items-start gap-3">
                <div className="w-6 h-6 rounded-full bg-auric/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <Check className="w-4 h-4 text-auric" />
                </div>
                <div>
                  <h3 className="font-semibold text-foreground mb-2">GINα</h3>
                  <p className="text-sm text-muted-foreground">
                    Interest-rate neutral alpha—skill, not currency luck.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footnote */}
        <div className="max-w-4xl mx-auto border-t border-border pt-8">
          <p className="text-xs text-muted-foreground text-center">
            Prototype. Paper trading only. Public data sources: Yahoo, FRED, Alpha Vantage, CoinGecko.
          </p>
        </div>
      </main>
    </div>
  );
};

export default Index;
