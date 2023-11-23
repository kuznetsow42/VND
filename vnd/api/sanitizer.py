import nh3


ALLOWED_TAGS = {
    'p', 'a', 'em', 'strong', 'tbody', 'td', 'table', 'br', 'img', 'th', 'tr', 'span', 'blockquote', 'ul',
    'code', 'pre', "h6", "h5", "h4", 'h3', "h2", "h1", 'li', 'hr', "sup"
}

ALLOWED_ATTRIBUTES = {
    "a": {"href", "title", "target"},
    "abbr": {"title"},
    "acronym": {"title"},
    "img": {"src", "alt", "aspect-ratio"},
    "td": {"colspan", "rowspan", "colwidth"},
    "th": {"colspan", "rowspan", "colwidth"},
    "*": {"style", "height", "width", "text-align"}
}


def sanitize_text(text: str) -> str:
    clean_text = nh3.clean(html=text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    if clean_text != text:
        pass
    return clean_text
