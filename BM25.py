"""Model class for BM25 model."""
from utils import denoise_text

from collections import Counter
from collections import namedtuple
import math


class BM25:
    def __init__(self, inverted_filepath, text_filepath):
        self.alltext_indexItems = self.load_invertedIndex(inverted_filepath)  # get inversed index
        self.k1 = 1.2  # regulatory factor in BM25 formular
        self.k2 = 200  # regulatory factor in BM25 formular
        self.b = 0.75  # regulatory factor in BM25 formular
        s = self.load_allTexts(text_filepath)  # get all texts and related statistics
        self.ave_len = s[0]  # int, the average length of all texts
        self.text_lens = s[1]  # list, the length of all texts
        self.N = s[2]  # int, the number of all texts
        self.all_texts = s[3]  # list, all texts

    def load_invertedIndex(self, file_path):
        '''read inverted index file
        file_path: str, the file path of inverted index file.
        '''
        alltext_indexItems = {}
        with open(file_path, "r") as fr:
            for line in fr:
                temp = line.strip().split()
                word = temp[0]
                temp = temp[1:]
                if len(temp) <= 1:
                    t = temp[0].split(":")
                    index_items = [[t[0], int(t[1])]]
                else:
                    t = [item.split(':') for item in temp]
                    index_items = [[item[0], int(item[1])] for item in t]
                alltext_indexItems[word] = index_items
        return alltext_indexItems

    def load_allTexts(self, file_path):
        '''read all texts, and do some statistics
        file_path: str, the file path of texts.
        '''
        text_lens, all_texts = {}, {}
        with open(file_path, "r") as fr:
            for line in fr:
                oid, text = line.split('\t')
                all_texts[oid] = text.strip()
                text_lens[oid] = len(text.split())
        ave_len = sum(text_lens.values()) / len(text_lens)
        return ave_len, text_lens, len(text_lens), all_texts

    def get_similarity(self, query):
        '''calculate the similarities between query and all candidate texts in related inverted index
        query: list, the query words after preprocessing.
        '''
        similarities = {}
        # k: query word, v: word times in query
        for k, v in query.items():
            if k in self.alltext_indexItems.keys():
                index_items = self.alltext_indexItems[k]
                # related text, namely the number of texts that included the word (k).
                related_text_num = len(index_items)

                for oid, word_times in index_items:
                    if oid not in similarities.keys():
                        similarities[oid] = 0.0
                    # the first factor in BM25 formular
                    factor1 = math.log((self.N - related_text_num + 0.5) / (related_text_num + 0.5))
                    # the second factor in BM25 formular
                    K = self.k1 * (1 - self.b + self.b * self.text_lens[oid] / self.ave_len)
                    factor2 = (self.k1 + 1) * word_times / (K + word_times)
                    # the third factor in BM25 formular
                    factor3 = (self.k2 + 1) * v / (self.k2 + v)
                    similarities[oid] += factor1 * factor2 * factor3
        return similarities

    def query_preprocessing(self, query):
        '''do query preprocessing
        query: str, the text that needed to calculated the top N similar texts in candidate.
        '''
        query = denoise_text(query)
        query = Counter(query.split())
        return query

    def get_result(self, similarities, topN):
        '''get most similar N texts
        similarities: dict, {$oid: similar score}.
        topN: int, how many most similar texts are needed to return.
        '''
        similarities = list(similarities.items())
        temp = [t[1] for t in similarities]
        sim_max, sim_min = max(temp), min(temp)
        similarities = [[t[0], (t[1] - sim_min) / (sim_max - sim_min)] for t in similarities]
        similarities.sort(key=lambda x: x[1], reverse=True)
        result = similarities[:topN]
        result = ["[%.3f]\t%s\t%s" % (r[1], r[0], self.all_texts[r[0]]) for r in result]
        return result

    def query(self, queryStr, topN):
        '''for a given query text, return most similar topN texts
        queryStr: str, the text that needed to calculated the top N similar texts in candidate,
        topN: int, how many most similar texts are needed to return.
        '''
        queryStr = self.query_preprocessing(queryStr)
        similarities = self.get_similarity(queryStr)
        query_result = self.get_result(similarities, topN)
        return query_result


