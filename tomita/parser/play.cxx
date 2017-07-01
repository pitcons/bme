#encoding "utf-8"    // сообщаем парсеру о том, в какой кодировке написана грамматика
#GRAMMAR_ROOT S      // указываем корневой нетерминал грамматики

// Семейство-Род
FamilyGenus -> "род" Word interp (FamilyGenus.Genus) Comma "сем." Word interp (FamilyGenus.Family);

S -> FamilyGenus;
