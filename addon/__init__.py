from .bootstrap import ensure_deps
ensure_deps()  # must run before any dep imports

from aqt import mw, gui_hooks
from aqt.qt import QAction

from .config import load_config
from .model import CardModel
from .note_factory import NoteFactory
from .tts_client import AzureTTSClient
from .dialogs.add_card import AddCardDialog
from .dialogs.config_dialog import ConfigDialog


def _setup():
    cfg     = load_config()
    model   = CardModel()
    # Ensure the model is properly added to Anki's card editor
    # without needing to open the top tooltip
    model.ensure(cfg)

    factory = NoteFactory(model)
    client  = AzureTTSClient(cfg)

    add_action = QAction("Add Chinese Card", mw)
    add_action.triggered.connect(
        lambda: AddCardDialog(client, factory, cfg, mw).exec()
    )

    cfg_action = QAction("Chinese TTS Settings…", mw)
    cfg_action.triggered.connect(lambda: ConfigDialog(mw).exec())

    mw.form.menuTools.addSeparator()
    mw.form.menuTools.addAction(add_action)
    mw.form.menuTools.addAction(cfg_action)


gui_hooks.main_window_did_init.append(_setup)
