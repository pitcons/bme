import re
import db
from tools.morphology import normal_form
from mongoengine import DoesNotExist, MultipleObjectsReturned

# см. <a href="/index.php/%D0%91%D0%98%D0%9E%D0%9B%D0%9E%D0%93%D0%98%D0%A7%D0%95%D0%A1%D0%9A%D0%98%D0%95_%D0%A0%D0%98%D0%A2%D0%9C%D0%AB" title="БИОЛОГИЧЕСКИЕ РИТМЫ">Биологические ритмы</a>
LINK_TO_1 = r'см\. <a href="[^"]+" title="(?P<title1>[^"]+)"[^>]*>(?P<text1>[^<]*)</a>'

# <a href="/index.php/%D0%91%D0%98%D0%9E%D0%A6%D0%95%D0%9D%D0%9E%D0%97" title="БИОЦЕНОЗ">биоценоза</a> (см.)
# <a href="/index.php/%D0%A1%D0%A3%D0%A1%D0%9F%D0%95%D0%9D%D0%97%D0%9E%D0%A0%D0%98%D0%99" title="СУСПЕНЗОРИЙ">суспензорий</a> (см.)
LINK_TO_2 = r'<a href="[^"]+" title="(?P<title2>[^"]+)"[^>]*>(?P<text2>[^<]*)</a> \(см\.\)'

# (см. Мембраны биологические)
LINK_TO_3 = r'\(см\. (?P<title3>[^\)]+)\)'

LINK_TO = LINK_TO_1  + r'|' + LINK_TO_2 + r'|' + LINK_TO_3
LINK_TO_RE = re.compile(LINK_TO)


def findall(what, where):
    pos = -1
    result = set()
    while True:
        pos = where.find(what, pos + 1)
        if pos == -1:
            return result

        result.add(pos)

def find_in_match(what, m, text):
    start, end = m.start(), m.end()
    mpos = text[start:end].find(what)
    return start + mpos

def get_first_not_none(group_dict, keys):
    for k in keys:
        if group_dict[k] is not None:
            return group_dict[k]

def extract_links(debug_miss=True):
    """Извлечение всех ссылок из одних статей на другие
    """
    articles = db.Article.objects.filter(first_sentence__contains='см.')
    i = 0
    for article in articles:
        text = article.raw
        article.links = []
        founded = findall('см.', text)

        for m in LINK_TO_RE.finditer(text):
            mpos = find_in_match('см.', m, text)
            founded.remove(mpos)

            title = get_first_not_none(m.groupdict(), ('title1', 'title2', 'title3'))
            try:
                link_obj = db.Article.objects.get(title=title.upper())
                article.links.append(link_obj.id)
            except DoesNotExist:
                pass
                # print('does not exists', title)

        if debug_miss:
            for pos in founded:
                # выбираем места, которые не соотвествую регулярному выражению
                # и пытаемся их найти в базе
                text_frame = text[pos-120:pos-1]
                text_frame = text_frame.replace('-', '')  # TODO

                words = [normal_form(w)
                         for w in text_frame.split(" ") if w]
                link_obj = None
                for last in reversed(range(len(words))):
                    try:
                        try_title = ' '.join(words[-last:])
                        # if 'тромбоэластогра' in text_frame:
                        #     print("try_title", try_title)
                        link_obj = db.Article.objects.get(normalized_title=try_title)
                        article.links.append(link_obj.id)
                        continue
                    except MultipleObjectsReturned:
                        pass
                    except DoesNotExist:
                        pass

                if not link_obj:
                    # так и не получилось найти
                    # print("NOT FOUND---BEGIN")
                    print(article.title)
                    print("NOT FOUND", pos, text[pos-40:pos+40])
                    # print("NOT FOUND---END")

        article.save()
        i += 1
        if i % 100 == 0:
            print(i)
