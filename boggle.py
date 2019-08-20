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
import curses
import string
import threading

game_title = [
    "██████╗  ██████╗  ██████╗  ██████╗ ██╗     ███████╗",
    "██╔══██╗██╔═══██╗██╔════╝ ██╔════╝ ██║     ██╔════╝",
    "██████╔╝██║   ██║██║  ███╗██║  ███╗██║     █████╗  ",
    "██╔══██╗██║   ██║██║   ██║██║   ██║██║     ██╔══╝  ",
    "██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝███████╗███████╗",
    "╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚══════╝"
]


class BoggleCube(object):
    def __init__(self, letters):
        self.letters = letters[:]
        self.topletter = random.choice(letters)

    def roll(self):
        self.topletter = random.choice(self.letters)

    def __str__(self):
        return self.topletter

    def __repr__(self):
        return self.__str__()


CUBES = [['R', 'I', 'F', 'O', 'B', 'X'], ['I', 'F', 'E', 'H', 'E', 'Y'],
         ['D', 'E', 'N', 'O', 'W', 'S'], ['U', 'T', 'O', 'K', 'N', 'D'],
         ['H', 'M', 'S', 'R', 'A', 'O'], ['L', 'U', 'P', 'E', 'T', 'S'],
         ['A', 'C', 'I', 'T', 'O', 'A'], ['Y', 'L', 'G', 'K', 'U', 'E'],
         ['QU', 'B', 'M', 'J', 'O', 'A'], ['E', 'H', 'I', 'S', 'P', 'N'],
         ['V', 'E', 'T', 'I', 'G', 'N'], ['B', 'A', 'L', 'I', 'Y', 'T'],
         ['E', 'Z', 'A', 'V', 'N', 'D'], ['R', 'A', 'L', 'E', 'S', 'C'],
         ['U', 'W', 'I', 'L', 'R', 'G'], ['P', 'A', 'C', 'E', 'M', 'D']]


class BoggleBoard(object):
    def __init__(self, boggle_cubes):
        self.build_board(boggle_cubes)

    def build_board(self, boggle_cubes):
        self.row_one = boggle_cubes[:4]
        self.row_two = boggle_cubes[4:8]
        self.row_three = boggle_cubes[8:12]
        self.row_four = boggle_cubes[12:16]
        self.board = [self.row_one, self.row_two,
                      self.row_three, self.row_four]

    #To print a visual BoggleBoard object to the console for inspection
    def __str__(self):
        board = ''
        for row in self.board:
            for cube in row:
                board += '[' + str(cube) + ']'
            board += '\n'
        return board

    def cube_at(self, row, column):
        return self.board[row][column]

    def shake(self):
        shuffle_list = []
        for row in self.board:
            for cube in row:
                cube.roll()
                shuffle_list.append(cube)
        random.shuffle(shuffle_list)
        self.build_board(shuffle_list)

    #Returns a list of valid adjacent indices given an index on the board
    def _adjacent_indices(self, reference_index):
        adjacent_indices = []
        adjacent_indices.append((reference_index[0], reference_index[1] - 1))
        adjacent_indices.append((reference_index[0], reference_index[1] + 1))
        adjacent_indices.append((reference_index[0] + 1, reference_index[1] + 1))
        adjacent_indices.append((reference_index[0] - 1, reference_index[1] + 1))
        adjacent_indices.append((reference_index[0] + 1, reference_index[1] - 1))
        adjacent_indices.append((reference_index[0] - 1, reference_index[1] - 1))
        adjacent_indices.append((reference_index[0] + 1, reference_index[1]))
        adjacent_indices.append((reference_index[0] - 1, reference_index[1]))
        valid_adjacent_indices = []
        for row, col in adjacent_indices:
            if row >= 0 and row <= 3 and col >= 0 and col <= 3:
                valid_adjacent_indices.append((row, col))
        return valid_adjacent_indices

    def _in_board_starting_at(self, valid_indices,
                              used_indices, remaining_word):
        if len(remaining_word) == 0:
            return True
        for i, j in valid_indices:
            new_used_indices = used_indices[:]
            if remaining_word[0] == 'Q' and remaining_word[1] == 'U':
                compare_letter = 'QU'
                letters_matched = 2
            else:
                compare_letter = remaining_word[0]
                letters_matched = 1
            if compare_letter == str(self.board[i][j]):
                new_used_indices.append((i, j))
                new_valid_indices = self._adjacent_indices((i, j))[:]
                for (i, j) in new_used_indices:
                    if (i, j) in new_valid_indices:
                        new_valid_indices.remove((i, j))
                if self._in_board_starting_at(new_valid_indices,
                                              new_used_indices,
                                              remaining_word[letters_matched:]):
                    return True
        return False

    def in_board(self, user_word):
        board_check = user_word.upper()
        valid_indices = []
        for i in range(4):
            for j in range(4):
                valid_indices.append((i, j))
        used_indices = []
        return self._in_board_starting_at(valid_indices, used_indices,
                                          board_check)


