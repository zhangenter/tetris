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
    screencaption = pygame.display.set_caption(u'人机对战')
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

    battle_panel_width = 160
    battle_block_width = battle_panel_width / COL_COUNT
    battle_panel_height = battle_block_width * ROW_COUNT
    battle_panel_x = main_panel_width + space + space + (addition_width - battle_panel_width)
    battle_panel_y = main_panel_height + space - battle_panel_height
    battle_panel = Panel(screen, battle_block_width,
                         [battle_panel_x, battle_panel_y, battle_panel_width, battle_panel_height])
    battle_panel.hint_box = VirtualHintBox(1, block_manage)
    battle_panel.score_box = VirtualScoreBox(screen, [battle_panel_x, battle_panel_y - 16, addition_width, 16])
    battle_panel.create_move_block()

    diff_ticks = 300
    ticks = pygame.time.get_ticks() + diff_ticks

    player1 = HumanPlayer()
    # player1 = AIPlayer(ai_diff_ticks=100)
    player2 = AIPlayer(level=5)

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
                    if main_panel.get_attach_num() > 0: battle_panel.add_hinder()

        screen.fill((100, 100, 100))  # make background gray
        main_panel.paint()
        battle_panel.paint()

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
            player2.run(battle_panel)
        if game_state == 1 and pygame.time.get_ticks() >= ticks:
            ticks += diff_ticks
            if main_panel.move_block() == 9: game_state = 2  # gameover
            if main_panel.get_attach_num() > 0: battle_panel.add_hinder()
            if battle_panel.move_block() == 9: game_state = 3  # gameover
            if battle_panel.get_attach_num() > 0: main_panel.add_hinder()