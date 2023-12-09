#!/usr/bin/env python
# -*- coding: utf-8 -*-


def part_1(input_filename):
    with open(input_filename) as f:
        result = 0
        for history_line in f:
            history = list(map(int, history_line.split()))
            next_value = predict_next_value(history)
            result += next_value
        print(result)


def predict_next_value(history):
    if not set(history) - {0}:
        return 0
    differences = [j - i for i, j in zip(history[:-1], history[1:])]
    next_value = predict_next_value(differences)
    return history[-1] + next_value