class BoggleDisplay(object):
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLUE, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)

        #Set dimensions

        #Outer window dimensions
        main_height = 46
        main_width = 79
        main_begin_y = 1
        main_begin_x = 1

        #Cube size
        cube_height = 3
        cube_width = 5

        #Boggle board dimensions
        board_y_margin = 1
        board_x_margin = 2
        board_y_space = 0
        board_x_space = 1

        #Make outer window
        self.mainWindow = curses.newwin(main_height, main_width, main_begin_y,
                                        main_begin_x)
        self.mainWindow.border()

        #Print title art
        title_begin_x = (main_width - len(game_title[0])) // 2
        for line in range(len(game_title)):
            self.mainWindow.addstr(2 + line, title_begin_x, game_title[line],
                                   curses.color_pair(1))
        self.mainWindow.refresh()

        #Make boggle board window
        board_height = cube_height * 4 + 2 * board_y_margin + 3 * board_y_space
        board_width = cube_width * 4 + 2 * board_x_margin + 3 * board_x_space
        board_begin_y = ((main_height - board_height) // 2) - 2
        board_begin_x = (main_width - board_width) // 2 + 1
        self.boardWindow = curses.newwin(board_height, board_width,
                                         board_begin_y, board_begin_x)
        self.boardWindow.border()
        self.boardWindow.refresh()

        #Make boggle cube windows
        self.cube_windows = []
        for row in range(4):
            cube_row = []
            for column in range(4):
                cube_start_y = (board_begin_y + board_y_margin +
                                (row * cube_height) + (row * board_y_space))
                cube_start_x = (board_begin_x + board_x_margin +
                                (column * cube_width) +
                                (column * board_x_space))
                cube_window = curses.newwin(cube_height, cube_width,
                                            cube_start_y, cube_start_x)
                cube_window.border()
                cube_window.refresh()
                cube_row.append(cube_window)
            self.cube_windows.append(cube_row)

        #Make user interaction window
        ui_height = 15
        ui_width = main_width - 4
        ui_begin_y = main_height - ui_height
        ui_begin_x = main_begin_x + 2
        self.ui_window = curses.newwin(ui_height, ui_width, ui_begin_y,
                                       ui_begin_x)
        self.ui_window.border()
        self.ui_window.refresh()

        #Make wordlist window
        wordlist_height = 20
        wordlist_width = 23
        wordlist_begin_y = ui_begin_y - wordlist_height
        wordlist_begin_x = ui_begin_x
        self.wordlist_window = curses.newwin(wordlist_height, wordlist_width,
                                             wordlist_begin_y,
                                             wordlist_begin_x)
        self.wordlist_window.border()
        self.wordlist_window.addstr(0, 5, " WORDS USED ", curses.color_pair(1))
        self.scroll_win = self.wordlist_window.derwin(wordlist_height - 2,
                                                      wordlist_width - 2, 1, 1)
        self.scroll_win.scrollok(True)
        self.scroll_win.idlok(True)
        self.wordlist_window.refresh()

        #Make timer window
        timer_height = 5
        timer_width = 23
        timer_begin_y = wordlist_begin_y + 4
        timer_begin_x = board_begin_x + board_width + 1
        self.timer_window = curses.newwin(timer_height, timer_width,
                                          timer_begin_y, timer_begin_x)
        self.timer_window.border()
        self.timer_window.addstr(0, 6, " TIME LEFT ", curses.color_pair(1))
        self.timer_window.refresh()

        #Make score window
        score_height = 5
        score_width = 23
        score_begin_y = timer_begin_y + 7
        score_begin_x = board_begin_x + board_width + 1
        self.score_window = curses.newwin(score_height, score_width,
                                          score_begin_y, score_begin_x)
        self.score_window.border()
        self.score_window.addstr(0, 8, " SCORE ", curses.color_pair(1))
        self.score_window.refresh()

        #Initialize game display data members
        self.used_word_count = 0

    def used_word(self, word):
        if self.used_word_count < 18:
            word_begin_y = self.used_word_count
        else:
            word_begin_y = 17
            self.scroll_win.scroll(1)
        self.scroll_win.addstr(word_begin_y, 1, word)
        self.used_word_count += 1
        self.scroll_win.refresh()

    def close(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def set_time(self, time):
        self.timer_window.addstr(2, (23 - len(time) + 1) // 2, time)
        self.timer_window.refresh()

    def set_score(self, score, high_score):
        self.score_window.addstr(2, (23 - len(str(score)) + 1) // 2,
                                 str(score))
        self.score_window.refresh()

    def set_user_message(self, feedback, prompt):
        self.ui_window.clear()
        self.ui_window.border()
        self.ui_window.addstr(1, 2, feedback)
        for string in range(len(prompt)):
            self.ui_window.addstr(3 + string, 2, prompt[string])
        self.ui_window.refresh()

    def display_cubes(self, board, color=0):
        for row in range(4):
            for column in range(4):
                win = self.cube_windows[row][column]
                cube_str = str(board.cube_at(row, column))
                win.addstr(1, 2, "  ")
                win.addstr(1, 2, cube_str, curses.color_pair(color))
                win.refresh()


class BoggleGame(object):
    def __init__(self):
        #Initialize the display
        self.display = BoggleDisplay()

    def run_menu(self):
        while True:
            self.feedback = "Welcome to Boggle!"
            self.prompt = [
                "Please select from the following options: ", "",
                "PRESS [1] to Begin a New Game", "PRESS [2] to See Game Rules",
                "PRESS [3] to Quit"
            ]
            curses.curs_set(0)
            self.display.set_user_message(self.feedback, self.prompt)
            while True:
                response = chr(self.display.ui_window.getch())
                if response == "1":
                    self.run_game()
                    self.display.close()
                    return
                elif response == "2":
                    rules = [
                        "Make as many words as you can out of the letters" +
                        " on the Boggle board in",
                        "three minutes. Words are formed by combining adjacent"
                        + " letters in a row, ", "without repeating letters." +
                        " Words can be formed using any combination of ",
                        "directions, including diagonals.", "",
                        "Longer words score more points! One point is deducted"
                        + " for entering a",
                        "word that isn't in the board or " +
                        "isn't a real word.", "",
                        "Press any key to return to menu."
                    ]
                    user_key = 0
                    while not user_key:
                        self.display.set_user_message(
                            "BOGGLE: Rules of the Game", rules)
                        curses.curs_set(0)
                        user_key = self.display.ui_window.getch()
                    break
                elif response == "3":
                    self.display.set_user_message("Goodbye!", [])
                    time.sleep(1)
                    self.display.close()
                    sys.exit()
                else:
                    self.feedback = "Please enter a valid selection!"
                    self.display.set_user_message(self.feedback, self.prompt)

    def pretty_time(self):
        minutes = self.time_remaining // 60
        ten_sec = (self.time_remaining - (minutes * 60)) // 10
        unit_sec = (self.time_remaining - (minutes * 60) - (ten_sec * 10))
        return str(minutes) + ":" + str(ten_sec) + str(unit_sec)

    def run_timer(self):
        while self.time_remaining:
            time.sleep(1)
            self.time_remaining -= 1
            self.display.set_time(self.pretty_time())

    def score_word(self, user_word):
        if len(user_word) == 0:
            return 0
        if len(user_word) > 2:
            if user_word in self.used_words:
                self.feedback = "Word already used."
                return 0
            if self.game.in_board(user_word):
                if twl.check(user_word.lower()):
                    if len(user_word) < 5:
                        word_score = 1
                    elif len(user_word) == 5:
                        word_score = 2
                    elif len(user_word) == 6:
                        word_score = 3
                    elif len(user_word) == 7:
                        word_score = 4
                    else:
                        word_score = 11
                    self.feedback = ("Your word " + '"' + user_word + '"' +
                                     " scored " + str(word_score) + " points!")
                    return word_score
                else:
                    self.feedback = 'That is not a valid word.'
                    return -1
            else:
                self.feedback = 'That word is not in the game board.'
                return -1
        else:
            self.feedback = 'Word must be at least 3 letters long.'
            return -1

    def run_game(self, high_score=0):

        #Initialize all data members
        self.user_score = 0
        self.used_words = []
        self.time_remaining = 180  # 3 minutes in seconds
        self.my_cubes = []
        self.high_score = high_score
        self.feedback = "Good luck!"

        #Display starting values (score of 0, time of 3:00, etc.)
        self.display.set_user_message("", [])
        self.display.set_time(self.pretty_time())
        time.sleep(1)
        self.display.set_score(self.user_score, self.high_score)
        time.sleep(1)

        #Initialize board, shuffle and display countdown and board
        self.display.set_user_message("Game will begin in", [])
        time.sleep(1)
        boggle_cubes = []
        for cube in CUBES:
            boggle_cubes.append(BoggleCube(cube))
        self.game = BoggleBoard(boggle_cubes)
        self.game.shake()
        self.display.set_user_message("Game will begin in 3...", [])
        self.display.display_cubes(self.game, 1)
        time.sleep(1)
        self.game.shake()
        self.display.set_user_message("Game will begin in 3... 2...", [])
        self.display.display_cubes(self.game, 2)
        time.sleep(1)
        self.game.shake()
        self.display.set_user_message("Game will begin in 3... 2... 1...", [])
        self.display.display_cubes(self.game, 3)
        time.sleep(1)
        self.game.shake()
        self.display.set_user_message(
            "Game will begin in 3... 2... 1... START!", [])
        self.display.display_cubes(self.game)

        #Begin running and handle display of timer
        threading.Thread(target=self.run_timer).start()

        #Accept and process user-entered words
        while self.time_remaining > 0:
            self.display.set_user_message(
                self.feedback, ["Enter a word. Press ENTER to submit: "])
            curses.echo()
            self.user_word = self.display.ui_window.getstr().decode("utf-8")
            #Process self.user_word
            word_score = self.score_word(self.user_word)
            self.user_score += word_score
            self.display.set_score(self.user_score, self.high_score)
            if word_score > 0:
                self.used_words.append(self.user_word)
                self.display.used_word(self.user_word)

        #When time is out, end game, present final score, and display endscreen
        self.feedback = "Time is up!"
        self.prompt = [
            "You scored " + str(self.user_score) + " points.", "",
            "Press any key to quit."

        user_key = 0
        while not user_key:
            self.display.set_user_message(self.feedback, self.prompt)
            user_key = self.display.ui_window.getch()


if __name__ == '__main__':

    my_game = BoggleGame()
    my_game.run_menu()
