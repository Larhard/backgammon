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
import threading

from backgammon.model.game import Game

log = logging.getLogger('Judge')


class Judge:
    def __init__(self, game_is_running_cv):
        super().__init__()

        self._game_is_running_cv = game_is_running_cv

    def update(self, observable):
        if observable.winner is not None:
            with self._game_is_running_cv:
                self._game_is_running_cv.notify_all()


def main(white, black, *args, **kwargs):
    game_is_running_cv = threading.Condition()

    with game_is_running_cv:
        game = Game()
        judge = Judge(game_is_running_cv)
        game.add_observer(judge)

        bots = []
        bots.append(white(game.get_player('w')))
        bots.append(black(game.get_player('b')))

        game.set_changed()
        game.notify_observers()

        game_is_running_cv.wait_for(lambda: game.winner is not None)

        print(game.winner)
