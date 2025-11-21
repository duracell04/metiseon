import { Header } from "@/components/Header";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";

const Brand = () => {
  const assets = [
    {
      name: "Σ-M Monogram (Solid)",
      file: "metiseon_sigmam_solid.svg",
      path: "/mnt/data/metiseon_sigmam_solid.svg",
      size: "2 KB"
    },
    {
      name: "Σ-M Monogram (Outline)",
      file: "metiseon_sigmam_outline.svg",
      path: "/mnt/data/metiseon_sigmam_outline.svg",
      size: "2 KB"
    },
    {
      name: "Lock-up Logo",
      file: "metiseon_lockup.svg",
      path: "/mnt/data/metiseon_lockup.svg",
      size: "3 KB"
    },
    {
      name: "MEΩ Coin Badge",
      file: "metior_meo_badge.svg",
      path: "/mnt/data/metior_meo_badge.svg",
      size: "4 KB"
    },
    {
      name: "Brand Tokens (JSON)",
      file: "brand.json",
      path: "/mnt/data/brand.json",
      size: "1 KB"
    },
    {
      name: "Palette (CSS)",
      file: "palette.css",
      path: "/mnt/data/palette.css",
      size: "1 KB"
    }
  ];

  const guidelines = [
    {
      rule: "Minimum Size",
      value: "24px height for monogram, 120px width for lock-up"
    },
    {
      rule: "Clear Space",
      value: "Equal to height of monogram on all sides"
    },
    {
      rule: "Primary Color",
      value: "Auric (#C8A156) on Midnight (#0B1220)"
    },
    {
      rule: "Secondary Color",
      value: "Platinum (#A9B2C3) for supporting elements"
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold text-foreground mb-4">Brand Assets</h1>
          <p className="text-lg text-muted-foreground mb-12">
            Download logos, color palettes, and brand guidelines. All assets are open-source.
          </p>

          {/* Logo Preview */}
          <div className="border border-border rounded-lg p-12 bg-card mb-12 flex items-center justify-center">
            <div className="w-32 h-32 bg-midnight rounded-lg flex items-center justify-center">
              <span className="text-auric font-bold text-6xl">ΣM</span>
            </div>
          </div>

          {/* Assets Grid */}
          <div className="mb-12">
            <h2 className="text-xl font-semibold text-foreground mb-6">Downloads</h2>
            <div className="grid md:grid-cols-2 gap-4">
              {assets.map((asset, idx) => (
                <div key={idx} className="border border-border rounded-lg p-4 bg-card flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-foreground text-sm">{asset.name}</h3>
                    <p className="text-xs text-muted-foreground mt-1">
                      {asset.file} • {asset.size}
                    </p>
                  </div>
                  <Button size="sm" variant="outline">
                    <Download className="w-4 h-4" />
                  </Button>
                </div>
              ))}
            </div>
          </div>

          {/* Guidelines */}
          <div className="mb-12">
            <h2 className="text-xl font-semibold text-foreground mb-6">Usage Guidelines</h2>
            <div className="border border-border rounded-lg bg-card divide-y divide-border">
              {guidelines.map((guideline, idx) => (
                <div key={idx} className="p-4 flex items-center justify-between">
                  <span className="text-sm font-medium text-foreground">{guideline.rule}</span>
                  <span className="text-sm text-muted-foreground font-mono">{guideline.value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Color Palette */}
          <div>
            <h2 className="text-xl font-semibold text-foreground mb-6">Color Palette</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { name: "Midnight", hex: "#0B1220", var: "--midnight" },
                { name: "Auric", hex: "#C8A156", var: "--auric" },
                { name: "Platinum", hex: "#A9B2C3", var: "--platinum" },
                { name: "Snow", hex: "#F8FAFC", var: "--snow" },
                { name: "Ink", hex: "#111827", var: "--ink" },
                { name: "Graph Green", hex: "#2ECC71", var: "--graph-green" },
                { name: "Signal Orange", hex: "#FF7A45", var: "--signal-orange" }
              ].map((color, idx) => (
                <div key={idx} className="border border-border rounded-lg overflow-hidden bg-card">
                  <div 
                    className="h-24" 
                    style={{ backgroundColor: color.hex }}
                  />
                  <div className="p-3">
                    <p className="text-xs font-semibold text-foreground">{color.name}</p>
                    <p className="text-xs text-muted-foreground font-mono mt-1">{color.hex}</p>
                    <p className="text-xs text-muted-foreground font-mono">{color.var}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Brand;
