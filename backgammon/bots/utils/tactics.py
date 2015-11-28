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

import random

from backgammon.model.utils import player_modifier
from backgammon.model.utils import jail_field
from backgammon.model.utils import enemy
from backgammon.model.utils import player_from_number


def tactic_killer(board, player):
    result = 0

    result += board[jail_field(enemy(player))] \
        - board[jail_field(player)]

    return result / 15


def tactic_push_forward(board, player):
    modifier = player_modifier(player)
    result = 0

    player_checkers = 0
    enemy_checkers = 0
    push_forward = 0

    for i, k in enumerate(board):
        if player_from_number(k) == player:
            push_forward += ((26 + modifier * i) % 26) * k / 28
            player_checkers += k
        elif player_from_number(k) == enemy(player):
            enemy_checkers += k
            push_forward -= ((26 + modifier * i) % 26) * k / 28

    push_forward -= player_checkers + enemy_checkers

    result += push_forward

    return result / 15


def tactic_doors(board, player):
    modifier = player_modifier(player)
    result = 0

    player_singles = 0
    enemy_singles = 0

    for k in board[1:25]:
        if k == modifier:
            player_singles += 1
        elif k == -modifier:
            enemy_singles += 1

    result -= player_singles - enemy_singles

    return result / 15


def tactic_random(board, player):
    return random.random() * 2 - 1
