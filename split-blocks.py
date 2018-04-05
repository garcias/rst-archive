import json

with open('temp.json', 'r') as f:
    blocks = json.load(f)

for block in blocks:
    block['citations'] = block['text'].split(" || ")

# While we're at it, remove empty journal entries:

for block in blocks:
    for i,journal in enumerate(block['journals']):
        if len(journal) == 0:
            block['journals'].pop(i)


print json.dumps(blocks, indent=2)


    