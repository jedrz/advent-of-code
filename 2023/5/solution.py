#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional
from pprint import pprint


@dataclass
class SeedRange:
    start: int
    end: int

    def __post_init__(self):
        assert self.start < self.end, f'{self.start} < {self.end}'

    def as_range(self) -> range:
        return range(self.start, self.end)

    @classmethod
    def from_start_range(cls, start: int, range_length: int):
        return SeedRange(start, start + range_length)


@dataclass
class LocationRange:
    # end is exclusive
    destination_start: int
    destination_end: int
    source_start: int
    source_end: int

    def __post_init__(self):
        assert self.source_start < self.source_end, f'{self.source_start} < f{self.source_end}'
        assert self.destination_start < self.destination_end, f'{self.destination_start} < {self.destination_end}'

    @classmethod
    def from_dest_source_range(cls,
                               destination_start: int,
                               source_start: int,
                               range_length: int):
        return LocationRange(destination_start, destination_start + range_length,
                             source_start, source_start + range_length)

    @classmethod
    def identity_range(cls, start: int, end: int):
        return LocationRange(start, end, start, end)

    @property
    def difference(self):
        return self.destination_start - self.source_start

    def lookup(self, start_location: int) -> Optional[int]:
        if start_location >= self.source_start \
           and start_location < self.source_end:
            return start_location + self.difference
        return None

    def flow(self, seed_range: SeedRange) -> Optional[SeedRange]:
        adj_start = max(self.source_start, seed_range.start)
        adj_end = min(self.source_end, seed_range.end)
        if adj_start < adj_end:
            return SeedRange(adj_start + self.difference, adj_end + self.difference)


class LocationMap:

    def __init__(self, name, mapping_ranges):
        self.name = name
        mapping_ranges = list(sorted(mapping_ranges, key=lambda r: r.source_start))
        self.ranges = []
        if mapping_ranges[0].source_start > 0:
            self.ranges += [
                LocationRange.identity_range(0, mapping_ranges[0].source_start)
            ]
        for before_range, after_range in zip(mapping_ranges, mapping_ranges[1:]):
            self.ranges += [before_range]
            if before_range.source_end < after_range.source_start:
                self.ranges += [LocationRange.identity_range(before_range.source_end, after_range.source_start)]
        self.ranges += [
            mapping_ranges[-1]
        ]
        max_end = 100
        if mapping_ranges[-1].source_end < max_end:
            self.ranges += [
                LocationRange.identity_range(mapping_ranges[-1].source_end, max_end)
            ]

    def lookup(self, start_location: int) -> int:
        for r in self.ranges:
            if destination_location := r.lookup(start_location):
                return destination_location
        return start_location


    def flow(self, seed_range: SeedRange) -> list[SeedRange]:
        result = []
        for r in self.ranges:
            if range_seed := r.flow(seed_range):
                result.append(range_seed)
        #print(f'from {seed_range}')
        #print(f'to {result}')
        return result


    def __repr__(self):
        return f"""LocationMap(
          {self.name},
          {pprint(self.ranges)}
        )
        """


def part12(input_filename: str):
    with open(input_filename) as f:
        input = f.read()
        splitted_input = input.split('\n\n')
        seeds = parse_seeds(splitted_input[0])
        seed_ranges = parse_seed_ranges(splitted_input[0])
        location_maps = list(map(parse_map, splitted_input[1:]))
        print(solve1(seeds, location_maps))
        #print(solve2_bruteforce(seed_ranges, location_maps))
        print(solve2(seed_ranges, location_maps))


def parse_seeds(line: str) -> list[int]:
    return list(map(int, line.removeprefix('seeds: ').split()))


def parse_seed_ranges(line: str) -> list[SeedRange]:
    seeds_str = line.removeprefix('seeds: ')
    numbers = list(map(int, seeds_str.split()))
    ranges = []
    for r in range(0, len(numbers), 2):
        [start, length] = numbers[r:r + 2]
        ranges.append(SeedRange.from_start_range(start, length))
    return ranges


def parse_map(text: str) -> LocationMap:
    splitted = text.split('\n')
    name = splitted[0]
    ranges = []
    for range_description in splitted[1:]:
        if range_description:
            range_components = list(map(int, range_description.split()))
            ranges.append(LocationRange.from_dest_source_range(range_components[0], range_components[1], range_components[2]))
    return LocationMap(name, ranges)


def solve1(seeds: list[int], location_maps: list[LocationMap]):
    return min(map(lambda seed: find_location(seed, location_maps), seeds))


def find_location(seed: int, location_maps: list[LocationMap]) -> int:
    location = seed
    for location_map in location_maps:
        location = location_map.lookup(location)
    return location


def solve2_bruteforce(seed_ranges: list[SeedRange], location_maps: list[LocationMap]) -> int:
    return min(find_location(seed, location_maps)
               for seed_range in seed_ranges
               for seed in seed_range.as_range())


def solve2(seed_ranges: list[SeedRange], location_maps: list[LocationMap]) -> int:
    #pprint(location_maps)
    expanded = flow_ranges(seed_ranges, location_maps)
    return list(sorted(expanded, key=lambda r: r.start))[0].start


def flow_ranges(seed_ranges: list[SeedRange], location_maps: list[LocationMap]) -> list[SeedRange]:
    result = []
    for seed_range in seed_ranges:
        result += flow(seed_range, location_maps)
    return result


def flow(seed_range: SeedRange, location_maps: list[LocationMap]) -> list[SeedRange]:
    if not location_maps:
        return [seed_range]
    return flow_ranges(location_maps[0].flow(seed_range), location_maps[1:])
