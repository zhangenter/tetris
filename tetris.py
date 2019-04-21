# -*- coding=utf-8 -*-
import random
import pygame
from pygame.locals import KEYDOWN,K_LEFT,K_RIGHT,K_UP,K_DOWN,K_SPACE
import pickle,os

ROW_COUNT=20
COL_COUNT=10
SCORE_MAP=(100,300,800,1600)

class Matrix(object):
    rows = 0
    cols = 0
    data = []
    def __init__(self, rows, cols, data=None):
        self.rows = rows
        self.cols = cols 
        if data is None: data = [0 for i in range(rows*cols)]
        self.data = data

    def set_val(self, x, y, val):
        self.data[y*self.cols+x] = val

    def get_val(self, x, y):
        return self.data[y*self.cols+x]
    
    def cross_block(self, rect_arr, xdiff=0, ydiff=0):
        for x,y in rect_arr:
            #if x+xdiff>=0 and x+xdiff<self.cols and y+ydiff>=0 and y+ydiff<self.rows:
            if self.get_val(x+xdiff,y+ydiff) == 1: return True
        return False

    def get_hole_number(self):
        hole_num=0
        for x in range(0,self.cols):
            for y in range(1,self.rows):
                if self.get_val(x,y) == 0 and self.get_val(x,y-1) == 1: 
                    hole_num+=1
        return hole_num

    def clone(self):
        clone_matrix=Matrix(self.rows, self.cols, list(self.data))
        return clone_matrix

    def fill_block(self, rect_arr, xdiff=0, ydiff=0):
        for x,y in rect_arr:
            self.set_val(x+xdiff,y+ydiff, 1)

    def do_clear(self):
        for i in range(self.rows-1,-1,-1):
            if sum(self.data[self.cols*i:self.cols*(i+1)])==self.cols:
                self.data[self.cols:self.cols*(i+1)]=self.data[0:self.cols*i]

    def print_matrix(self):
        for i in range(self.rows):
            print self.data[self.cols*i:self.cols*(i+1)]

class Player(object):
    auto_mode=False
    def __init__(self):
        pass
    def run(self, panel): 
        pass

class HumanPlayer(Player):
    def __init__(self):
        super(Player, self).__init__()

class AIPlayer(Player):
    cal_block_id=-1 
    ctl_arr=[] # control arr, 1＝change、2＝left、3＝right、4＝down
    auto_mode=True
    ai_diff_ticks = 100 #timespan between two controls
    
    def __init__(self):
        super(Player, self).__init__()
        self.ctl_ticks = pygame.time.get_ticks() + self.ai_diff_ticks

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
            for x,y in tmp_shape: center_shape.append((x+COL_COUNT/2-2,y-2))
            minx = COL_COUNT
            maxx = 0
            miny = ROW_COUNT
            maxy = -2
            for x,y in center_shape:
                if x<minx: minx = x
                if x>maxx: maxx = x
                if y<miny: miny = y
                if y>maxy: maxy = y

            for xdiff in range(-minx,COL_COUNT-maxx): 
                arr = [1 for _ in range(i)] 
                if xdiff < 0: [arr.append(2) for _ in range(-xdiff)]
                if xdiff > 0: [arr.append(3) for _ in range(xdiff)]

                max_yindex = -miny
                for yindex in range(-miny, ROW_COUNT-maxy):
                    if matrix.cross_block(center_shape, xdiff=xdiff, ydiff=yindex):
                        break
                    max_yindex = yindex
                score = sum([y+max_yindex for x,y in center_shape])

                # clone matrix and fill new block to calculate holes
                clone_matrix = matrix.clone()
                clone_matrix.fill_block(center_shape, xdiff=xdiff, ydiff=max_yindex)
                clone_matrix.do_clear()
                score -= clone_matrix.get_hole_number() * COL_COUNT

                if score > max_score: 
                    max_score = score
                    best_arr = arr
        self.ctl_arr = best_arr+[4]

    def run(self, panel):
        if pygame.time.get_ticks() < self.ctl_ticks: return
        self.ctl_ticks += self.ai_diff_ticks
        if panel.block_id == self.cal_block_id: # block_id not change
            if len(self.ctl_arr)>0:
                ctl = self.ctl_arr.pop(0)
                if ctl == 1: panel.change_block()
                if ctl == 2: panel.control_block(-1,0)
                if ctl == 3: panel.control_block(1,0)
                if ctl == 4:
                    flag = panel.move_block()
                    while flag==1: 
                        flag = panel.move_block()

        else: # block_id is new
            self.cal_block_id = panel.block_id
            self.cal_best_arr(panel)
            

