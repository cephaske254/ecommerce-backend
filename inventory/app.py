import re


def solution(S):
    sentences = re.split(r" *[\.\?!\.] *", S)

    # lengths = [(len(sentence.split(" "))) for sentence in sentences]
    lengths = []

    for sentence in sentences:
        lengths.append(len(sentence.split(" ")))

    return sorted(lengths)[-1]


solution("Forget CVs..Save time . x x")
