import numpy as np
import random


class Game:

    def __init__(self):
        #0-empty space, 1-obs, 2-prisoner, 3-police, 4-tunnel
        self.board = np.zeros((5,5), dtype=int)
        self.po_pos = None
        self.pri_pos = None
        self.colors = ['white','yellow','pink']
        self.c_color = 'white'
        self.po_skin = 0
        self.pri_skin = 0
        self.pause = False
        self.mode = 'normal'
        self.po_power = 'mortal'
        self.pr_power = 'mortal'
        self.emo_po = 0
        self.emo_pri = 0

    def emoji1_po(self):
        if self.emo_po == 0:
            self.emo_po = 1
        elif self.emo_po == 1:
            self.emo_po = 0

    def emoji1_pri(self):
        if self.emo_pri == 0:
            self.emo_pri = 1
        elif self.emo_pri == 1:
            self.emo_pri = 0

    def make_zeros(self):
        self.board = np.zeros((5,5), dtype=int)

    def random_pos(self):
        x = random.randrange(0,5)
        y = random.randrange(0,5)
        return (x,y)
    
    def get_board(self):
        return self.board

    def random_board(self): 
        #random_ob
        if self.mode == 'normal':
            for j in range(5):
                x, y = self.random_pos()
                while self.board[x][y] != 0:
                    x, y = self.random_pos()
                self.board[x][y] = 1

            #random theif, police, tunnel positions
            for i in range(3):
                x, y = self.random_pos()
                while self.board[x][y] != 0: 
                    x, y = self.random_pos()
                self.board[x][y] = i+2
        elif self.mode == 'mspring':
            for j in range(5):
                x, y = self.random_pos()
                while self.board[x][y] != 0:
                    x, y = self.random_pos()
                self.board[x][y] = 1

            #random theif, police, tunnel positions
            for i in range(3):
                x, y = self.random_pos()
                while self.board[x][y] != 0: 
                    x, y = self.random_pos()
                self.board[x][y] = i+2

            for k in range(1):
                x, y = self.random_pos()
                while self.board[x][y] != 0: 
                    x, y = self.random_pos()
                self.board[x][y] = 11 

        elif self.mode == 'mbreaker':
            for j in range(5):
                x, y = self.random_pos()
                while self.board[x][y] != 0:
                    x, y = self.random_pos()
                self.board[x][y] = 1

            #random theif, police, tunnel positions
            for i in range(3):
                x, y = self.random_pos()
                while self.board[x][y] != 0: 
                    x, y = self.random_pos()
                self.board[x][y] = i+2

            for k in range(1):
                x, y = self.random_pos()
                while self.board[x][y] != 0: 
                    x, y = self.random_pos()
                self.board[x][y] = 12

        elif self.mode == 'mdoor':
            for j in range(5):
                x, y = self.random_pos()
                while self.board[x][y] != 0:
                    x, y = self.random_pos()
                self.board[x][y] = 1

            #random theif, police, tunnel positions
            for i in range(3):
                x, y = self.random_pos()
                while self.board[x][y] != 0: 
                    x, y = self.random_pos()
                self.board[x][y] = i+2

            for k in range(1):
                x, y = self.random_pos()
                while self.board[x][y] != 0: 
                    x, y = self.random_pos()
                self.board[x][y] = 13
    
    def door_where(self):
        x, y = self.random_pos()
        while self.board[x][y] != 0: 
            x, y = self.random_pos()
        return (int(x),int(y))

    
    def decode_where(self, a):
        x, y = np.where(self.board == a)
        return (int(x),int(y))

    def get_pri_pos(self):
        self.pri_pos = self.decode_where(2)
        return self.pri_pos
    
    def get_po_pos(self):
        self.po_pos = self.decode_where(3)
        return self.po_pos

    def get_tun_pos(self):
        self.tun_pos = self.decode_where(4)
        return self.tun_pos
    
    def get_item_pos(self):
        self.item_pos = self.decode_where(11)
        return self.item_pos
    
    def get_item2_pos(self):
        self.item_pos = self.decode_where(12)
        return self.item_pos

    def get_item3_pos(self):
        self.item_pos = self.decode_where(13)
        return self.item_pos

    def get_mode(self):
        return self.mode

    def swap(self,x,y,x2,y2):
        self.board[x][y],self.board[x2][y2] = self.board[x2][y2],self.board[x][y]

    def move(self, x, y, x2, y2):
        self.board[x2][y2] = self.board[x][y]
        self.board[x][y] = 0
        
    def set(self, x, y, c):
        self.board[x][y] = c

    def set_color(self, value):
        self.c_color = value
    
    def change_color(self):
        if (self.colors.index(self.c_color)+1) >= len(self.colors):
            self.c_color = self.colors[0]
        else:
            self.c_color = self.colors[self.colors.index(self.c_color)+1]

    def set_poskin(self, value):
        self.po_skin = value
    
    def get_poskin(self):
        return self.po_skin
    
    def set_priskin(self, value):
        self.pri_skin = value

    def get_priskin(self):
        return self.pri_skin
    
    def poskin(self):
        if self.po_skin == 1:
            self.po_skin = 0
        else:
            self.po_skin = self.po_skin+1

    def priskin(self):
        if self.pri_skin == 1:
            self.pri_skin = 0
        else:
            self.pri_skin = self.pri_skin+1

    def check_legit(self, pos): 
        if 0 <= pos[0] <=4 and 0 <= pos[1] <=4:
            return True
        else:
            return False
    
    def check_obs(self, pos):
        if self.board[pos] == 1:
            return True
        else:
            return False
    
    def check_tunnel(self, pos):
        if self.board[pos] == 4:
            return True
        else:
            return False

    def spring_mode(self):
        if self.mode == 'normal':
            self.mode = 'mspring'
        elif self.mode == 'mspring':
            self.mode = 'normal'
        elif self.mode == 'mbreaker':
            self.mode = 'mspring'
        elif self.mode == 'mdoor':
            self.mode = 'mspring'
    
    def breaker_mode(self):
        if self.mode == 'normal':
            self.mode = 'mbreaker'
        elif self.mode == 'mbreaker':
            self.mode = 'normal'
        elif self.mode == 'mspring':
            self.mode = 'mbreaker'
        elif self.mode == 'mdoor':
            self.mode = 'mbreaker'

    def door_mode(self):
        if self.mode == 'normal':
            self.mode = 'mdoor'
        elif self.mode == 'mspring':
            self.mode = 'mdoor'
        elif self.mode == 'mbreaker':
            self.mode = 'mdoor'
        elif self.mode == 'mdoor':
            self.mode = 'normal'
        
    def policejumper(self):
        self.po_power = 'jumper'
    
    def prisonerjumper(self):
        self.pr_power = 'jumper'

    def policebreaker(self):
        self.po_power = 'breaker'

    def prisonerbreaker(self):
        self.pr_power = 'breaker'

    def get_po_power(self):
        return self.po_power

    def get_pr_power(self):
        return self.pr_power

    def reset_power(self):
        self.po_power = 'mortal'
        self.pr_power = 'mortal'

