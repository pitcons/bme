# encoding: utf-8
import db


def dump_as_html(self):
    for article in db.Article.objects.all():
        path = os.path.join(config.data_path, 'dump.html')
        with open(path, 'w') as f:
            pass
