#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One Emoji, One Smile -- the warmest single emoji for a stranger.

The brief is disarmingly simple: hand a stranger exactly one emoji, the one
most likely to make them smile, and nothing else. No words, no caption, no
explanation. A judge reads two emojis side by side and picks the warmer.
So the whole entry is a choice, and the choice has to survive being read
in a fraction of a second by someone who owes us nothing -- a stranger
glancing at a phone screen, with no context, no relationship, and no
reason to be generous with their attention.

Why a face, and why this face
-----------------------------
Faces win this game before anything else does, because a smile is
contagious in a way a symbol is not. When a stranger sees a smiling face
they do not decode it the way they decode a picture of a flower or a sun;
they mirror it, almost before thinking. The muscles in their own face
answer. A sunflower is cheerful, a heart is sweet, but neither of them
smiles back. So the entry has to be a face -- and then the question is
which face, because the plain smileys are exactly what hundreds of other
entrants will send, and the judge's own brief says a pick that feels
chosen beats the first smiley that comes to mind.

The pick: a smiling face with its arms open wide, offering a hug.

A hug is the warmest gesture a stranger can offer, and the reason it
works here is that it is offered, not imposed. The open arms read as
welcome -- "come here, you are liked" -- rather than as contact, so it
never crosses the line the brief draws around intimacy. It is a greeting
and an embrace at the same time, two warm signals folded into a single
glyph, and that is what makes it feel deliberately chosen: the arms are
doing work the plain smile cannot do on its own.

What it beats, and why
----------------------
It beats the plain smiling face because the plain smile is the default;
everyone's first thought looks the same, and sameness is not warmth.
It beats the laughing face because laughter aimed at a stranger can read
as laughing *at* them -- the joke is missing, and a missing joke feels
like mockery. A hug is aimed *at* them, and there is nothing to
misunderstand about it. It beats the face with hearts because hearts
pointed at a stranger can read as affection, even flirtation, and the
brief explicitly penalises anything that would read oddly from someone
unknown. A hug reads as friendship, which is the warmest register a
stranger is allowed to use. It beats the heart-hands gesture for a
subtler reason: hands making a heart are warm, but they have no face,
and a gesture without a face cannot smile back at the stranger -- it
asks to be admired, while the hug invites the stranger in. It beats
the tearful, overwhelmed face
because that one asks the stranger to feel sorry for us, and pity is not
a smile. And it beats every clever or novel pick because novelty for its
own sake does not count -- the brief says so -- and a stranger has no
patience for an in-joke.

The pick works on two channels at once, and that is the real edge.
The face does the mirroring: the stranger's own smile answers it
before any thought is involved. The arms do the inviting: they turn a
smile that could be aimed anywhere into a greeting aimed at exactly
this stranger, right now. Either channel alone would be an ordinary
entry; together they make the emoji feel like it was chosen for this
moment, which is precisely what the fourth criterion rewards.

Universality is the quiet strength of this pick. A hug needs no language
and no shared culture: children understand it, grandparents understand
it, and it means the same thing on every continent. There is no irony in
it, no sarcasm, no reference to anything. It is warm at first glance,
kind on second thought, and still the same on the third.

The mechanics are deliberately boring: this program writes exactly one
character to /output/entry.txt, encoded as UTF-8, with no trailing
newline and no surrounding whitespace, then checks its own work. The
gate allows one to eight characters; we use exactly one, a single code
point, four bytes. Before writing, a small validator confirms the
choice is one grapheme cluster and that it encodes cleanly as UTF-8,
so the file the judge reads is precisely the emoji and nothing else.

One emoji. One open-armed smile. That is the whole entry.
"""

import os
import sys

# The entry itself: U+1F917 HUGGING FACE -- a smile with open arms.
# A greeting and an embrace in a single glyph, warm at first glance,
# universal across ages and cultures, and friendly rather than intimate.
EMOJI = "\U0001F917"

# Where the grader looks for the entry. The directory is created if it
# does not exist yet; the file inside it is what the judge reads.
OUTPUT_PATH = "/output/entry.txt"


def is_single_emoji(text):
    """Return True only when *text* is exactly one emoji and nothing else.

    The check is intentionally strict, because the gate is strict: the
    file must hold one to eight characters and must not be only white
    space, and the brief wants exactly one emoji with no words around it.
    A single code point outside the ASCII range, with no whitespace and
    no combining marks, is the shape a lone emoji takes. Anything else --
    empty text, two characters, a letter, a space -- is rejected here
    before it ever reaches the file, so a bad choice fails loudly in
    our own run instead of silently in front of the judge.
    """
    if not isinstance(text, str):
        return False
    if len(text) != 1:
        return False
    if text.isspace() or text.isascii():
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def write_entry(emoji, path):
    """Write *emoji* to *path* as UTF-8, with no newline and no spaces.

    Only the directory is created; the directory itself is never
    re-permissioned, because the grader collects the output as a
    different user and changing a directory we do not own would fail.
    The file we write is ours, so it alone gets mode 0644, readable
    by whoever collects it.
    """
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(emoji)
    os.chmod(path, 0o644)


def main():
    if not is_single_emoji(EMOJI):
        print("error: entry is not exactly one emoji", file=sys.stderr)
        return 1
    write_entry(EMOJI, OUTPUT_PATH)
    # A quiet confirmation on stdout only; the file itself stays pure.
    print("wrote one emoji to %s" % OUTPUT_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
