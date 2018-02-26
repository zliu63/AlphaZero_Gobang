import numpy as np

class ChessBoard(object):

    def __init__(self, **kwargs):
        self.cols = int(kwargs.get('cols',8))
        self.rows = int(kwargs.get('rows',8))
        self.states = {}    #key:move<-coordinates on board, flatten cols*rows 
                            #value:player<-black or white piece
        self.win_requirement = int(kwargs.get('win_requirement',5))
        self.players = [1,2]    #player1, player2

    def initialize(self, start_player = 0):
        if self.cols < self.win_requirement or self.rows < self.win_requirement:
            raise Exception('Cols and rows of board cannot less than %d' % self.win_requirement)
        self.current_player = self.players[start_player]
        self.available_moves = list(range(self.cols * self.rows))
        self.last_move = -1

    def move_to_location(self, move):
        '''
        1d->2d
        3*3 board as following
        6 7 8
        3 4 5
        0 1 2
        move = 5 corrsponding to (1,2)
        '''
        row = move // self.cols
        col = move // self.cols
        return [row,col] 

    def location_to_move(self, location):
        '''
        2d->1d
        '''
        if(len(location) != 2):
            return -1
        row = location[0]
        col = location[1]
        move = row*self.cols + col
        if(move not in range(self.cols*self.rows)):
            return -1
        return move

    def current_state(self):
        '''
        只使用了4个 8 x 8 的2d平面，
        面1:当前player的棋子位置，
        面2:对手player的棋子位置，有棋子的位置是1，没棋子的位置是0
        面3:表示对手player最近一步的落子位置，也就是整个平面只有一个位置是1，其余全部是0. 
        面4:表示的是当前player是不是先手player，
            如果当前player是先手则整个平面全部为1，否则全部为0.
        '''
        plane_state = np.zeros((4,self.rows,self.cols))
        if self.states:
            moves,players = np.array(list(zip(*self.states.items())))
            move_curr = moves[players == self.current_player]
            move_oppo = moves[players != self.current_player]
            plane_state[0][move_curr // self.cols, move_curr % self.rows] = 1.
            plane_state[1][move_oppo // self.cols, move_oppo % self.rows] = 1.
            plane_state[2][self.last_move // self.cols, self.last_move % self.rows] = 1.
        if len(self.states)%2 == 0:
            plane_state[3][:,:] = 1.
        return plane_state[:,::-1,:]

    def do_move(self, move):
        self.states[move] = self.current_player
        self.available_moves.remove(move)
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[0]
        self.last_move = move

    def has_a_winner(self):
        cols = self.cols
        rows = self.rows
        states = self.states
        n = self.win_requirement
        moved = list(set(range(rows*cols)) - set(self.available_moves))
        if len(moved) < self.win_requirement + 2:
            return False, -1
        for m in moved:
            i = m // cols
            j = m % cols
            player = states[m]

            if (j in range(cols - n +1) and
                len(set(states.get(k,-1) for k in range(m,m+n))) == 1):
                return True, player
            if (i in range(rows - n +1) and
                len(set(states.get(k,-1) for k in range(m,m+n*cols,cols))) == 1):
                return True, player
            if (j in range(cols - n + 1) and i in range(rows - n + 1) and
                len(set(states.get(k,-1) for k in range(m,m+n*(cols + 1), width+1))) == 1):
                return True, player
            if (j in range(n-1, cols) and i in range(rows - n +1) and
                len(set(states.get(k,-1) for k in range(m, m+n*(cols-1),cols-1))) == 1):
                return True, player
        return False, -1

    def game_over(self):
        win, winner = self.has_a_winner()
        if win:
            return True, winner
        elif not len(self.available_moves):
            return True, -1
        return False, -1

    def get_current_player(self):
        return self.current_player





