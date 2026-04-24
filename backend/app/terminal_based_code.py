import sys
from pathlib import Path

# Allow running this file directly: python backend/app/terminal_based_code.py
backend_root = Path(__file__).resolve().parents[1]
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

from app.file_reader.file_reader import read_documents
from app.hashing.hashing import build_inverted_index
from app.jaccard_similarity.jaccard_similarity import compute_all_jaccard
from app.preprocessing.preprocessing import preprocess_documents


def high_similarity_label(rank, total_high, score):
    if rank == 1:
        return "MOST SUSPICIOUS"
    if rank == total_high:
        return "LEAST SIMILAR"
    if score >= 0.75:
        return "SUSPICIOUS"
    return "HIGH SIMILARITY"


def display_bucket_details(inverted_index):
    print("\n" + "=" * 70)
    print("INVERTED INDEX - ALL BUCKETS SUMMARY")
    print("=" * 70)

    total_ngrams = 0
    for outer_idx in range(26):
        bucket_letter = chr(outer_idx + ord("a"))
        content = []
        for inner_idx in range(1009):
            slot = inverted_index[outer_idx][inner_idx]
            if slot is not None:
                content.append(slot)

        count = len(content)
        total_ngrams += count
        if count > 0:
            print(f"\n📁 Bucket '{bucket_letter.upper()}' ({bucket_letter}) : {count} n-grams")
            print("   Samples:")
            for ngram, docs in content:
                print(f"     → {ngram} : {docs}")
        else:
            print(f"\n📁 Bucket '{bucket_letter.upper()}' ({bucket_letter}) : 0 n-grams (empty)")

    print("\n" + "=" * 70)
    print(f"TOTAL N-GRAMS STORED: {total_ngrams}")
    print("=" * 70)


def display_distribution_chart(inverted_index):
    print("\n DISTRIBUTION BAR CHART:")
    print("   (Each █ = 1 n-gram, max 30 shown)")
    for outer_idx in range(26):
        letter = chr(outer_idx + ord("a")).upper()
        count = 0
        for inner_idx in range(1009):
            if inverted_index[outer_idx][inner_idx] is not None:
                count += 1
        if count > 0:
            bar = "█" * min(count, 30)
            print(f"   {letter}: {bar} ({count})")
        else:
            print(f"   {letter}: (0)")


def display_high_similarity_pairs(rb_tree, threshold=0.5):
    high_pairs = []
    rb_tree.collect_high_similarity(rb_tree.root, high_pairs, threshold)
    if not high_pairs:
        print("No document pairs found with similarity >= 0.5.")
        return

    print(f"{'Rank':<4} {'Pair':<12} {'Score':<8} {'Label'}")
    print("-" * 50)
    total_high = len(high_pairs)
    for rank, (doc1, doc2, score) in enumerate(high_pairs, start=1):
        label = high_similarity_label(rank, total_high, score)
        print(f"{rank:<4} Doc{doc1}-Doc{doc2:<5} {score:.2f}     {label}")


def main():
    folder_path = input("Enter folder path: ").strip().strip('"').strip("'") # for copying from  file exploerer
    documents = read_documents(folder_path)
    print("\nDocuments Loaded.")
    for doc_id, words in documents:
        print(f"Doc {doc_id}: {len(words)} words")

    clean_documents = preprocess_documents(
        documents,
        remove_stopwords=True,
        apply_stemming=True,
        ngram_size=2,
    )

    print("\nPreprocessed Documents.")
    for doc_id, tokens in clean_documents:
        print(f"\nDoc {doc_id}:")
        print(tokens)

    inverted_index = build_inverted_index(clean_documents)
    print("Inverted index built successfully.")

    display_bucket_details(inverted_index)
    display_distribution_chart(inverted_index)

    print("STEP 4: COMPUTING JACCARD SIMILARITIES")
    print("=" * 70)
    rb_tree = compute_all_jaccard(clean_documents, inverted_index)
    rb_tree.display_sorted_pairs(threshold_high=0.5, threshold_moderate=0.25)
    display_high_similarity_pairs(rb_tree, threshold=0.5)


if __name__ == "__main__":
    main()
