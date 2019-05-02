# -*- coding=utf-8 -*-
import pygame
from bf_form import BFForm
from bf_button import BFButton
from globals import LanguageConfigParser, LanguageLib

class SelectLanguageForm(BFForm):
    def __init__(self, screen, after_close):
        super(SelectLanguageForm, self).__init__(screen, after_close)

    def select_language(self, btn):
        lang_conf_parser = LanguageConfigParser()
        lang_conf_parser.set_cut_language(btn.tag)
        lang_conf_parser.save()
        LanguageLib.instance().reload_language()
        self.result = 1
        if self.after_close: self.after_close(self)

    def prepare(self):
        lang_conf_parser = LanguageConfigParser()

        supports = lang_conf_parser.get_support_names()
        num = len(supports)

        parent_width, parent_height = self.screen.get_size()

        self.desc = LanguageLib.instance().get_text('please select language')
        self.width = 400
        btn_width = self.width * 0.6
        btn_height = 40
        btn_top = 20
        btn_space = 20
        self.height = btn_top + 30 + num * btn_height + (num - 1) * btn_space + 30 + self.footer_height
        btn_left = (self.width - btn_width) / 2 + (parent_width-self.width) / 2
        btn_y = btn_top + 30 + (parent_height - self.height)/2
        for k in supports:
            label = lang_conf_parser.get_support_label(k)
            btn = BFButton(self.screen, (btn_left, btn_y, btn_width, btn_height), text=label.decode('utf-8'), click=self.select_language)
            btn.tag = k
            self.btn_group.add_button(btn)
            btn_y += btn_height + btn_space

        self.add_cancel_btn(parent_width, parent_height)



