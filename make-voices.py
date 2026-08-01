#!/usr/bin/env python3
"""
Builds the voice pack for Letter Board.

    pip install edge-tts
    python make-voices.py

Writes ~130 mp3 files into ./audio/ using the exact filenames the app looks for.
Drop that folder next to abc-app.html, then turn on "Use a voice pack" in the
grown-ups panel.

VOICE
-----
en-AU-NatashaNeural  (female, Australian)   <- default
en-AU-WilliamNeural  (male, Australian)
Run `edge-tts --list-voices` for the rest.

edge-tts is not open source and is technically outside Microsoft's terms, which
scope it to Edge's Read Aloud feature. Fine for a kid's tablet at home; don't
ship it commercially. For a fully open alternative see the note at the bottom.

RE-RECORDING IN YOUR OWN VOICE
------------------------------
Record over any file and keep the filename. Your voice beats every model here,
and the phoneme clips (sound-*.mp3) are worth doing yourself regardless — no TTS
engine says an isolated /b/ properly.
"""

import asyncio, os, edge_tts

VOICE = "en-AU-NatashaNeural"
RATE  = "-15%"          # slower for a 5-year-old
OUT   = "audio"

# letter, word, phoneme spoken approximation
DATA = [
    ("A", "Apple",      "ah"),   ("B", "Ball",   "buh"),
    ("C", "Cat",        "kuh"),  ("D", "Dog",    "duh"),
    ("E", "Egg",        "eh"),   ("F", "Fish",   "ff"),
    ("G", "Goat",       "guh"),  ("H", "Hat",    "huh"),
    ("I", "Igloo",      "ih"),   ("J", "Jug",    "juh"),
    ("K", "Kite",       "kuh"),  ("L", "Leaf",   "ll"),
    ("M", "Moon",       "mm"),   ("N", "Nest",   "nn"),
    ("O", "Octopus",    "oh"),   ("P", "Pig",    "puh"),
    ("Q", "Queen",      "kwuh"), ("R", "Rainbow","rr"),
    ("S", "Sun",        "sss"),  ("T", "Tree",   "tuh"),
    ("U", "Umbrella",   "uh"),   ("V", "Van",    "vv"),
    ("W", "Watermelon", "wuh"),  ("X", "Box",    "ks"),
    ("Y", "Yoyo",       "yuh"),  ("Z", "Zebra",  "zzz"),
]

def manifest():
    m = {
        "trace-first":  "Trace the letter with your finger first.",
        "praise-trace": "Beautiful writing!",
        "try-again":    "Not that one. Try again.",
        "ask-grownup":  "Ask a grown-up to turn on sounds.",
    }
    for L, word, snd in DATA:
        m[f"letter-{L}"] = f"{L} ... {L} is for {word}."
        m[f"sound-{L}"]  = f"{snd}, {snd}, {word}."
        m[f"find-{L}"]   = f"Find the letter {L}."
        m[f"which-{L}"]  = f"{snd}, {snd}. Which one starts with {snd}?"
        m[f"yes-{L}"]    = f"Yes! {L}!"
        # Isolated phoneme for the Build (blending) screen. TTS is poor at
        # these — re-recording phon-*.mp3 in your own voice is well worth it.
        m[f"phon-{L}"]   = snd
    # Whole CVC words for the Build screen (must match CVC in abc-app.html).
    for w in ("cat","dog","pig","hen","sun","bus","bed","cup","hat","box",
              "fox","bug","van","jet","log","pot","pin","fan","map","bat",
              "net","ten"):
        m[f"word-{w}"] = w
    return m

async def build():
    os.makedirs(OUT, exist_ok=True)
    items = manifest()
    for i, (key, text) in enumerate(items.items(), 1):
        path = os.path.join(OUT, f"{key}.mp3")
        if os.path.exists(path):
            continue                      # keeps anything you've re-recorded
        await edge_tts.Communicate(text, VOICE, rate=RATE).save(path)
        print(f"[{i:>3}/{len(items)}] {key}")
    print(f"\nDone. {len(items)} clips in ./{OUT}/")

if __name__ == "__main__":
    asyncio.run(build())

# ---------------------------------------------------------------------------
# FULLY OPEN ALTERNATIVE — Kokoro-82M (Apache 2.0), no Australian accent:
#
#   pip install kokoro soundfile
#
#   from kokoro import KPipeline
#   import soundfile as sf
#   pipe = KPipeline(lang_code="b")            # b = British English
#   for key, text in manifest().items():
#       audio = next(pipe(text, voice="bf_emma", speed=0.85)).audio
#       sf.write(f"audio/{key}.wav", audio, 24000)
#
# Change the app's file extension from .mp3 to .wav, or convert with ffmpeg.
# Piper is the other good option if you want something even lighter:
#   piper --model en_GB-jenny_dioco-medium --output_file audio/letter-A.wav
# ---------------------------------------------------------------------------
