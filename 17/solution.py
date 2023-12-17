#!/usr/bin/env python
# -*- coding: utf-8 -*-


from collections import defaultdict


INF = 1000000000


def part_1_and_2(input_filename):
    with open(input_filename) as f:
        heat_loss_map = parse_heat_loss_map(f)
        print(find_least_heat_loss(heat_loss_map, min_in_same_direction=1, max_in_same_direction=3))
        print(find_least_heat_loss(heat_loss_map, min_in_same_direction=4, max_in_same_direction=10))


def parse_heat_loss_map(lines):
    heat_loss_map = {}
    for y, line in enumerate(lines):
        for x, heat_loss in enumerate(line.strip()):
            heat_loss_map[(x, y)] = int(heat_loss)
    return heat_loss_map


def find_least_heat_loss(heat_loss_map, min_in_same_direction, max_in_same_direction):
    start_pos = (0, 0)
    end_pos = max(heat_loss_map.keys())
    distances = defaultdict(lambda: INF)
    distances[(start_pos, (0, 0))] = 0
    previous = {}
    q = [(start_pos, (0, 0))]

    while q:
        pos, direction = find_with_shortest_distance(q, distances)
        if pos == end_pos:
            return distances[(end_pos, direction)]
        q.remove((pos, direction))
        nexts = get_nexts(heat_loss_map, pos, direction, min_in_same_direction, max_in_same_direction)
        for next_pos, next_dir, next_heat_loss in nexts:
            if distances[(next_pos, next_dir)] > (better_distance := distances[(pos, direction)] + next_heat_loss):
                distances[(next_pos, next_dir)] = better_distance
                previous[(next_pos, next_dir)] = (pos, direction)
                q.append((next_pos, next_dir))

    raise BaseException('Should not happen')


def find_with_shortest_distance(q, distances):
    return min(q, key=distances.get)


def get_nexts(heat_loss_map, pos, direction, min_in_same_direction, max_in_same_direction):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    # Exclude current direction.
    allowed_directions = list(filter(lambda d: d[0] * direction[0] == d[1] * direction[1] == 0, directions))
    possible_nexts = []
    for d in allowed_directions:
        heat_loss = 0
        for times_in_same_dir in range(1, max_in_same_direction + 1):
            next_pos = (pos[0] + d[0] * times_in_same_dir, pos[1] + d[1] * times_in_same_dir)
            if next_pos in heat_loss_map:
                heat_loss += heat_loss_map[next_pos]
                if times_in_same_dir >= min_in_same_direction:
                    possible_nexts += [(next_pos, d, heat_loss)]
    return possible_nexts
