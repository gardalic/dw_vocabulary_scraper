class Lesson:
    """Lesson data scraped from the overview page of the DW A1 course."""

    def __init__(
        self, sequence_id, lesson_id, title, link, subtitle=None, description=None
    ):
        self.sequence_id = sequence_id
        self.lesson_id = lesson_id
        self.title = title
        self.link = link
        self.subtitle = subtitle
        self.description = description

    def __str__(self):
        return f"Lesson {self.sequence_id} - {self.title}"


class VocabEntry:
    """Class to represent the vocabulary entry (phrases or verbs/adjectives/other)."""

    def __init__(self, entry, translation, lesson_id=0, e_type="misc"):
        self.entry = entry
        self.translation = translation
        self.lesson_id = lesson_id
        self.e_type = e_type

    def __str__(self):
        return self.entry


class Noun(VocabEntry):
    """Class to represent nouns, extends VocabEntry."""

    def __init__(self, entry, translation, article, plural, lesson_id=0):
        super().__init__(entry, translation, e_type="noun", lesson_id=lesson_id)
        self.article = article
        self.plural = plural
        self.full_noun = f"{article} {entry}"

    def __str__(self):
        return self.full_noun
