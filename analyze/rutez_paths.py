# encoding: utf-8
import db
from rutez.rutez import Rutez


def rutez_paths():
    """Добавляем иерархию рутеза в статьи
    """
    tez = Rutez()
    used_sinsets = set()
    for article in db.Article.objects.all()[:100]:
        word = article.title.upper()
        if word in tez.word2sinsets:
            for sinset in tez.word2sinsets[word]:
                # print(word, '|', sinset, '|', tez.upper_sinsets(sinset))
                article.rutez_path[sinset] = tez.upper_sinsets(sinset)
                used_sinsets.add(article.rutez_path[word][0])

            article.save()

    print(used_sinsets)
