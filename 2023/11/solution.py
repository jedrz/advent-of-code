#!/usr/bin/env python
# -*- coding: utf-8 -*-


import itertools
import numpy


def part_1_and_2(input_filename):
    with open(input_filename) as f:
        lines_split = [list(line.rstrip()) for line in f]
        universe = numpy.array(lines_split)
        to_expand = expand(universe)
        print(sum_all_galaxies_length(universe, 2, to_expand))
        print(sum_all_galaxies_length(universe, 1_000_000, to_expand))


def expand(universe):
    max_x, max_y = universe.shape
    x_indices = [x for x in range(max_x) if set(universe[x]) == {'.'}]
    y_indices = [y for y in range(max_y) if set(universe[:,y]) == {'.'}]
    return (x_indices, y_indices)


def sum_all_galaxies_length(universe, expand_by, to_expand):
    galaxy_positions = [(pos[0].item(), pos[1].item()) for pos in numpy.nditer(numpy.where(universe == '#'))]
    galaxy_pairs = itertools.combinations(galaxy_positions, 2)
    s = 0
    for (g1, g2) in galaxy_pairs:
        s += manhattan_distance_expanded(g1, g2, expand_by, to_expand)
    return s


def manhattan_distance(p1, p2):
    return sum([abs(c1 - c2) for c1, c2 in zip(p1, p2)])


def manhattan_distance_expanded(p1, p2, expand_by, to_expand):
    return sum([abs(c1 - c2) + (expand_by - 1) * count_between(min(c1, c2), max(c1, c2), to_expand_axis)
                for c1, c2, to_expand_axis in zip(p1, p2, to_expand)])


def count_between(a, b, elems):
    # kind of range tree could be used
    return len(list(e for e in elems if a < e < b))
