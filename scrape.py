from urllib2 import urlopen
from lxml import html, etree
import json

url = 'https://web.archive.org/web/20160609033304/http://reducingstereotypethreat.org:80/bibliography.html'
doc = html.parse(urlopen(url)).getroot()
page = doc.xpath('/html/body/table/tr/td/table/tr[6]/td/table/tr[2]/td')[0]

paragraphs = page.xpath('.//p')
# Some of these paragraphs enclose multiple <p> elements, and some of these are blank lines
# But if there is a blank line, it likely doesn't have a corresponding <a>

def cleanup(s):
    return ' '.join(s.split())

blocks = [
    {
        'index' : i,
        'text' : cleanup(p.text_content()),
        'links' : [
            {
                'href' : link.xpath('.//@href'),
                'text' : cleanup(link.text_content()),
            } for link in p.xpath('.//a') 
        ],
        'journals' : [ cleanup(i.text_content()) for i in p.xpath('.//i') ],
    } 
    for i,p in enumerate(paragraphs)
]

print json.dumps(blocks, indent=2)


    

# Bosson (2004) missing journal ("Journal of Experimental Social Psychology, 40")
# Dweck (1999) name of journal "oping" should be "Coping"
# Inzilcht, 4th journal is empty
# Keller (2000) missing journal ("Sex Roles")
# Kray (2002) journal and volume split
# Levy (1996) journal and volume split
# Leyens (2000) journal and volume split
# McKay (2002) missing journal "Journal of Applied Social Psychology, 32"
# Mendoza (2002) missing journal "Journal of Personality and Social Psychology, 83"
# Nguyen (2008) journal and volume split
# Osborne (2007) journal and volume split
# Osborne (2000) journal and volume split
# Rydell (in press) journal and volume split
# Rosenthal (2007) journal and volume split
# Ryan (2005) duplicate
# Sackett (2004) duplicate
# Sackett (2001) duplicate
# Schmader (2008) duplicate
# Stangor (1998) journal and volume split
# Walsh (1999) journal and volume split
# Wheeler (2001) journal and volume split; duplicate
# Wheeler (2001) journal and volume split; duplicate
# Yopyk (2005) journal and volume split
# Zirkel (2004) journal and volume split

