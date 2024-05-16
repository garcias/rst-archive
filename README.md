# rst-archive

Recovering data from the Internet Archive snapshot of Reducing Stereotype Threat

## Update: Website hosting the articles

I created a [website](https://garcias.github.io/reducing-stereotype-threat) to render the archived data as modern web pages. The site offers [8 review articles](https://garcias.github.io/reducing-stereotype-threat/reviews/) about different aspects of stereotype threat, each linking to summary pages of relevant articles. Thanks to the Jekyll theme [Just The Docs](https://github.com/just-the-docs/just-the-docs), the entire archive is searchable! 

I use this site for employee training, each person reads a summary of a research study, and analyzes how stereotype threat operates in it.

[Source of the website](https://github.com/garcias/reducing-stereotype-threat)

## Why?

For years Catherine Good (Baruch College) and Steve Stroessner (Barnard College) maintained `www.reducingstereotypethreat.org`. It consisted of an annotated bibliography of research on stereotype threat, along with discussions of various aspects of stereotype threat (e.g. vulnerable groups, situations, mechanisms, ...). This made it an indispensable resource for learning about stereotype threat and then teaching it to others. When training teaching assistants, I would send them to the site to explore specific questions. This research would prime them for discussion at training sessions.

Sometime in May 2017 the site went down. I searched for reports about why this might have happened, but couldn't find anything. Inquiries to the authors went unanswered. This happened just as I was gearing up for another training. Luckily it had been captured by Internet Archive and I directed students to use the Wayback Machine, but page loads were pretty slow. 

This project is my attempt to extract the relevant data from the archived pages. My immediate goal is to have the data available for colleagues, students, and trainees to access. My longer-term goal is to make the data available through an API, enabling others to build new resources from it (like maybe reviews, case studies, or more recent research). My stretch goal is to find a valid doi corresponding to each citation.

## How?

1. Bibliography
    1. Run `bibliography.py` to scrape the bibliography page (on Wayback) into `temp.json`.
    2. Inspect `temp.json` and make manual changes, such as joining journal name and volume, or appending missing text to citation.
    3. Detect blocks of text containing multiple citations entries.
    4. Mark separation between citations with ` || `.
    5. Run `split-blocks.py` to split text into lists of citations within each block; save into `blocks.json`.
    6. Detect and fix discrepancies between citation list and journal and href lists within each block.
    7. Run `split-citations.py` to create a separate bibliographic entry for each citation; save into `citations.json`
    8. Run `annotations.py` to scrape annotation text from Internet Archive; save into `annotations.json`
    9. Run `separate-title.py` to extract title text into new field; save into `bibliography.json`.
2. Topic pages
    1. Run `scrape-topics.py` to scrape the topic pages (on Wayback) into `topics.json`.
    2. Inspect `topics.json` and make manual changes, such as paragraph breaks and missing subtopics
3. Validation
    - Check that each link in the topic pages corresponds to an `href` in either the bibliography entries or to a topic page.

## To do

- [x] Scrape topic pages and store as JSON
- [x] Check manually
- [x] Validate links
- [ ] Add attribution

## Reflection

This was one of the more challenging scraping projects I've done in a while. I'm glad I invested time to learn Xpath syntax; I really needed it for navigating the structures in this website. Regular expressions expedited some of the parsing, too. I appreciated Python's extensive support especially the mercy that is the `re.escape` function!

The website overall had a reasonable high-level structure, divided between topics and bibliography. A lot of the challenge arose from the text itself. Not every paragraph fell into a `<p>` node, and around any inline element (`span`, `a`, formatting) was a veritable alphabet soup of various white-space characters. Unfortunately there was no clear pattern to the number or sequence of these characters, so I couldn't use them to infer paragraph breaks. My best guess is that the text was originally written in some word processor like MS Word, and then copied and pasted into a CMS interface. The process likely would have included invisible formatting codes that the CMS then translated into these excess characters.

I learned to embrace regular expressions, having resisted or written around them for the past 15 years. Another thing I discovered was that you can unpack lists much as you would tuples; not sure how I missed that for the past 20 years. And this is not new, but I noticed that I continue to favor comprehensions for list and dictionary creation. This became apparent when writing the scanning routine in `scrape-topics.py`, which really called for a more imperative pattern.
