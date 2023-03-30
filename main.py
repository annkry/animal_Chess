#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
The agent playing against a random opponent will choose the most favorable move based on simulated random games starting from a possible next move. 
During the algorithm execution,it will also count how much time it takes for our agent to make a move. 
It will also count how many moves were simulated during the entire game.

Notations:
0 - Random opponent
1 - Our agent
'''


import random
import sys
import copy
import time

count_ROZGR = 4  # number of simulated random games for each possible next move at a given moment


class WrongMove(Exception):
    def __init__(self):
        self.message = 'Wrong move'
        super().__init__(self.message)


class Jungle:
    PIECE_VALUES = {
        0: 4,
        1: 1,
        2: 2,
        3: 3,
        4: 5,
        5: 7,
        6: 8,
        7: 10
    }
    MAXIMAL_PASSIVE = 30
    DENS_DIST = 0.1
    MX = 7
    MY = 9
    traps = {(2, 0), (4, 0), (3, 1), (2, 8), (4, 8), (3, 7)}
    ponds = {(x, y) for x in [1, 2, 4, 5] for y in [3, 4, 5]}
    dens = [(3, 8), (3, 0)]
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    rat, cat, dog, wolf, jaguar, tiger, lion, elephant = range(8)

    def __init__(self):
        self.board = self.initial_board()
        self.pieces = {0: {}, 1: {}}

        for y in range(Jungle.MY):
            for x in range(Jungle.MX):
                C = self.board[y][x]
                if C:
                    pl, pc = C
                    self.pieces[pl][pc] = (x, y)
        self.curplayer = 0
        self.peace_counter = 0
        self.winner = None

    def initial_board(self):
        pieces = """
        L.....T
        .D...C.
        R.J.W.E
        .......
        .......
        .......
        e.w.j.r
        .c...d.
        t.....l
        """

        B = [x.strip() for x in pieces.split() if len(x) > 0]
        T = dict(zip('rcdwjtle', range(8)))

        res = []
        for y in range(9):
            raw = 7 * [None]
            for x in range(7):
                c = B[y][x]
                if c != '.':
                    if 'A' <= c <= 'Z':
                        player = 1
                    else:
                        player = 0
                    raw[x] = (player, T[c.lower()])
            res.append(raw)
        return res

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return None

    def can_beat(self, p1, p2, pos1, pos2):
        if pos1 in Jungle.ponds and pos2 in Jungle.ponds:
            return True  # rat vs rat
        if pos1 in Jungle.ponds:
            return False  # rat in pond cannot beat any piece on land
        if p1 == Jungle.rat and p2 == Jungle.elephant:
            return True
        if p1 == Jungle.elephant and p2 == Jungle.rat:
            return False
        if p1 >= p2:
            return True
        if pos2 in Jungle.traps:
            return True
        return False

    def pieces_comparison(self):
        for i in range(7, -1, -1):
            ps = []
            for p in [0, 1]:
                if i in self.pieces[p]:
                    ps.append(p)
            if len(ps) == 1:
                return ps[0]
        return None

    def rat_is_blocking(self, player_unused, pos, dx, dy):
        x, y = pos
        nx = x + dx
        for player in [0, 1]:
            if Jungle.rat not in self.pieces[1-player]:
                continue
            rx, ry = self.pieces[1-player][Jungle.rat]
            if (rx, ry) not in self.ponds:
                continue
            if dy != 0:
                if x == rx:
                    return True
            if dx != 0:
                if y == ry and abs(x-rx) <= 2 and abs(nx-rx) <= 2:
                    return True
        return False

    def draw(self):
        TT = {0: 'rcdwjtle', 1: 'RCDWJTLE'}
        for y in range(Jungle.MY):

            L = []
            for x in range(Jungle.MX):
                b = self.board[y][x]
                if b:
                    pl, pc = b
                    L.append(TT[pl][pc])
                else:
                    L.append('.')
            print(''.join(L))
        print('')

    def moves(self, player):
        res = []
        for p, pos in self.pieces[player].items():
            x, y = pos
            for (dx, dy) in Jungle.dirs:
                pos2 = (nx, ny) = (x+dx, y+dy)
                if 0 <= nx < Jungle.MX and 0 <= ny < Jungle.MY:
                    if Jungle.dens[player] == pos2:
                        continue
                    if pos2 in self.ponds:
                        if p not in (Jungle.rat, Jungle.tiger, Jungle.lion):
                            continue
                        if p == Jungle.tiger or p == Jungle.lion:
                            if dx != 0:
                                dx *= 3
                            if dy != 0:
                                dy *= 4
                            if self.rat_is_blocking(player, pos, dx, dy):
                                continue
                            pos2 = (nx, ny) = (x+dx, y+dy)
                    if self.board[ny][nx] is not None:
                        pl2, piece2 = self.board[ny][nx]
                        if pl2 == player:
                            continue
                        if not self.can_beat(p, piece2, pos, pos2):
                            continue
                    res.append((pos, pos2))
        return res

    def victory(self, player):
        oponent = 1-player
        if len(self.pieces[oponent]) == 0:
            self.winner = player
            return True

        x, y = self.dens[oponent]
        if self.board[y][x]:
            self.winner = player
            return True

        if self.peace_counter >= Jungle.MAXIMAL_PASSIVE:
            r = self.pieces_comparison()
            if r is None:
                self.winner = 1  # draw is second player's victory
            else:
                self.winner = r
            return True
        return False

    def do_move(self, m):
        self.curplayer = 1 - self.curplayer
        if m is None:
            return
        pos1, pos2 = m
        x, y = pos1
        pl, pc = self.board[y][x]

        x2, y2 = pos2
        if self.board[y2][x2]:  # piece taken!
            pl2, pc2 = self.board[y2][x2]
            del self.pieces[pl2][pc2]
            self.peace_counter = 0
        else:
            self.peace_counter += 1

        self.pieces[pl][pc] = (x2, y2)
        self.board[y2][x2] = (pl, pc)
        self.board[y][x] = None

    def update(self, player, move_string):
        self.curplayer = player
        move = tuple(int(m) for m in move_string.split(' '))
        if len(move) != 4:
            raise WrongMove
        possible_moves = self.moves(player)
        if not possible_moves:
            if move != (-1, -1, -1, -1):
                raise WrongMove
            move = None
        else:
            move = ((move[0], move[1]), (move[2], move[3]))
            if move not in possible_moves:
                raise WrongMove
        self.do_move(move)

        if self.victory(player):
            assert self.winner is not None
            return 2 * self.winner - 1
        else:
            return None


class Player(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.game = Jungle()
        self.my_player = 1

    def say(self, what):
        sys.stdout.write(what)
        sys.stdout.write('\n')
        sys.stdout.flush()

    def hear(self):
        line = sys.stdin.readline().split()
        return line[0], line[1:]

    def sym(self, J, move):  # random game generation
        countba_ruchow_zasym = 0  # how many moves have been simulated
        # perform move
        (a, b), (c, d) = move
        move_string = str(a)+' '+str(b)+' '+str(c)+' '+str(d)
        J.curplayer = 1
        kon = J.update(1, move_string)
        countba_ruchow_zasym += 1
        if kon != None:
            if kon == 1:
                return (True, countba_ruchow_zasym)
            else:
                return (False, countba_ruchow_zasym)
        # end of a move
        player = 1
        op = 0
        while True:
            # random move of our opponent - 1
            J.curplayer = 0
            moves = J.moves(0)
            if moves:
                move = random.choice(moves)
                (a, b), (c, d) = move
                move_string = str(a)+' '+str(b)+' '+str(c)+' '+str(d)
                # return will be 1 if we won, otherwise -1
                kon = J.update(0, move_string)
                countba_ruchow_zasym += 1
                if kon != None:  # we check if the game is over
                    if kon == 1:
                        return (True, countba_ruchow_zasym)
                    else:
                        return (False, countba_ruchow_zasym)
                move = (move[0][0], move[0][1], move[1][0], move[1][1])
            else:
                J.do_move(None)
                move = (-1, -1, -1, -1)
            # random move of our agent - 1
            movess = J.moves(1)
            if movess:
                move = random.choice(movess)
                (a, b), (c, d) = move
                move_string = str(a)+' '+str(b)+' '+str(c)+' '+str(d)
                # return will be 1 if we won, otherwise -1
                kon = J.update(1, move_string)
                countba_ruchow_zasym += 1
                if kon != None:  # we check if the game is over
                    if kon == 1:
                        return (True, countba_ruchow_zasym)
                    else:
                        return (False, countba_ruchow_zasym)
                move = (move[0][0], move[0][1], move[1][0], move[1][1])
            else:
                J.do_move(None)
                move = (-1, -1, -1, -1)

    def loop(self):
        player = 1
        count_moves_sim = 0
        op = 0
        while True:
            # self.game.draw()
            # random player movement - 0
            moves = self.game.moves(0)
            if moves:
                move = random.choice(moves)
                (a, b), (c, d) = move
                move_string = str(a)+' '+str(b)+' '+str(c)+' '+str(d)
                kon = self.game.update(0, move_string)
                if kon != None:
                    if kon == 1:
                        return (True, count_moves_sim)
                    else:
                        return (False, count_moves_sim)
                move = (move[0][0], move[0][1], move[1][0], move[1][1])
            else:
                self.game.do_move(None)
                move = (-1, -1, -1, -1)
            # move of our agent - 1
            start = time.time()
            mov = self.game.moves(1)
            max_wygr = -1
            max_move = []
            for i in mov:
                count = 0
                for j in range(count_ROZGR):
                    res, count = self.sym(copy.deepcopy(self.game), i)
                    count_moves_sim += count
                    if res:
                        count += 1
                if max_wygr <= count:
                    max_wygr = count
                    max_move.append(i)
            (a, b), (c, d) = random.choice(max_move)
            move_string = str(a)+' '+str(b)+' '+str(c)+' '+str(d)
            kon = self.game.update(1, move_string)
            end = time.time()
            print("time for one move made by our agent: ", end-start)
            if kon != None:
                if kon == 1:
                    return (True, count_moves_sim)
                else:
                    return (False, count_moves_sim)
            if player == 0:
                self.my_player = 0


if __name__ == '__main__':
    player = Player()
    # count - number of simulated moves
    # res - did our agent win
    res, count = player.loop()
    print("a number of moves that have been simulated: " + str(count))
    if res:
        print("Victory")
