from app.file_reader.file_reader import read_uploaded_files
from app.hashing.hashing import build_inverted_index
from app.jaccard_similarity.jaccard_similarity import compute_all_jaccard
from app.preprocessing.preprocessing import preprocess_documents
from app.utils.utils import build_inverted_index_summary, high_similarity_label


def run_plagiarism_pipeline(uploaded_files):
    documents = read_uploaded_files(uploaded_files)
    if len(documents) < 2:
        return {"error": "At least two .txt documents are required."}

    clean_documents = preprocess_documents(
        documents,
        remove_stopwords=True,
        apply_stemming=True,
        ngram_size=2,
    )
    inverted_index = build_inverted_index(clean_documents)
    rb_tree = compute_all_jaccard(clean_documents, inverted_index)

    all_pairs = rb_tree.get_sorted_descending()
    high_pairs = []
    rb_tree.collect_high_similarity(rb_tree.root, high_pairs, threshold=0.5)

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
        suspicious_pairs.append(
            {
                "rank": rank,
                "doc_a": doc1,
                "doc_b": doc2,
                "score": score,
                "label": high_similarity_label(rank, total_high, score),
            }
        )

    bucket_summary = build_inverted_index_summary(inverted_index)
    return {
        "documents": [{"id": doc_id, "token_count": len(tokens)} for doc_id, tokens in documents],
        "pairs": ranked_pairs,
        "suspicious_pairs": suspicious_pairs,
        "thresholds": {"high": 0.5, "moderate": 0.25},
        "inverted_index_summary": bucket_summary,
    }
