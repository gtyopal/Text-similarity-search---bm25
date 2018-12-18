"""build inverted index file"""
from collections import Counter


def build_invertedIndex(file_path):
    '''build inverted index file
    file_path: str, the file path of texts.
    '''
    inverted_index = {}
    with open(file_path, "r") as fr:
        for line in fr:
            oid, text = line.strip().split('\t')
            words = text.split()
            words_times = Counter(words)
            # save in inverted_index
            for k, v in words_times.items():
                if k not in inverted_index.keys():
                    inverted_index[k] = []
                inverted_index[k].append("%s:%d" % (oid, v))

    return inverted_index


if __name__ == '__main__':
    inverted_index = build_invertedIndex("data/article_parsed.txt")
    with open("data/inverted_index.txt", "w") as fw:
        for k, v in inverted_index.items():
            fw.write(" ".join([k] + v) + '\n')

