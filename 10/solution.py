#!/usr/bin/env python
# -*- coding: utf-8 -*-


import itertools
import operator


def part_1_and_2(input_filename):
    with open(input_filename) as f:
        grid = parse_tiles_grid(f)
        start_pos = find_start_position(grid)
        extend_paths(grid, start_pos)


def parse_tiles_grid(lines):
    return {(x, y): tile
            for y, line in enumerate(lines)
            if line.strip()
            for x, tile in enumerate(line.strip())}


def find_start_position(grid):
    for position, tile in grid.items():
        if tile == 'S':
            return position


def extend_paths(grid, start_pos):
    paths = {start_pos: []}
    is_not_visited = lambda pos: pos not in paths
    current_positions = extend_position(grid, start_pos)
    for pos in current_positions:
        paths[pos] = [start_pos]
    while current_positions:
        current_pos = current_positions[0]
        current_positions = current_positions[1:]
        next_positions = list(filter(is_not_visited, extend_position(grid, current_pos)))
        for next_pos in next_positions:
            paths[next_pos] = paths[current_pos] + [current_pos]
        current_positions += next_positions
    print('part1', len(max(paths.values(), key=len)))

    # fill outside
    loop_path = list(itertools.chain(*list(sorted(paths.values(), key=len))[-2:]))
    outside = set(loop_path)
    queue = [pos for pos in grid.keys() if pos in paths]
    grid_size = (max(grid.keys(), key=operator.itemgetter(0))[0] + 1) \
        * (max(grid.keys(), key=operator.itemgetter(1))[1] + 1)
    print(outside)
    print(queue)
    print(grid_size)
    while queue:
        pos = queue.pop(0)
        outside |= set([pos])
        print('outside', outside)
        #print(pos)
        x, y = pos
        next_positions = [adj_pos
                          for x_offset, y_offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]
                          if (adj_pos := (x + x_offset, y + y_offset)) in grid \
                          and adj_pos not in outside \
                          and adj_pos not in queue \
                          and not (pos in loop_path and not can_go_from(adj_pos, (x_offset, y_offset)))]
        queue += next_positions
        print(next_positions)
    print(grid_size - len(outside))

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


