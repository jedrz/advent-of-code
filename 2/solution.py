#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import StrEnum
from typing import TypeAlias


CubeColor = StrEnum('CubeColor', ['red', 'green', 'blue'])


# str should be CubeColor
CubesSet: TypeAlias = dict[str, int]

@dataclass
class Game:
    id: int
    revealed_sets: list[CubesSet]


cubes_in_bag = {
    CubeColor.red: 12,
    CubeColor.green: 13,
    CubeColor.blue: 14,
}

empty_cubes_in_bag = {
    CubeColor.red: 0,
    CubeColor.green: 0,
    CubeColor.blue: 0,
}


def part1(input_filename: str):
    with open(input_filename) as f:
        games = parse_games(f)
        return solve1(games)


def parse_games(lines) -> list[Game]:
    return list(map(parse_game, lines))


def parse_game(input: str) -> Game:
    input = input.rstrip().removeprefix('Game ')
    (game_id, _, cubes_sets_str) = input.partition(':')
    cubes_set_str_list = cubes_sets_str.lstrip().split('; ')
    cubes_set_list = list(map(parse_cubes_set, cubes_set_str_list))
    return Game(int(game_id), cubes_set_list)


def parse_cubes_set(input: str) -> CubesSet:
    return dict(map(parse_cubes_count, input.split(', ')))


def parse_cubes_count(input: str) -> tuple[str, int]:
    (count, color) = input.split(' ')
    return (color, int(count))


def solve1(games: list[Game]) -> int:
    possible_games = filter(is_possible_game, games)
    possible_game_ids = map(lambda game: game.id, possible_games)
    return sum(possible_game_ids)


def is_possible_game(game: Game) -> bool:
    for cubes_set in game.revealed_sets:
        for color, count in cubes_set.items():
            if count > cubes_in_bag[color]:
                return False
    return True


def part2(input_filename: str):
    with open(input_filename) as f:
        games = parse_games(f)
        return solve2(games)


def solve2(games: list[Game]) -> int:
    minimal_power_of_games = map(find_minimal_power, games)
    return sum(minimal_power_of_games)


def find_minimal_power(game: Game) -> int:
    minimal_cubes_in_bag = empty_cubes_in_bag
    for cubes_set in game.revealed_sets:
        minimal_cubes_in_bag = {
            CubeColor.red: max(cubes_set.get(CubeColor.red, 0), minimal_cubes_in_bag[CubeColor.red]),
            CubeColor.green: max(cubes_set.get(CubeColor.green, 0), minimal_cubes_in_bag[CubeColor.green]),
            CubeColor.blue: max(cubes_set.get(CubeColor.blue, 0), minimal_cubes_in_bag[CubeColor.blue]),
        }

    power = 1
    for count in minimal_cubes_in_bag.values():
        power *= count
    return power
