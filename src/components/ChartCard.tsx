"use client";

interface ChartCardProps {
  title: string;
  subtitle?: string;
  footer?: string;
  children: React.ReactNode;
  heightClass?: string;
}

export const ChartCard = ({ title, subtitle, footer, children, heightClass = "h-64" }: ChartCardProps) => {
  return (
    <div className="border border-border rounded bg-card p-6">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-foreground">{title}</h3>
        {subtitle && <p className="text-sm text-muted-foreground mt-1">{subtitle}</p>}
      </div>
      <div className={`${heightClass} flex items-end justify-center border border-border/50 rounded bg-background/50 relative`}>
        {children}
        {footer && (
          <div className="absolute bottom-2 left-2 text-xs text-muted-foreground font-mono">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
};