if __name__ == '__main__':
    inverted_filepath = "data/inverted_index.txt"
    text_filepath = "data/article_parsed.txt"
    model = BM25(inverted_filepath, text_filepath)

    queryStr = "display panel removed power supply contains high voltage capacitor may remain charged hour unplugging computer wait one 1 hour unplugging computer electrical outlet removing power supply working near power supply leads never remove install physical components computer plugged electrical outlet plugged power supply logic board energized even computer powered unplug computer possible allow sufficient time power supply logic board self discharge removing display panel touch logic board power supply computer plugged sufficient time passed discharge stored voltage safe level unplugged refer apple support article tp833 imac displays power supply cover instructions information installing protective cover power supply power supply cover provides protection unintended contact energized power supply may result injury electric shock always use power supply cover service glass panel lcd removed imac led cinema display thunderbolt display electrical safety precautions working computer exposed potentially energized parts remove rings watches necklaces metal rimmed eyewear metallic articles increase risk electric shock wear cell phone signaling device may cause dangerous startle reflex energized work imac needs plugged led checks similar troubleshooting wear esd wrist strap wearing esd grounding systems increases risk electric shock remain alert focused work performed aware proximity grounded objects body use plastic black stick non metal extension tool needed connect disconnect cables keep fingers away potentially energized parts broken glass cleaning handling glass panel follow cleaning procedures manual ensure glass panel free dust particles returning computer user glass panel tempered break sharp pieces mishandled scratched broken glass panel covered warranty removing glass panel requires special tools lint free gloves rubber suction cups microfoam storage bags prevent contamination wear lint free gloves handle glass edges dont handle glass panel using lint free gloves use sticky silicone roller clean inside surface glass lcd panel place glass panel clean protective microfoam bag removed computer store glass panel safe area broken damaged store lcd panel anti static bag prevent buildup static charges may attract dust particles display surface store silicone roller sticky paper within temperature range 39 104 f 5 40 c silicone roller longer tacky wash warm soapy water wipe isopropyl alcohol tackiness return replace silicone roller touch inside glass bare hands dirty gloves fingerprints difficult remove place glass panel onto work surface may collect dust contaminants unless first placed protective microfoam bag handling broken glass panel glass panel tempered break sharp pieces mishandled glass broken must carefully removed computer prevent irreparable damage front surface lcd front surface lcd scratched broken glass lcd panel may need replaced remove broken glass panel shattered glass panel removed using safety glasses packing tape leather gloves 1 put safety glasses leather gloves 2 lay computer smooth clean work surface 3 peel protective covering front glass remove discard large pieces broken glass 4 apply strip packing tape horizontally across top bottom glass panel next apply tape diagonally across broken glass panel forming x 5 continue applying tape horizontally thoroughly covering broken glass glass still attached steel ring runs around perimeter glass panel 6 use black stick pry glass panel magnets rear housing 7 lift entire glass panel rear housing 8 place broken glass inside large box label box dispose properly 9 using whisk broom clean work surface tiny glass particles 10 stand imac use lint free cloth carefully brush particles imac onto table clean work surface 11 repair finished cloth disposed immediately 12 use broom dustpan sweep much broken glass possible glass fragments may traveled several feet location glass panel sure thoroughly clean entire area use vacuum remove smaller fragments picked broom note broken glass panel may leave one scratches lcd panel depending severity glass breakage long lcd fractured lcd panel require replacement sure let user know scratches caused broken glass panel imac 27 inch mid 2011 safety warning high voltage power supply remains powered whenever computer plugged whether computer turned use extreme caution troubleshooting "
    result = model.query(queryStr, 5)
    for r in result:
        print(r)
