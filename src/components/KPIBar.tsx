interface KPIBarProps {
  metrics: {
    label: string;
    value: string;
    variant?: "default" | "positive" | "warning" | "focus";
  }[];
}

export const KPIBar = ({ metrics }: KPIBarProps) => {
  const variantClasses = {
    default: "text-foreground",
    positive: "text-graphgreen",
    warning: "text-signal",
    focus: "text-auric",
  };

  return (
    <div className="border border-border rounded bg-card p-4">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {metrics.map((metric, idx) => (
          <div key={idx} className="flex flex-col gap-1">
            <span className="text-xs text-muted-foreground uppercase tracking-wide">
              {metric.label}
            </span>
            <span className={`font-mono text-lg font-semibold ${variantClasses[metric.variant || "default"]}`}>
              {metric.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
