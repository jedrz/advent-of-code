#!/usr/bin/env python
# -*- coding: utf-8 -*-


from collections import namedtuple


Energized = namedtuple('Energized', ['pos', 'direction'])


def part_1(input_filename):
    with open(input_filename) as f:
        grid = parse_grid(f)
        print(energize(grid))


def parse_grid(lines):
    return {(x, y): c
            for y, line in enumerate(lines)
            for x, c in enumerate(line.strip())}


def energize(grid):
    visited = set()
    queue = [Energized(pos=(-1, 0), direction=(1, 0))]

    while queue:
        energized = queue.pop()
        if energized in visited:
            continue
        visited |= {energized}
        pos, direction = energized
        next_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if next_pos in grid:
            element = grid[next_pos]
            #print(energized, element)
            if element == '.':
                queue.append(Energized(next_pos, direction))
            elif element == '/':
                queue.append(Energized(next_pos, (-direction[1], -direction[0])))
            elif element == '\\':
                queue.append(Energized(next_pos, (direction[1], direction[0])))
            elif element == '|':
                if direction[1] != 0:
                    queue.append(Energized(next_pos, direction))
                else:
                    queue.append(Energized(next_pos, (0, 1)))
                    queue.append(Energized(next_pos, (0, -1)))
            elif element == '-':
                if direction[0] != 0:
                    queue.append(Energized(next_pos, direction))
                else:
                    queue.append(Energized(next_pos, (1, 0)))
                    queue.append(Energized(next_pos, (-1, 0)))

    return len(set(map(lambda energized: energized.pos, visited))) - 1
