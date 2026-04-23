import json
import sys

def count_english_q(data):
    count = 0
    for q in data:
        has_jp = any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff' for c in q.get('question',''))
        if not has_jp:
            count += 1
    return count

for fname in ['src/data/calc-training.json', 'src/data/subject-b-training.json']:
    with open(fname, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"{fname}: total={len(data)}, english={count_english_q(data)}")
