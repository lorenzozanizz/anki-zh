import os
import sys
import subprocess

from aqt import mw

_LIBS = os.path.join(os.path.dirname(__file__), "libs")

_DEPS = [
    ("edge-tts", "edge_tts"),
    ("pypinyin",  "pypinyin"),
]


def ensure_deps() -> None:
    os.makedirs(_LIBS, exist_ok=True)

    missing = [pip for pip, imp in _DEPS if not _importable(imp)]

    if missing:
        _install(missing)

    if _LIBS not in sys.path:
        sys.path.insert(0, _LIBS)


def _importable(name: str) -> bool:
    """

    :param name:
    :return:
    """
    try:
        __import__(name)
        return True
    except ImportError:
        return False


def _install(packages: list) -> None:
    mw.progress.start(label="Chinese TTS: installing dependencies…", immediate=True)
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--target", _LIBS, *packages],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    finally:
        mw.progress.finish()
