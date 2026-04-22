from pydantic import BaseModel


class PairResult(BaseModel):
    rank: int
    doc_a: int
    doc_b: int
    score: float
    label: str


class DocumentSummary(BaseModel):
    id: int
    token_count: int


class BucketSummary(BaseModel):
    bucket: str
    count: int


class InvertedIndexSummary(BaseModel):
    total_ngrams: int
    buckets: list[BucketSummary]


class CompareFilesResponse(BaseModel):
    documents: list[DocumentSummary]
    pairs: list[PairResult]
    suspicious_pairs: list[PairResult]
    thresholds: dict[str, float]
    inverted_index_summary: InvertedIndexSummary


class ErrorResponse(BaseModel):
    error: str
