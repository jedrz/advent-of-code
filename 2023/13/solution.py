#!/usr/bin/env python
# -*- coding: utf-8 -*-


def part_1_and_2(input_filename):
    with open(input_filename) as f:
        patterns = [parse_pattern(input_part)
                    for input_part in f.read().split('\n\n')]
        print(sum(count_reflection(pattern) for pattern in patterns))
        print(sum(count_reflection_smudge(pattern) for pattern in patterns))


def parse_pattern(pattern_s):
    return pattern_s.split()


def count_reflection(pattern):
    return find_horizontal_reflection(flip_pattern(pattern)) \
        + 100 * find_horizontal_reflection(pattern)


def count_reflection_smudge(pattern):
    return find_horizontal_reflection_smudge(flip_pattern(pattern)) \
        + 100 * find_horizontal_reflection_smudge(pattern)


def find_horizontal_reflection(pattern):
    for i in range(1, len(pattern)):
        j = min(i, len(pattern) - i)
        before = list(reversed(pattern[:i]))[:j]
        after = pattern[i:i + j]
        if before == after:
            return i
    return 0

def find_horizontal_reflection_smudge(pattern):
    for i in range(1, len(pattern)):
        j = min(i, len(pattern) - i)
        before = list(reversed(pattern[:i]))[:j]
        after = pattern[i:i + j]
        if can_fix_smudge(before, after):
            return i
    return 0


def can_fix_smudge(before, after):
    differences = 0
    for c_before, c_after in zip(''.join(before), ''.join(after)):
        if c_before != c_after:
            differences += 1
        if differences > 1:
            return False
    return differences == 1


def flip_pattern(pattern):
    flipped_pattern = ['' for _ in pattern[0]]
    for line in pattern:
        for i, c in enumerate(line):
            flipped_pattern[i] += c
    return flipped_pattern
