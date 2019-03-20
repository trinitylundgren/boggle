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

import sys
sys.path.insert(0, './TWL06')
import random
import twl
import time

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
         ['QU', 'B', 'M', 'J', 'O', 'A'],
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
    def _adjacent_indices(self,previousIndex):
        adjacentIndices = []
        adjacentIndices.append((previousIndex[0],previousIndex[1] - 1))
        adjacentIndices.append((previousIndex[0],previousIndex[1] + 1))
        adjacentIndices.append((previousIndex[0] + 1,previousIndex[1] + 1))
        adjacentIndices.append((previousIndex[0] - 1,previousIndex[1] + 1))
        adjacentIndices.append((previousIndex[0] + 1,previousIndex[1] - 1))
        adjacentIndices.append((previousIndex[0] - 1,previousIndex[1] - 1))
        adjacentIndices.append((previousIndex[0] + 1,previousIndex[1]))
        adjacentIndices.append((previousIndex[0] - 1,previousIndex[1]))
        return_list = []
        for x,y in adjacentIndices:
            if x >= 0 and x <= 3 and y >= 0 and y <= 3:
                return_list.append((x,y))
        return return_list
    def _in_board_starting_at(self, validIndices, used_indices, remainingWord):
        if len(remainingWord) == 0:
            return True
        for i,j in validIndices:
            new_used_indices = used_indices[:]
            if remainingWord[0] == 'Q' and remainingWord[1] == 'U':
                compare_letter = 'QU'
            else:
                compare_letter = remainingWord[0]
            if compare_letter == str(self.board[i][j]):
                new_used_indices.append((i,j))
                newValidIndices = self._adjacent_indices((i,j))[:]
                for (i,j) in new_used_indices:
                    if (i,j) in newValidIndices:
                        newValidIndices.remove((i,j))
                if self._in_board_starting_at(newValidIndices, new_used_indices, remainingWord[1:]):
                    return True
        return False            
    def in_board(self, user_word):
        board_check = user_word.upper()
        validIndices = []
        for i in range(4):
            for j in range(4):
                validIndices.append((i,j))
        used_indices = []
        return self._in_board_starting_at(validIndices, used_indices, board_check)
    def score_word(self, user_word):
        if len(user_word) > 2:
            if self.in_board(user_word):
                if twl.check(user_word.lower()):
                    print("Word is valid.")
                    if len(user_word) < 5:
                        return 1
                    elif len(user_word) == 5:
                        return 2
                    elif len(user_word) == 6:
                        return 5
                    elif len(user_word) == 7:
                        return 4
                    else:
                        return 11
                else: 
                    print('That is not a valid word.')
                    return -1
            else:
                print('That word is not in the game board.')
                return -1
        else:
            print('Word must be at least 3 letters long.')
            return -1
    def countdown(self, t):
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end ='\r')
            time.sleep(1)
            t -= 1
if __name__ == '__main__':
    boggle_cubes = []
    for cube in cubes:
        boggle_cubes.append(BoggleCube(cube)) 
    game = BoggleBoard(boggle_cubes)
    game.shake()
    print(game)
    user_word = None
    user_score = 0
    used_words = []
    while True:
        user_word = input('Please enter a word or enter 0 to stop:').upper()
        if user_word == '0':
            print('Goodbye!')
            break
        if user_word in used_words:
            print('Word already used. Running score: ' + str(user_score) + ' points')
            word_score = 0
        else:
            word_score = game.score_word(user_word)
            user_score += word_score
            if word_score > 0:
                used_words.append(user_word.upper())
                print('That word scored ' + str(word_score) + ' points. Running score: ' + str(user_score) + ' points')
            else:
                print('Running score: ' + str(user_score) + ' points')

    
    
    
    
    
    
    
    