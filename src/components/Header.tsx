import { Link } from "react-router-dom";
import { Badge } from "@/components/ui/badge";

export const Header = () => {
  return (
    <header className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-8 h-8 bg-midnight rounded flex items-center justify-center">
              <span className="text-auric font-bold text-lg">ΣM</span>
            </div>
            <span className="font-semibold text-foreground">Metiseon</span>
          </Link>
          
          <nav className="hidden md:flex items-center gap-6">
            <Link to="/" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Home
            </Link>
            <Link to="/how-it-works" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              How it works
            </Link>
            <Link to="/demo" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Demo
            </Link>
            <Link to="/docs" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Docs
            </Link>
            <Link to="/reports" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Reports
            </Link>
          </nav>
          
          <Badge variant="outline" className="hidden sm:flex items-center gap-1.5 border-auric/30 text-auric">
            <span className="font-mono text-xs">Powered by Mêtior (MEΩ)</span>
          </Badge>
        </div>
      </div>
    </header>
  );
};
