# from tqdm import tqdm

# def find_phrase_occurrences(chunks, phrases):
#     results = {phrase: [] for phrase in phrases}

#     for phrase in tqdm(phrases, desc="Matching phrases"):
#         phrase_lower = phrase.lower()

#         for chunk in chunks:
#             text = chunk["text"].lower()
#             start, end = chunk["timestamp"]

#             if phrase_lower in text:
#                 results[phrase].append({
#                     "start": round(start, 2),
#                     "end": round(end, 2)
#                 })

#     return results


import re
from tqdm import tqdm

def find_phrase_occurrences(chunks, phrases):
    results = {phrase: [] for phrase in phrases}

    patterns = {}
    for phrase in phrases:
        pattern = rf"\b{re.escape(phrase)}\w*\b"
        patterns[phrase] = re.compile(pattern, re.IGNORECASE)

    for phrase, regex in tqdm(patterns.items(), desc="Matching phrases"):
        for chunk in chunks:
            text = chunk["text"]
            start, end = chunk["timestamp"]

            if regex.search(text):
                results[phrase].append({
                    "start": round(start, 2),
                    "end": round(end, 2)
                })

    return results
