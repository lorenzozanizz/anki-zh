from .config import TTSConfig
from .model import CardModel
from .pinyin_utils import to_ruby_html

from pathlib import Path

from anki.notes import Note
from aqt import mw


class NoteFactory:
    def __init__(self, card_model: CardModel):
        self._model = card_model

    def build(self, hanzi: str, audio_path: Path, cfg: TTSConfig) -> Note:
        model = self._model.ensure(cfg)
        note = Note(mw.col, model)

        note["Hanzi"]              = hanzi
        note["Ruby"]               = to_ruby_html(hanzi)
        note["Audio"]              = f"[sound:{audio_path.name}]"
        note["Meaning"]            = ""
        note["text_front_prompt"]  = cfg.card_prompts.get("text_front",  "How is this pronounced?")
        note["audio_front_prompt"] = cfg.card_prompts.get("audio_front", "What phrase do you hear?")

        return note
