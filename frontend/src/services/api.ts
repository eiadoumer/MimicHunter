import type { CompareFilesResponse } from "../types/plagiarism";

const API_BASE = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/+$/, "");

type LegacyAnalyzePair = {
  doc_a: number;
  doc_b: number;
  score: number;
  label?: string;
};

type LegacyAnalyzeResponse = {
  documents?: Array<{ id: number; filename?: string }>;
  pairs?: LegacyAnalyzePair[];
  top_pairs?: LegacyAnalyzePair[];
  report_text?: string;
  error?: string;
};

function normalizeResponse(data: CompareFilesResponse | LegacyAnalyzeResponse): CompareFilesResponse {
  // Already in the new app contract.
  if ("suspicious_pairs" in data && "thresholds" in data && "inverted_index_summary" in data) {
    return data;
  }

  const high = 0.5;
  const moderate = 0.25;
  const basePairs = data.top_pairs ?? data.pairs ?? [];
  const pairs = basePairs.map((p, idx) => ({
    rank: idx + 1,
    doc_a: p.doc_a,
    doc_b: p.doc_b,
    score: p.score,
    label:
      p.label ??
      (p.score >= high ? "HIGH SIMILARITY" : p.score >= moderate ? "MODERATE SIMILARITY" : "LOW SIMILARITY"),
  }));

  const suspicious_pairs = pairs.filter((p) => p.score >= high);
  const documents = (data.documents ?? []).map((d) => ({ id: d.id, token_count: 0 }));

  return {
    documents,
    pairs,
    suspicious_pairs,
    thresholds: { high, moderate },
    inverted_index_summary: { total_ngrams: 0, buckets: [] },
  };
}

export async function compareFiles(files: File[]): Promise<CompareFilesResponse> {
  const fd = new FormData();
  for (const file of files) {
    fd.append("files", file, file.name);
  }

  const res = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    body: fd,
  });
  const data = (await res.json()) as CompareFilesResponse | LegacyAnalyzeResponse;
  if (!res.ok) {
    throw new Error(("error" in data && data.error) || "Request failed");
  }
  return normalizeResponse(data);
}
