#!/usr/bin/env python
# -*- coding: utf-8 -*-


import functools


# Dict remembers insertion order after Python 3.7
hand_type_checks = {
    "Five of a kind": lambda hand: is_hand_type(hand, [5]),
    "Four of a kind": lambda hand: is_hand_type(hand, [1, 4]),
    "Full house": lambda hand: is_hand_type(hand, [2, 3]),
    "Three of a kind": lambda hand: is_hand_type(hand, [1, 1, 3]),
    "Two pair": lambda hand: is_hand_type(hand, [1, 2, 2]),
    "One pair": lambda hand: is_hand_type(hand, [1, 1, 1, 2]),
    "High card": lambda hand: is_hand_type(hand, [1, 1, 1, 1, 1]),
}


def is_hand_type(hand, expected_card_counts):
    card_types = set(hand)
    counts = sorted([hand.count(card) for card in card_types])
    return counts == expected_card_counts


cards_strength = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']


def cmp_stronger_hand(hand1, hand2):
    for c1, c2 in zip(hand1, hand2):
        i1  = cards_strength.index(c1)
        i2 = cards_strength.index(c2)
        if i1 < i2:
            return -1
        elif i1 > i2:
            return 1
    return 0


def part_1(input_filename):
    with open(input_filename) as f:
        hands_bids = parse_input(f)
        print(solve1(hands_bids))


def parse_input(lines):
    return [parse_hand_bid(l) for l in lines]


def parse_hand_bid(line):
    [hand, bid_s] = line.split()
    bid = int(bid_s)
    return (hand, bid)


def solve1(hands_bids):
    sorted_hands_bids = reversed(sorted(hands_bids, key=lambda hand_bid: functools.cmp_to_key(cmp_hand)(hand_bid[0])))
    total_winnings = 0
    for index, (_, bid) in enumerate(sorted_hands_bids):
        rank = index + 1
        total_winnings += rank * bid
    return total_winnings


def cmp_hand(hand1, hand2):
    for hand_type_check in hand_type_checks.values():
        check1 = hand_type_check(hand1)
        check2 = hand_type_check(hand2)
        if check1 and check2:
            return cmp_stronger_hand(hand1, hand2)
        elif check1:
            return -1
        elif check2:
            return 1
    raise Exception(f'Unexpected hands {hand1}, {hand2}')
