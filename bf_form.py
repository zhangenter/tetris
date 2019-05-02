# -*- coding=utf-8 -*-
import pygame
from bf_button import BFButtonGroup,BFButton
from globals import get_user_font,LanguageLib

class BFForm(object):
    def __init__(self, screen, after_close):
        self.width = 400
        self.height = 300
        self.text = 'bf_form'
        self.result = -1
        self.is_close = False
        self.btn_group = BFButtonGroup()
        self.screen = screen
        self.after_close = after_close
        self.footer_height = 100
        self.is_visible = False
        self._desc = ''
        self.init_desc_font()

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value
        self.init_desc_font()

    def init_desc_font(self):
        font = get_user_font(18)
        white = 255, 255, 255
        self.textImage = font.render(self._desc, True, white)

    def do_cancel(self, btn):
        self.result = 0
        if self.after_close:
            self.after_close(self)

    def add_cancel_btn(self, parent_width, parent_height):
        cancel_btn_width = 100
        cancel_btn_height = 40
        cancel_btn_x = (parent_width - self.width) / 2 + self.width - cancel_btn_width - 20
        cancel_btn_y = (parent_height - self.height) / 2 + self.height - cancel_btn_height - 20
        btn = BFButton(self.screen, (cancel_btn_x, cancel_btn_y, cancel_btn_width, cancel_btn_height), text=LanguageLib.instance().get_text('cancel'), click=self.do_cancel)
        btn.font_size = 18
        self.btn_group.add_button(btn)

    def show(self):
        parent_width, parent_height = self.screen.get_size()
        self._x = (parent_width - self.width) / 2
        self._y = (parent_height - self.height) / 2
        self.is_visible = True

    def update(self, event):
        if not self.is_visible: return

        self.btn_group.update(event)

    def draw(self):
        if not self.is_visible: return

        self.screen.fill((100, 100, 100))  # make background gray

        self.screen.blit(self.textImage, (self._x + 10, self._y + 10))

        pygame.draw.rect(self.screen, [255, 255, 255],
                                 [self._x, self._y, self.width, self.height], 1)
        self.btn_group.draw()

