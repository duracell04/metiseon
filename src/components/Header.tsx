"use client";

import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { NavLink } from "@/components/NavLink";

export const Header = () => {
  return (
    <header className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center gap-3">
            <div className="w-8 h-8 bg-midnight rounded flex items-center justify-center">
              <span className="text-auric font-bold text-lg symbols">ΣM</span>
            </div>
            <span className="font-semibold text-foreground">Metiseon</span>
          </Link>

          <nav className="hidden md:flex items-center gap-6">
            <NavLink href="/" className="text-sm text-muted-foreground hover:text-foreground transition-colors" activeClassName="text-foreground">
              Home
            </NavLink>
            <NavLink href="/how-it-works" className="text-sm text-muted-foreground hover:text-foreground transition-colors" activeClassName="text-foreground">
              How it works
            </NavLink>
            <NavLink href="/demo" className="text-sm text-muted-foreground hover:text-foreground transition-colors" activeClassName="text-foreground">
              Demo
            </NavLink>
            <NavLink href="/docs" className="text-sm text-muted-foreground hover:text-foreground transition-colors" activeClassName="text-foreground">
              Docs
            </NavLink>
            <NavLink href="/reports" className="text-sm text-muted-foreground hover:text-foreground transition-colors" activeClassName="text-foreground">
              Reports
            </NavLink>
          </nav>

          <Badge variant="outline" className="hidden sm:flex items-center gap-1.5 border-auric/30 text-auric">
            <span className="font-mono text-xs symbols">Powered by Metior (MEΩ)</span>
          </Badge>
        </div>
      </div>
    </header>
  );
};
