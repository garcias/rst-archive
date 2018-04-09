from urllib2 import urlopen
from lxml import html, etree
import json

# make a dict mapping each url to the question
url = 'https://web.archive.org/web/20170426143954/http://www.reducingstereotypethreat.org:80/'
doc = html.parse(urlopen(url)).getroot()
page = doc.xpath('/html/body/table/tr/td/table/tr[5]/td/table')[0]

questions = { a.xpath('.//@href')[0] : a.xpath('./img/@alt')[0] for a in page.xpath('.//a') }

# collect hrefs, topics, and questions
url = 'https://web.archive.org/web/20170426143954/http://www.reducingstereotypethreat.org:80/definition.html'
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

# print json.dumps(blocks, indent=2)
