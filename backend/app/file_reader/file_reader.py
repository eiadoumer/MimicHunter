import os

from app.sorting.sorting import merge_sort
from app.preprocessing.preprocessing import normalize_text_to_words


def read_documents(folder_path):
    documents = []
    doc_id = 1
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    sorted_files = merge_sort(txt_files)
    for filename in sorted_files:
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            words = normalize_text_to_words(text)
            documents.append((doc_id, words))
            doc_id += 1
    return documents


def read_uploaded_files(uploaded_files):
    documents = []
    doc_id = 1
    sorted_files = merge_sort(list(uploaded_files))
    for filename, text in sorted_files:
        words = normalize_text_to_words(text)
        documents.append((doc_id, words))
        doc_id += 1
    return documents
