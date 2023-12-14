#!/usr/bin/env python
# -*- coding: utf-8 -*-


def part_1(input_filename):
    with open(input_filename) as f:
        grid = parse_grid(f)
        print(calculate_load(grid))


def parse_grid(f):
    return flip(f.readlines())


def flip(lines):
    flipped = ['' for _ in lines[0].strip()]
    for line in lines:
        for i, c in enumerate(line.strip()):
            flipped[i] += c
    return flipped


def calculate_load(grid):
    return sum(calculate_single_load(column) for column in grid)


def calculate_single_load(column):
    load = 0
    current_load = len(column)
    last_round_rock_pos = len(column)
    for i, c in enumerate(column):
        row = len(column) - i
        if c == 'O':
            load += last_round_rock_pos
            last_round_rock_pos -= 1
        elif c == '#':
            last_round_rock_pos = row - 1
        current_load -= 1
    return load
