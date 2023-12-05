#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import re
from collections import defaultdict


@dataclass
class Card:
    id: int
    winning_numbers: set[int]
    owned_numbers: set[int]

    def points(self) -> int:
        mutual_numbers = list(self.winning_numbers & self.owned_numbers)
        match mutual_numbers:
            case []:
                return 0
            case more_than_one:
                return 2 ** (len(more_than_one) - 1)

    def count_matching_numbers(self) -> int:
        return len(self.winning_numbers & self.owned_numbers)


def part_1_and_2(input_filename: str):
    with open(input_filename) as f:
        cards = list(map(parse_card, f))
        print(sum(map(lambda card: card.points(), cards)))
        print(solve2(cards))


def parse_card(line: str) -> Card:
    m = re.match(r'Card\W*(\d+):(.*)\|(.*)', line)
    return Card(int(m.group(1)),
                extract_numbers(m.group(2)),
                extract_numbers(m.group(3)))


def extract_numbers(numbers_str: str) -> set[int]:
    return set(map(int, numbers_str.strip().split()))


def solve2(cards: list[Card]) -> int:
    winning_scratchcards = defaultdict(lambda: 0)
    for card in cards:
        winning_scratchcards[card.id] += 1
        for next_card_id in range(card.id + 1, card.id + card.count_matching_numbers() + 1):
            winning_scratchcards[next_card_id] += winning_scratchcards[card.id]
    return sum(winning_scratchcards.values())
