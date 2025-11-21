import re

def find_phrase_occurrences(transcript_segments, phrases):
    occurrences = {p: [] for p in phrases}
    for seg in transcript_segments:
        text = seg["text"].lower()
        start, end = seg["timestamp"]
        for phrase in phrases:
            p = phrase.lower()
            # simple word-boundary match
            pattern = r"\b" + re.escape(p) + r"\b"
            if re.search(pattern, text):
                occurrences[phrase].append({"start": float(start), "end": float(end)})
    return occurrences
