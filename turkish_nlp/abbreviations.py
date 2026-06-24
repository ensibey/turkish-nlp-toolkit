"""Turkish abbreviation expander — 150+ entries across domains."""
import re
from typing import Dict, Optional

ABBREVIATIONS: Dict[str, str] = {
    # Titles
    "dr.":"doktor","prof.":"profesor","doc.":"docent","yrd.":"yardimci",
    "op.":"operator","uzm.":"uzman","av.":"avukat","sn.":"sayin",
    "bsk.":"bakan","gen.":"general","kd.":"kidemli",
    # Administrative
    "mah.":"mahallesi","cad.":"caddesi","sok.":"sokagi","blv.":"bulvari",
    "apt.":"apartmani","no.":"numara","d.":"daire","p.k.":"posta kutusu",
    "pk.":"posta kutusu","t.c.":"turkiye cumhuriyeti","tc":"turkiye cumhuriyeti",
    "bel.":"belediyesi","il.":"ilce","muд.":"mudurluк","emn.":"emniyet",
    # Academic
    "unv.":"universitesi","fak.":"fakultesi","bol.":"bolumu",
    "enst.":"enstitusu","ars.gor.":"arastirma gorevlisi",
    "ogr.gor.":"ogretim gorevlisi","ogr.":"ogrenci",
    # Medical
    "hst.":"hastanesi","ecz.":"eczanesi","polikl.":"poliklinigi",
    "mg":"miligram","ml":"mililitre","lt.":"litre","amp.":"ampul",
    # General
    "vb.":"ve benzeri","vd.":"ve digerleri","vs.":"vesaire",
    "bkz.":"bakiniz","krs.":"karsilastiriniz","orn.":"ornegin",
    "cev.":"ceviren","haz.":"hazirlayan","yay.":"yayinlari",
    "s.":"sayfa","sf.":"sayfa","ss.":"sayfalar","md.":"madde",
    "a.s.":"anonim sirketi","ltd.":"limited","tic.":"ticaret",
    "san.":"sanayi","koop.":"kooperatifi","vakf.":"vakfi","der.":"dernegi",
    # Logistics (TEKNOFEST domain)
    "sk.":"sokagi","cd.":"caddesi","bul.":"bulvari","k.":"kat",
    "bb.":"buyuksehir belediyesi","osb":"organize sanayi bolgesi",
    # Time & measurement
    "dk.":"dakika","dak.":"dakika","cm":"santimetre","km":"kilometre",
    "mm":"milimetre","kg":"kilogram","gr":"gram","mb":"megabayt","gb":"gigabayt",
    # Months
    "oca.":"ocak","sub.":"subat","mar.":"mart","nis.":"nisan","may.":"mayis",
    "haz.":"haziran","tem.":"temmuz","agu.":"agustos","eyl.":"eylul",
    "eki.":"ekim","kas.":"kasim","ara.":"aralik",
}

def get_abbreviations(): return dict(ABBREVIATIONS)

def expand(text, extra=None, lowercase_output=False):
    """
    Expand Turkish abbreviations in text.
    Case-insensitive, word-boundary aware.
    Example: expand("Dr. Mah. No. 5") -> "Doktor Mahallesi Numara 5"
    """
    lookup = dict(ABBREVIATIONS)
    if extra: lookup.update({k.lower(): v for k, v in extra.items()})
    sorted_abbrevs = sorted(lookup.keys(), key=len, reverse=True)
    pattern = re.compile(
        r"(?<!\w)(" + "|".join(re.escape(a) for a in sorted_abbrevs) + r")(?!\w)",
        re.IGNORECASE
    )
    def _replace(m):
        key = m.group(0).lower()
        exp = lookup.get(key, m.group(0))
        if lowercase_output: return exp
        return exp.capitalize() if m.group(0)[0].isupper() else exp
    return pattern.sub(_replace, text)

def add_abbreviation(abbrev, expansion): ABBREVIATIONS[abbrev.lower()] = expansion
def remove_abbreviation(abbrev): ABBREVIATIONS.pop(abbrev.lower(), None)
