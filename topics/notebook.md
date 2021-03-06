# Plan

1. Get list of topics from '/html/body/table/tbody/tr/td/table/tbody/tr[5]/td/table'; eight `<td>`s
2. from each `<td>`, get the `<a>`'s `@href`, and its `<img>`'s `@alt`
3. follow hrefs to each page, on each page:
4. focus on the main content in: 
    - /html/body/table/tbody/tr/td/table/tbody/tr[6]/td/table/tbody/tr[2]/td
4. Delete the nav table if it exists at 
    - /html/body/table/tbody/tr/td/table/tbody/tr[6]/td/table/tbody/tr[2]/td/span/table
5. collect all a tags and make a list of their text_content and @href
6. collect all p tags and clean up their text_content
7. text at beginning may be missed. subtract the collected p tags and get the text_content remaining
8. subheadings seem to have a tag with @name attribute
9. Assemble text into paragraphs and assign to appropriate subtopics
10. Search for text of links found earlier and format as link for Markdown
11. Infer subtopics

## Get the topics

Each topic is associated with a framing question. The questions are only listed on the front page (hidden as alt text of images). Parse that page and match the `<table>` element containing eight topic tiles as `page`. From each tile get the url and question, and build a dictionary mapping url => question.

```python
    questions = { a.xpath('.//@href')[0] : a.xpath('./img/@alt')[0] for a in page.xpath('.//a') }
```

The page `definition.html` has a nav bar containing the eight topics, containing both url and topic name. Parse this page, match the enclosing element, and get these data. From them, and the `questions` mapping, build a list of entries storing the url, topic name, and question.

```python
    topics = [ 
        { 
            'href' : a.xpath('.//@href')[0],
            'topic' : a.xpath('./img/@alt')[0],
            'question' : questions[a.xpath('.//@href')[0]],
        } for a in page.xpath('.//a') 
    ]
```

## Follow a link

Follow each topic link to its topic page. Except for topics[0], each page has a navigation table, so find and remove it.

```python
    url = base_url + topics[1]['href']
    doc = html.parse(urlopen(url)).getroot()
    page = doc.xpath('/html/body/table/tr/td/table/tr[6]/td/table/tr[2]/td')[0]

    # check for nav table; if it exists, remove from parent
    try:
        nav = page.xpath('.//span/table')[0]
        nav.getparent().getparent().remove(nav.getparent())
```

## Grab links and subtopic headings in page

Search for all `<a>`s that have href, and collect both the `@href` and text. Do the same for `<a>`s that have name property, and collect their `@name` and text; these are subtopic headings.

```python
    links = [ 
        {
            'href' : a.attrib['href'], 
            'text' : cleanup(a.text_content())
        } 
        for a in page.xpath('.//a[@href]') 
        if not "#top" in a.attrib['href']
    ]

    topics = [ 
        { 
            'href' : a.xpath('.//@href')[0],
            'topic' : a.xpath('./img/@alt')[0],
            'question' : questions[a.xpath('.//@href')[0]],
        } 
        for a in page.xpath('.//a') 
    ]

```

Finally grab the text.

```python
    text = ' '.join(page.text_content().split())
```

### Check that you can find each one in the cleaned-up text

Seems like each heading is unique within the text. But some references are linked 2 or 3 times.

```python
    [ text.count(heading['text']) for heading in headings ]
    # [1, 1, 1, 1, 2, 1, 1, 1, 1]

    [ (text.count(link['text']), link['href'] ) for link in links if text.count(link['text']) > 1 ]
    # [(3, 'bibliography_steele_aronson.html'),
    #  (2, 'bibliography_oswald_harvey.html'),
    #  (2, 'bibliography_keller.html'),
    #  (3, 'bibliography_steele_aronson.html'),
    #  (2, 'bibliography_keller.html'),
    #  (3, 'bibliography_steele_aronson.html'),
    #  (2, 'bibliography_oswald_harvey.html')]    
```

