import re
import db
from rutez.rutez import Rutez
from tools.morphology import normal_form

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

PERSONS = [
    'холдин семен абрамович',
    'чечулин сергей ионович',
    'шамсиев сайфи шамсиевич',
    'черномордик соломон исаевич',
    'де кастро жозуэ',
    'барсуков михаил иванович',
    'юдин тихон иванович',
    'аркевич дмитрий александрович',
    'фролов иван тимофеевич',
    'турчинович-выжникевич владислав иванович',
    'харкевич дмитрий александрович',
    'зайко николай никифорович',
    'николаев владимир васильевич',
]
PROFESSIONS = [
    'физикохимик', 'паразитолог', 'анатом', 'врач', 'анестезиолог', 'биофизик',
    'радиотоксиколог', 'протозоолог', 'хирург', 'военный', 'патофизиолог',
    'естествоиспытатель', 'гигиенист', 'невропа', 'ортопед-травматолог',
    'кардиолог', 'инфекционист', 'художник', 'микробиолог', 'гистолог',
    'терапевт', 'педиатр', 'биохимик', 'акушер', 'химик', 'вирусолог',
    'дерматолог', 'бактериолог', 'зоолог', 'физик', 'клиницист-терапевт',
    'физиолог', 'психиатр', 'ученый-энциклопедист', 'патолог', 'фармаколог',
    'организатор здравоохранения', 'эмбриолог', 'ботаник', 'патологоанатом',
    'санитарный врач', 'судебный медик', 'ученый и врач', 'ученый-физиолог',
    'эпидемиолог', 'иммуногематолог', 'гематолог',
]
NATIONS = [
    'первый русский',
    'русский, советский', 'сербский', 'болгарский', 'австрийский', 'китайский',
    'советский', 'отечественный', 'голландский', 'русский', 'чешский',
    'английский', 'немецкий', 'голландский', 'американский',
    'французский', 'итальянский', 'финский', 'бельгийский',
    'датский', 'бразильский', 'шведский', 'румынский',
]
PROFESSIONS_ANCHORS = [
    f'— {nation} {profession}'
    for nation in NATIONS
    for profession in PROFESSIONS
] + [
    'врач-гигиенист',
    'организатор советской военной медицины',
] + [f'— {profession}' for profession in PROFESSIONS]

IGNORED_TITLES = [
    'верднига-гоффманна спинальная амиотрофия',
    'сент-винсент и гренадины',
    'дерматофиброз лентикулярный диссеминированный',
    'идиопатический гемосидероз лёгких',
    'accessorius nervus willisii',
    'вишневского линимент бальзамический',
    'экономо летаргический энцефалит',
    'риттера дерматит эксфолиативный',
    'иванова-гаусса кожноголовные щипцы',
    'situs viscerum inversus',
    'эритема экссудативная многоформная',
    'locus minoris resistentiae',
    'сан-томе и принсипи',
    'дюбрея меланоз предраковый',
    'дежерина-сотта гипертрофический неврит',
    'всё или ничего',
    'дюшенна псевдогипертрофическая миопатия',
    'carotis communis arteria',
    'induratio penis plastica',
    'carcinoma in situ',
    'катетеризация вен пункционная',
    'гемосидероз лёгких идиопатический',
    'мортоновская метатарзальная невралгия',

    'фабрично-заводская медицина',
    'медицина в россии в 18 веке',
]

def _emit_person(article):
    article.category = 'person'
    article.save()

def extract_persons():
    """Извлечение статей описывающих людей
    """
    tez = Rutez()

    for article in db.Article.objects.all():
        title = article.title.strip().lower()
        parts = title.split(' ')

        if title in IGNORED_TITLES:
            continue

        if title in PERSONS:
            _emit_person(article)
        elif any(anchor in article.first_sentence
                 for anchor in PROFESSIONS_ANCHORS):
            _emit_person(article)
        else:
            m = PERSON_MATCH_RE.match(article.first_sentence)
            if m:
                _emit_person(article)
                # if len(parts) == 3:
                #     words = [normal_form(p) for p in parts]
                #     sinsets = [tez.word2sinsets.get(w.upper()) for w in words]
                #     if any(sinsets):
                #         print(title)
                #         print(article.first_sentence)

        # if len(parts) == 3 and title not in IGNORED_TITLES:
        #     m = PERSON_MATCH_RE.match(article.first_sentence)
        #     if not m and not any(anchor in article.first_sentence
        #                          for anchor in PROFESSIONS_ANCHORS):
        #
        #         words = [normal_form(p) for p in parts]
        #         sinsets = [tez.word2sinsets.get(w.upper()) for w in words]
        #
        #         # print(title)
        #         # print(article.first_sentence)
        #
        #         # if not any(sinsets):
        #         #     print(title)
        #             # print(article.first_sentence)
