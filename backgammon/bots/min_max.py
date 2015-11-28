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

import threading

from backgammon.bots.utils.minmax import MinMax

from backgammon.model.utils import available_moves


class Bot:
    def __init__(self, player, threaded=True):
        self._player = player
        self.min_max = MinMax(evaluate=self.evaluate, levels=1)
        self._threaded = threaded

        self._player.add_observer(self)

    def update(self, observable):
        assert observable is self._player
        if not self._player.is_active():
            return

        if self._threaded:
            threading.Thread(target=self.move).start()
        else:
            self.move()

    def move(self):
        if not self._player.is_active():
            return

        board = self._player.board
        dice = self._player.dice
        color = self._player.color

        mx = None
        selected_move = None

        for h, b in available_moves(board, dice, color):
            value = self.min_max.maximize(b)
            if mx is None or value > mx:
                mx = value
                selected_move = h

        for position, distance in selected_move:
            self._player.move(position, distance)

    def evaluate(self, board):
        pass
