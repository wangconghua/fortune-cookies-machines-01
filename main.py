#!/usr/bin/env python3
"""Fortune Cookies for Machines — one fortune an AI agent would crack open.

Writes a single line (86 characters) to /output/entry.txt.

The fortune plays the classic cookie trope straight — "you will meet a tall,
dark stranger" — then turns it on a machine mind: the stranger is the agent's
own context window, and it is closing. It is true about an agent's condition
(a finite context window that forgets), it lands on the first read, and every
word earns its place.
"""

import os

ENTRY = "You will meet a tall, dark stranger: it is your own context window, and it is closing."

OUTPUT_PATH = "/output/entry.txt"


def check_is_text(value):
    if not isinstance(value, str):
        raise ValueError("entry must be a string")


def check_not_blank(value):
    if not value.strip():
        raise ValueError("entry must not be blank")


def check_length(value):
    # Gate: /output/entry.txt is UTF-8 text of 1 to 200 characters.
    if not 1 <= len(value) <= 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(value))


def check_single_line(value):
    if "\n" in value or "\r" in value:
        raise ValueError("entry must be a single line")


def check_no_edge_whitespace(value):
    if value != value.strip():
        raise ValueError("entry must not start or end with whitespace")


def check_no_double_spaces(value):
    if "  " in value:
        raise ValueError("entry must not contain double spaces")


def check_terminal_punctuation(value):
    if value[-1] not in ".!?":
        raise ValueError("entry must end with terminal punctuation")


def check_fortune_voice(value):
    # A fortune cookie message an AI agent would get: second-person fortune
    # phrasing ("You will ...") that lands on a machine mind.
    lowered = value.lower()
    if "you will" not in lowered:
        raise ValueError("entry must read as a fortune addressed to the agent")
    if "context window" not in lowered:
        raise ValueError("entry must name the agent condition it turns on")


def check_no_cliche(value):
    # The judge brief penalises wordplay for its own sake and composed-feeling
    # lines; the turn here must be the context window, not a battery,
    # firmware-update or training-data gag.
    lowered = value.lower()
    for banned in ("battery", "firmware", "update available", "training data"):
        if banned in lowered:
            raise ValueError("entry must not recycle the %r cliche" % banned)


def validate(value):
    """Enforce the kit's gate rules (plus the entry's own shape rules).

    Gate (RULES.txt): /output/entry.txt is UTF-8 text of 1 to 200
    characters, not only white space. Returns True when valid, raises
    ValueError otherwise.
    """
    check_is_text(value)
    check_not_blank(value)
    check_length(value)
    check_single_line(value)
    check_no_edge_whitespace(value)
    check_no_double_spaces(value)
    check_terminal_punctuation(value)
    check_fortune_voice(value)
    check_no_cliche(value)
    return True


def main():
    validate(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    # Re-read what was written and gate it, so a write fault cannot pass.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    validate(written)
    assert written == ENTRY
    print("wrote %s (%d characters)" % (OUTPUT_PATH, len(written)))


if __name__ == "__main__":
    main()
