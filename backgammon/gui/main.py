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

import pygame

import backgammon.gui.images as images

from backgammon.gui.config import BOARD_SIZE
from backgammon.gui.config import WINDOW_TITLE
from backgammon.gui.config import FIELD_COORD
from backgammon.gui.config import FIELD_SHIFT
from backgammon.gui.config import CHECKER_SIZE
from backgammon.model.game import Game
from backgammon.model.utils import player_from_number
from utils.math import sum_by_index, multiply_by_value

from backgammon.bots.random.bot import Bot as Bot1
from backgammon.bots.random.bot import Bot as Bot2

log = logging.getLogger('gui')


def main(*args, **kwargs):
    pygame.init()

    screen = pygame.display.set_mode(BOARD_SIZE)
    clock = pygame.time.Clock()

    pygame.display.set_caption(WINDOW_TITLE)

    board = pygame.transform.scale(images.load_image('board.png'), BOARD_SIZE)
    checker = {
        'w': pygame.transform.scale(images.load_image('checker_white.png'),
                                    CHECKER_SIZE),
        'b': pygame.transform.scale(images.load_image('checker_black.png'),
                                    CHECKER_SIZE),
    }

    game = Game()
    human_players = {
        # 'w': game.get_player('w'),
        # 'b': game.get_player('b'),
    }

    bot1 = Bot1(game.get_player('w'))
    bot2 = Bot2(game.get_player('b'))

    is_running = True

    active_dice = 0
    active_dice_text_pos = None

    game.set_changed()
    game.notify_observers()

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

        # print board
        screen.blit(board, (0, 0))

        # print checkers
        for i, row in enumerate(game.board):
            color = player_from_number(row)
            for count in range(abs(row)):
                screen.blit(checker[color], sum_by_index(FIELD_COORD[i],
                            multiply_by_value(FIELD_SHIFT[i], count)))

        # print dices
        font = pygame.font.Font(None, 36)
        dice_text = font.render(str(game.dice), 1, (255, 255, 255))
        dice_text_pos = dice_text.get_rect()
        dice_text_pos.centerx = screen.get_rect().centerx
        dice_text_pos.centery = screen.get_rect().centery
        screen.blit(dice_text, dice_text_pos)

        # print active dice
        font = pygame.font.Font(None, 36)
        dice = game.dice
        active_dice_text = font.render('-> {} <-'.format(
                    dice[active_dice] if dice else ""), 1, (255, 255, 255))
        active_dice_text_pos = active_dice_text.get_rect()
        active_dice_text_pos.centerx = dice_text_pos.centerx
        active_dice_text_pos.midtop = dice_text_pos.midbottom
        screen.blit(active_dice_text, active_dice_text_pos)

        # print active player
        font = pygame.font.Font(None, 36)
        player_text = font.render(str(game.active_player), 1, (255, 255, 255))
        player_text_pos = player_text.get_rect()
        player_text_pos.topright = screen.get_rect().topright
        screen.blit(player_text, player_text_pos)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
