import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def normal_form(word):
    return morph.parse(word)[0].normal_form
