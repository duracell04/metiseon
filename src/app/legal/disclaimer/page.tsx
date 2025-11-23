import { Header } from "@/components/Header";

const LegalDisclaimerPage = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-4xl font-bold text-foreground mb-4">Legal Disclaimer</h1>
          <p className="text-lg text-muted-foreground mb-12">Important information about Metiseon's prototype status and limitations.</p>

          <div className="prose prose-sm max-w-none">
            <div className="border border-border rounded-lg p-8 bg-card">
              <h2 className="text-xl font-semibold text-foreground mb-6">Prototype Software Notice</h2>

              <div className="space-y-4 text-muted-foreground leading-relaxed">
                <p>
                  <strong className="text-foreground">Prototype software.</strong> Metiseon is research software provided as-is for educational and
                  demonstration purposes only. It is not production-ready and has not been audited or tested for live trading.
                </p>

                <p>
                  <strong className="text-foreground">Paper trading only.</strong> All backtests and simulations are historical. Metiseon does not execute
                  real trades, manage real capital, or interact with brokerage accounts. Results shown are hypothetical.
                </p>

                <p>
                  <strong className="text-foreground">Public data sources.</strong> Market data is sourced from Yahoo Finance, FRED, Alpha Vantage (demo tier),
                  and CoinGecko. Data quality, availability, and accuracy are subject to third-party limitations. No guarantees are made regarding data
                  completeness.
                </p>

                <p>
                  <strong className="text-foreground">No investment advice.</strong> Nothing on this site or in Metiseon's output constitutes financial,
                  investment, tax, or legal advice. Do not make investment decisions based on this software without consulting qualified professionals.
                </p>

                <p>
                  <strong className="text-foreground">MEΩ-denominated results.</strong> All performance metrics are expressed in{" "}
                  <a href="https://metior.akalabs.dev/" target="_blank" rel="noreferrer" className="text-auric underline symbols">
                    Metior (MEΩ)
                  </a>
                  , a synthetic numeraire. Results may differ materially when converted to any fiat currency. Currency conversion introduces additional risks
                  and uncertainties.
                </p>

                <p>
                  <strong className="text-foreground">GINα performance metric.</strong> Global Interest-Rate Neutral Alpha (GINα) is a research metric designed
                  to isolate skill from currency and interest-rate effects. It is not a standard industry metric and may not be comparable to traditional
                  performance measures.
                </p>

                <p>
                  <strong className="text-foreground">No warranties.</strong> Metiseon is provided "as is" without warranties of any kind, express or implied,
                  including but not limited to fitness for a particular purpose, merchantability, or non-infringement.
                </p>

                <p>
                  <strong className="text-foreground">Limitation of liability.</strong> The creators and contributors of Metiseon shall not be liable for any
                  damages arising from the use or inability to use this software, including but not limited to financial losses, data loss, or business
                  interruption.
                </p>
              </div>

              <div className="mt-8 pt-6 border-t border-border">
                <p className="text-xs text-muted-foreground">
                  By using Metiseon, you acknowledge that you have read, understood, and agree to this disclaimer. If you do not agree, do not use this
                  software.
                </p>
                <p className="text-xs text-muted-foreground mt-2">Last updated: 2025-01-01</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default LegalDisclaimerPage;
