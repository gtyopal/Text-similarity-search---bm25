from BM25 import BM25
import numpy as np
import os
from collections import Counter

data = []
idx_list = []
with open("data/data.txt", "r") as fr:
    for line in fr:
        idx, text = line.strip().split('\t')
        idx_list.append(idx)
        data.append([idx, text])

inverted_filepath = "data/inverted_index.txt"
text_filepath = "data/data.txt"
model = BM25(inverted_filepath, text_filepath)

if os.path.exists("data/all_similarities.txt"):
    os.remove("data/all_similarities.txt")
with open("data/all_similarities.txt", "a") as fw:
    print ("Started outputing similarities matrix...")
    idx_str = "idx %s\n" % " ".join(idx_list)
    fw.write(idx_str)
    for idx1, text in data:
        query = Counter(text.split())
        similarities = model.get_similarity(query)
        result = []
        for idx2 in idx_list:
            if idx2 in similarities.keys():
                result.append(similarities[idx2])
            else:
                result.append(0.0)
        sim_max = max(result)
        sim_min = min(result)
        result = [str((x - sim_min) / (sim_max - sim_min)) for x in result]
        fw.write("%s %s\n" % (idx1, " ".join(result)))
    print ("Ended uutputing similarities matrix...")
