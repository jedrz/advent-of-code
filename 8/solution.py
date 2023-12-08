#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import itertools


def part_1(input_filename):
    with open(input_filename) as f:
        lines = f.readlines()
        instructions = lines[0].strip()
        network = parse_network(lines[2:])
        print(solve1(instructions, network))


def parse_network(lines):
    line_regex = r"(\w+) = \((\w+), (\w+)\)"
    network = {}
    for line in lines:
        m = re.search(line_regex, line)
        network[m.group(1)] = {
            'L': m.group(2),
            'R': m.group(3),
        }
    return network


def solve1(instructions, network):
    moves = 0
    next = 'AAA'
    end = 'ZZZ'
    for ins in itertools.cycle(instructions):
        if next == end:
            break
        next = network[next][ins]
        moves += 1
    return moves
