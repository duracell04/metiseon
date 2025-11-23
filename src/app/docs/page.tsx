import { ReactNode } from "react";
import { Header } from "@/components/Header";
import { Button } from "@/components/ui/button";
import { ExternalLink, FileText } from "lucide-react";

type Paper = {
  title: ReactNode;
  description: string;
  path: string;
  type: string;
};

const papers: Paper[] = [
  {
    title: (
      <>
        <span className="symbols">MEΩ</span>:{" "}
        <a href="https://metior.akalabs.dev/" target="_blank" rel="noreferrer" className="text-auric underline symbols">
          Metior
        </a>{" "}
        Numeraire
      </>
    ),
    description:
      "Construction, governance, and stability analysis of the MEΩ global numeraire. Inclusion requires public M2 or free-float mcap >= 1% of MEΩ. Weights recompute daily from open feeds; zero discretion; persisted as (date, symbol, weight, meo_usd, m_world_usd).",
    path: "/mnt/data/Metiseon Robo-Allocator.pdf",
    type: "Core",
  },
  {
    title: <span className="symbols">GINα: Global Interest-Rate Neutral Alpha</span>,
    description:
      "Performance metric that isolates skill from currency effects and interest-rate environments. Formula: ((1 + R) / (1 + r_IRS + I_MEΩ)) - 1 - carry.",
    path: "/mnt/data/GINA.pdf",
    type: "Metric",
  },
  {
    title: "Mathematical Appendix",
    description:
      "Complete derivations, proofs, and numerical methods. Includes DCC-GARCH correlation estimation, replicator dynamics, and EVT tail thresholds.",
    path: "#",
    type: "Math",
  },
];

const stability = {
  title: <span className="symbols">MEΩ Stability Analysis</span>,
  content:
    "MEΩ vs USD/EUR/CHF (1970–today) shows lower drift/vol; construction uses DCC-GARCH for correlations, replicator dynamics for weights, EVT thresholds for tail stability.",
};

const DocsPage = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold text-foreground mb-4">Documentation</h1>
          <p className="text-lg text-muted-foreground mb-12">Technical papers, mathematical foundations, and implementation details.</p>

          <div className="grid md:grid-cols-2 gap-6 mb-12">
            {papers.map((paper) => (
              <div key={paper.path} className="border border-border rounded-lg p-6 bg-card hover:border-auric/50 transition-colors">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <FileText className="w-5 h-5 text-auric" />
                    <span className="text-xs font-mono text-muted-foreground">{paper.type}</span>
                  </div>
                </div>
                <h3 className="text-lg font-semibold text-foreground mb-2">{paper.title}</h3>
                <p className="text-sm text-muted-foreground mb-4 leading-relaxed">{paper.description}</p>
                <Button variant="outline" size="sm" className="w-full">
                  <ExternalLink className="w-4 h-4 mr-2" />
                  Open PDF
                </Button>
              </div>
            ))}
          </div>

          <div className="border border-border rounded-lg p-6 bg-card mb-12">
            <h2 className="text-xl font-semibold text-foreground mb-3">{stability.title}</h2>
            <p className="text-muted-foreground leading-relaxed">{stability.content}</p>
          </div>

          <div className="border border-auric/30 bg-auric/5 rounded-lg p-6">
            <h3 className="font-semibold text-foreground mb-3 symbols">MEΩ Governance</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Inclusion requires public M2 or free-float mcap >= 1% of MEΩ. Weights recompute daily from open feeds; zero discretion; persisted as (date,
              symbol, weight, meo_usd, m_world_usd).
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DocsPage;
