"""Turkish text cleaner — removes HTML, URLs, emojis, mentions, hashtags."""
import re

_HTML = re.compile(r"<[^>]+>")
_URL  = re.compile(r"https?://\S+|www\.\S+")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[a-z]{2,}")
_MENTION = re.compile(r"@\w+")
_HASHTAG = re.compile(r"#\w+")
_NUMBER  = re.compile(r"\b\d[\d.,]*\b")
_PUNCT   = re.compile(r"[^\w\s]", re.UNICODE)
_SPACE   = re.compile(r"\s+")
_EMOJI   = re.compile(
    "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0\U000024C2-\U0001F251]+",
    flags=re.UNICODE
)

def clean(text, html=True, urls=True, emails=True, mentions=True,
          hashtags=True, emojis=True, numbers=False, punctuation=False, min_length=None):
    """
    Configurable cleaning pipeline.
    Example:
        clean("<b>Hi</b> @user https://x.com") -> "Hi"
    """
    if html: text = _HTML.sub(" ", text)
    if urls: text = _URL.sub(" ", text)
    if emails: text = _EMAIL.sub(" ", text)
    if mentions: text = _MENTION.sub(" ", text)
    if hashtags: text = _HASHTAG.sub(" ", text)
    if emojis: text = _EMOJI.sub(" ", text)
    if numbers: text = _NUMBER.sub(" ", text)
    if punctuation: text = _PUNCT.sub(" ", text)
    text = _SPACE.sub(" ", text).strip()
    if min_length and len(text) < min_length:
        return ""
    return text
