from urllib2 import urlopen
from lxml import html, etree
import json
import re

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
    }
    for a in page.xpath('.//a') 
]


def relativize(link):
    pattern = u'https\\:\\/\\/.*www\\.reducingstereotypethreat\\.org\\/'
    return re.sub(pattern, "", link)    

def cleanup(s):
    return ' '.join(s.split())


for topic in topics[1:]:
    url = base_url + topic['href']
    doc = html.parse(urlopen(url)).getroot()
    page = doc.xpath('/html/body/table/tr/td/table/tr[6]/td/table/tr[2]/td')[0]

    # check for nav table; if it exists, remove from parent
    try:
        nav = page.xpath('.//span/table')[0]
        nav.getparent().getparent().remove(nav.getparent())
    except IndexError:
        print "no navigation found"

    # get links and headings from tags in text, then clean up text

    links = [ 
        {
            'href' : a.attrib['href'], 
            'text' : cleanup(a.text_content())
        } 
        for a in page.xpath('.//a[@href]') 
        if not "#top" in a.attrib['href']
    ]

    subtopics = [
        {
            'name' : relativize(a.attrib['name']),
            'title' : cleanup(a.getparent().text_content())
        }
        for a in page.xpath('.//a[@name]') 
    ]

    text = cleanup(page.text_content())

    # scan for link text, replace with Markdown-style link tags

    scanned_text = []
    unscanned_text = text

    for link in links:
        [ left, right ] = unscanned_text.split(link['text'], 1)  # maxsplit = 1
        center = u"[{text}]({href})".format(**link)
        scanned_text.append(left)
        scanned_text.append(center)
        unscanned_text = right

    scanned_text.append(unscanned_text)
    text = ''.join(scanned_text)


    # scan for heading text, break into subtopic blocks

    scanned_text = []
    unscanned_text = text

    for subtopic in subtopics:
        [ left, right ] = unscanned_text.split(subtopic['title'], 1)
        scanned_text.append(left)
        unscanned_text = right

    last_text = re.sub("[Bb]ack [Tt]o [Tt]op", "", unscanned_text)
    scanned_text.append(last_text)

    for i, subtopic in enumerate(subtopics):
        subtopic['text'] = scanned_text[i + 1]

    topic['text'] =  scanned_text[0]
    topic['subtopics'] = subtopics

# print json.dumps(blocks, indent=2)
