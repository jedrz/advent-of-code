#!/usr/bin/env python
# -*- coding: utf-8 -*-


def part_1(input_filename):
    with open(input_filename) as f:
        init_seq = f.read().strip().split(',')
        print(sum(map(calculate_hash, init_seq)))


def calculate_hash(s):
    current = 0
    for c in s:
        current += ord(c)
        current *= 17
        current %= 256
    return current
