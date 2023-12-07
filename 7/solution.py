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


hand_type_checks_with_joker = {
    "Five of a kind": lambda hand: is_hand_type_with_joker(hand, [5]),
    "Four of a kind": lambda hand: is_hand_type_with_joker(hand, [1, 4]),
    "Full house": lambda hand: is_hand_type_with_joker(hand, [2, 3]),
    "Three of a kind": lambda hand: is_hand_type_with_joker(hand, [1, 1, 3]),
    "Two pair": lambda hand: is_hand_type_with_joker(hand, [1, 2, 2]),
    "One pair": lambda hand: is_hand_type_with_joker(hand, [1, 1, 1, 2]),
    "High card": lambda hand: is_hand_type_with_joker(hand, [1, 1, 1, 1, 1]),
}


def is_hand_type_with_joker(hand, expected_card_counts):
    for possible_hand in generate_cards(hand):
        if is_hand_type(possible_hand, expected_card_counts):
            return True
    return False


def generate_cards(hand_with_joker):
    for card_index, card in enumerate(hand_with_joker):
        if card == joker:
            for possible_card in possible_cards_without_joker:
                left_part = hand_with_joker[:card_index]
                right_part = hand_with_joker[card_index + 1:]
                for left_possible_part in generate_cards(left_part):
                    for right_possible_part in generate_cards(right_part):
                        new_hand = left_possible_part + possible_card + right_possible_part
                        yield new_hand
    yield hand_with_joker


cards_strength = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
cards_strength_with_joker = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
possible_cards_without_joker = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
joker = 'J'


def cmp_stronger_hand_with(cards_strength):

    def cmp_stronger_hand(hand1, hand2):
        for c1, c2 in zip(hand1, hand2):
            i1  = cards_strength.index(c1)
            i2 = cards_strength.index(c2)
            if i1 < i2:
                return -1
            elif i1 > i2:
                return 1
        return 0

    return cmp_stronger_hand


def part_1_and_2(input_filename):
    with open(input_filename) as f:
        hands_bids = parse_input(f)
        print(solve1(hands_bids))
        print(solve2(hands_bids))


def parse_input(lines):
    return [parse_hand_bid(l) for l in lines]


def parse_hand_bid(line):
    [hand, bid_s] = line.split()
    bid = int(bid_s)
    return (hand, bid)


def solve1(hands_bids):
    cmp_hand = cmp_hand_with(hand_type_checks, cmp_stronger_hand_with(cards_strength))
    return solve_with(hands_bids, cmp_hand)


def solve2(hands_bids):
    cmp_hand = cmp_hand_with(hand_type_checks_with_joker, cmp_stronger_hand_with(cards_strength_with_joker))
    return solve_with(hands_bids, cmp_hand)


def solve_with(hands_bids, cmp_hand):
    sorted_hands_bids = reversed(sorted(hands_bids, key=lambda hand_bid: functools.cmp_to_key(cmp_hand)(hand_bid[0])))
    total_winnings = 0
    for index, (_, bid) in enumerate(sorted_hands_bids):
        rank = index + 1
        total_winnings += rank * bid
    return total_winnings


def cmp_hand_with(hand_type_checks, cmp_stronger_hand):

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

    return cmp_hand
