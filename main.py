# -*- coding=utf-8 -*-
import pygame
from globals import *
from bf_button import BFButtonGroup

def start_single_game(btn):
    from single_tetris import start_play
    start_play()
    main.do_loop()

def start_battle_game(btn):
    from battle_tetris import start_play
    start_play()
    main.do_loop()

def do_click_quit(btn):
    pygame.quit()
    exit()

class Main():
    def __init__(self):
        pygame.init()
        addition_width = ADDITION_WIDTH
        space=SPACE
        main_block_size=MAIN_BLOCK_SIZE
        main_panel_width=main_block_size*COL_COUNT
        main_panel_height=main_block_size*ROW_COUNT

        self.form_width = main_panel_width+addition_width+space*3+200
        self.form_height = main_panel_height+space*2

        btn_num = 3
        btn_width = self.form_width * 0.7
        btn_height = 40
        btn_left = (self.form_width - btn_width) / 2
        btn_space = 20
        btn_y = self.form_height - (btn_height + btn_space) * btn_num

        self.screen = pygame.display.set_mode((self.form_width,self.form_height))

        self.btn_group = BFButtonGroup()
        self.btn_group.make_button(self.screen, (btn_left, btn_y, btn_width, btn_height), text=u'单人游戏', click=start_single_game)
        self.btn_group.make_button(self.screen, (btn_left, btn_y + btn_height + btn_space, btn_width, btn_height), text=u'人机对战', click=start_battle_game)
        self.btn_group.make_button(self.screen, (btn_left, btn_y + (btn_height + btn_space) * 2, btn_width, btn_height), text=u'退出', click=do_click_quit)

        self.image = pygame.image.load('main.jpg') # 343 * 382
        image_height = btn_y - space * 2
        self.image_width = image_height * 343 / 382
        self.image = pygame.transform.scale(self.image, (self.image_width, image_height))

    def do_loop(self):
        pygame.init()
        screencaption = pygame.display.set_caption(u'俄罗斯方块')
        self.screen = pygame.display.set_mode((self.form_width,self.form_height))
        self.btn_group.set_screen(self.screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.btn_group.update(event)

            self.screen.fill((100, 100, 100))  # make background gray

            self.screen.blit(self.image, ((self.form_width - self.image_width) / 2, SPACE))
            self.btn_group.draw()

            pygame.display.update()

main = Main()
main.do_loop()
