
# Scrape bibliography page

Run bibliography scraper.

```bash
    python bibliography.py > temp.json
```

Resulting document has 170 blocks, with following fields:

```
    index:
    journals:
    -
    links:
    - text:
        href:
    text:
```

# Manual changes to journal lists and text as needed

```
    15.journals: Add name "Journal of Experimental Social Psychology, 40"
    42.journals: Change "oping" to "Coping"
    59.journals: remove empty 4th journal
    67.journals: Add name "Sex Roles, 47"
    67.text: append " Blatant stereotype threat and women’s math performance: Self-handicapping as a strategic means to cope with obtrusive negative performance expectations. Sex Roles, 47, 193–198."
    77.journals: join journal name and volume
    82.journals: join journal name and volume
    83.journals: join journal name and volume
    98.journals: add name "Journal of Applied Social Psychology, 32"
    98.text: append " Stereotype threat effects on the Raven Advanced Progressive Matrices scores of African Americans. Journal of Applied Social Psychology, 32,767–787."
    101.journals: add name "Journal of Personality and Social Psychology, 83"
    101.text: append " Journal of Personality and Social Psychology, 83, 896–918."
    107.journals: remove empty 2nd journal
    115.journals: remove empty 2nd journal
    117.journals: join journal name and volume
    120.journals: remove empty 7th journal
    124.journals: remove empty 2nd journal
    145.journals: join journal name and volume
    158.journals[1]: join journal name and volume
    158.journals[6]: join journal name and volume
    163.journals: join journal name and volume
    167.journals: remove empty 2nd journal
    167.journals: remove empty 4th journal
```

Save changes to `temp.json`.


# Manual changes to separate text in blocks

First find out which blocks have multiple entries. Seems that ")." is a pretty consistent marker of a unique citation. Search for this in the 'text' field of each block and fitler on it.

```python
    # in python shell
    %run bibliography.py
    block_counts = filter( lambda (i,b): b > 1, [ (i, block['text'].count(').')) for i,block in enumerate(blocks) ] )
```

Result is:
```
    (30, 2) - not really
    (31, 4) - only 2
    (39, 2) 
    (42, 7)
    (48, 5)
    (52, 3)
    (56, 2) - not really
    (59, 4)
    (80, 2) - not really
    (90, 2)
    (118, 3)
    (119, 2)
    (120, 13)
    (135, 2)
    (144, 2)
    (148, 2)
    (150, 2)
    (154, 2)
    (158, 8)
    (167, 2)
```

Open `temp.json` and add the character sequence "` || `" between citations in blocks that contain multiple citations. Save changes to `temp.json`


# Split blocks

For each string in the 'text' field with a list of strings, split across the separator ` || ` and store result as the property `citations`.

Run `python split-blocks.py > blocks.json` 

```python
# in file: split-blocks.py
    with open('temp.json', 'r') as f:
        blocks = json.load(f)
    
    for block in blocks:
        block['citations'] = block['text'].split(" || ")
```

Also checks for and removes empty journal entries. 


# Check for correspondence

Check that every journal in a block can be found in its corresponding citation list. Check that every link text in a block can be found in its corresponding citation list.


```python
    # in python shell
    %run split-blocks.py
    journal_check = [ 
        (block['index'], [
            True in [
                (journal in citation)
                for citation in block['citations']
            ]
            for journal in block['journals']
        ] )
        for block in blocks
    ] # generates list of tuples e.g. (144, [True, True])

    link_check = [ 
        (block['index'], [
            True in [
                (link['text'] in citation)
                for citation in block['citations']
            ]
            for link in block['links']
        ] )
        for block in blocks
    ] # generates list of tuples e.g. (144, [True, True])
```

Detect any discrepancies.

```python
    # in python shell
    [ i for (i, checks) in journal_check if True not in checks ]
    # [15, 131, 168, 169]

    [ i for (i, checks) in link_check if False in checks ]
    # []
```

No issues for link correspondence! But for journal correspondence, four blocks contain `False` or no values. 

# Manual changes to resolve inconsistencies in journals

```
    15.citations: is incomplete. Append " When saying and doing diverge: The effects of stereotype threat on self-reported versus non-verbal anxiety. Journal of Experimental Social Psychology, 40, 247–255."
    131: is empty. Delete
    168: is a duplicate. Delete
    169: is empty. Delete
    198: is a duplicate. Delete
    159: is a duplicate. Delete (discovered by inspection)
```

Save changes to `blocks.json`.

# Next

At this point, we should be able to construct a list of individual citations:
```
    - citation: 
      citation_md:  # marked up with <i class='journal'></i>
      href:         # use in the future just as an identifier, or to construct separate file
      title:        # scraped from wayback annotation page
      annotation:   # scraped from wayback
      doi:          # much bigger project probably using Google Scholar API
```

# Split to individual citations

Run `python split-citations.py > citations.json` 

Also checks for and removes duplicates, using `pandas.DataFrame.groupby` to identify unique groups.

In `citations.json`, add entry for Abrams, Eller, and Bryant b/c wasn't picked up in initial scrape.

# Following links to grab annotations (next)

Check that all links can be followed successfully.


