#!/usr/bin/env python
# -*- coding: utf-8 -*-


def part_1(input_filename):
    with open(input_filename) as f:
        grid = parse_grid(f)
        print(calculate_load_north(grid))


def part_2(input_filename):
    with open(input_filename) as f:
        grid = parse_grid(f)
        cycled_grid = cycle(grid, 1000000000)
        print(calculate_load(cycled_grid))


def parse_grid(f):
    return flip([l.strip() for l in f.readlines()])


def flip(lines):
    flipped = ['' for _ in lines[0]]
    for line in lines:
        for i, c in enumerate(line):
            flipped[i] += c
    return tuple(flipped)


def rotate(lines):
    flipped = ['' for _ in lines[0]]
    for line in lines:
        for i, c in enumerate(reversed(line)):
            flipped[i] += c
    return tuple(flipped)


def calculate_load(grid):
    load = 0
    for column in grid:
        for i, c in enumerate(reversed(column)):
            if c == 'O':
                load += i + 1
    return load


def calculate_load_north(grid):
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


def tilt_north(grid):
    tilted_grid = []
    for column in grid:
        by_cube_shaped_rock = column.split('#')
        # Sort . and O so that O is the first char.
        tilted_column = '#'.join([''.join(sorted(to_cube_shaped_rock, reverse=True))
                                 for to_cube_shaped_rock
                                 in by_cube_shaped_rock])
        tilted_grid.append(tilted_column)
    return tuple(tilted_grid)


def cycle(grid, times):
    grid_to_step = {}
    steps = 0
    #print(f'Step {steps}')
    #print_grid(grid)
    while not grid in grid_to_step:
        grid_to_step[grid] = steps
        for _ in range(4):
            grid = rotate(tilt_north(grid))
        #print(f'Step {steps}')
        #print_grid(grid)
        steps += 1
    #print(f'Found cycle in {steps} steps')
    cycles = steps - grid_to_step[grid]
    #print(f'Cycle length: {cycles}')
    #print(f'Cycle starts after: {grid_to_step[grid]}')
    for _ in range((times - steps) % cycles):
        for _ in range(4):
            grid = rotate(tilt_north(grid))
    #print_grid(grid)
    return grid


def print_grid(grid):
    print('\n'.join(flip(grid)))
    print()
