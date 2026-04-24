import string
from nltk.stem import PorterStemmer


STOPWORDS = ["the", "is", "in", "and", "of", "to", "a", "an", "on", "for", "with"]
stemmer = PorterStemmer()


def generate_ngrams(tokens, n=2):
    ngrams = []
    for i in range(len(tokens) - n + 1):
        ngram = tuple(tokens[i : i + n])
        ngrams.append(ngram)
    return ngrams


def preprocess_documents(documents, remove_stopwords=False, apply_stemming=False, ngram_size=None):
    processed_docs = []
    for doc_id, tokens in documents:
        if remove_stopwords:
            tokens = [word for word in tokens if word not in STOPWORDS]
        if apply_stemming:
            tokens = [stemmer.stem(word) for word in tokens]
        if ngram_size:
            tokens = generate_ngrams(tokens, ngram_size)
        processed_docs.append((doc_id, tokens))
    return processed_docs


def normalize_text_to_words(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    words = [word for word in words if word.isalpha()]
    return words
