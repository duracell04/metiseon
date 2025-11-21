import { Header } from "@/components/Header";
import { CodeBlock } from "@/components/CodeBlock";
import { Button } from "@/components/ui/button";
import { Github, Play } from "lucide-react";

const Demo = () => {
  const cliCode = `python run.py backtest --start 2015-01-01 --end 2025-01-01 --denom MEΩ
open reports/latest.html`;

  const ledgerCode = `SELECT ts, ticker, qty, price, fee 
FROM trades 
ORDER BY ts DESC 
LIMIT 5;`;

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold text-foreground mb-4">Demo</h1>
          <p className="text-lg text-muted-foreground mb-12">
            Run Metiseon locally or in the cloud. No accounts, no API keys required.
          </p>

          <div className="space-y-8">
            {/* Run in Cloud */}
            <div className="border border-border rounded-lg p-6 bg-card">
              <h2 className="text-xl font-semibold text-foreground mb-4">
                Run in Codespace / Colab
              </h2>
              <p className="text-muted-foreground mb-6">
                Click to launch a pre-configured environment with all dependencies installed.
              </p>
              <div className="flex gap-4">
                <Button className="bg-auric text-midnight hover:bg-auric/90">
                  <Github className="w-4 h-4 mr-2" />
                  Open in Codespaces
                </Button>
                <Button variant="outline">
                  <Play className="w-4 h-4 mr-2" />
                  Open in Colab
                </Button>
              </div>
            </div>

            {/* Local CLI */}
            <div className="border border-border rounded-lg p-6 bg-card">
              <h2 className="text-xl font-semibold text-foreground mb-4">
                Run locally (CLI)
              </h2>
              <p className="text-muted-foreground mb-4">
                Clone the repository and run a backtest with a single command.
              </p>
              <CodeBlock code={cliCode} />
            </div>

            {/* Ledger Teaser */}
            <div className="border border-border rounded-lg p-6 bg-card">
              <h2 className="text-xl font-semibold text-foreground mb-4">
                Embedded DuckDB ledger
              </h2>
              <p className="text-muted-foreground mb-4">
                Every trade, fee, and position is recorded in an embedded database. 
                Query the ledger directly with SQL.
              </p>
              <CodeBlock code={ledgerCode} language="sql" />
            </div>

            {/* No Keys Required */}
            <div className="border border-auric/30 bg-auric/5 rounded-lg p-6">
              <h3 className="font-semibold text-foreground mb-2">
                No accounts or keys required
              </h3>
              <p className="text-sm text-muted-foreground">
                Metiseon uses only public data sources. No sign-ups, no API keys, no credentials. 
                Just clone and run.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Demo;
