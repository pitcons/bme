# -*- encoding: utf-8 -*-
import os
from config import config
from subprocess import check_output


class TomitaWrap(object):

    def run(self, text):
        with open('tomita/prosecutor/test.txt', 'w') as f:
            f.write(text.encode('utf-8'))

        out = check_output(
            [config.tomita_path, 'config.proto'],
            cwd='tomita/prosecutor/'
        )
        #print out
