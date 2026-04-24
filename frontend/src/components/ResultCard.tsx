import type { PairResult } from "../types/plagiarism";
import ScoreBadge from "./ScoreBadge";

type Props = {
  pair: PairResult;
  docLabel: (id: number) => string;
};

export default function ResultCard({ pair, docLabel }: Props) {
  return (
    <article className="pair-card">
      <div className="pair-card__top">
        <span className="pair-card__rank">#{pair.rank}</span>
        <div className="pair-card__titles">
          <span className="pair-card__name">
            <span className="pair-card__id">{pair.doc_a}</span> {docLabel(pair.doc_a)}
          </span>
          <span className="pair-card__vs" aria-hidden>
            ↔
          </span>
          <span className="pair-card__name">
            <span className="pair-card__id">{pair.doc_b}</span> {docLabel(pair.doc_b)}
          </span>
        </div>
        <div className="pair-card__score-block">
          <span className="pair-card__pct">{(pair.score * 100).toFixed(2)}%</span>
          <ScoreBadge score={pair.score} label={pair.label} />
        </div>
      </div>
    </article>
  );
}
