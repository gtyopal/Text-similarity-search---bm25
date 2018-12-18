from BM25 import BM25

inverted_filepath = "data/inverted_index.txt"
text_filepath = "data/article_parsed.txt"
model = BM25(inverted_filepath, text_filepath)

queryStr = "safari 5 1 7 safari 5 1 7"
result = model.query(queryStr, 5)
for r in result:
	print(r)