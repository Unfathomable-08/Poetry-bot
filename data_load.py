import json

with open('Poetry.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

poets = list(set([row['poet'] for row in data]))

print(data[:2])
print(poets, len(poets))