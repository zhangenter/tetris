# -*- coding=utf-8 -*-
import random
import os,pickle
import pygame
from globals import *
from matrix import Matrix

class VirtualHintBox(object):
    pid = 0
    block_manage=None
    next_block= None
    def __init__(self, pid, block_manage):
        #print pid
        self.pid = pid
        self.block_manage = block_manage

    def take_block(self):
        block = self.next_block
        if block is None:  # make first block
            block = self.block_manage.get_block(self.pid)

        self.next_block = self.block_manage.get_block(self.pid)
        return block

    def paint(self):
        pass


class HintBox(VirtualHintBox):
    def __init__(self, bg, block_size, position, block_manage):
        super(VirtualHintBox, self).__init__()
        self._bg = bg;
        self._x, self._y, self._width, self._height = position
        self._block_size = block_size
        self._bgcolor = [0, 0, 0]
        self.block_manage = block_manage

    def paint(self):
        mid_x = self._x + self._width / 2
        pygame.draw.line(self._bg, self._bgcolor, [mid_x, self._y], [mid_x, self._y + self._height], self._width)
        bz = self._block_size

        if self.next_block:
            arr = self.next_block.get_rect_arr()
            minx, miny = arr[0]
            maxx, maxy = arr[0]
            for x, y in arr:
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
            w = (maxx - minx) * bz
            h = (maxy - miny) * bz

            cx = self._width / 2 - w / 2 - minx * bz - bz / 2
            cy = self._height / 2 - h / 2 - miny * bz - bz / 2

            for rect in arr:
                x, y = rect
                pygame.draw.line(self._bg, self.next_block.color,
                                 [self._x + x * bz + cx + bz / 2, self._y + cy + y * bz],
                                 [self._x + x * bz + cx + bz / 2, self._y + cy + (y + 1) * bz], bz)
                pygame.draw.rect(self._bg, [255, 255, 255],
                                 [self._x + x * bz + cx, self._y + y * bz + cy, bz + 1, bz + 1], 1)


class ScoreBox(object):
    total_score = 0
    high_score = 0
    db_file = 'tetris.db'

    def __init__(self, bg, block_size, position):
        self._bg = bg;
        self._x, self._y, self._width, self._height = position
        self._block_size = block_size
        self._bgcolor = [0, 0, 0]

        if os.path.exists(self.db_file): self.high_score = pickle.load(open(self.db_file, 'rb'))

    def paint(self):
        myfont = pygame.font.Font(None, 36)
        white = 255, 255, 255
        textImage = myfont.render('High: %06d' % (self.high_score), True, white)
        self._bg.blit(textImage, (self._x, self._y - 10))
        textImage = myfont.render('Score:%06d' % (self.total_score), True, white)
        self._bg.blit(textImage, (self._x, self._y + 20))

    def add_score(self, score):
        self.total_score += score
        if self.total_score > self.high_score:
            self.high_score = self.total_score
            pickle.dump(self.high_score, open(self.db_file, 'wb+'))


class VirtualScoreBox(object):
    total_score = 0

    def __init__(self, bg, position):
        self._bg = bg;
        self._x, self._y, self._width, self._height = position
        self._bgcolor = [0, 0, 0]

    def paint(self):
        myfont = pygame.font.Font(None, 22)
        white = 255, 255, 255
        textImage = myfont.render('Player2 Score:%06d' % (self.total_score), True, white)
        self._bg.blit(textImage, (self._x, self._y))

    def add_score(self, score):
        self.total_score += score


