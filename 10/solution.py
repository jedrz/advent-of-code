#!/usr/bin/env python
# -*- coding: utf-8 -*-


import itertools


def part_1(input_filename):
    with open(input_filename) as f:
        grid = parse_tiles_grid(f)
        start_pos = find_start_position(grid)
        return extend_paths(grid, [[start_pos]])


def parse_tiles_grid(lines):
    return {(x, y): tile
            for y, line in enumerate(lines)
            for x, tile in enumerate(line)}


def find_start_position(grid):
    for position, tile in grid.items():
        if tile == 'S':
            return position


def extend_path_once(grid, path):
    current_pos = path[-1]
    (x, y) = current_pos
    next_positions = [adj_pos
                      for x_offset, y_offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]
                      if (adj_pos := (x + x_offset, y + y_offset)) not in path \
                          and adj_pos in grid \
                          and can_go_from(grid[adj_pos], (x_offset, y_offset))]
    return [path + [next_pos] for next_pos in next_positions]


def extend_paths(grid, paths):
    extended_paths_once = list(itertools.chain(*[extend_path_once(grid, path) for path in paths]))
    last_positions = [extended_path[-1] for extended_path in extended_paths_once]
    for last_pos in last_positions:
        if last_positions.count(last_pos) > 1:
            return len(extended_paths_once[0]) - 1
    return extend_paths(grid, extended_paths_once)


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



