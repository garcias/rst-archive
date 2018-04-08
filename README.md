# rst-archive

Recovering data from the Internet Archive snapshot of Reducing Stereotype Threat

## Why?

For years Catherine Good (Baruch College) and Steve Stroessner (Barnard College) maintained `www.reducingstereotypethreat.org`. It consisted of an annotated bibliography of research on stereotype threat, along with discussions of various aspects of stereotype threat (e.g. vulnerable groups, situations, mechanisms, ...). This made it an indispensable resource for learning about stereotype threat and then teaching it to others. When training teaching assistants, I would send them to the site to explore specific questions. This research would prime them for discussion at training sessions.

Sometime in May 2017 the site went down. I searched for reports about why this might have happened, but couldn't find anything. Inquiries to the authors went unanswered. This happened just as I was gearing up for another training. Luckily it had been captured by Internet Archive and I directed students to use the Wayback Machine, but page loads were pretty slow. 

This project is my attempt to extract the relevant data from the archived pages. My immediate goal is to have the data available for colleagues, students, and trainees to access. My longer-term goal is to make the data available through an API, enabling others to build new resources from it (like maybe reviews, case studies, or more recent research). My stretch goal is to find a valid doi corresponding to each citation.

## How?

1. Run `bibliography.py` to scrape the bibliography page (on Wayback) into `temp.json`.
2. Inspect `temp.json` and make manual changes, such as joining journal name and volume, or appending missing text to citation.
3. Detect blocks of text containing multiple citations entries.
4. Mark separation between citations with ` || `.
5. Run `split-blocks.py` to split text into lists of citations within each block; save into `blocks.json`.
6. Detect and fix discrepancies between citation list and journal and href lists within each block.
7. Run `split-citations.py` to create a separate bibliographic entry for each citation; save into `citations.json`
8. Run `annotations.py` to scrape annotation text from Internet Archive; save into `annotations.json`
9. Run `separate-title.py` to extract title text into new field; save into `bibliography.json`.

## To do

- Scrape topic pages and store as JSON
