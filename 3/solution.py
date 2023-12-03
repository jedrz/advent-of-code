#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy


def part1(input_filename: str) -> int:
    schematic = read_schematic(input_filename)
    return solve1(schematic)


def read_schematic(input_filename: str):
    with open(input_filename) as f:
        lines_split = [list(line.rstrip()) for line in f]
        return numpy.array(lines_split)


def solve1(matrix) -> int:
    part_numbers = []
    current_digits = ''
    (rows_no, cols_no) = matrix.shape
    for row_index in range(rows_no):
        current_digits = ''
        for col_index in range(cols_no):
            is_last_col = col_index == cols_no - 1
            char = matrix[row_index][col_index]
            is_digit = char.isdigit()

            def can_be_part_number() -> bool:
                end_row_idx = min(row_index + 1, rows_no - 1)
                end_col_idx = col_index
                start_row_idx = max(row_index - 1, 0)
                start_col_idx = max(col_index + (1 if is_digit else 0) - len(current_digits) - 1, 0)
                print(current_digits, is_last_col)
                print(start_row_idx, end_row_idx + 1, start_col_idx, end_col_idx + 1)
                part_area = matrix[start_row_idx:end_row_idx + 1, start_col_idx:end_col_idx + 1]
                surroudings_elems = part_area.flatten().tolist()
                print(part_area)
                return any(c != '.' and not c.isdigit() for c in surroudings_elems)

            if is_digit:
                current_digits += char
                #print(char, current_digits, row_index, col_index)
            # last digit in row
            elif is_digit \
                 and is_last_col \
                 and can_be_part_number():
                part_numbers += [int(current_digits)]
            # current char non digit but previous one was
            elif current_digits \
                 and can_be_part_number():
                part_numbers += [int(current_digits)]
                current_digits = ''
            else:
                current_digits = ''
    return sum(part_numbers)
