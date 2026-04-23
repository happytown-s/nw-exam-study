import json

for fname in ['src/data/calc-training.json', 'src/data/subject-b-training.json']:
    with open(fname, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"\n=== {fname} ({len(data)} Qs) ===")
    cats = {}
    for q in data:
        c = q.get('category','?')
        cats[c] = cats.get(c, 0) + 1
    for c, n in sorted(cats.items()):
        print(f"  {c}: {n}")
