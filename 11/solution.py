#!/usr/bin/env python
# -*- coding: utf-8 -*-


import itertools
import numpy


def part_1(input_filename):
    with open(input_filename) as f:
        lines_split = [list(line.rstrip()) for line in f]
        universe = numpy.array(lines_split)
        print(sum_all_galaxies_length(expand(universe)))


def expand(universe):
    max_x, max_y = universe.shape
    x_indices = [x for x in range(max_x) if set(universe[x]) == {'.'}]
    y_indices = [y for y in range(max_y) if set(universe[:,y]) == {'.'}]
    x_expanded = numpy.insert(universe, x_indices, '.', axis=0)
    expanded = numpy.insert(x_expanded, y_indices, '.', axis=1)
    return expanded


def sum_all_galaxies_length(universe):
    galaxy_positions = [(pos[0].item(), pos[1].item()) for pos in numpy.nditer(numpy.where(universe == '#'))]
    galaxy_pairs = itertools.combinations(galaxy_positions, 2)
    s = 0
    for (g1, g2) in galaxy_pairs:
        s += manhattan_distance(g1, g2)
    return s


def manhattan_distance(p1, p2):
    return sum([abs(c1 - c2) for c1, c2 in zip(p1, p2)])


