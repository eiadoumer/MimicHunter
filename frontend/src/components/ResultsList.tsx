import type { PairResult } from "../types/plagiarism";
import ResultCard from "./ResultCard";

type Props = {
  title: string;
  items: PairResult[];
  docLabel: (id: number) => string;
};

export default function ResultsList({ title, items, docLabel }: Props) {
  return (
    <section className="panel panel--pairs">
      <div className="panel__intro">
        <h2>{title}</h2>
        <p className="panel__note">Ranked by similarity score from highest to lowest.</p>
      </div>
      {items.length === 0 ? (
        <p className="panel__note">No items.</p>
      ) : (
        <div className="pair-grid">
          {items.map((item) => (
            <ResultCard
              key={`${item.doc_a}-${item.doc_b}-${item.rank}`}
              pair={item}
              docLabel={docLabel}
            />
          ))}
        </div>
      )}
    </section>
  );
}
