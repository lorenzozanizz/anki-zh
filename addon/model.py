from aqt import mw
from .config import TTSConfig
from .constants import MODEL_NAME


class CardModel:

    _CSS = """
    .card       { font-family: sans-serif; text-align: center; font-size: 1.2em; }
    .hanzi      { font-size: 3em; margin-bottom: 0.2em; }
    ruby rt     { font-size: 0.4em; color: #888; }
    .prompt     { color: #888; font-size: 0.9em; margin-bottom: 1em; }
    .meaning    { font-size: 1.4em; margin-top: 0.5em; }
    """

    _FRONT_TEXT = """
    <div class="prompt">{{text_front_prompt}}</div>
    <div class="hanzi">{{Ruby}}</div>
    """

    _BACK_TEXT = """
    {{FrontSide}}
    <hr>
    {{Audio}}
    <div class="meaning">{{Meaning}}</div>
    """

    _FRONT_AUDIO = """
    <div class="prompt">{{audio_front_prompt}}</div>
    {{Audio}}
    """

    _BACK_AUDIO = """
    {{FrontSide}}
    <hr>
    <div class="hanzi">{{Ruby}}</div>
    <div class="meaning">{{Meaning}}</div>
    """

    def ensure(self, cfg: TTSConfig):
        mm = mw.col.models
        m = mm.by_name(MODEL_NAME)
        return m if m else self._create(mm, cfg)

    def _create(self, mm, cfg: TTSConfig):
        m = mm.new(MODEL_NAME)
        m["css"] = CardModel._CSS

        for name in ["Hanzi", "Ruby", "Audio", "Meaning",
                     "text_front_prompt", "audio_front_prompt"]:
            mm.add_field(m, mm.new_field(name))

        self._add_template(mm, m, "Text to Pronunciation", CardModel._FRONT_TEXT, CardModel._BACK_TEXT)
        if cfg.inverse_card:
            self._add_template(mm, m, "Audio to Meaning", CardModel._FRONT_AUDIO, CardModel._BACK_AUDIO)

        mm.add(m)
        return m

    def _add_template(self, mm, model, name: str, front: str, back: str):
        t = mm.new_template(name)
        t["qfmt"] = front
        t["afmt"] = back
        mm.add_template(model, t)
