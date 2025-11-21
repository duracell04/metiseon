interface ChartCardProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
}

export const ChartCard = ({ title, subtitle, children }: ChartCardProps) => {
  return (
    <div className="border border-border rounded bg-card p-6">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-foreground">{title}</h3>
        {subtitle && (
          <p className="text-sm text-muted-foreground mt-1">{subtitle}</p>
        )}
      </div>
      <div className="h-64 flex items-end justify-center border border-border/50 rounded bg-background/50 relative">
        {children}
        <div className="absolute bottom-2 left-2 text-xs text-muted-foreground font-mono">
          NAV (MEΩ)
        </div>
      </div>
    </div>
  );
};
