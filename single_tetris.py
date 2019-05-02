# -*- coding=utf-8 -*-
import pygame
from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE
from globals import *
from block_manage import BlockManage
from controls import *
from players import *

def start_play():
    block_manage = BlockManage(2)  # two players
    pygame.init()
    addition_width = ADDITION_WIDTH
    space=SPACE
    main_block_size=MAIN_BLOCK_SIZE
    main_panel_width = main_block_size * COL_COUNT
    main_panel_height = main_block_size * ROW_COUNT
    screencaption = pygame.display.set_caption(u'单人游戏')
    screen = pygame.display.set_mode((main_panel_width + addition_width + space * 3, main_panel_height + space * 2))
    main_panel = Panel(screen, main_block_size, [space, space, main_panel_width, main_panel_height])
    hint_box = HintBox(screen, main_block_size,
                       [main_panel_width + space + space, space, addition_width, addition_width], block_manage)
    score_box = ScoreBox(screen, main_block_size,
                         [main_panel_width + space + space, addition_width + space * 2, addition_width, addition_width])

    main_panel.hint_box = hint_box
    main_panel.score_box = score_box

    pygame.key.set_repeat(200, 30)
    main_panel.create_move_block()

    diff_ticks = 300
    ticks = pygame.time.get_ticks() + diff_ticks

    player1 = HumanPlayer()

    pause = 0
    game_state = 1  # game status 1.normal 2.gameover
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return # back to menu

            if event.type == KEYDOWN:
                if event.key == 97: pause = 1 - pause  # press a to pause
                if event.key == 112:  # for debug where press p
                    main_panel.get_rect_matrix().print_matrix()
            if player1.auto_mode: continue
            if event.type == KEYDOWN:
                if event.key == K_LEFT: main_panel.control_block(-1, 0)
                if event.key == K_RIGHT: main_panel.control_block(1, 0)
                if event.key == K_UP: main_panel.change_block()
                if event.key == K_DOWN: main_panel.control_block(0, 1)
                if event.key == K_SPACE:
                    flag = main_panel.move_block()
                    while flag == 1:
                        flag = main_panel.move_block()
                    if flag == 9: game_state = 2

        screen.fill((100, 100, 100))  # make background gray
        main_panel.paint()

        if game_state == 2:
            myfont = pygame.font.Font(None, 30)
            white = 255, 255, 255
            textImage = myfont.render("Game over", True, white)
            screen.blit(textImage, (160, 190))
        if game_state == 3:
            myfont = pygame.font.Font(None, 30)
            white = 255, 255, 255
            textImage = myfont.render("Player1 win", True, white)
            screen.blit(textImage, (160, 190))

        pygame.display.update()

        if pause == 1: continue
        if game_state == 1:
            player1.run(main_panel)
        if game_state == 1 and pygame.time.get_ticks() >= ticks:
            ticks += diff_ticks
            if main_panel.move_block() == 9: game_state = 2  # gameover