# Add tags for links in text

## First try using repeated scans

Search for link text throughout cleaned up page and replace with markdown-style `[]()` tags.

```python
    # This doesn't work!
    md_text = text
    for link in links:
        pattern = "(?<!\[)" + re.escape(link['text'])  # excludes tagged text from match
        repl = u"[{text}]({href})".format(**link)
        md_text = re.sub(pattern, repl, md_text, count=1)
```

Doesn't work! Some text (like "2007a") are contained in links and get matched and substituted. Need a different approach.

## Second try using fragmentation

This time remove already-scanned text each time a match is found. (Did you know you can unpack a list? First time doing it!)

```python
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
```

Search for subtopic text throughout cleaned up page and break into individual sections. Store each in a new `text` field.

```python
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
```

Finish up by assigning to the `topics` list.

```python
    topics[1]['text'] =  scanned_text[0]
    topics[1]['subtopics'] = subtopics
```

Now extend to multiple pages, by replacing `topics[1]` with iterator `topic`.

```python
    for topic in topics[1:]:
        url = base_url + topic['href']
        # etc ...

    topic['text'] =  scanned_text[0]
    topic['subtopics'] = subtopics
```

### Test that links are good

In loop, accumulate links into `all_links`. After running script, test that each link goes to an actual page.

```python
    from requests import get
    [
        {
            'index' : i,
            'code' : get(base_url + link['href']).status_code,
            'href' : link['href'],
        }
        for i, link in enumerate(all_links)
    ]

    [ link['index'] for link in _ if link['code'] != 200 ]
    # []
```

```python
    [ 
        [ 
            u"{title:40.40}: {text:60.60}".format(**subtopic) 
            for subtopic in topic['subtopics'] 
        ] 
        for topic in topics
    ]
    # [u'Decreased performance                   :  Perhaps the most widely known consequence of stereotype thr',
    #  u'Internal Attributions for Failure       :  Individuals often attempt to identify what factors are resp',
    #  u'Reactance                               :  Stereotype threat can produce the opposite effects, actuall',    
```

## Do the scrape

```bash
    python scrape-topics.py > topics.json
```

"Low coping sense of humor" missing from topic list, its text is in "Internal Locus of Control/Proactive Personality"

In `topics.json`, insert record at line 93, and move text beginning with " One's sense of humor can also" into this record:

```json
      {
        "text": " One's sense of humor can also affect how one views and interacts with the world. Humor appears to buffer ... ", 
        "name": "lowcoping", 
        "title": "Low coping sense of humor"
      }, 
```

## Validate links

```python
    with open('topics.json','r') as f:
        topics = json.load(f)
    
    with open('./bibliography/bibliography.json','r') as f:
        bibliography = json.load(f)
    
    all_href = []
    all_href += [ topic['href'] for topic in topics ]
    all_href += [ b['href'] for b in bibliography]
    
    all_text = []
    all_text +=  [ " ".join([ subtopic['text'] for subtopic in topic['subtopics'] ]) for topic in topics ]
    all_text +=  [topic['text'] for topic in topics ]
    all_text += [ b['annotation'] for b in bibliography if 'annotation' in b ]
    all_text = ' '.join(all_text)
    all_links = re.compile('(?<=\]\().*?html(?=\))').findall(all_text)

    [ link for link in all_links if not link in all_href ]
    # [u'bibliography_osborne_2001.html',
    #  u'q04.html', 
    #  u'bibliography_katz_roberts_robinson.html',
    #  u'bibliography.html']
```

- 'bibliography_osborne_2001.html'
    - year dropped from url in later versions of RST => 'bibliography_osborne.html'
    - replace reference to point to later url
- 'q04.html'
    - changed in later versions of RST => 'situations.html'
    - replace reference to point to later url
- 'bibliography_katz_roberts_robinson.html'
    - pulled from later versions of RST
    - no change

Make change manually.
