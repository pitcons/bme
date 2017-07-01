#encoding "utf-8"    // сообщаем парсеру о том, в какой кодировке написана грамматика
#GRAMMAR_ROOT S      // указываем корневой нетерминал грамматики

HtmlLink -> "title" "=" Word interp (LinkToArticle.Name) ">" Word* "<" "/" "a" ">";

// Смотри
LinkToArticle -> HtmlLink LBracket "см." RBracket;

S -> LinkToArticle;
