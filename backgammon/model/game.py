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
import threading

from backgammon.model.config import INIT_BOARD

from backgammon.model.utils import make_move
from backgammon.model.utils import get_winner
from backgammon.model.utils import is_any_legal_move
from backgammon.model.utils import roll_dice
from backgammon.model.utils import player_modifier
from backgammon.model.utils import enemy

from utils.observable import Observable

log = logging.getLogger('model')


class Game(Observable):
    class LogicError(Exception):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class Player(Observable):
        def __init__(self, game, color):
            super().__init__()

            self._game = game
            self._color = color
            self._game.add_observer(self)

        def __enter__(self):
            pass

        def __exit__(self, exc_type, exc_value, exl_traceback):
            self._game.remove_observer(self)

        def move(self, position, distance):
            self._game.move(self._color, position, distance)

        def update(self, observable):
            assert observable is self._game
            self.set_changed()
            self.notify_observers()

        def is_active(self):
            return self._game.active_player == self._color

        @property
        def color(self):
            return self._color

    def __init__(self, _dice_roller=None, _starting_player=None, _board=None):
        super().__init__()

        self._game_mutex = threading.RLock()
        self._board = _board or INIT_BOARD.copy()
        self._active_player = _starting_player \
            or random.sample(('w', 'b'), 1)[0]

        self._roll_dice = _dice_roller or (lambda: (roll_dice(), roll_dice()))

        self._dice = list(self._roll_dice())

    @property
    def board(self):
        return self._board.copy()

    @property
    def active_player(self):
        return self._active_player

    @property
    def dice(self):
        return self._dice.copy()

    def move(self, color, position, distance):
        with self._game_mutex:
            player = self._active_player
            board = self._board
            dice = self._dice

            if get_winner(board) is not None:
                self._active_player = None
                raise Game.LogicError('game has ended')

            if color != player:
                raise Game.LogicError('not players turn')

            if abs(distance) not in dice:
                raise Game.LogicError('move is invalid')

            new_board = make_move(board, position, distance, player)

            if new_board is None:
                raise Game.LogicError('move is invalid')

            self._board = new_board
            dice.remove(abs(distance))

            if len(dice) == 0:
                self._next_player()
            elif not is_any_legal_move(self._board, self._dice,
                    self._active_player):
                self._next_player()

            log.debug("{}: move {} {}".format(color, position, distance))

            self.set_changed()
            self.notify_observers()

    def _next_player(self):
        if get_winner(self._board) is None:
            with self._game_mutex:
                self._active_player = enemy(self._active_player)
                self._dice = list(self._roll_dice())
                if not is_any_legal_move(self._board, self._dice,
                        self._active_player):
                    self._next_player()

    def get_player(self, color):
        assert color in ('w', 'b')
        return Game.Player(self, color)

    @property
    def winner(self):
        return Game.get_winner(self._board)

    def __str__(self):
        return str(self.board)
