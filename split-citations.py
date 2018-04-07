import json
from pandas import DataFrame

with open('blocks.json', 'r') as f:
    blocks = json.load(f)

bibliography = []

for block in blocks:
    for citation in block['citations']:

        href = ""
        for link in block['links']:
            if link['text'] in citation:
                href = link['href'][0] 
                # [0]  is to get rid of list structure mistakenly introduced in bibliography.py

        journal = ""
        for journal_text in block['journals']:
            if journal_text in citation:
                journal = journal_text
        
        bibliography.append(
            {
                'citation' : citation,
                'journal' : journal,
                'href' : href,
            }
        )

# # add an index just for testing
# for i, each in enumerate(bibliography):
#     each['index'] = i

# eliminate duplicates
df = DataFrame(bibliography)
groups = df.groupby('citation').groups # dict of unique group : index
indices = [ index[0] for group,index in groups.items() ] 
indices.sort()
citations = [ bibliography[i] for i in indices ]

print json.dumps(citations, indent=2)
