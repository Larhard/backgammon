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

import logging
import random

from backgammon.model.config import INIT_BOARD

log = logging.getLogger('model')


class Game:
    class LogicError(Exception):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class Player:
        def __init__(self, game, color):
            self._game = game
            self._color = color

        def move(self, position, distance):
            self._game.move(self._color, position,
                            Game.distance_modifier(self._color) * distance)

    def __init__(self):
        self._board = INIT_BOARD.copy()
        # self._active_player = random.sample(('w', 'b'), 1)[0]
        self._active_player = 'w'
        self._dice = self._roll_dice()
        self._jail = {'w': [], 'b': []}

    @staticmethod
    def _roll_dice():
        return [random.randint(1, 6), random.randint(1, 6)]

    @property
    def board(self):
        return self._board.copy()

    @property
    def jail(self):
        return self._jail.copy()

    @property
    def active_player(self):
        return self._active_player

    @property
    def dice(self):
        return self._dice.copy()

    @staticmethod
    def distance_modifier(player):
        return 1 if player == 'w' else -1

    @staticmethod
    def jail_field(player):
        return -1 if player == 'w' else 24

    @staticmethod
    def non_home_fields(player):
        return slice(0, 18) if player == 'w' else slice(6, 24)

    @staticmethod
    def goes_offboard(player, k):
        return k >= 24 if player == 'w' else k < 0

    @staticmethod
    def enemy(player):
        return 'b' if player == 'w' else 'w'

    @staticmethod
    def valid_distance(player):
        return range(0, 7) if player == 'w' else range(-6, 1)

    @staticmethod
    def board_range():
        return range(0, 24)

    @staticmethod
    def winner(board, jail):
        for color in ('w', 'b'):
            if sum(k.count(color) for k in board) + len(jail[color]) == 0:
                return color
        return None

    @staticmethod
    def verify_move(board, jail, position, distance, player):
        new_position = position + distance

        if position not in Game.board_range() \
                and position != Game.jail_field(player):
            log.info('{}: invalid position'.format(player))
            return False

        if distance not in Game.valid_distance(player):
            log.info('{}: invalid distance {}'.format(player, distance))
            return False

        if position in Game.board_range() and player not in board[position]:
            log.info('{}: no player in position {}'.format(player, position))
            return False

        if position == Game.jail_field(player) \
                and player not in jail[player]:
            log.info('{}: no player in jail'.format(player))
            return False

        if len(jail[player]) > 0 and position != Game.jail_field(player):
            log.info('{}: player is in jail'.format(player))
            return False

        if Game.goes_offboard(player, new_position):
            log.debug("{}".format(sum(field.count(player) for field
                      in board[Game.non_home_fields(player)])))
            result = sum(field.count(player) for field
                         in board[Game.non_home_fields(player)]) == 0
            if not result:
                log.info('{}: can not go offboard'.format(player))
            return result

        log.debug('{} {}'.format(new_position, Game.goes_offboard(player,
                  new_position)))
        if not Game.goes_offboard(player, new_position) \
                and board[new_position].count(Game.enemy(player)) > 1:
            log.info('enemy door')
            return False

        return True

    @staticmethod
    def is_any_legal_move(board, jail, dice, player):
        modifier = Game.distance_modifier(player)

        if player in jail[player]:
            for distance in dice:
                if Game.verify_move(board, jail, Game.jail_field(player),
                                    modifier * distance, player):
                    return True
        else:
            for position in Game.board_range():
                for distance in dice:
                    if Game.verify_move(board, jail, position,
                                        modifier * distance, player):
                        return True
        return False

    def move(self, color, position, distance):
        new_position = position + distance
        player = self._active_player
        enemy = Game.enemy(player)
        board = self._board
        dice = self._dice
        jail = self._jail

        if Game.winner(board, jail) is not None:
            log.info('{}: game has ended'.format(player))
            raise Game.LogicError('game has ended')

        if color != player:
            log.info('{}: not players turn'.format(player))
            raise Game.LogicError('not players turn')

        if abs(distance) not in dice:
            log.info('{}: distance {} not in dice'.format(player, distance))
            raise Game.LogicError('move is invalid')

        if not self.verify_move(board, jail, position, distance, player):
            raise Game.LogicError('move is invalid')

        dice.remove(abs(distance))
        if position == Game.jail_field(player):
            jail[player].pop()
        else:
            board[position].pop()

        if not Game.goes_offboard(player, new_position):
            if Game.enemy(player) in board[new_position]:
                jail[enemy].extend(board[new_position])
                board[new_position].clear()
            if not Game.goes_offboard(player, new_position):
                board[new_position].append(player)

        if len(dice) == 0:
            self.next_player()
        elif not Game.is_any_legal_move(self._board, self._jail, self._dice,
                                        self._active_player):
            self.next_player()

    def next_player(self):
        self._active_player = Game.enemy(self._active_player)
        self._dice = self._roll_dice()
        if not Game.is_any_legal_move(self._board, self._jail, self._dice,
                                      self._active_player):
            self.next_player()

    def get_player(self, color):
        return Game.Player(self, color)
