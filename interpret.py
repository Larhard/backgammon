#!/usr/bin/python3

import collections


def main():
    result = collections.defaultdict(lambda: 0)
    tactics = set()

    with open('matches', 'r') as matches_file:
        while True:
            white_line = matches_file.readline()[2:]
            if not white_line:
                break
            black_line = matches_file.readline()[2:]
            white = frozenset(eval(white_line))
            black = frozenset(eval(black_line))
            winner_line = matches_file.readline()

            tactics.add(white)
            tactics.add(black)

            if 'w' in winner_line:
                result[(white, black)] += 1
            elif 'b' in winner_line:
                result[(black, white)] += 1

    print("{:100}".format(""), end=' ')

    for second in tactics:
        print("{:100}".format(str(second)), end=' ')
    print()

    for first in tactics:
        print("{:100}".format(str(first)), end=' ')
        for second in tactics:
            print("{:100}".format(result.get((first, second, ), 0)), end=' ')
        print()

if __name__ == '__main__':
    main()
