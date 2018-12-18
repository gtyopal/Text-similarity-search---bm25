import math
from utils import denoise_text


def load_data(fpath):
    data = []
    with open(fpath, "r") as fr:
        for line in fr:
            temp = line.strip().split('\t')
            data.append([temp[0], set(temp[1].split())])
    return data


def query_preprocessing(query):
    '''do query preprocessing
    query: str, the text that needed to calculated the top N similar texts in candidate.
    '''
    query = denoise_text(query)
    query = set(query.split())
    return query


def calculate_sim_score(query_set, candidate_set):
    sim_scores = []
    for idx, words in candidate_set:
        co_words = query_set & words
        if len(co_words) == 0:
            score = 0.0
        else:
            score = len(co_words) / (math.sqrt(len(query_set)) * math.sqrt(len(words)))
        sim_scores.append([idx, score])
    return sim_scores


def get_result(sim_scores, data, topN=3):
    sim_scores.sort(key=lambda x: x[1], reverse=True)
    for line in sim_scores[:topN]:
        print("%s\t%.4f\t%s" % (line[0], line[1], ' '.join(list(data[line[0]]))))


def main():
    data = load_data("data/article_parsed.txt")
    #query_str = "though paper usually ordered weight apple printer manuals often specify required type paper thickness following table help determine paper thickness proper weight paper order weight thickness thickness original original 3 copies pounds inches inches 12 0 0025 0 01 15 0 0029 0 0116 18 0 0036 0 0144 20 0 0040 0 016 note table lists thicknesses one typical sample tractor paper thicknesses types paper ncr paper may different printer paper correlating thickness weight"
    query_str = "warning high voltage power supply remains powered whenever computer plugged whether computer turned use extreme caution troubleshooting display panel removed power supply contains high voltage capacitor may remain charged hour unplugging computer wait one 1 hour unplugging computer electrical outlet removing power supply working near power supply leads never remove install physical components computer plugged electrical outlet plugged power supply logic board energized even computer powered unplug computer possible allow sufficient time power supply logic board self discharge removing display panel touch logic board power supply computer plugged sufficient time passed discharge stored voltage safe level unplugged refer apple support article tp833 imac displays power supply cover instructions information installing protective cover power supply power supply cover provides protection unintended contact energized power supply may result injury electric shock always use power supply cover service glass panel lcd removed imac led cinema display thunderbolt display electrical safety precautions working computer exposed potentially energized parts remove rings watches necklaces metal rimmed eyewear metallic articles increase risk electric shock wear cell phone signaling device may cause dangerous startle reflex energized work imac needs plugged led checks similar troubleshooting wear esd wrist strap wearing esd grounding systems increases risk electric shock remain alert focused work performed aware proximity grounded objects body use plastic black stick non metal extension tool needed connect disconnect cables keep fingers away potentially energized parts broken glass cleaning handling glass panel follow cleaning procedures manual ensure glass panel free dust particles returning computer user glass panel tempered break sharp pieces mishandled scratched broken glass panel covered warranty removing glass panel requires special tools lint free gloves rubber suction cups microfoam storage bags prevent contamination wear lint free gloves handle glass edges dont handle glass panel using lint free gloves use sticky silicone roller clean inside surface glass lcd panel place glass panel clean protective microfoam bag removed computer store glass panel safe area broken damaged store lcd panel anti static bag prevent buildup static charges may attract dust particles display surface store silicone roller sticky paper within temperature range 39 104 f 5 40 c silicone roller longer tacky wash warm soapy water wipe isopropyl alcohol tackiness return replace silicone roller touch inside glass bare hands dirty gloves fingerprints difficult remove place glass panel onto work surface may collect dust contaminants unless first placed protective microfoam bag handling broken glass panel glass panel tempered break sharp pieces mishandled glass broken must carefully removed computer prevent irreparable damage front surface lcd front surface lcd scratched broken glass lcd panel may need replaced remove broken glass panel shattered glass panel removed using safety glasses packing tape leather gloves 1 put safety glasses leather gloves 2 lay computer smooth clean work surface 3 peel protective covering front glass remove discard large pieces broken glass 4 apply strip packing tape horizontally across top bottom glass panel next apply tape diagonally across broken glass panel forming x 5 continue applying tape horizontally thoroughly covering broken glass glass still attached steel ring runs around perimeter glass panel 6 use black stick pry glass panel magnets rear housing 7 lift entire glass panel rear housing 8 place broken glass inside large box label box dispose properly 9 using whisk broom clean work surface tiny glass particles 10 stand imac use lint free cloth carefully brush particles imac onto table clean work surface 11 repair finished cloth disposed immediately 12 use broom dustpan sweep much broken glass possible glass fragments may traveled several feet location glass panel sure thoroughly clean entire area use vacuum remove smaller fragments picked broom note broken glass panel may leave one scratches lcd panel depending severity glass breakage long lcd fractured lcd panel require replacement sure let user know scratches caused broken glass panel imac 27 inch mid 2011 safety"
    query_set = query_preprocessing(query_str)
    sim_scores = calculate_sim_score(query_set, data)
    get_result(sim_scores, dict(data), 5)


if __name__ == '__main__':
    main()
