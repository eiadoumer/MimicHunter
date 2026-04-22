from app.hashing.hashing import lookup_ngram
from app.tree.tree import RedBlackTree


def jaccard_for_pair(doc_id1, doc_id2, documents, inverted_index):
    set1 = set(documents[doc_id1 - 1][1])
    set2 = set(documents[doc_id2 - 1][1])
    if len(set1) > len(set2):
        set1, set2 = set2, set1
        doc_id1, doc_id2 = doc_id2, doc_id1

    intersection = 0
    for ngram in set1:
        doc_ids = lookup_ngram(ngram, inverted_index)
        if doc_ids is not None and doc_id2 in doc_ids:
            intersection += 1
    union = len(set1) + len(set2) - intersection
    return intersection / union


def compute_all_jaccard(documents, inverted_index):
    rb_tree = RedBlackTree()
    n = len(documents)
    for i in range(n):
        doc_id1 = documents[i][0]
        for j in range(i + 1, n):
            doc_id2 = documents[j][0]
            score = jaccard_for_pair(doc_id1, doc_id2, documents, inverted_index)
            rb_tree.insert(score, (doc_id1, doc_id2))
    return rb_tree
from app.hashing.hashing import lookup_ngram
from app.tree.tree import RedBlackTree


def jaccard_for_pair(doc_id1, doc_id2, documents, inverted_index):
    set1 = set(documents[doc_id1 - 1][1])
    set2 = set(documents[doc_id2 - 1][1])
    if len(set1) > len(set2):
        set1, set2 = set2, set1
        doc_id1, doc_id2 = doc_id2, doc_id1

    intersection = 0
    for ngram in set1:
        doc_ids = lookup_ngram(ngram, inverted_index)
        if doc_ids is not None and doc_id2 in doc_ids:
            intersection += 1
    union = len(set1) + len(set2) - intersection
    return intersection / union


def compute_all_jaccard(documents, inverted_index):
    rb_tree = RedBlackTree()
    n = len(documents)
    for i in range(n):
        doc_id1 = documents[i][0]
        for j in range(i + 1, n):
            doc_id2 = documents[j][0]
            score = jaccard_for_pair(doc_id1, doc_id2, documents, inverted_index)
            rb_tree.insert(score, (doc_id1, doc_id2))
    return rb_tree
