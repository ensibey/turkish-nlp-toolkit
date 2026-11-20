"""
Lightweight lexicon-assisted Turkish diacritic restorer (deasciifier).

Restores Turkish diacritics (ç, ğ, ı, ö, ş, ü, İ) on common ASCII-typed
e-commerce, logistics, and conversational words while preserving original casing.
"""

from __future__ import annotations

import re
from typing import Dict

ASCII_LEXICON: Dict[str, str] = {
    # Common high-frequency Turkish words
    "cok": "çok", "guzel": "güzel", "tesekkur": "teşekkür", "tesekkurler": "teşekkürler",
    "urun": "ürün", "urunu": "ürünü", "urunler": "ürünler", "musteri": "müşteri",
    "sirket": "şirket", "ogrenci": "öğrenci", "universite": "üniversite", "egitim": "eğitim",
    "turkiye": "türkiye", "turkce": "türkçe", "sehir": "şehir", "ilce": "ilçe",
    "mahalle": "mahalle", "sokak": "sokak", "kapi": "kapı", "kat": "kat",
    "siparis": "sipariş", "siparisim": "siparişim", "hizli": "hızlı", "kaliteli": "kaliteli",
    "saglam": "sağlam", "begendim": "beğendim", "guvenli": "güvenli", "odeme": "ödeme",
    "iade": "iade", "degisim": "değişim", "ulasim": "ulaşım", "teslimat": "teslimat",
    "kargo": "kargo", "gonderi": "gönderi", "gonderildi": "gönderildi", "cozum": "çözüm",
    "calisiyor": "çalışıyor", "calismiyor": "çalışmıyor", "yardim": "yardım", "lutfen": "lütfen",
    "simdi": "şimdi", "bugun": "bugün", "yarin": "yarın", "ozel": "özel",
    "acik": "açık", "kapali": "kapalı", "buyuk": "büyük", "kucuk": "küçük",
    "yeni": "yeni", "eski": "eski", "iyi": "iyi", "kotu": "kötü",
    "dogru": "doğru", "yanlis": "yanlış", "basarili": "başarılı", "hatali": "hatalı",
    # Major Turkish cities & districts (logistics / address NLP)
    "istanbul": "istanbul", "izmir": "izmir", "ankara": "ankara", "kadikoy": "kadıköy",
    "besiktas": "beşiktaş", "sisli": "şişli", "uskudar": "üsküdar", "bakirkoy": "bakırköy",
    "cankaya": "çankaya", "kecioren": "keçiören", "yenimahalle": "yenimahalle",
    "karsiyaka": "karşıyaka", "bornova": "bornova", "konak": "konak", "buca": "buca",
    "nilufer": "nilüfer", "osmangazi": "osmangazi", "yildirim": "yıldırım",
    "eskisehir": "eskişehir", "diyarbakir": "diyarbakır", "sanliurfa": "şanlıurfa",
    "kahramanmaras": "kahramanmaraş", "mugla": "muğla", "tekirdag": "tekirdağ",
    "balikesir": "balıkesir", "canakkale": "çanakkale", "aydin": "aydın",
    "elazig": "elazığ", "isparta": "ısparta", "igdir": "ığdır", "kirikkale": "kırıkkale",
    "kirklareli": "kırklareli", "kirsehir": "kırşehir", "kutahya": "kütahya",
    "nevsehir": "nevşehir", "nigde": "niğde", "sirnak": "şırnak", "usak": "uşak",
    "bartin": "bartın", "bingol": "bingöl", "corum": "çorum", "duzce": "düzce",
    "gumushane": "gümüşhane", "karabuk": "karabük", "agri": "ağrı",
}

WORD_RE = re.compile(r"[A-Za-zçğıöşüÇĞİÖŞÜ]+")

_TR_UPPER = str.maketrans("iıçğöşü", "İIÇĞÖŞÜ")


def _apply_casing(original: str, restored_lower: str) -> str:
    if original.isupper():
        return restored_lower.translate(_TR_UPPER).upper()
    if original[0].isupper():
        first = restored_lower[0].translate(_TR_UPPER).upper()
        return first + restored_lower[1:]
    return restored_lower


def restore_diacritics(text: str) -> str:
    """Restore Turkish diacritics on ASCII-typed tokens while preserving case."""
    if not text:
        return ""

    def _sub(match: re.Match) -> str:
        tok = match.group(0)
        key = tok.lower()
        restored = ASCII_LEXICON.get(key)
        if not restored:
            return tok
        return _apply_casing(tok, restored)

    return WORD_RE.sub(_sub, text)
