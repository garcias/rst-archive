from urllib2 import urlopen
from lxml import html, etree
import json

base_url = 'https://web.archive.org/web/20170426143954/http://www.reducingstereotypethreat.org:80/'

# make a dict mapping each url to the question
url = base_url
doc = html.parse(urlopen(url)).getroot()
page = doc.xpath('/html/body/table/tr/td/table/tr[5]/td/table')[0]

questions = { a.xpath('.//@href')[0] : a.xpath('./img/@alt')[0] for a in page.xpath('.//a') }

# collect hrefs, topics, and questions
url = base_url + 'definition.html'
doc = html.parse(urlopen(url)).getroot()
page = doc.xpath('/html/body/table/tr/td/table/tr[3]/td/table/tr')[0]

topics = [ 
    { 
        'href' : a.xpath('.//@href')[0],
        'topic' : a.xpath('./img/@alt')[0],
        'question' : questions[a.xpath('.//@href')[0]],
    } for a in page.xpath('.//a') 
]


def cleanup(s):
    return ' '.join(s.split())


url = base_url + topics[1]['href']
doc = html.parse(urlopen(url)).getroot()
page = doc.xpath('/html/body/table/tr/td/table/tr[6]/td/table/tr[2]/td')[0]

# check for nav table; if it exists, remove from parent
try:
    nav = page.xpath('.//span/table')[0]
    nav.getparent().getparent().remove(nav.getparent())
except IndexError:
    print "no navigation found"

links = [ 
    {
        'href' : a.attrib['href'], 
        'text' : cleanup(a.text_content())
    } 
    for a in page.xpath('.//a[@href]') 
    if not "#top" in a.attrib['href']
]

headings = [
    {
        'name' : a.attrib['name'],
        'title' : cleanup(a.getparent().text_content())
    }
    for a in page.xpath('.//a[@name]') 
]

text = cleanup(page.text_content())

# print json.dumps(blocks, indent=2)
