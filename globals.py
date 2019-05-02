# -*- coding=utf-8 -*-
import sys
import threading
from ConfigParser import ConfigParser
import platform
import pygame
reload(sys)
sys.setdefaultencoding('utf-8')

LANGUAGE_CONF_FILE = 'language.conf'

OS_SYS_STR = platform.system()

ROW_COUNT=20
COL_COUNT=10
SCORE_MAP=(100,300,800,1600)

ADDITION_WIDTH = 160
SPACE = 30
MAIN_BLOCK_SIZE = 30

class RectInfo(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

def get_user_font(font_size):
    return pygame.font.Font(u'syht.otf', font_size)

class LanguageConfigParser(object):
    def __init__(self):
        self.conf = ConfigParser()
        self.conf.read(LANGUAGE_CONF_FILE)

    def get_support_names(self):
        return self.conf.options('supports')

    def get_support_label(self, name):
        return self.conf.get('supports', name)

    def get_cut_language(self):
        return self.conf.get('common', 'default')

    def set_cut_language(self, name):
        self.conf.set('common', 'default', name)

    def get_words(self, language):
        words = self.conf.options(language)
        dic = {}
        for word in words:
            dic[word] = self.conf.get(language, word).decode('utf-8')
        return dic

    def save(self):
        self.conf.write(open(LANGUAGE_CONF_FILE, 'w+'))


class LanguageLib(object):
    _instance_lock = threading.Lock()
    def __init__(self):
        self.dic={}

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(LanguageLib, "_instance"):
            LanguageLib._instance = LanguageLib(*args, **kwargs)
        return LanguageLib._instance

    def reload_language(self):
        lang_conf_parser = LanguageConfigParser()
        cur_lang = lang_conf_parser.get_cut_language()
        self.dic = lang_conf_parser.get_words(cur_lang)

    def get_text(self, str):
        return self.dic.get(str, str)