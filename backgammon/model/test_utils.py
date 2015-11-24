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

import copy
import unittest

import backgammon.model.utils as utils
import backgammon.model.config as config


class TestUtils(unittest.TestCase):
    def test_player_modifier(self):
        self.assertEqual(utils.player_modifier('w'), 1)
        self.assertEqual(utils.player_modifier('b'), -1)

    def test_goes_offboard(self):
        self.assertFalse(utils.goes_offboard('w', 24))
        self.assertTrue(utils.goes_offboard('w', 25))
        self.assertFalse(utils.goes_offboard('b', 1))
        self.assertTrue(utils.goes_offboard('b', 0))

    def test_enemy(self):
        self.assertEqual(utils.enemy('w'), 'b')
        self.assertEqual(utils.enemy('b'), 'w')

    def test_bard_range(self):
        self.assertTrue(utils.goes_offboard('w', utils.board_range().stop))
        self.assertFalse(utils.goes_offboard('w', utils.board_range().stop-1))
        self.assertTrue(utils.goes_offboard('b', utils.board_range().start-1))
        self.assertFalse(utils.goes_offboard('b', utils.board_range().start))

    def test_get_winner(self):
        board = [0] * 26

        b = copy.deepcopy(board)
        b[3] = 1
        self.assertEqual(utils.get_winner(b), 'w')

        b = copy.deepcopy(board)
        b[3] = -1
        self.assertEqual(utils.get_winner(b), 'b')

        b = copy.deepcopy(board)
        b[4] = 1
        b[3] = -1
        self.assertIsNone(utils.get_winner(b))

    def test_is_any_legal_move(self):
        board = [0] * 26

        b = copy.deepcopy(board)
        b[0] = 1
        b[1] = -2
        b[2] = -2
        b[3] = -2
        b[4] = -2
        b[5] = -2
        b[6] = -2
        b[12] = 3

        self.assertFalse(utils.is_any_legal_move(b, (3, 5), 'w'))

        b = copy.deepcopy(board)
        b[0] = 1
        b[1] = -2
        b[2] = -2
        b[3] = -1
        b[4] = -2
        b[5] = -2
        b[6] = -2
        b[12] = 3

        self.assertTrue(utils.is_any_legal_move(b, (3, 5), 'w'))

    def test_make_move_white(self):
        player = 'w'
        start = 1
        modifier = utils.player_modifier(player)

        board_start = config.INIT_BOARD.copy()

        board_end = config.INIT_BOARD.copy()
        board_end[start] -= modifier
        board_end[start + modifier] += modifier

        self.assertEqual(utils.make_move(board_start, start, 1, player),
                board_end)

    def test_make_move_black(self):
        player = 'b'
        start = 6
        modifier = utils.player_modifier(player)

        board_start = config.INIT_BOARD.copy()

        board_end = config.INIT_BOARD.copy()
        board_end[start] -= modifier
        board_end[start + modifier] += modifier

        self.assertEqual(utils.make_move(board_start, start, 1, player),
                board_end)

    def test_make_invalid_move_black(self):
        player = 'b'
        start = 1

        board_start = config.INIT_BOARD.copy()

        self.assertEqual(utils.make_move(board_start, start, 1, player), None)

    def test_make_door(self):
        board = [0] * 26

        p = copy.deepcopy(board)
        p[10] = 1
        p[14] = 1

        q = copy.deepcopy(board)
        q[14] = 2

        self.assertEqual(utils.make_move(p, 10, 4, 'w'), q)

    def test_enter_door(self):
        board = [0] * 26

        p = copy.deepcopy(board)
        p[10] = 1
        p[14] = 2

        q = copy.deepcopy(board)
        q[14] = 3

        self.assertEqual(utils.make_move(p, 10, 4, 'w'), q)

    def test_kill_enemy(self):
        board = [0] * 26

        p = copy.deepcopy(board)
        p[10] = 1
        p[14] = -1

        q = copy.deepcopy(board)
        q[14] = 1
        q[25] = -1

        self.assertEqual(utils.make_move(p, 10, 4, 'w'), q)

    def test_move_into_enemy_door(self):
        board = [0] * 26

        p = copy.deepcopy(board)
        p[10] = 1
        p[14] = -2

        self.assertEqual(utils.make_move(p, 10, 4, 'w'), None)
