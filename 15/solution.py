#!/usr/bin/env python
# -*- coding: utf-8 -*-


from collections import defaultdict
from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class Step:
    label: str
    operation: str
    focal_length: Optional[int]

    @property
    def box_no(self):
        return calculate_hash(self.label)


def part_1_and_2(input_filename):
    with open(input_filename) as f:
        init_seq = f.read().strip().split(',')
        print(sum(map(calculate_hash, init_seq)))
        print(calc_focusing_power(map(parse_step, init_seq)))


def calculate_hash(s):
    current = 0
    for c in s:
        current += ord(c)
        current *= 17
        current %= 256
    return current


def parse_step(s):
    m = re.match(r"(\w+)(=|-)(\d*)", s)
    return Step(m.group(1),
                m.group(2),
                int(m.group(3)) if m.group(3) else None)


def calc_focusing_power(init_seq):
    boxes = defaultdict(lambda: {})

    for step in init_seq:
        if step.operation == '-':
            lenses = boxes[step.box_no]
            if step.label in lenses:
                del lenses[step.label]
        elif step.operation == '=':
            lenses = boxes[step.box_no]
            lenses[step.label] = step.focal_length

    focusing_power = 0
    for box, lenses in boxes.items():
        for slot, focal_length in enumerate(lenses.values()):
            focusing_power += (box + 1) * (slot + 1) * focal_length
    return focusing_power
