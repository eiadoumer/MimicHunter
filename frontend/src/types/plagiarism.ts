export type PairResult = {
  rank: number;
  doc_a: number;
  doc_b: number;
  score: number;
  label: string;
  shared_ngrams?: string[];
  shared_ngrams_total?: number;
};

export type DocumentSummary = {
  id: number;
  filename?: string;
  token_count: number;
};

export type BucketSummary = {
  bucket: string;
  count: number;
};

export type CompareFilesResponse = {
  note?: string;
  documents: DocumentSummary[];
  pairs: PairResult[];
  suspicious_pairs: PairResult[];
  thresholds: { high: number; moderate: number };
  inverted_index_summary: {
    total_ngrams: number;
    buckets: BucketSummary[];
  };
};
