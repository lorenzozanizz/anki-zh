from dataclasses import dataclass, field, asdict
from aqt import mw


@dataclass
class TTSConfig:
    api_key: str = ""
    region: str = "eastus"
    voice: str = "zh-CN-XiaoxiaoNeural"
    inverse_card: bool = True
    card_prompts: dict = field(default_factory=lambda: {
        "audio_front": "What phrase do you hear?",
        "text_front":  "How is this pronounced?",
    })


def load_config() -> TTSConfig:
    raw = mw.addonManager.getConfig(__name__) or {}
    cfg = TTSConfig()
    for k, v in raw.items():
        if hasattr(cfg, k):
            setattr(cfg, k, v)
    return cfg


def save_config(cfg: TTSConfig) -> None:
    mw.addonManager.writeConfig(__name__, asdict(cfg))
