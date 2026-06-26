from pypinyin import lazy_pinyin, Style


def to_ruby_html(hanzi: str) -> str:
    """ Returns <ruby> HTML with pinyin above each character. """
    readings = lazy_pinyin(hanzi, style=Style.TONE)
    parts = []
    for char, tone in zip(hanzi, readings):
        # Chinese character ranges from unicode (this is a bit brittle admittedly)
        if "\u4e00" <= char <= "\u9fff":
            parts.append(f"<ruby>{char}<rt>{tone}</rt></ruby>")
        else:
            parts.append(char)
    return "".join(parts)
