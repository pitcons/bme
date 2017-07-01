import re
import db

YEAR_RANGE = r'([0-9]{4}\s*[—-]\s*[0-9]{4})'
ONE_YEAR = r'(род\.|родился) в [0-9]{4} (г\.?|году)'
NAME_MATCH = (
    r'<p>(<b>)?[^<]*(</b>)?\s+' +  # Название статьи
    r'\((' + r'((\w*\s?){0,5},)?' + 
           YEAR_RANGE + r'|' +
           ONE_YEAR +
    r')\)'
)
PERSON_MATCH_RE = re.compile(NAME_MATCH)


def extract_persons():
    """Извлечение статей описывающих людей
    """
    for article in db.Article.objects.all()[:1000]:
        title = article.title.strip().lower()
        parts = title.split(' ')
        if len(parts) == 3:
            m = PERSON_MATCH_RE.match(article.first_sentence)
            if not m:
                print(title)
                print(article.first_sentence)
