import db
from tools.morphology import normal_form


def fill_norm_title():
    for article in db.Article.objects.all():
        article.normalized_title = ' '.join(
            [normal_form(w) for w in article.title.split(' ')]
        )
        article.save()
