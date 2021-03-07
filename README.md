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
- saves the data in three separate files in JSON format in the working directory:
  1. lessons.json
  2. nouns.json
  3. phrases.json
## Usage
It can be run from the command line without any parameters, any flags are optional. Usage:

```python vocabulary_scraper.py [args]```

Currently implemented parameters:
- `-h, --help` - shows help message and exits
- `-u (--url) URL` - URL of the landing (overview) page
- `-w (--write) WRITE` - Write mode for files, the `main` function, as well as the `write_files` initializes it as "w". It will raise an exception if it is not set to "w" or "a".
- `-l (--lesson) LESSON` - Specify the URL for the single lesson to scrape, uses `'https://learngerman.dw.com/<LESSON>/lv'` format. Will append to files.
