#!/usr/bin/env python
# -*- coding: utf-8 -*-


def part1(filename: str) -> int:
    with open(filename) as f:
        calibration_value_sum = sum(map(calibration_value, f))
        return calibration_value_sum


def calibration_value(text: str) -> int:
    first_digit = next(filter(lambda c: c.isdigit(), text))
    last_digit = next(filter(lambda c: c.isdigit(), reversed(text)))
    return int(f'{first_digit}{last_digit}')


def part2(filename: str) -> int:
    with open(filename) as f:
        calibration_value_sum = sum(map(calibration_value_with_spelled_letters_alt, f))
        return calibration_value_sum


word_digits = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

word_digits_rev = {word[::-1]: digit for word, digit in word_digits.items()}


def calibration_value_with_spelled_letters_alt(text: str) -> int:
    hacked = text
    [hacked := hacked.replace(word, f'{word}{digit}{word}')
     for word, digit in word_digits.items()]
    return calibration_value(hacked)


def calibration_value_with_spelled_letters(text: str) -> int:
    first_digit = find_best_digit(text, word_digits)
    last_digit = find_best_digit(text[::-1], word_digits_rev)
    return int(f'{first_digit}{last_digit}')


def find_best_digit(text: str, word_digits: dict[str, str]) -> int:
    best_index = len(text)
    best_digit = -1
    for word, digit in word_digits.items():
        word_index = text.find(word)
        if word_index != -1 and word_index < best_index:
            best_index = word_index
            best_digit = int(digit)
        digit_index = text.find(digit)
        if digit_index != -1 and digit_index < best_index:
            best_index = digit_index
            best_digit = int(digit)
    return best_digit
