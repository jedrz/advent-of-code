#!/usr/bin/env python
# -*- coding: utf-8 -*-


def part_1_and_2(input_filename):
    with open(input_filename) as f:
        result = 0
        result_backwards = 0
        for history_line in f:
            history = list(map(int, history_line.split()))
            next_value = predict_next_value(history)
            next_value_backwards = predict_next_value_backwards(history)
            result += next_value
            result_backwards += next_value_backwards
        print(result)
        print(result_backwards)


def predict_next_value(history):
    if not set(history) - {0}:
        return 0
    differences = [j - i for i, j in zip(history[:-1], history[1:])]
    next_value = predict_next_value(differences)
    return history[-1] + next_value


def predict_next_value_backwards(history):
    if not set(history) - {0}:
        return 0
    differences = [j - i for i, j in zip(history[:-1], history[1:])]
    next_value = predict_next_value_backwards(differences)
    return history[0] - next_value

