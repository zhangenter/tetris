# -*- coding=utf-8 -*-
import threading
import pygame
from pygame.locals import MOUSEBUTTONDOWN
from globals import get_user_font

class BFControlId(object):
    _instance_lock = threading.Lock()
    def __init__(self):
        self.id = 1

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(BFControlId, "_instance"):
            BFControlId._instance = BFControlId(*args, **kwargs)
        return BFControlId._instance

    def get_new_id(self):
        self.id += 1
        return self.id

    @property
    def click_id(self):
        return self._click_id

    @click_id.setter
    def click_id(self, value):
        self._click_id = value

CLICK_EFFECT_TIME = 100
class BFButton(object):
    def __init__(self, parent, rect, text='Button', click=None):
        self.x,self.y,self.width,self.height = rect
        self.bg_color = (225,225,225)
        self.parent = parent
        self.surface = parent.subsurface(rect)
        self.is_hover = False
        self.in_click = False
        self.click_loss_time = 0
        self.click_event_id = -1
        self.ctl_id = BFControlId().instance().get_new_id()
        self._text = text
        self._click = click
        self._visible = True
        self.tag = None
        self._font_size = 28
        self.init_font()

    def init_font(self):
        #font = pygame.font.SysFont('SimHei', 28)
        font = get_user_font(self._font_size)
        white = 100, 100, 100
        self.textImage = font.render(self._text, True, white)
        w, h = self.textImage.get_size()
        self._tx = (self.width - w) / 2
        self._ty = (self.height - h) / 2

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.init_font()

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self._font_size = value
        self.init_font()

    @property
    def click(self):
        return self._click

    @click.setter
    def click(self, value):
        self._click = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    def update(self, event):
        if self.in_click and event.type == self.click_event_id and BFControlId().instance().click_id == self.ctl_id:
            self.in_click = False
            if self._click: self._click(self)
            self.click_event_id = -1
            return

        x, y = pygame.mouse.get_pos()
        if x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height:
            self.is_hover = True
            if event.type == MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                if pressed_array[0]:
                    self.in_click = True
                    self.click_loss_time = pygame.time.get_ticks() + CLICK_EFFECT_TIME
                    self.click_event_id = pygame.USEREVENT+1
                    BFControlId().instance().click_id = self.ctl_id
                    pygame.time.set_timer(self.click_event_id,CLICK_EFFECT_TIME-10)
        else:
            self.is_hover = False

    def draw(self):
        if self.in_click:
            if self.click_loss_time < pygame.time.get_ticks():
                self.in_click = False
        if not self._visible:
            return
        if self.in_click:
            r,g,b = self.bg_color
            k = 0.95
            self.surface.fill((r*k, g*k, b*k))
        else:
            self.surface.fill(self.bg_color)
        if self.is_hover:
            pygame.draw.rect(self.surface, (0,0,0), (0,0,self.width,self.height), 1)
            pygame.draw.rect(self.surface, (100,100,100), (0,0,self.width-1,self.height-1), 1)
            layers = 5
            r_step = (210-170)/layers
            g_step = (225-205)/layers
            for i in range(layers):
                pygame.draw.rect(self.surface, (170+r_step*i, 205+g_step*i, 255), (i, i, self.width - 2 - i*2, self.height - 2 - i*2), 1)
        else:
            self.surface.fill(self.bg_color)
            pygame.draw.rect(self.surface, (0,0,0), (0,0,self.width,self.height), 1)
            pygame.draw.rect(self.surface, (100,100,100), (0,0,self.width-1,self.height-1), 1)
            pygame.draw.rect(self.surface, self.bg_color, (0,0,self.width-2,self.height-2), 1)

        self.surface.blit(self.textImage, (self._tx, self._ty))

class BFButtonGroup(object):
    def __init__(self):
        self.btn_list = []

    def add_button(self, button):
        self.btn_list.append(button)

    def make_button(self, screen, rect, text='Button', click=None):
        button = BFButton(screen, rect,text=text,click=click)
        self.add_button(button)

    def set_screen(self, screen):
        for button in self.btn_list: button.parent = screen

    def update(self, event):
        for button in self.btn_list: button.update(event)

    def draw(self):
        for button in self.btn_list: button.draw()
