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

import os

WINDOW_TITLE = 'Backgammon'

BOARD_SIZE = (720, 640)
CHECKER_SIZE = (48, 48)

FIELD_COORD = [
    (639, 559),
    (589, 559),
    (540, 559),
    (491, 559),
    (442, 559),
    (392, 559),
    (281, 559),
    (231, 559),
    (182, 559),
    (132, 559),
    (83, 559),
    (34, 559),
    (34, 34),
    (83, 34),
    (132, 34),
    (182, 34),
    (231, 34),
    (281, 34),
    (392, 34),
    (442, 34),
    (491, 34),
    (540, 34),
    (589, 34),
    (639, 34),
]

FIELD_SHIFT = [(0, -20)] * 12 + [(0, 20)] * 12

JAIL_COORD = {
    'w': (-18, 500),
    'b': (688, 500),
}
JAIL_SHIFT = {
    'w': (0, -20),
    'b': (0, -20),
}
JAIL_SIZE = (48, 300)

ROW_SIZE = (48, 200)

RESOURCE_DIR = '{}/resources'.format(os.path.dirname(__file__))