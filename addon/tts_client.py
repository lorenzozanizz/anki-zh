from .config import TTSConfig

import asyncio
from pathlib import Path
from uuid import uuid4

from aqt import mw
import edge_tts
# + vendored or installed at runtime by the import script


class AzureTTSClient:

    def __init__(self, config: TTSConfig):
        self._config = config

    def generate(self, text: str, velocity: str) -> Path:
        """ Blocking. Call from a worker thread, not the Qt main thread. """
        return asyncio.run(self._fetch(text, velocity))

    async def _fetch(self, text: str, velocity: str) -> Path:

        dest = Path(mw.col.media.dir()) / f"zh_{uuid4().hex[:10]}.mp3"

        kwargs = {"text": text, "voice": self._config.voice}
        if velocity != "0%":
            kwargs["rate"] = velocity

        comm = edge_tts.Communicate(**kwargs)
        await comm.save(str(dest))
        return dest
