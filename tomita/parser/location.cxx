#encoding "utf-8"    // сообщаем парсеру о том, в какой кодировке написана грамматика
#GRAMMAR_ROOT S      // указываем корневой нетерминал грамматики


// расположен   в   Арденнах   ,   в   долине   р.   Воэ   ,   в   провинции   Льеж   .

S-> "расположить" "в" Word Comma "в";
