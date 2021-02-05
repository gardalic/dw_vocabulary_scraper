# DW Vocabulary Scraper
Script to scrape the vocabulary sections of DW Learn German "Nico's weg" course. 
- currently supports A1

## Project goal
Help with learning German. Primarily created to support the DW course Nico's weg. How it works:
- it scrapes the Overview page of the (currently supports only A1) course
- parses the links to the individual lessons
- navigates to each lesson vocabulary page
  - vocabulary page follows a static naming convention, so the script doesn't have to crawl, it can go there directly
- scrapes and parses the vocabulary page
  - saves the parsed entry as a noun (saves the article separate from the base noun) or phrase/verb
- saves the data in three separate files in dictionary format
  1. lessons.txt
  2. nouns.txt
  3. phrases.txt
