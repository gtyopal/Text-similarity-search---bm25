# coding: utf-8
import numpy as np
import json

import multiprocessing
from multiprocessing import Pool

from utils import denoise_text

with open("data/article.txt", "r") as fr:
    data = fr.readlines()

# extract '$oid', 'articleId' and 'content'
oid_contents = []
for line in data:
    try:
        temp = json.loads(line)
        oid = temp["_id"]["$oid"]
        articleId = temp["articleId"]
        main = temp["content"]["main"]
        sections = temp["content"]["sections"]
        oid_contents.append(["%s-%s" % (oid, articleId), main, sections])
    except Exception:
        pass

# extract 'summary', 'text' and 'title'
all_texts = []
for i in range(len(oid_contents)):
    oid = oid_contents[i][0]
    main = oid_contents[i][1]
    sections = oid_contents[i][2]
    summary, text, title = '', '', ''
    if "summary" in main.keys():
        summary = main["summary"]
        if not isinstance(summary, str):
            summary = summary["summaryText"]
    if "title" in main.keys():
        title = main["title"]
    for s in sections:
        if "text" in s.keys():
            text = ' '.join([text, s["text"]])
    all_texts.append([oid, ' '.join([summary, text, title])])

# filter non-English texts 
def is_english(x):
    return all(ord(c) < 128 for c in x[1])
all_texts = list(filter(lambda x: is_english(x), all_texts))

print("english texts number: ", len(all_texts))

# multiprocess for data preprocessing
def task(texts):
    res = []
    for line in texts:
        t = denoise_text(line[1])
        if len(t.split()) > 0:
            res.append([line[0], t])
    return res
core_num = multiprocessing.cpu_count()
slices = np.linspace(0, len(all_texts), core_num+1).astype(int)

pool = Pool(core_num)
temp = []
for i in range(core_num):
    slice_texts = all_texts[slices[i]:slices[i+1]]
    temp.append(pool.apply_async(task, args=(slice_texts,)))
pool.close()
pool.join()

result = []
for t in temp:
    result.extend(t.get())

# write to disk
all_texts = ["%s\t%s\n" % (t[0], t[1]) for t in result]
with open("data/article_parsed.txt", "w") as fr:
    fr.writelines(all_texts)
