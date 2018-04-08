from urllib2 import urlopen
from lxml import html
from time import sleep
import json

base_url = 'https://web.archive.org/web/20160609033304/http://reducingstereotypethreat.org:80/'

with open("citations.json", "r") as f:
    citations = json.load(f)

def extract_annotation(doc):
    elem = doc.xpath('/html/body/table/tr/td/table/tr[6]/td/table/tr[1]/td')[0]
    nav_links = elem.xpath('.//a')
    for nav in nav_links:
        nav.getparent().remove(nav)
    
    return elem.text_content()

def cleanup(s):
    return ' '.join(s.split())

for citation in citations:
    sleep(2)
    href = citation['href']

    if len(href) > 0:
        try:
            doc = html.parse(urlopen(base_url + href)).getroot()    
            citation['annotation'] = cleanup(extract_annotation(doc))
        except HTTPError:
            print "not found: " + href

print json.dumps(citations, indent=2)
