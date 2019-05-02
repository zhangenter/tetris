# -*- coding=utf-8 -*-
import random
import pickle

class Block(object):
    sx=0
    sy=0
    def __init__(self):
        self.rect_arr=[]

    def get_rect_arr(self):
        return self.rect_arr

    def move(self,xdiff,ydiff):
        self.sx+=xdiff
        self.sy+=ydiff
        self.new_rect_arr=[]
        for x,y in self.rect_arr:
            self.new_rect_arr.append((x+xdiff,y+ydiff))
        self.rect_arr=self.new_rect_arr

    def can_move(self,xdiff,ydiff):
        for x,y in self.rect_arr:
            if y+ydiff>=20: return False
            if x+xdiff<0 or x+xdiff>=10: return False
        return True

    def change(self):
        self.shape_id+=1
        if self.shape_id >= self.shape_num:
            self.shape_id=0

        arr = self.get_shape()
        new_arr = []
        for x,y in arr:
            if x+self.sx<0 or x+self.sx>=10:
                self.shape_id -= 1
                if self.shape_id < 0: self.shape_id = self.shape_num - 1
                return None

            new_arr.append([x+self.sx,y+self.sy])

        return new_arr

class LongBlock(Block):
    shape_id=0
    shape_num=2
    def __init__(self, n=None):
        super(LongBlock, self).__init__()
        if n is None: n=random.randint(0,1)
        self.shape_id=n
        self.rect_arr=self.get_shape()
        self.color=(50,180,50)

    def get_shape(self, sid=None):
        if sid is None: sid = self.shape_id
        return [(1,0),(1,1),(1,2),(1,3)] if sid==0 else [(0,2),(1,2),(2,2),(3,2)]

class SquareBlock(Block):
    shape_id=0
    shape_num=1
    def __init__(self, n=None):
        super(SquareBlock, self).__init__()
        self.rect_arr=self.get_shape()
        self.color=(0,0,255)

    def get_shape(self, sid=None):
        if sid is None: sid = self.shape_id
        return [(1,1),(1,2),(2,1),(2,2)]

class ZBlock(Block):
    shape_id=0
    shape_num=2
    def __init__(self, n=None):
        super(ZBlock, self).__init__()
        if n is None: n=random.randint(0,1)
        self.shape_id=n
        self.rect_arr=self.get_shape()
        self.color=(30,200,200)

    def get_shape(self, sid=None):
        if sid is None: sid = self.shape_id
        return [(2,0),(2,1),(1,1),(1,2)] if sid==0 else [(0,1),(1,1),(1,2),(2,2)]

class SBlock(Block):
    shape_id=0
    shape_num=2
    def __init__(self, n=None):
        super(SBlock, self).__init__()
        if n is None: n=random.randint(0,1)
        self.shape_id=n
        self.rect_arr=self.get_shape()
        self.color=(255,30,255)

    def get_shape(self, sid=None):
        if sid is None: sid = self.shape_id
        return [(1,0),(1,1),(2,1),(2,2)] if sid==0 else [(0,2),(1,2),(1,1),(2,1)]

class LBlock(Block):
    shape_id=0
    shape_num=4
    def __init__(self, n=None):
        super(LBlock, self).__init__()
        if n is None: n=random.randint(0,3)
        self.shape_id=n
        self.rect_arr=self.get_shape()
        self.color=(200,200,30)

    def get_shape(self, sid=None):
        if sid is None: sid = self.shape_id
        if sid==0: return [(1,0),(1,1),(1,2),(2,2)]
        elif sid==1: return [(0,1),(1,1),(2,1),(0,2)]
        elif sid==2: return [(0,0),(1,0),(1,1),(1,2)]
        else: return [(0,1),(1,1),(2,1),(2,0)]

class JBlock(Block):
    shape_id=0
    shape_num=4
    def __init__(self, n=None):
        super(JBlock, self).__init__()
        if n is None: n=random.randint(0,3)
        self.shape_id=n
        self.rect_arr=self.get_shape()
        self.color=(200,100,0)

    def get_shape(self, sid=None):
        if sid is None: sid = self.shape_id
        if sid==0: return [(1,0),(1,1),(1,2),(0,2)]
        elif sid==1: return [(0,1),(1,1),(2,1),(0,0)]
        elif sid==2: return [(2,0),(1,0),(1,1),(1,2)]
        else: return [(0,1),(1,1),(2,1),(2,2)]

class TBlock(Block):
    shape_id=0
    shape_num=4
    def __init__(self, n=None):
        super(TBlock, self).__init__()
        if n is None: n=random.randint(0,3)
        self.shape_id=n
        self.rect_arr=self.get_shape()
        self.color=(255,0,0)

    def get_shape(self, sid=None):
        if sid is None: sid = self.shape_id
        if sid==0: return [(0,1),(1,1),(2,1),(1,2)]
        elif sid==1: return [(1,0),(1,1),(1,2),(0,1)]
        elif sid==2: return [(0,1),(1,1),(2,1),(1,0)]
        else: return [(1,0),(1,1),(1,2),(2,1)]

def create_block():
    n = random.randint(0,18)
    if n==0: return SquareBlock(n=0)
    elif n==1 or n==2: return LongBlock(n=n-1)
    elif n==3 or n==4: return ZBlock(n=n-3)
    elif n==5 or n==6: return SBlock(n=n-5)
    elif n>=7 and n<=10: return LBlock(n=n-7)
    elif n>=11 and n<=14: return JBlock(n=n-11)
    else: return TBlock(n=n-15)


class BlockManage(object):
    pnum=1
    blocks = []
    def __init__(self,pnum):
        self.pnum=pnum
        self.blocks=[[] for i in range(self.pnum)]

    def get_block(self, pid=0):
        if len(self.blocks[pid]) == 0:
            block = create_block()
            for arr in self.blocks:
                arr.append(pickle.loads(pickle.dumps(block)))
        return self.blocks[pid].pop(0)
