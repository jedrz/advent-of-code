#!/usr/bin/env python
# -*- coding: utf-8 -*-


import itertools


def part_1(input_filename):
    with open(input_filename) as f:
        grid = parse_tiles_grid(f)
        start_pos = find_start_position(grid)
        return extend_paths(grid, start_pos)


def parse_tiles_grid(lines):
    return {(x, y): tile
            for y, line in enumerate(lines)
            for x, tile in enumerate(line)}


def find_start_position(grid):
    for position, tile in grid.items():
        if tile == 'S':
            return position


def extend_paths(grid, start_pos):
    distances = {start_pos: 0}
    is_not_visited = lambda pos: pos not in distances
    current_positions = extend_position(grid, start_pos)
    for pos in current_positions:
        distances[pos] = 1
    while current_positions:
        current_pos = current_positions[0]
        current_positions = current_positions[1:]
        next_positions = list(filter(is_not_visited, extend_position(grid, current_pos)))
        for next_pos in next_positions:
            distances[next_pos] = distances[current_pos] + 1
        current_positions += next_positions
    return max(distances.values())


def extend_position(grid, current_pos):
    x, y = current_pos
    next_positions = [adj_pos
                      for x_offset, y_offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]
                      if (adj_pos := (x + x_offset, y + y_offset)) in grid \
                          and can_go_from(grid[adj_pos], (x_offset, y_offset))]
    return next_positions


def can_go_from(tile, offset):
    match (tile, offset):
        case '|', ((0, -1) | (0, 1)):
            return True
        case '-', ((-1, 0) | (1, 0)):
            return True
        case 'L', ((0, 1) | (-1, 0)):
            return True
        case 'J', ((0, 1) | (1, 0)):
            return True
        case '7', ((0, -1) | (1, 0)):
            return True
        case 'F', ((0, -1) | (-1, 0)):
            return True
    return False



