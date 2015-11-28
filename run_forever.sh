#!/bin/bash

while [ 1 ]; do ./backgammon.py -w backgammon.bots.random_tactic -b backgammon.bots.random_tactic --no-gui | tee -a matches ; done
