#!/usr/bin/env python
# -*- coding: utf-8 -*-


import queue
from dataclasses import dataclass, field
from typing import Any


INF = 1000000000


@dataclass(order=True)
class PrioritizedPos:
    heat_loss: int
    pos: Any=field(compare=False)


@dataclass
class PreviousItem:
    pos: tuple[int, int]
    direction: tuple[int, int]


def part_1(input_filename):
    with open(input_filename) as f:
        heat_loss_map = parse_heat_loss_map(f)
        print(heat_loss_map)
        print(find_least_heat_loss(heat_loss_map))


def parse_heat_loss_map(lines):
    heat_loss_map = {}
    for y, line in enumerate(lines):
        for x, heat_loss in enumerate(line.strip()):
            heat_loss_map[(x, y)] = int(heat_loss)
    return heat_loss_map


def find_least_heat_loss(heat_loss_map):
    start_pos = (0, 0)
    end_pos = max(heat_loss_map.keys())
    distances = {pos: INF for pos in heat_loss_map.keys()}
    distances[start_pos] = heat_loss_map[start_pos]
    previous = {}
    q = list(heat_loss_map.keys())

    while q:
        pos = find_with_shortest_distance(q, distances)
        if pos == end_pos:
            return distances[end_pos]
        print(pos)
        q.remove(pos)
        nexts = get_nexts(heat_loss_map, previous, pos)
        for next_pos in nexts:
            if distances[next_pos] > (better_distance := distances[pos] + heat_loss_map[next_pos]):
                distances[next_pos] = better_distance
                previous[next_pos] = pos
        print('pos', pos)
        print('nexts', nexts)
        for n in nexts:
            print(n, distances[n])
            print(n, previous[n])

    p = max(heat_loss_map.keys())
    print('path')
    while p in previous:
        p = previous[p]
        print(p)

    return distances[max(heat_loss_map.keys())]


def find_with_shortest_distance(q, distances):
    return min(q, key=distances.get)


def get_nexts(heat_loss_map, previous, pos):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    possible_nexts = [(possible_next, d)
                      for d in directions
                      if (possible_next := get_next(pos, d)) in heat_loss_map]
    nexts = list(filter(lambda possible_next: can_go_from_to(previous, pos, possible_next[1]), possible_nexts))
    return [n[0] for n in nexts]


def can_go_from_to(previous, pos, direction):
    print ('pos can', pos, direction)
    if pos in previous and get_direction(pos, previous[pos]) == direction:
        print('pos first if', pos)
        return False

    max_in_same_direction = 3
    cur_pos = pos
    while max_in_same_direction > 0:
        if cur_pos in previous:
            prev_pos = previous[cur_pos]
            prev_dir = get_direction(prev_pos, cur_pos)
            print('prev', prev_pos, prev_dir)
            if prev_dir != direction:
                return True
            cur_pos = prev_pos
        else:
            return True
        max_in_same_direction -= 1
    print('pos while', pos)
    return False


def get_direction(pos, next_pos):
    return (next_pos[0] - pos[0], next_pos[1] - pos[1])


def get_next(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])
