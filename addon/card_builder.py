
from .pinyin_utils import to_ruby_html
from .model import ensure_model

from aqt import mw
from aqt.qt import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from aqt.utils import showInfo
from anki.notes import Note

def open_dialog():
    dlg = _AddCardDialog(mw)
    dlg.exec()


class _AddCardDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Add Chinese Card")

        layout = QVBoxLayout()
        self.hanzi_input = QLineEdit(placeholderText="Hanzi  e.g. 你好")
        self.pinyin_input = QLineEdit(placeholderText="Pinyin e.g. nǐ hǎo")
        self.meaning_input = QLineEdit(placeholderText="Meaning e.g. Hello")
        self.btn = QPushButton("Create Card")
        self.btn.clicked.connect(self._create_card)

        for w in [QLabel("Hanzi"), self.hanzi_input,
                  QLabel("Pinyin (space-separated per character)"), self.pinyin_input,
                  QLabel("Meaning"), self.meaning_input, self.btn]:
            layout.addWidget(w)
        self.setLayout(layout)

    def _create_card(self):
        hanzi   = self.hanzi_input.text().strip()
        pinyin  = self.pinyin_input.text().strip()
        meaning = self.meaning_input.text().strip()

        if not hanzi or not meaning:
            showInfo("Hanzi and Meaning are required.")
            return

        model = ensure_model()  # get-or-create our Note Type
        note  = Note(mw.col, model)

        # Fields must be set by name; order matches the model definition.
        note["Hanzi"]   = hanzi
        note["Ruby"]    = to_ruby_html(hanzi, pinyin)   # <ruby> HTML
        note["Meaning"] = meaning

        # add_note(note, deck_id) - 0 uses the default deck.
        mw.col.add_note(note, mw.col.decks.get_current_id())
        mw.reset()  # refresh the main window card count

        showInfo(f"Card added for: {hanzi}")
        self.accept()
