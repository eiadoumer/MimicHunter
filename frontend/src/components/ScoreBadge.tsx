type Props = {
  score: number;
  label: string;
};

export default function ScoreBadge({ score, label }: Props) {
  const pct = Math.min(100, Math.max(0, score * 100));
  const tierClass =
    score >= 0.5 ? "meter__fill meter__fill--high" : score >= 0.25 ? "meter__fill meter__fill--mod" : "meter__fill meter__fill--low";
  const pillClass = score >= 0.5 ? "pill pill--high" : score >= 0.25 ? "pill pill--moderate" : "pill pill--low";
  return (
    <>
      <div className="score-cell">
        <span className="score-cell__val">{pct.toFixed(2)}%</span>
        <div className="meter" aria-hidden>
          <div className={tierClass} style={{ width: `${pct}%` }} />
        </div>
      </div>
      <span className={pillClass}>{label}</span>
    </>
  );
}
