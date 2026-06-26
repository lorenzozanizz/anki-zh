
from ..constants import VOICES
from ..config import load_config, save_config

from aqt.qt import (
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QCheckBox, QPushButton, QDialogButtonBox, QGroupBox, QVBoxLayout
)
from aqt.utils import showInfo

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chinese TTS Settings")
        self.setMinimumWidth(400)
        self._cfg = load_config()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        tts_box = QGroupBox("Azure / Edge TTS")
        tts_form = QFormLayout(tts_box)

        self._voice = QComboBox()
        self._voice.addItems(VOICES)
        idx = self._voice.findText(self._cfg.voice)
        self._voice.setCurrentIndex(max(0, idx))
        tts_form.addRow("Voice:", self._voice)

        self._inverse = QCheckBox("Generate reverse card (audio to meaning)")
        self._inverse.setChecked(self._cfg.inverse_card)
        tts_form.addRow(self._inverse)

        layout.addWidget(tts_box)

        prompt_box = QGroupBox("Card prompt text")
        prompt_form = QFormLayout(prompt_box)

        self._prompt_text = QLineEdit(self._cfg.card_prompts.get("text_front", ""))
        prompt_form.addRow("Text card front:", self._prompt_text)

        self._prompt_audio = QLineEdit(self._cfg.card_prompts.get("audio_front", ""))
        prompt_form.addRow("Audio card front:", self._prompt_audio)

        layout.addWidget(prompt_box)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._save)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _save(self):
        self._cfg.voice        = self._voice.currentText()
        self._cfg.inverse_card = self._inverse.isChecked()
        self._cfg.card_prompts = {
            "text_front":  self._prompt_text.text(),
            "audio_front": self._prompt_audio.text(),
        }
        save_config(self._cfg)
        showInfo("Settings saved. Restart Anki to apply voice changes.")
        self.accept()
