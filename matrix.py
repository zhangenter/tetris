# -*- coding=utf-8 -*-

class Matrix(object):
    rows = 0
    cols = 0
    data = []

    def __init__(self, rows, cols, data=None):
        self.rows = rows
        self.cols = cols
        if data is None: data = [0 for i in range(rows * cols)]
        self.data = data

    def set_val(self, x, y, val):
        self.data[y * self.cols + x] = val

    def get_val(self, x, y):
        return self.data[y * self.cols + x]

    def cross_block(self, rect_arr, xdiff=0, ydiff=0):
        for x, y in rect_arr:
            # if x+xdiff>=0 and x+xdiff<self.cols and y+ydiff>=0 and y+ydiff<self.rows:
            if self.get_val(x + xdiff, y + ydiff) == 1: return True
        return False

    def get_block_above_hole(self):
        blocks = 0
        for x in range(0, self.cols):
            for y in range(1, self.rows):
                if self.get_val(x, y) == 0 and self.get_val(x, y - 1) == 1:
                    blocks += sum(self.data[x:(y * self.cols + x):self.cols])

        return blocks

    def get_hole_number(self):
        hole_num = 0
        for x in range(0, self.cols):
            for y in range(1, self.rows):
                if self.get_val(x, y) == 0 and self.get_val(x, y - 1) == 1:
                    hole_num += 1
        return hole_num

    def clone(self):
        clone_matrix = Matrix(self.rows, self.cols, list(self.data))
        return clone_matrix

    def fill_block(self, rect_arr, xdiff=0, ydiff=0):
        for x, y in rect_arr:
            self.set_val(x + xdiff, y + ydiff, 1)

    def do_clear(self):
        clear_num = 0
        for i in range(self.rows - 1, -1, -1):
            if sum(self.data[self.cols * i:self.cols * (i + 1)]) == self.cols:
                self.data[self.cols:self.cols * (i + 1)] = self.data[0:self.cols * i]
                clear_num += 1
        return clear_num

    def get_empty_col(self):
        miny_arr = []
        for x in range(self.cols):
            miny = 19
            for y in range(self.rows):
                miny = y
                if self.get_val(x, y) == 1: break
            miny_arr.append(miny)
        empty_arr = []
        if miny_arr[1] - miny_arr[0] > 2: empty_arr.append((self.cols, miny_arr[1] - miny_arr[0]))
        if miny_arr[self.cols - 2] - miny_arr[self.cols - 1] > 2: empty_arr.append(
            (miny_arr[self.cols - 2] - miny_arr[self.cols - 1], self.cols))
        for x in range(1, self.cols - 1):
            if miny_arr[x - 1] - miny_arr[x] > 2 or miny_arr[x + 1] - miny_arr[x] > 2: empty_arr.append(
                (miny_arr[x - 1] - miny_arr[x], miny_arr[x + 1] - miny_arr[x]))
        return empty_arr

    def print_matrix(self):
        for i in range(self.rows):
            print self.data[self.cols * i:self.cols * (i + 1)]