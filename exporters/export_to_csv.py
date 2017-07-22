import os
import db
import csv
from tools.file_system import ensure_directory

def _export_articles():
    with open(os.path.join(ensure_directory('../data/csv'), 'articles.csv'),
              'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                            #fieldnames=['article'],
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['article'])
        for article in db.Article.objects.all():
            writer.writerow([article.title])

def _export_links():
    with open(os.path.join(ensure_directory('../data/csv'), 'links.csv'),
              'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                            #fieldnames=['article1', 'link', 'article2'],
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # writer.writeheader()
        writer.writerow(['article1', 'link', 'article2'])
        for article in db.Article.objects.all():
            for link in article['links']:
                to_article = db.Article.objects.get(id=link)
                writer.writerow([article.title, 'см.', to_article.title])

def export_to_csv():
    _export_articles()
    _export_links()
