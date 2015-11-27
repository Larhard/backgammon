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

from backgammon.model.utils import player_from_number
from backgammon.model.utils import available_moves


class MinMax:
    def __init__(self, evaluate, levels):
        self.evaluate = evaluate
        self.levels = levels

    def maximize(self, board, level=0, previous_value=None):
        modifier = 1 if level % 2 == 0 else -1
        if level == self.levels:
            return self.evaluate(board)

        result = 0
        for dices in it.combinations_with_replacement(range(1, 7), 2):
            multiplier = 1/36 if dices[0] == dices[1] else 1/18
            max_value = modifier * -2**31

            for _, possible_board in available_moves(board, dices,
                    player_from_number(modifier)):
                possible_board_value = self.maximize(possible_board, level+1,
                        max_value)
                if modifier * max_value < modifier * possible_board_value:
                    max_value = possible_board_value

                if previous_value is not None \
                        and modifier * max_value <= modifier * previous_value:
                    return max_value

            result += modifier * multiplier * max_value

        return result
