# Plan

1. Get list of topics from '/html/body/table/tbody/tr/td/table/tbody/tr[5]/td/table'; eight <td>s
2. from each td, get the <a>'s @href, and its <img>'s @alt
3. follow hrefs to each page, on each page:
4. focus on the main content in: 
    - /html/body/table/tbody/tr/td/table/tbody/tr[6]/td/table/tbody/tr[2]/td
    - /html/body/table/tbody/tr/td/table/tbody/tr[6]/td/table/tbody/tr[2]/td
4. Delete the nav table if it exists at 
    - /html/body/table/tbody/tr/td/table/tbody/tr[6]/td/table/tbody/tr[2]/td/span/table
5. collect all <a> tags and make a list of their text_content and @href
6. collect all <p> tags and clean up their text_content
7. text at beginning may be missed. subtract the collected <p> tags and get the text_content remaining
8. subheadings seem to have <a> tag with @name attribute
9. Assemble text into paragraphs and assign to appropriate subtopics
10. Search for text of links found earlier and format as link for Markdown
11. Infer subtopics


