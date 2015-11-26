# Copyright (c) 2015, Bartlomiej Puget <larhard@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#   * Neither the name of the Bartlomiej Puget nor the names of its
#     contributors may be used to endorse or promote products derived from this
#     software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL BARTLOMIEJ PUGET BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import itertools as it
import random

from copy import copy

from utils.math import signum


def roll_dice():
    return random.randint(1, 6)


def players():
    return ['w', 'b']


def player_modifier(player):
    return 1 if player == 'w' else -1


def player_from_number(count):
    modifier = signum(count)

    if modifier == 0:
        return None

    return 'w' if modifier == 1 else 'b'


def jail_field(player):
    return 0 if player == 'w' else 25


def non_home_fields(player):
    return slice(1, 19) if player == 'w' else slice(7, 25)


def goes_offboard(player, k):
    return k > 24 if player == 'w' else k < 1


def enemy(player):
    return 'b' if player == 'w' else 'w'


def valid_distance(player):
    return range(0, 7) if player == 'w' else range(-6, 1)


def board_range():
    return range(1, 25)


def board_slice():
    return slice(1, 25)


def get_winner(board):
    white_checkers = sum(k for k in board if k < 0)
    black_checkers = sum(k for k in board if k > 0)

    if white_checkers == 0:
        return 'w'

    if black_checkers == 0:
        return 'b'

    return None


def verify_move(board, position, distance, player):
    distance = distance * player_modifier(player)
    new_position = position + distance

    if position not in board_range() \
            and position != jail_field(player):
        return False

    if distance not in valid_distance(player):
        return False

    if position in board_range() \
            and signum(board[position]) != player_modifier(player):
        return False

    if position == jail_field(player) \
            and board[jail_field(player)] == 0:
        return False

    if board[jail_field(player)] and position != jail_field(player):
        return False

    if goes_offboard(player, new_position):
        for field in board[non_home_fields(player)]:
            if player_from_number(field) == player:
                return False

    if not goes_offboard(player, new_position) \
            and board[new_position] * player_modifier(enemy(player)) > 1:
        return False

    return True


def make_move(board, position, distance, player):
    if not verify_move(board, position, distance, player):
        return None

    new_position = position + distance * player_modifier(player)
    board = board.copy()
    checker = player_modifier(player)

    board[position] -= checker
    if new_position in board_range():
        if signum(board[new_position] == player_modifier(enemy(player))):
            board[jail_field(enemy(player))] += board[new_position]
            board[new_position] = 0
        board[new_position] += checker

    return board


def is_any_legal_move(board, dice, player):
    if board[jail_field(player)]:
        for distance in dice:
            if verify_move(board, jail_field(player), distance, player):
                return True
    else:
        for position in board_range():
            for distance in dice:
                if verify_move(board, position, distance, player):
                    return True
    return False


def player_fields(board, player):
    for i, field in enumerate(board):
        if player_from_number(player) == player:
            yield i


def available_moves(board, dices, player, history=[]):
    yielded = False

    if not dices:
        yielded = True
        yield copy(history), copy(board)

    for dice in dices:
        new_dices = list(dices)
        new_dices.remove(dice)
        new_history = list(history)

        for position in range(0, 26):
            new_history.append((position, dice))
            new_board = make_move(board, position, dice, player)
            if new_board is not None:
                for h, b in available_moves(new_board, new_dices, player,
                        new_history):
                    yielded = True
                    yield h, b
            new_history.pop()

    if not yielded:
        yield copy(history), copy(board)
