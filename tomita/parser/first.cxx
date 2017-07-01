#encoding "utf-8"    // сообщаем парсеру о том, в какой кодировке написана грамматика
#GRAMMAR_ROOT S      // указываем корневой нетерминал грамматики

// S -> Adj interp (Fact.Field1) Noun;

// S -> Adj interp (Fact.Field1) Noun;
// S -> AnyWord<wff='бактерии'>;
// S -> AnyWord<wff='<'> Word<wff='p'> AnyWord<wff='>'>;
// S -> AnyWord<wfl='<'> Word<wfl='p'> AnyWord<wfl='>'>;
// S -> AnyWord<wfl='<p'>;

html_p_open -> AnyWord<wff='HTML_P_OPEN'>;
html_p_close -> AnyWord<wff='HTML_P_CLOSE'>;

html_b_open -> AnyWord<wff='HTML_B_OPEN'>;
html_b_close -> AnyWord<wff='HTML_B_CLOSE'>;

LSBracket -> AnyWord<wff='SQUARE_BRACKET_OPEN'>;
RSBracket -> AnyWord<wff='SQUARE_BRACKET_CLOSE'>;

dash -> AnyWord<wff='—'>;


// язык
Lang -> AnyWord<kwtype="язык">;
Lang -> AnyWord<kwtype="язык"> Punct;

// предложение в скобках
SubSentence -> Word* Lang Word* Comma;
SubSentence -> Word* Lang Word*;

// Уточнение термина, т.е. то, что находится в скобках сразу после названия статьи
// Пример:  СПА (Spa) — бальнеологический курорт в Бельгии...

Clarification -> LBracket AnyWord* RBracket;
Clarification -> LSBracket AnyWord* RSBracket;


// Определение статьи, т.е все то, что находится после дефиса
ArticleDefinition -> Hyphen Noun interp (Article.FirstWord);


// Название статьи
ArticleName -> html_p_open html_b_open Word+ interp (Article.Name) html_b_close;

// Полное определение
S -> ArticleName Clarification ArticleDefinition;
S -> ArticleName ArticleDefinition;

// S -> Clarification;
