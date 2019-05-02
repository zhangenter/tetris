# -*- coding=utf-8 -*-
from globals import *
import pygame

class Player(object):
    auto_mode= False
    def __init__(self):
        pass

    def run(self, panel):
        pass

class HumanPlayer(Player):
    def __init__(self):
        super(Player, self).__init__()

class AIPlayer(Player):
    cal_block_id = -1
    ctl_arr = []  # control arr, 1��change��2��left��3��right��4��down
    auto_mode = True
    ai_diff_ticks = 100  # timespan between two controls
    level = None

    def __init__(self, level=None, ai_diff_ticks=100):
        super(Player, self).__init__()
        self.ai_diff_ticks = ai_diff_ticks
        self.level = level
        if level is not None:
            level = int(level)
            if level < 1: level = 1
            if level > 10: level = 10
            self.ai_diff_ticks = 1000 / level

        self.ctl_ticks = pygame.time.get_ticks() + self.ai_diff_ticks

    def get_cost_of_emptycol(self, empty_arr):
        cost = 0
        for l, r in empty_arr:
            if l > 2 and r > 2:
                cost += (l + r) * 2
            elif l > 2:
                cost += l
            else:
                cost += r
        return cost

    def cal_best_arr(self, panel):
        matrix = panel.get_rect_matrix()
        cur_shape_id = panel.moving_block.shape_id
        shape_num = panel.moving_block.shape_num
        max_score = -10000
        best_arr = []
        for i in range(shape_num):
            tmp_shape_id = cur_shape_id + i
            if tmp_shape_id >= shape_num: tmp_shape_id = tmp_shape_id % shape_num
            tmp_shape = panel.moving_block.get_shape(sid=tmp_shape_id)
            center_shape = []
            for x, y in tmp_shape: center_shape.append((x + COL_COUNT / 2 - 2, y - 2))
            minx = COL_COUNT
            maxx = 0
            miny = ROW_COUNT
            maxy = -2
            for x, y in center_shape:
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y

            for xdiff in range(-minx, COL_COUNT - maxx):
                arr = [1 for _ in range(i)]
                if xdiff < 0: [arr.append(2) for _ in range(-xdiff)]
                if xdiff > 0: [arr.append(3) for _ in range(xdiff)]

                max_yindex = -miny
                for yindex in range(-miny, ROW_COUNT - maxy):
                    if matrix.cross_block(center_shape, xdiff=xdiff, ydiff=yindex):
                        break
                    max_yindex = yindex
                score = sum([y + max_yindex for x, y in center_shape])

                # clone matrix and fill new block to calculate holes
                clone_matrix = matrix.clone()
                clone_matrix.fill_block(center_shape, xdiff=xdiff, ydiff=max_yindex)
                clear_num = clone_matrix.do_clear()
                score -= clone_matrix.get_block_above_hole()
                empty_arr = clone_matrix.get_empty_col()
                score -= self.get_cost_of_emptycol(empty_arr)
                score += clear_num * 5
                score -= clone_matrix.get_hole_number() * COL_COUNT

                if score > max_score:
                    max_score = score
                    best_arr = arr
        self.ctl_arr = best_arr + [4]

    def run(self, panel):
        if pygame.time.get_ticks() < self.ctl_ticks: return
        self.ctl_ticks += self.ai_diff_ticks
        if panel.block_id == self.cal_block_id:  # block_id not change
            if len(self.ctl_arr) > 0:
                ctl = self.ctl_arr.pop(0)
                if ctl == 1: panel.change_block()
                if ctl == 2: panel.control_block(-1, 0)
                if ctl == 3: panel.control_block(1, 0)
                if ctl == 4:
                    flag = panel.move_block()
                    while flag == 1:
                        flag = panel.move_block()

        else:  # block_id is new
            self.cal_block_id = panel.block_id
            self.cal_best_arr(panel)
