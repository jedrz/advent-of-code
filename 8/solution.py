#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import itertools


def part_1_and_2(input_filename):
    with open(input_filename) as f:
        lines = f.readlines()
        instructions = lines[0].strip()
        network = parse_network(lines[2:])
        #print(solve1(instructions, network))
        print(solve2(instructions, network))


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


def solve2(instructions, network):
    nexts = find_starting_nodes(network)
    moves_list = []
    for next in nexts:
        moves = 0
        for ins in itertools.cycle(instructions):
            if is_ending_node(next):
                moves_list.append(moves)
                break
            next = network[next][ins]
            moves += 1
    return find_least_common_multiplier(moves_list)


def find_starting_nodes(network):
    return [node for node in network.keys() if node.endswith('A')]


def all_are_ending_nodes(nodes):
    return all(node.endswith('Z') for node in nodes)


def is_ending_node(node):
    return node.endswith('Z')


def find_least_common_multiplier(numbers):
    # Found online LCM calculator for the below numbers :P
    print(numbers)
    multipliers = {n: n for n in numbers}
    while not all((min_multiplier := min(multipliers.keys())) % n == 0 for n in numbers):
        next_multiplier = min_multiplier + (number := multipliers[min_multiplier])
        multipliers.pop(min_multiplier)
        multipliers[next_multiplier] = number
    return min(multipliers.keys())
