#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import re

@dataclass
class Card:
    winning_numbers: set[int]
    owned_numbers: set[int]

    def score(self) -> int:
        mutual_numbers = list(self.winning_numbers & self.owned_numbers)
        match mutual_numbers:
            case []:
                return 0
            case more_than_one:
                return 2 ** (len(more_than_one) - 1)


def part1(input_filename: str) -> int:
    with open(input_filename) as f:
        cards = map(parse_card, f)
        return sum(map(lambda card: card.score(), cards))


def parse_card(line: str) -> Card:
    m = re.match(r'Card\W*\d+:(.*)\|(.*)', line)
    return Card(extract_numbers(m.group(1)), extract_numbers(m.group(2)))


def extract_numbers(numbers_str: str) -> set[int]:
    return set(map(int, numbers_str.strip().split()))
