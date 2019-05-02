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

def start_select_language(btn):
    def after_close(cur_form):
        main.sub_forms.pop(-1)
        if cur_form.result > 0:
            main.do_loop()

    from select_language import SelectLanguageForm
    form = SelectLanguageForm(main.screen, after_close)
    form.prepare()
    main.sub_forms.append(form)
    form.show()

def do_click_quit(btn):
    pygame.quit()
    exit()

class Main():
    def __init__(self):
        LanguageLib.instance().reload_language()

        self.sub_forms = []

        pygame.init()
        addition_width = ADDITION_WIDTH
        space=SPACE
        main_block_size=MAIN_BLOCK_SIZE
        main_panel_width=main_block_size*COL_COUNT
        main_panel_height=main_block_size*ROW_COUNT

        self.form_width = main_panel_width+addition_width+space*3+200
        self.form_height = main_panel_height+space*2

        btn_num = 4
        btn_width = self.form_width * 0.7
        btn_height = 40
        btn_left = (self.form_width - btn_width) / 2
        btn_space = 20
        btn_y = self.form_height - (btn_height + btn_space) * btn_num

        self.screen = pygame.display.set_mode((self.form_width,self.form_height))

        self.btn_text_arr = ['single mode', 'battle mode', 'select language', 'exit']
        self.btn_group = BFButtonGroup()
        self.btn_group.make_button(self.screen, (btn_left, btn_y, btn_width, btn_height), click=start_single_game)
        self.btn_group.make_button(self.screen, (btn_left, btn_y + btn_height + btn_space, btn_width, btn_height), click=start_battle_game)
        self.btn_group.make_button(self.screen, (btn_left, btn_y + (btn_height + btn_space) * 2, btn_width, btn_height), click=start_select_language)
        self.btn_group.make_button(self.screen, (btn_left, btn_y + (btn_height + btn_space) * 3, btn_width, btn_height), click=do_click_quit)

        self.image = pygame.image.load('main.jpg') # 343 * 382
        image_height = btn_y - space * 2
        self.image_width = image_height * 343 / 382
        self.image = pygame.transform.scale(self.image, (self.image_width, image_height))

    def reset_display_text(self):
        caption = LanguageLib.instance().get_text('tetris')
        screencaption = pygame.display.set_caption(caption)
        for i in range(len(self.btn_group.btn_list)):
            if i >= len(self.btn_text_arr): break
            self.btn_group.btn_list[i].text = LanguageLib.instance().get_text(self.btn_text_arr[i])

    def do_loop(self):
        pygame.init()
        self.reset_display_text()
        self.screen = pygame.display.set_mode((self.form_width,self.form_height))
        self.btn_group.set_screen(self.screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if len(self.sub_forms) > 0:
                    for sub_form in self.sub_forms:
                        sub_form.update(event)
                else:
                    self.btn_group.update(event)

            if len(self.sub_forms) > 0:
                for sub_form in self.sub_forms:
                    sub_form.draw()
            else:
                self.screen.fill((100, 100, 100))  # make background gray

                self.screen.blit(self.image, ((self.form_width - self.image_width) / 2, SPACE))
                self.btn_group.draw()

            pygame.display.update()

main = Main()
main.do_loop()
