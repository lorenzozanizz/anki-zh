
from anki.cards import Card
from aqt.reviewer import Reviewer


def on_card_answered(reviewer: Reviewer, card: Card, ease: int) -> None:
    """
    Fires after the user rates a card.
    ease: 1=Again  2=Hard  3=Good  4=Easy

    'card' gives access to card.note() for field data, card.ivl (interval), etc.
    This demo just prints; a real add-on might log to a file or call an API.
    """
    note   = card.note()
    hanzi  = note.fields[0]  # first field = Hanzi
    labels = {1: "Again", 2: "Hard", 3: "Good", 4: "Easy"}
    print(f"[zh-addon] {hanzi!r:>10}  →  {labels.get(ease, ease)}")
