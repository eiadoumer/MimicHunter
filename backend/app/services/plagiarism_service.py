from app.file_reader.file_reader import read_uploaded_files
from app.hashing.hashing import build_inverted_index
from app.jaccard_similarity.jaccard_similarity import compute_all_jaccard
from app.preprocessing.preprocessing import preprocess_documents

MAX_RESPONSE_PAIRS = 50


def run_plagiarism_pipeline(uploaded_files):
    documents = read_uploaded_files(uploaded_files)
    if len(documents) < 2:
        return {"error": "At least two .txt documents are required."}

    doc_rows = [(doc_id, words) for doc_id, _filename, words in documents]
    clean_documents = preprocess_documents(
        doc_rows,
        remove_stopwords=True,
        apply_stemming=True,
        ngram_size=2,
    )
    inverted_index = build_inverted_index(clean_documents)
    rb_tree = compute_all_jaccard(clean_documents, inverted_index)

    all_pairs = rb_tree.get_sorted_descending()[:MAX_RESPONSE_PAIRS]
    high_pairs = []
    rb_tree.collect_high_similarity(rb_tree.root, high_pairs, threshold=0.5)
    high_pairs = high_pairs[:MAX_RESPONSE_PAIRS]

    ranked_pairs = []
    for rank, (doc1, doc2, score) in enumerate(all_pairs, start=1):
        label = "LOW SIMILARITY"
        if score >= 0.5:
            label = "HIGH SIMILARITY"
        elif score >= 0.25:
            label = "MODERATE SIMILARITY"
        ranked_pairs.append(
            {"rank": rank, "doc_a": doc1, "doc_b": doc2, "score": score, "label": label}
        )

    suspicious_pairs = []
    total_high = len(high_pairs)
    for rank, (doc1, doc2, score) in enumerate(high_pairs, start=1):
        label = "HIGH SIMILARITY"
        if rank == 1:
            label = "MOST SUSPICIOUS"
        elif rank == total_high:
            label = "LEAST SIMILAR"
        elif score >= 0.75:
            label = "SUSPICIOUS"

        suspicious_pairs.append(
            {
                "rank": rank,
                "doc_a": doc1,
                "doc_b": doc2,
                "score": score,
                "label": label,
            }
        )

    total_ngrams = 0
    buckets = []
    for outer_idx in range(26):
        bucket_letter = chr(outer_idx + ord("a"))
        count = 0
        for j in range(1009):
            if inverted_index[outer_idx][j] is not None:
                count += 1
        total_ngrams += count
        buckets.append({"bucket": bucket_letter, "count": count})

    bucket_summary = {"total_ngrams": total_ngrams, "buckets": buckets}
    return {
        "documents": [
            {"id": doc_id, "filename": filename, "token_count": len(tokens)}
            for doc_id, filename, tokens in documents
        ],
        "pairs": ranked_pairs,
        "suspicious_pairs": suspicious_pairs,
        "thresholds": {"high": 0.5, "moderate": 0.25},
        "inverted_index_summary": bucket_summary,
    }
