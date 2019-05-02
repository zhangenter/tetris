# -*- coding=utf-8 -*-

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
