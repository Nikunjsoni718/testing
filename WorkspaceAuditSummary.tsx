import React from 'react';

export interface AuditMetric {
  category: string;
  score: number;
  criticalIssuesCount: number;
}

export interface WorkspaceAuditSummaryProps {
  repositoryName: string;
  overallScore: number;
  metrics: AuditMetric[];
  onRefresh?: () => void;
}

export const WorkspaceAuditSummary: React.FC<WorkspaceAuditSummaryProps> = ({
  repositoryName,
  overallScore,
  metrics,
  onRefresh,
}) => {
  const getScoreBadgeClass = (score: number): string => {
    if (score >= 80) return 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20';
    if (score >= 50) return 'text-amber-500 bg-amber-500/10 border-amber-500/20';
    return 'text-rose-500 bg-rose-500/10 border-rose-500/20';
  };

  return (
    <section className="rounded-xl border border-neutral-800 bg-neutral-900/60 p-6 backdrop-blur">
      <header className="flex items-center justify-between border-b border-neutral-800 pb-4">
        <div>
          <h2 className="text-lg font-semibold text-neutral-100">{repositoryName}</h2>
          <p className="text-xs text-neutral-400">Automated Audit & Compliance Score</p>
        </div>
        <div className={`rounded-full border px-3 py-1 text-sm font-bold ${getScoreBadgeClass(overallScore)}`}>
          {overallScore}/100
        </div>
      </header>

      <ul className="mt-4 space-y-2">
        {metrics.map((metric) => (
          <li
            key={metric.category}
            className="flex items-center justify-between rounded-lg bg-neutral-800/40 px-3 py-2 text-sm"
          >
            <span className="text-neutral-300">{metric.category}</span>
            <div className="flex items-center gap-3">
              {metric.criticalIssuesCount > 0 && (
                <span className="text-xs text-rose-400 font-medium">
                  {metric.criticalIssuesCount} issues
                </span>
              )}
              <span className="font-mono text-neutral-200">{metric.score}%</span>
            </div>
          </li>
        ))}
      </ul>

      {onRefresh && (
        <button
          type="button"
          onClick={onRefresh}
          className="mt-5 w-full rounded-lg bg-neutral-800 py-2 text-xs font-medium text-neutral-200 transition hover:bg-neutral-700 active:scale-[0.99]"
        >
          Trigger Re-Audit
        </button>
      )}
    </section>
  );
};