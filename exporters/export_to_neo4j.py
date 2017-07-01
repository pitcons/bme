import ssl

import neo4j
from neo4j.v1 import GraphDatabase, basic_auth

import db


def export_to_neo4j():
    driver = GraphDatabase.driver("bolt://localhost:7687",
                                  encrypted=False,
                                  auth=basic_auth("neo4j", "asdzxc"))
    session = driver.session()

    for article in db.Article.objects.all():
        if article['links']:
            # session.run("CREATE (a:Article {name: {name}})",
            #             {"name": article['title']})

            for link in article['links']:
                to_article = db.Article.objects.get(id=link)
                print(to_article['title'])
                session.run("CREATE (a:Article {name: {name}})",
                            {"name": article['title']})

    #
    # result = session.run("MATCH (a:Person) WHERE a.name = {name} "
    #                    "RETURN a.name AS name, a.title AS title",
    #                    {"name": "Arthur"})
    # for record in result:
    #     print("%s %s" % (record["title"], record["name"]))
    #
    session.close()