class Panel(object):
    attack_num = 0
    block_id = 0
    rect_arr = []
    moving_block = None
    hint_box = None
    score_box = None

    def __init__(self, bg, block_size, position):
        self._bg = bg;
        self._x, self._y, self._width, self._height = position
        self._block_size = block_size
        self._bgcolor = [0, 0, 0]
        self.block_id = 0
        self.rect_arr = []
        self.moving_block = None

    def get_rect_matrix(self):
        matrix = Matrix(ROW_COUNT, COL_COUNT)
        for rect_info in self.rect_arr:
            matrix.set_val(rect_info.x, rect_info.y, 1)
        return matrix

    def add_block(self, block):
        #print block.get_rect_arr()
        for x, y in block.get_rect_arr():
            self.rect_arr.append(RectInfo(x, y, block.color))
        #print len(self.rect_arr)

    def create_move_block(self):
        self.block_id += 1
        block = self.hint_box.take_block()
        # block = create_block()
        block.move(COL_COUNT / 2 - 2, -2)  # move block to top center
        self.moving_block = block

    def check_overlap(self, diffx, diffy, check_arr=None):
        if check_arr is None: check_arr = self.moving_block.get_rect_arr()
        for x, y in check_arr:
            for rect_info in self.rect_arr:
                if x + diffx == rect_info.x and y + diffy == rect_info.y:
                    return True
        return False

    def control_block(self, diffx, diffy):
        if self.moving_block.can_move(diffx, diffy) and not self.check_overlap(diffx, diffy):
            self.moving_block.move(diffx, diffy)

    def change_block(self):
        if self.moving_block:
            new_arr = self.moving_block.change()
            if new_arr and not self.check_overlap(0, 0, check_arr=new_arr):
                self.moving_block.rect_arr = new_arr

    def move_block(self):
        if self.moving_block is None: self.create_move_block()
        if self.moving_block.can_move(0, 1) and not self.check_overlap(0, 1):
            self.moving_block.move(0, 1)
            return 1
        else:
            self.add_block(self.moving_block)
            self.check_clear()

            for rect_info in self.rect_arr:
                if rect_info.y < 0: return 9  # gameover
            self.create_move_block()
            return 2

    def check_clear(self):
        tmp_arr = [[] for i in range(20)]

        for rect_info in self.rect_arr:
            if rect_info.y < 0: return
            tmp_arr[rect_info.y].append(rect_info)

        clear_num = 0
        clear_lines = set([])
        y_clear_diff_arr = [[] for i in range(20)]

        for y in range(19, -1, -1):
            if len(tmp_arr[y]) == 10:
                clear_lines.add(y)
                clear_num += 1
            y_clear_diff_arr[y] = clear_num

        if clear_num > 0:
            new_arr = []

            for y in range(19, -1, -1):
                if y in clear_lines: continue
                tmp_row = tmp_arr[y]
                y_clear_diff = y_clear_diff_arr[y]
                for rect_info in tmp_row:
                    # new_arr.append([x,y+y_clear_diff])
                    new_arr.append(RectInfo(rect_info.x, rect_info.y + y_clear_diff, rect_info.color))

            self.rect_arr = new_arr
            score = SCORE_MAP[clear_num - 1]
            self.score_box.add_score(score)

    def get_attach_num(self):
        if self.score_box.total_score / 1000 > self.attack_num:
            self.attack_num += 1
            return 1
        else:
            return 0

    def add_hinder(self):
        hinder_lines = 2
        for tmp in self.rect_arr:
            tmp.y -= hinder_lines
        for y in range(hinder_lines):
            arr = range(10)
            for i in range(5):
                n = random.randint(0, len(arr) - 1)
                arr.pop(n)
            for x in arr:
                self.rect_arr.append(RectInfo(x, 19 - y, [0, 0, 255]))

    def paint(self):
        mid_x = self._x + self._width / 2
        pygame.draw.line(self._bg, self._bgcolor, [mid_x, self._y], [mid_x, self._y + self._height],
                         self._width)  # ��һ�����߶�����䱳��

        bz = self._block_size
        for rect_info in self.rect_arr:
            x = rect_info.x
            y = rect_info.y
            pygame.draw.line(self._bg, rect_info.color, [self._x + x * bz + bz / 2, self._y + y * bz],
                             [self._x + x * bz + bz / 2, self._y + (y + 1) * bz], bz)
            pygame.draw.rect(self._bg, [255, 255, 255], [self._x + x * bz, self._y + y * bz, bz + 1, bz + 1], 1)

        if self.moving_block:
            for rect in self.moving_block.get_rect_arr():
                x, y = rect
                pygame.draw.line(self._bg, self.moving_block.color, [self._x + x * bz + bz / 2, self._y + y * bz],
                                 [self._x + x * bz + bz / 2, self._y + (y + 1) * bz], bz)
                pygame.draw.rect(self._bg, [255, 255, 255], [self._x + x * bz, self._y + y * bz, bz + 1, bz + 1], 1)

        self.score_box.paint()
        self.hint_box.paint()