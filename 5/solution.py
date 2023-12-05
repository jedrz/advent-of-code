#!/usr/bin/env python
# -*- coding: utf-8 -*-


from dataclasses import dataclass
from typing import Optional


@dataclass
class LocationRange:
    destination_start: int
    source_start: int
    range_length: int

    def lookup(self, start_location: int) -> Optional[int]:
        if start_location >= self.source_start \
           and start_location <= self.source_start + self.range_length:
            return start_location + self.destination_start - self.source_start
        return None


@dataclass
class LocationMap:
    name: str
    ranges: list[LocationRange]

    def lookup(self, start_location: int) -> int:
        for r in self.ranges:
            if destination_location := r.lookup(start_location):
                return destination_location
        return start_location


def part12(input_filename: str):
    with open(input_filename) as f:
        input = f.read()
        splitted_input = input.split('\n\n')
        seeds = parse_seeds(splitted_input[0])
        seed_ranges = parse_seed_ranges(splitted_input[0])
        location_maps = list(map(parse_map, splitted_input[1:]))
        print(solve1(seeds, location_maps))
        print(solve2(seed_ranges, location_maps))


def parse_seeds(line: str) -> list[int]:
    return list(map(int, line.removeprefix('seeds: ').split()))


def parse_seed_ranges(line: str) -> list[range]:
    seeds_str = line.removeprefix('seeds: ')
    numbers = list(map(int, seeds_str.split()))
    ranges = []
    for r in range(0, len(numbers), 2):
        [start, length] = numbers[r:r + 2]
        ranges.append(range(start, start + length))
    return ranges


def parse_map(text: str) -> LocationMap:
    splitted = text.split('\n')
    name = splitted[0]
    ranges = []
    for range_description in splitted[1:]:
        if range_description:
            range_components = list(map(int, range_description.split()))
            ranges.append(LocationRange(range_components[0], range_components[1], range_components[2]))
    return LocationMap(name, ranges)


def solve1(seeds: list[int], location_maps: list[LocationMap]):
    return min(map(lambda seed: find_location(seed, location_maps), seeds))


def find_location(seed: int, location_maps: list[LocationMap]) -> int:
    location = seed
    for location_map in location_maps:
        location = location_map.lookup(location)
    return location


def solve2(seed_ranges: list[range], location_maps: list[LocationMap]) -> int:
    return min(find_location(seed, location_maps)
               for seed_range in seed_ranges
               for seed in seed_range)
