"""Turkish stopword list (~350 high-frequency function words)."""

_STOPWORDS = {
    "ben","sen","o","biz","siz","onlar","beni","seni","onu","bizi","sizi","onlari",
    "bana","sana","ona","bize","size","onlara","bende","sende","onda","bizde","sizde",
    "bu","su","bunlar","sunlar","bunu","sunu","buna","suna","burada","surada","orada",
    "ne","neden","nicin","nasil","hangi","hangisi","kim","kimi","kime","kimde","kimden",
    "ve","ile","veya","ya","yahut","yoksa","ama","fakat","lakin","ancak","oysa","oysaki",
    "cunki","zira","nitekim","dolayisiyla","ki","dahi","bile","da","de","ta","te",
    "hem","eger","sayet","madem","mademki","halbuki","meger","megerki",
    "icin","gibi","kadar","gore","karsi","beri","once","sonra","uzerinde","altinda",
    "arasinda","tarafindan","hakkinda","konusunda","uzerne","yonelik","iliskin","dair",
    "ragmen","karsin","dogru","ol","olmak","oldu","olur","olmus","olacak",
    "et","etmek","etti","eder","etmis","edecek","var","yok","vardi","yoktu",
    "ise","imis","idi","idim","degil","degildi","degilmis",
    "cok","az","daha","en","epey","gayet","oldukca","hic","hicbir","hep",
    "her","herkes","hepsi","butun","tum","bazi","birkac","bircok",
    "artik","zaten","sadece","yalniz","yalnizca","iste","yani","sanki",
    "belki","muhtemelen","kesinlikle","tabii","elbette","aslinda","gercekten",
    "bir","iki","uc","dort","bes","alti","yedi","sekiz","dokuz","on",
    "yuz","bin","milyon","milyar","birinci","ikinci","ucuncu","ilk","son",
    "bu","su","o","bir","ve","de","da","ile","ki","da","mi","mu",
}

def get_stopwords(): return set(_STOPWORDS)

def remove_stopwords(tokens, extra=None, keep=None):
    """Filter stopwords from token list."""
    sw = set(_STOPWORDS)
    if extra: sw.update(extra)
    if keep: sw -= set(keep)
    return [t for t in tokens if t.lower() not in sw]

def is_stopword(word): return word.lower() in _STOPWORDS
def add_stopword(word): _STOPWORDS.add(word.lower())
def remove_from_stopwords(word): _STOPWORDS.discard(word.lower())
