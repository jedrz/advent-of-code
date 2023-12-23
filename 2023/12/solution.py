#!/usr/bin/env python
# -*- coding: utf-8 -*-


from dataclasses import dataclass
import functools


@dataclass
class SpringsConditions:
    conditions: str
    damaged_groups: tuple[int]


def part_1(input_filename):
    with open(input_filename) as f:
        inputs = [parse_input(line) for line in f]
        print(sum(calculate_arrangements(input) for input in inputs))
        print(sum(calculate_arrangements_count(input.conditions, input.damaged_groups) for input in inputs))


def part_2(input_filename):
    with open(input_filename) as f:
        inputs = [parse_input(unfold_input(line)) for line in f]
        print(sum(calculate_arrangements_count(input.conditions, input.damaged_groups) for input in inputs))


def parse_input(line):
    [conditions, damaged_groups_s] = line.strip().split()
    damaged_groups = tuple(map(int, damaged_groups_s.split(',')))
    return SpringsConditions(conditions, damaged_groups)


def unfold_input(line):
    [conditions, damaged_groups] = line.strip().split()
    return '?'.join([conditions] * 5) + ' ' + ','.join([damaged_groups] * 5)


# brute force
def calculate_arrangements(springs_condtions: SpringsConditions) -> int:
    return sum(1
               for possible_conditions
               in generate_possible_conditions(springs_condtions.conditions)
               if is_valid_arrangement(springs_condtions, possible_conditions))


def generate_possible_conditions(conditions: str):
    if not conditions:
        return ['']

    cond = conditions[0]
    rest_conds = conditions[1:]
    all_possible_for_rest = generate_possible_conditions(rest_conds)
    all_possible = []
    for possible_for_rest in all_possible_for_rest:
        if cond == '?':
            all_possible += [
                '#' + possible_for_rest,
                '.' + possible_for_rest
            ]
        else:
            all_possible += [cond + possible_for_rest]
    return all_possible


def is_valid_arrangement(springs_conditions, possible_conditions):
    damaged_groups = tuple(len(c) for c in possible_conditions.split('.') if c)
    return damaged_groups == springs_conditions.damaged_groups


@functools.cache
def calculate_arrangements_count(conditions: str,
                                 damaged_groups: tuple[int],
                                 in_group: bool = False) -> int:
    if not damaged_groups:
        if '#' in conditions:
            return 0
        else:
            return 1
    if not conditions:
        if sum(damaged_groups) > 0:
            return 0
        else:
            return 1

    cond, rest_conds = conditions[0], conditions[1:]
    damaged_group, rest_damaged_groups = damaged_groups[0], damaged_groups[1:]

    if damaged_group == 0:
        if cond == '#':
            return 0
        else:
            return calculate_arrangements_count(rest_conds, rest_damaged_groups, False)
    # if damaged_group > 0:
    if in_group:
        if cond == '.':
            return 0
        else:
            return calculate_arrangements_count(rest_conds,
                                                (damaged_group - 1, ) + rest_damaged_groups,
                                                in_group)
    if cond == '.':
        return calculate_arrangements_count(rest_conds, damaged_groups, False)
    if cond == '#':
        return calculate_arrangements_count(rest_conds,
                                            (damaged_group - 1, ) + rest_damaged_groups,
                                            True)
    # if cond == '?':
    return calculate_arrangements_count(rest_conds, damaged_groups, False) \
        + calculate_arrangements_count(rest_conds, (damaged_group - 1, ) + rest_damaged_groups, True)
