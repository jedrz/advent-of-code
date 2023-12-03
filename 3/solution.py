#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import re


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
                # last digit in row
                if is_last_col and can_be_part_number():
                    part_numbers += [int(current_digits)]
            else:
                # current char non digit but previous one was
                if current_digits and can_be_part_number():
                    part_numbers += [int(current_digits)]
                current_digits = ''
    return sum(part_numbers)


def part_1_alt(input_filename: str):
    with open(input_filename) as f:
        board = [line.rstrip() for line in f]
        size = len(board[0])
        only_symbols_positions = {(r, c)
                                  for r in range(size)
                                  for c in range(size)
                                  if not board[r][c].isdigit() and board[r][c] != '.'}

        part_numbers = []

        for row_idx, row in enumerate(board):
            for number_match in re.finditer(r'\d+', row):
                surroundings_positions = {(r, c)
                                          for r in range(row_idx - 1, row_idx + 2)
                                          for c in range(number_match.start() - 1, number_match.end() + 1)}
                if surroundings_positions & only_symbols_positions:
                    part_numbers += [int(number_match.group())]

        print(sum(part_numbers))
