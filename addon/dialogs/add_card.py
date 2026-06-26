
from ..config import TTSConfig
from ..tts_client import AzureTTSClient
from ..note_factory import NoteFactory

import threading
from pathlib import Path

from aqt import mw
from aqt.qt import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QSlider,
    QPushButton, QProgressBar, pyqtSignal, Qt, QWidget
)

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl

from aqt.utils import showWarning



class AddCardDialog(QDialog):

    READY_MSG = """
    """


    _audio_ready = pyqtSignal(str)   # emits str(Path)
    _tts_error   = pyqtSignal(str)

    def __init__(self, tts: AzureTTSClient, factory: NoteFactory,
                 cfg: TTSConfig, parent=None):
        super().__init__(parent)
        self._tts     = tts
        self._factory = factory
        self._cfg     = cfg
        self._audio_path: Path | None = None

        self.setWindowTitle("Add Chinese Card")
        self.setMinimumWidth(420)
        self._build_ui()

        self._audio_ready.connect(self._on_audio_ready)
        self._tts_error.connect(self._on_tts_error)

    def _build_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Chinese text:"))
        self._text_input = QTextEdit()
        self._text_input.setFixedHeight(80)
        self._text_input.setPlaceholderText("e.g. 你好，世界")
        layout.addWidget(self._text_input)

        self._progress = QProgressBar()
        self._progress.setRange(0, 0)
        self._progress.setVisible(False)
        layout.addWidget(self._progress)

        self._status = QLabel("")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._status)

        layout.addLayout(self._build_velocity_row())

        buttons = QHBoxLayout()
        self._btn_generate = QPushButton("Generate audio")
        self._btn_add = QPushButton("Add card")
        self._btn_add.setEnabled(False)

        self._playback_bnt = QPushButton("Playback")
        self._playback_bnt.setEnabled(False)
        self._btn_generate.clicked.connect(self._on_generate)
        self._btn_add.clicked.connect(self._on_add_card)
        self._playback_bnt.clicked.connect(self._on_play_sound)


        buttons.addWidget(self._btn_generate)
        buttons.addWidget(self._playback_bnt)
        buttons.addWidget(self._btn_add)

        layout.addLayout(buttons)

    def _build_velocity_row(self) -> QHBoxLayout:
        row = QHBoxLayout()

        self._speed_slider = QSlider(Qt.Orientation.Horizontal)
        self._speed_slider.setMinimum(-40)
        self._speed_slider.setMaximum(40)
        self._speed_slider.setValue(0)
        self._speed_slider.setSingleStep(10)
        self._speed_slider.setPageStep(10)
        self._speed_slider.setTickInterval(10)
        self._speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._speed_slider.valueChanged.connect(self._snap_velocity)

        self._speed_label = QLabel("+0%")
        row.addWidget(QLabel("Velocity:"))
        row.addWidget(self._speed_slider)
        row.addWidget(self._speed_label)
        return row

    def _snap_velocity(self, value: int) -> None:
        snapped = round(value / 10) * 10
        if snapped != value:
            self._speed_slider.blockSignals(True)
            self._speed_slider.setValue(snapped)
            self._speed_slider.blockSignals(False)
        self._speed_label.setText(f"{snapped:+d}%")  # always use snapped value


    def _on_generate(self):
        text = self._text_input.toPlainText().strip()
        if not text:
            showWarning("Please enter some Chinese text.")
            return

        self._set_generating(True)
        threading.Thread(target=self._worker, args=(text,), daemon=True).start()

    def _worker(self, text: str):
        velocity = f"{self._speed_slider.value()}%"
        try:
            path = self._tts.generate(text, velocity)
            self._audio_ready.emit(str(path))
        except Exception as e:
            self._tts_error.emit(str(e))

    def _on_audio_ready(self, path_str: str):
        self._audio_path = Path(path_str)
        self._set_generating(False)
        self._status.setText("Audio ready.")
        self._btn_add.setEnabled(True)
        self._playback_bnt.setEnabled(True)

    def _on_play_sound(self):
        if not self._audio_path:
            return

        # Store as instance vars to prevent garbage collection
        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._player.setAudioOutput(self._audio_output)

        self._player.setSource(QUrl.fromLocalFile(str(self._audio_path)))
        self._player.play()

    def _on_tts_error(self, msg: str):
        self._set_generating(False)
        self._status.setText(f"Error: {msg}")

    def _on_add_card(self):
        if not self._audio_path:
            return
        hanzi = self._text_input.toPlainText().strip()
        note  = self._factory.build(hanzi, self._audio_path, self._cfg)
        mw.col.add_note(note, mw.col.decks.get_current_id())
        mw.reset()
        self._status.setText("Card added!")
        self._btn_add.setEnabled(False)
        self._audio_path = None
        self._text_input.clear()

    def _set_generating(self, active: bool):
        self._progress.setVisible(active)
        self._btn_generate.setEnabled(not active)
        if active:
            self._status.setText("Generating audio…")
            self._btn_add.setEnabled(False)
