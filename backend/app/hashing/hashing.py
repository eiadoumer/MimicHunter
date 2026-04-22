def h2(ngram, m=1009):
    s = " ".join(ngram)
    return 1 + (len(s) % 10)


def h1(ngram, m=1009):
    s = " ".join(ngram)
    result = 0
    for j in range(len(s)):
        power = len(s) - 1 - j
        term = ord(s[j]) * pow(31, power, m)
        result = (result + term) % m
    return result


def probe(ngram, i, m=1009):
    return (h1(ngram, m) + i * h2(ngram, m)) % m


def build_inverted_index(documents):
    table = [[None for _ in range(1009)] for _ in range(26)]
    for doc_id, ngrams in documents:
        for ngram in ngrams:
            first_char = ngram[0][0]
            if not ("a" <= first_char <= "z"):
                continue
            outer_idx = ord(first_char) - ord("a")
            i = 0
            while i < 1009:
                inner_idx = probe(ngram, i)
                slot = table[outer_idx][inner_idx]
                if slot is None:
                    table[outer_idx][inner_idx] = (ngram, [doc_id])
                    break
                elif slot[0] == ngram:
                    if doc_id not in slot[1]:
                        slot[1].append(doc_id)
                    break
                i += 1
    return table


def lookup_ngram(ngram, inverted_index):
    first_char = ngram[0][0]
    if not ("a" <= first_char <= "z"):
        return None
    outer_idx = ord(first_char) - ord("a")
    i = 0
    while i < 1009:
        inner_idx = probe(ngram, i)
        slot = inverted_index[outer_idx][inner_idx]
        if slot is None:
            return None
        if slot[0] == ngram:
            return slot[1]
        i += 1
    return None
def h2(ngram, m=1009):
    s = " ".join(ngram)
    return 1 + (len(s) % 10)


def h1(ngram, m=1009):
    s = " ".join(ngram)
    result = 0

    for j in range(len(s)):
        power = len(s) - 1 - j
        term = ord(s[j]) * pow(31, power, m)
        result = (result + term) % m
    return result


def probe(ngram, i, m=1009):
    return (h1(ngram, m) + i * h2(ngram, m)) % m


def build_inverted_index(documents):
    table = [[None for _ in range(1009)] for _ in range(26)]
    for doc_id, ngrams in documents:
        for ngram in ngrams:
            first_char = ngram[0][0]
            if not ("a" <= first_char <= "z"):
                continue
            outer_idx = ord(first_char) - ord("a")
            i = 0
            while i < 1009:
                inner_idx = probe(ngram, i)
                slot = table[outer_idx][inner_idx]
                if slot is None:
                    table[outer_idx][inner_idx] = (ngram, [doc_id])
                    break
                elif slot[0] == ngram:
                    if doc_id not in slot[1]:
                        slot[1].append(doc_id)
                    break
                i += 1
    return table


def lookup_ngram(ngram, inverted_index):
    first_char = ngram[0][0]
    if not ("a" <= first_char <= "z"):
        return None
    outer_idx = ord(first_char) - ord("a")
    i = 0
    while i < 1009:
        inner_idx = probe(ngram, i)
        slot = inverted_index[outer_idx][inner_idx]
        if slot is None:
            return None
        if slot[0] == ngram:
            return slot[1]
        i += 1
    return None