class RectInfo(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class HintBox(object):
    next_block=None
    def __init__(self, bg, block_size, position):
        self._bg=bg;
        self._x,self._y,self._width,self._height=position
        self._block_size=block_size
        self._bgcolor=[0,0,0]

    def take_block(self):
        block = self.next_block
        if block is None: # make first block
            block = create_block()
    
        self.next_block = create_block()
        return block

    def paint(self):
        mid_x=self._x+self._width/2
        pygame.draw.line(self._bg,self._bgcolor,[mid_x,self._y],[mid_x,self._y+self._height],self._width) 
        bz=self._block_size
        
        if self.next_block:
            arr = self.next_block.get_rect_arr()
            minx,miny=arr[0]
            maxx,maxy=arr[0]
            for x,y in arr:
                if x<minx: minx=x
                if x>maxx: maxx=x
                if y<miny: miny=y
                if y>maxy: maxy=y
            w=(maxx-minx)*bz
            h=(maxy-miny)*bz
            
            cx=self._width/2-w/2-minx*bz-bz/2 
            cy=self._height/2-h/2-miny*bz-bz/2

            for rect in arr:
                x,y=rect
                pygame.draw.line(self._bg,self.next_block.color,[self._x+x*bz+cx+bz/2,self._y+cy+y*bz],[self._x+x*bz+cx+bz/2,self._y+cy+(y+1)*bz],bz)
                pygame.draw.rect(self._bg,[255,255,255],[self._x+x*bz+cx,self._y+y*bz+cy,bz+1,bz+1],1)

class ScoreBox(object):
    total_score = 0
    high_score = 0
    db_file = 'tetris.db'
    def __init__(self, bg, block_size, position):
        self._bg=bg;
        self._x,self._y,self._width,self._height=position
        self._block_size=block_size
        self._bgcolor=[0,0,0]
        
        if os.path.exists(self.db_file): self.high_score = pickle.load(open(self.db_file,'rb'))

    def paint(self):
        myfont = pygame.font.Font(None,36)
        white = 255,255,255
        textImage = myfont.render('High: %06d'%(self.high_score), True, white)
        self._bg.blit(textImage, (self._x,self._y))
        textImage = myfont.render('Score:%06d'%(self.total_score), True, white)
        self._bg.blit(textImage, (self._x,self._y+40))

    def add_score(self, score):
        self.total_score += score
        if self.total_score > self.high_score:
            self.high_score=self.total_score
            pickle.dump(self.high_score, open(self.db_file,'wb+'))

class Panel(object): 
    block_id=0
    rect_arr=[] 
    moving_block=None 
    hint_box=None
    score_box=None
    def __init__(self,bg, block_size, position):
        self._bg=bg;
        self._x,self._y,self._width,self._height=position
        self._block_size=block_size
        self._bgcolor=[0,0,0]
    
    def get_rect_matrix(self):
        matrix = Matrix(ROW_COUNT, COL_COUNT)
        for rect_info in self.rect_arr:
            matrix.set_val(rect_info.x, rect_info.y, 1)
        return matrix

    def add_block(self,block):
        for x,y in block.get_rect_arr():
            self.rect_arr.append(RectInfo(x,y, block.color))

    def create_move_block(self):
        self.block_id+=1
        block = self.hint_box.take_block()
        #block = create_block()
        block.move(COL_COUNT/2-2,-2) # move block to top center
        self.moving_block=block

    def check_overlap(self, diffx, diffy, check_arr=None):
        if check_arr is None: check_arr = self.moving_block.get_rect_arr()
        for x,y in check_arr:
            for rect_info in self.rect_arr:
                if x+diffx==rect_info.x and y+diffy==rect_info.y:
                    return True
        return False

    def control_block(self, diffx, diffy):
        if self.moving_block.can_move(diffx,diffy) and not self.check_overlap(diffx, diffy):
            self.moving_block.move(diffx,diffy)

    def change_block(self):
        if self.moving_block:
            new_arr = self.moving_block.change()
            if new_arr and not self.check_overlap(0, 0, check_arr=new_arr): 
                self.moving_block.rect_arr=new_arr


    def move_block(self):
        if self.moving_block is None: create_move_block()
        if self.moving_block.can_move(0,1) and not self.check_overlap(0,1): 
            self.moving_block.move(0,1)
            return 1
        else:
            self.add_block(self.moving_block)
            self.check_clear()

            for rect_info in self.rect_arr:
                if rect_info.y<0: return 9 # gameover
            self.create_move_block()
            return 2

    def check_clear(self):
        tmp_arr = [[] for i in range(20)]
       
        for rect_info in self.rect_arr:
            if rect_info.y<0: return
            tmp_arr[rect_info.y].append(rect_info)

        clear_num=0
        clear_lines=set([])
        y_clear_diff_arr=[[] for i in range(20)]
        
        for y in range(19,-1,-1):
            if len(tmp_arr[y])==10:
                clear_lines.add(y)
                clear_num += 1
            y_clear_diff_arr[y] = clear_num

        if clear_num>0:
            new_arr=[]
            
            for y in range(19,-1,-1):
                if y in clear_lines: continue
                tmp_row = tmp_arr[y]
                y_clear_diff=y_clear_diff_arr[y]
                for rect_info in tmp_row:
                    #new_arr.append([x,y+y_clear_diff])
                    new_arr.append(RectInfo(rect_info.x, rect_info.y+y_clear_diff, rect_info.color))
            
            self.rect_arr = new_arr
            score = SCORE_MAP[clear_num-1]
            self.score_box.add_score(score)


    def paint(self):
        mid_x=self._x+self._width/2
        pygame.draw.line(self._bg,self._bgcolor,[mid_x,self._y],[mid_x,self._y+self._height],self._width) # 用一个粗线段来填充背景
        
        bz=self._block_size
        for rect_info in self.rect_arr:
            x=rect_info.x
            y=rect_info.y
            pygame.draw.line(self._bg,rect_info.color,[self._x+x*bz+bz/2,self._y+y*bz],[self._x+x*bz+bz/2,self._y+(y+1)*bz],bz)
            pygame.draw.rect(self._bg,[255,255,255],[self._x+x*bz,self._y+y*bz,bz+1,bz+1],1)
       
        if self.move_block:
            for rect in self.moving_block.get_rect_arr():
                x,y=rect
                pygame.draw.line(self._bg,self.moving_block.color,[self._x+x*bz+bz/2,self._y+y*bz],[self._x+x*bz+bz/2,self._y+(y+1)*bz],bz)
                pygame.draw.rect(self._bg,[255,255,255],[self._x+x*bz,self._y+y*bz,bz+1,bz+1],1)

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

def run():
    pygame.init()
    space=30
    main_block_size=30
    main_panel_width=main_block_size*COL_COUNT
    main_panel_height=main_block_size*ROW_COUNT
    screencaption = pygame.display.set_caption('Tetris')
    screen = pygame.display.set_mode((main_panel_width+160+space*3,main_panel_height+space*2)) 
    main_panel=Panel(screen,main_block_size,[space,space,main_panel_width,main_panel_height])
    hint_box=HintBox(screen,main_block_size,[main_panel_width+space+space,space,160,160])
    score_box=ScoreBox(screen,main_block_size,[main_panel_width+space+space,160+space*2,160,160])
    
    main_panel.hint_box=hint_box
    main_panel.score_box=score_box

    pygame.key.set_repeat(200, 30)
    main_panel.create_move_block()

    diff_ticks = 300 
    ticks = pygame.time.get_ticks() + diff_ticks

    player = AIPlayer()

    pause=0
    game_state = 1 # game status 1.normal 2.gameover
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()
                 exit()
            if event.type == KEYDOWN:
                if event.key==97: pause=1-pause # press a to pause
                if event.key==112: # for debug where press p
                    main_panel.get_rect_matrix().print_matrix()
            if player.auto_mode:continue
            if event.type == KEYDOWN:
                if event.key == K_LEFT: main_panel.control_block(-1,0)
                if event.key == K_RIGHT: main_panel.control_block(1,0)
                if event.key == K_UP: main_panel.change_block()
                if event.key == K_DOWN: main_panel.control_block(0,1)
                if event.key == K_SPACE:
                    flag = main_panel.move_block()
                    while flag==1: 
                        flag = main_panel.move_block()
                    if flag == 9: game_state = 2
       
        screen.fill((100,100,100)) # make background gray
        main_panel.paint() 
        hint_box.paint() 
        score_box.paint() 

        if game_state == 2:
            myfont = pygame.font.Font(None,30)
            white = 255,255,255
            textImage = myfont.render("Game over", True, white)
            screen.blit(textImage, (160,190))

        pygame.display.update() 

        if pause==1: continue
        if game_state == 1: player.run(main_panel)
        if game_state == 1 and pygame.time.get_ticks() >= ticks:
            ticks+=diff_ticks
            if main_panel.move_block()==9: game_state = 2 # gameover

run()
