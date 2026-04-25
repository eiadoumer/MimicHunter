import { useState } from "react";

import ResultsList from "../components/ResultsList";
import StatusMessage from "../components/StatusMessage";
import { compareFiles } from "../services/api";
import type { CompareFilesResponse, DocumentSummary } from "../types/plagiarism";

function docDisplayName(documents: DocumentSummary[], id: number) {
  const row = documents.find((d) => d.id === id);
  return row?.filename?.trim() ? row.filename : `Document ${id}`;
}

function similarityTier(score: number) {
  if (score >= 0.5) return { tier: "high", label: "HIGH SIMILARITY (plagiarism suspected)" };
  if (score >= 0.25) return { tier: "moderate", label: "MODERATE SIMILARITY" };
  return { tier: "low", label: "LOW SIMILARITY" };
}

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [dragOver, setDragOver] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<CompareFilesResponse | null>(null);
  const [ngramSize, setNgramSize] = useState(2);
  const [applyStemming, setApplyStemming] = useState(true);
  const [removeStopwords, setRemoveStopwords] = useState(true);

  async function onRun() {
    setError(null);
    setResult(null);
    if (files.length < 2) {
      setError("Please upload at least two .txt files.");
      return;
    }
    setLoading(true);
    try {
      const data = await compareFiles(files, { ngramSize, applyStemming, removeStopwords });
      setResult(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unknown error";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  function addFiles(incoming: FileList | File[]) {
    const list = Array.from(incoming).filter((f) => f.name.toLowerCase().endsWith(".txt"));
    if (list.length === 0) {
      setError("Please add .txt files only.");
      return;
    }
    setError(null);
    setFiles((prev) => {
      const map = new Map(prev.map((f) => [f.name, f]));
      for (const f of list) map.set(f.name, f);
      return Array.from(map.values());
    });
  }

  function clearFiles() {
    setFiles([]);
    setResult(null);
    setError(null);
  }

  const topScore = result?.pairs?.[0]?.score ?? 0;
  const topTier = similarityTier(topScore);

  return (
    <div className="app">
      <div className="app__bg" aria-hidden />

      <header className="header">
        <div className="header__inner">
          <div className="header__brand">
            <span className="header__mark" aria-hidden />
            <div>
              <p className="header__eyebrow">Document Similarity</p>
              <h1 className="header__title">Mimic Hunter Dashboard</h1>
              <p className="header__sub">
                Upload plain-text files and detect overlap using the preserved hashing and Jaccard
                pipeline.
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="main">
        <section
          className={`dropzone ${dragOver ? "dropzone--active" : ""} ${loading ? "dropzone--loading" : ""}`}
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragOver(false);
            addFiles(e.dataTransfer.files);
          }}
        >
          <div className="dropzone__inner">
            {loading ? (
              <div className="loading-block">
                <div className="spinner" aria-hidden />
                <p className="loading-block__text">Running preprocess, hash index, and pairwise Jaccard...</p>
              </div>
            ) : (
              <>
                <p className="dropzone__head">Drop submissions here</p>
                <p className="dropzone__hint">Only UTF-8 .txt files, at least two files required</p>
                <label className="btn btn--ghost">
                  Browse files
                  <input
                    type="file"
                    accept=".txt,text/plain"
                    multiple
                    className="sr-only"
                    onChange={(e) => addFiles(e.target.files || [])}
                  />
                </label>
              </>
            )}
          </div>
        </section>

        {files.length > 0 && (
          <section className="panel panel--files">
            <div className="panel__head">
              <h2>Queue</h2>
              <button type="button" className="btn btn--text" onClick={clearFiles} disabled={loading}>
                Clear
              </button>
            </div>
            <ul className="file-list">
              {files.map((f) => (
                <li key={f.name} className="file-list__item">
                  <span className="file-list__icon" aria-hidden />
                  <span className="file-list__name">{f.name}</span>
                  <span className="file-list__meta">{(f.size / 1024).toFixed(1)} KB</span>
                </li>
              ))}
            </ul>
            <div className="actions">
              <div className="analysis-controls">
                <label className="analysis-controls__field">
                  <span className="analysis-controls__label">n-gram size</span>
                  <input
                    className="analysis-controls__input"
                    type="number"
                    min={1}
                    max={5}
                    value={ngramSize}
                    onChange={(e) => {
                      const parsed = Number(e.target.value);
                      if (!Number.isNaN(parsed)) {
                        setNgramSize(Math.min(5, Math.max(1, Math.trunc(parsed))));
                      }
                    }}
                    disabled={loading}
                  />
                </label>

                <label className="analysis-controls__checkbox">
                  <input
                    type="checkbox"
                    checked={applyStemming}
                    onChange={(e) => setApplyStemming(e.target.checked)}
                    disabled={loading}
                  />
                  <span>Apply stemming</span>
                </label>

                <label className="analysis-controls__checkbox">
                  <input
                    type="checkbox"
                    checked={removeStopwords}
                    onChange={(e) => setRemoveStopwords(e.target.checked)}
                    disabled={loading}
                  />
                  <span>Remove stopwords</span>
                </label>
              </div>
              <button type="button" className="btn btn--primary" onClick={onRun} disabled={loading}>
                {loading ? "Analyzing..." : "Run plagiarism detection"}
              </button>
            </div>
          </section>
        )}

        <StatusMessage error={error} loading={loading} />

        {result && (
          <>
            <section className="stats-strip">
              <div className="stats-strip__item">
                <span className="stats-strip__label">Documents</span>
                <span className="stats-strip__value">{result.documents.length}</span>
              </div>
              <div className="stats-strip__item">
                <span className="stats-strip__label">Top pairs shown</span>
                <span className="stats-strip__value">{result.pairs.length}</span>
                <span className="stats-strip__hint">(capped)</span>
              </div>
              <div className="stats-strip__item">
                <span className="stats-strip__label">Suspicious pairs</span>
                <span className="stats-strip__value">{result.suspicious_pairs.length}</span>
              </div>
              <div className="stats-strip__item stats-strip__item--accent">
                <span className="stats-strip__label">Top match</span>
                <span className="stats-strip__value">{(topScore * 100).toFixed(2)}%</span>
                <span className={`pill pill--${topTier.tier}`}>{topTier.label}</span>
              </div>
            </section>

            <p className="results-note">
              {result.note ??
                "Pair lists are limited to 50 entries for optimization (smaller payloads and faster responses)."}
            </p>

            <section className="panel panel--results">
              <h2>Document index</h2>
              <ul className="doc-index">
                {result.documents.map((d) => (
                  <li key={d.id}>
                    <span className="doc-index__id">{d.id}</span>
                    <span className="doc-index__name">{docDisplayName(result.documents, d.id)}</span>
                  </li>
                ))}
              </ul>
            </section>

            <ResultsList
              title="Top overlapping pairs"
              items={result.pairs}
              docLabel={(id) => docDisplayName(result.documents, id)}
            />
            <ResultsList
              title="Suspicious documents / pairs"
              items={result.suspicious_pairs}
              docLabel={(id) => docDisplayName(result.documents, id)}
            />
          </>
        )}
      </main>

      <footer className="footer">
        <span>All rights reserved @2026 - Mimic Hunter</span>
      </footer>
    </div>
  );
}
