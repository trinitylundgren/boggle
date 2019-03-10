#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 18:40:12 2019

@author: trinity
"""

# Boggle game premise
# 16 cubes in a 4 x 4 grid, each cube has 6 letters (including 'Qu')
# Cube permutation and orientation in grid gets randomized by 'shaking'
# Once cubes in final positions; start a 3-minute timer
# Players must then identify as many words in the grid as possible during time
# Rules: letters must be adjoining in a chain, horizontally, vertically or
# diagonally. Words must contain at least 3 letters and no letter cube may be
# used more than once within a single word. 
# Scoring: fewer than 3 letters scored no points, 3 letters scores 1, 4 letters
# scores 1, 5 letters scores 2, 6 scores 3, 7 scores 4, 8+ scores 11. The
# 'Qu' cube counts as two letters. Full credit is awarded for singular and plural.
# Scored words must be unique. Penalty of -1 point for non-legal word guesses.
# No penalty for submitting same word twice.

# Standard US English Boggle Dice:
# DIE0: R, I, F, O, B, X
# DIE1: I, F, E, H, E, Y
# DIE2: D, E, N, O, W, S
# DIE3: U, T, O, K, N, D
# DIE4: H, M, S, R, A, O
# DIE5: L, U, P, E, T, S
# DIE6: A, C, I, T, O, A
# DIE7: Y, L, G, K, U, E
# DIE8: Qu, B, M, J, O, A
# DIE9: E, H, I, S, P, N
# DIE10: V, E, T, I, G, N
# DIE11: B, A, L, I, Y, T
# DIE12: E, Z, A, V, N, D
# DIE13: R, A, L, E, S, C
# DIE14: U, W, I, L, R, G
# DIE15: P, A, C, E, M, D

import random

class BoggleCube(object):
    def __init__(self, letters):
        self.letters = letters[:]
        self.topletter = random.choice(self.letters)        
    def roll(self):
        self.topletter = random.choice(self.letters)
    def __str__(self):
        return self.topletter
    def __repr__(self):
        return self.__str__()

cubes = [['R', 'I', 'F', 'O', 'B', 'X'],
         ['I', 'F', 'E', 'H', 'E', 'Y'],
         ['D', 'E', 'N', 'O', 'W', 'S'],
         ['U', 'T', 'O', 'K', 'N', 'D'],
         ['H', 'M', 'S', 'R', 'A', 'O'],
         ['L', 'U', 'P', 'E', 'T', 'S'],
         ['A', 'C', 'I', 'T', 'O', 'A'],
         ['Y', 'L', 'G', 'K', 'U', 'E'],
         ['Qu', 'B', 'M', 'J', 'O', 'A'],
         ['E', 'H', 'I', 'S', 'P', 'N'],
         ['V', 'E', 'T', 'I', 'G', 'N'],
         ['B', 'A', 'L', 'I', 'Y', 'T'],
         ['E', 'Z', 'A', 'V', 'N', 'D'],
         ['R', 'A', 'L', 'E', 'S', 'C'],
         ['U', 'W', 'I', 'L', 'R', 'G'],
         ['P', 'A', 'C', 'E', 'M', 'D']]



class BoggleBoard(object):
    def __init__(self, boggle_cubes):
        self.build_board(boggle_cubes)
    def build_board(self, boggle_cubes):
        self.row_one = boggle_cubes[:4]
        self.row_two = boggle_cubes[4:8]
        self.row_three = boggle_cubes[8:12]
        self.row_four = boggle_cubes[12:16]
        self.board = [self.row_one, self.row_two, self.row_three, self.row_four]
    def __str__(self):
        board = ''
        for row in self.board:
            for cube in row:
                board += '[' + str(cube) + ']'
            board += '\n'
        return board 
    def shake(self):
        shuffle_list = []
        for row in self.board:
            for cube in row:
                cube.roll()
                shuffle_list.append(cube)
        random.shuffle(shuffle_list)
        self.build_board(shuffle_list)
        

if __name__ == '__main__':
    boggle_cubes = []
    for cube in cubes:
        boggle_cubes.append(BoggleCube(cube))
    
    game = BoggleBoard(boggle_cubes)
    game.shake()
    print(game)
     

    
    
    
    
    
    
    
    