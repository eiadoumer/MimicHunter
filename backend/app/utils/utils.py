def high_similarity_label(rank, total_high, score):
    if rank == 1:
        return "MOST SUSPICIOUS"
    if rank == total_high:
        return "LEAST SIMILAR"
    if score >= 0.75:
        return "SUSPICIOUS"
    return "HIGH SIMILARITY"


def build_inverted_index_summary(inverted_index):
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
    return {"total_ngrams": total_ngrams, "buckets": buckets}
