from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""
    lines_a = set(a.split(sep="\n"))
    lines_b = set(b.split(sep="\n"))

    return lines_a & lines_b


def sentences(a, b):
    """Return sentences in both a and b"""
    sentences_a = set(sent_tokenize(a))
    sentences_b = set(sent_tokenize(b))

    return sentences_a & sentences_b

def extract_substring(str, n):
    substrings = [str[i:i+n] for i in range(0, len(str), n)]

def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    substrings_a = set(extract_substring(a, n))
    substrings_b = set(extract_substring(b, n))

    return substrings_a & substrings_b
