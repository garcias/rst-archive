import json
import re

# pattern is 4-digit number, possibly followed by a / and another 4-digit number;
# possibly followed by letter that may be wrapped in parens;
# or the word "in press"; wrapped optionally with space
pattern = re.compile(' ?([[0-9]{4}(\/[[0-9]{4})? ?\(?[a-z]?\)?| ?[Ii]n [Pp]ress) ?')

with open("annotations.json", "r") as f:
    annotations = json.load(f)

def separate_title(s):
    year = pattern.findall(s)[0][0]
    year_right = s.rindex(year) + len(year)
    return {
        'title' : s[0:year_right].rstrip(),
        'annotation' : s[year_right:].lstrip()
    }

for annotation in annotations:
    if "annotation" in annotation:
        annotation.update(separate_title(annotation['annotation']))

print json.dumps(annotations, indent=2)
