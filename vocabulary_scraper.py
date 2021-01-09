import requests
import re
import dw_vocabulary as dv
from bs4 import BeautifulSoup
from time import sleep
from random import randint


class ScrapeVocabulary:
    """
    Class to scrape the A1 course Overview page and get the links to the individual lessons.\n
    From there it follows the link to the vocabulary page and scrapes the words and phrases.\n
    Saves the word list and the lesson list in separate files.
    """
    # TODO Error handling on requests and file I/O
    # TODO Testing scripts, implement unittest

    def __init__(self, url):
        self.url = url
        self.lesson_list = []
        self.noun_list = []
        self.phrase_list = []

    def scrape_lessons(self, url):
        """Parse the landing page and get links to the lessons, lesson title, lesson subtitles and
        description (if they exist)."""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        lessons = soup.select("div[data-lesson-id]")

        for i, lesson in enumerate(lessons, 1):
            sequence_id = i
            current_lesson = dv.Lesson(
                i,
                lesson.find("a")["data-lesson-id"],
                lesson.find("a").find("h3").get_text(),
                lesson.find("a")["href"],
                lesson.find("a").find("p").select(".title ")[0].get_text(),
                lesson.find("a").find("p").select(".description ")[0].get_text(),
            )
            # Save the lesson
            self.lesson_list.append(current_lesson.__dict__)

            # Call the lesson vocabulary scraper and sleep
            self.scrape_vocabulary(current_lesson.link, current_lesson.sequence_id)
            sleep_time = randint(1, 4)
            print(f"Scrapped '{str(current_lesson)}', sleeping for {sleep_time}s...")
            sleep(sleep_time)

    def scrape_vocabulary(self, url, id=0):
        """Parse the lesson vocabulary page and return a dictionary with the word/phrase data.\n
        id = 0 means that the entry is manual, scraped lessons start the id sequence at 1."""

        response = requests.get(f"https://learngerman.dw.com/{url}/lv")
        soup = BeautifulSoup(response.text, "html.parser")
        entries = soup.find_all("div", class_="row vocabulary")

        for entry in entries:
            # .replace() is for clean up, escapes "\xa0" characters in input
            phrase = entry.select("strong")[0].get_text().replace("\xa0", " ")
            translation = (
                entry.find("div", class_="col-sm-4 col-lg-3 vocabulary-entry")
                .find("div")
                .find("p")
                .get_text()  # looks bad, but it is black formatter recomendation
            ).replace("\xa0", " ")
            formatted = self.format_entry(phrase, translation, id)
            if isinstance(formatted, dv.Noun):
                self.noun_list.append(formatted.__dict__)
            else:
                self.phrase_list.append(formatted.__dict__)

    def format_entry(self, entry, translation, id=0):
        """Formats the entry and returns either VocabEntry or Noun."""
        noun = re.compile("^(der|die|das) (\w*), die (\w*)").search(entry)
        phrase = re.compile("[\w\s.,]*[?.!]$").search(entry)

        if noun:
            return dv.Noun(noun.group(2), translation, noun.group(1), noun.group(3), id)
        elif phrase:
            return dv.VocabEntry(entry, translation, id, "phrase")
        else:
            return dv.VocabEntry(entry, translation, id)

    def write_list_file(self, lst, outname):
        with open(outname, "w", encoding="utf-8") as file:
            for line in lst:
                file.write(f"{str(line)}\n")
            print(f"Saved list to file '{outname}'")


if __name__ == "__main__":
    url = "https://learngerman.dw.com/en/beginners/c-36519789"
    scraper = ScrapeVocabulary(url)
    print("Beginning scraping...\n")
    scraper.scrape_lessons(scraper.url)

    print("Scraping finished, writing lists to files...")
    scraper.write_list_file(scraper.lesson_list, "lessons.txt")
    scraper.write_list_file(scraper.noun_list, "nouns.txt")
    scraper.write_list_file(scraper.phrase_list, "phrases.txt")

    print("Processing done!")

    # scraper.scrape_vocabulary("en/tschüss/l-37251033")
    # scraper.write_list_file(scraper.phrase_list, "phrases.txt")
