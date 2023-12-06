#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dataclasses
from dataclasses import dataclass
from typing import Optional


@dataclass
class SeedRange:
    start: int
    range_length: int

    @property
    def end(self) -> int:
        return self.start + self.range_length - 1

    def as_range(self) -> range:
        return range(self.start, self.start + self.range_length)

    @classmethod
    def from_start_end(cls, start: int, end: int) -> SeedRange:
        return SeedRange(start, end - start + 1)


@dataclass
class LocationRange:
    destination_start: int
    source_start: int
    range_length: int

    @property
    def source_end(self):
        return self.source_start + self.range_length - 1

    @property
    def destination_end(self):
        return self.destination_start + self.range_length

    def lookup(self, start_location: int) -> Optional[int]:
        if start_location >= self.source_start \
           and start_location < self.source_start + self.range_length:
            return self.destination_start + start_location - self.source_start
        return None

    def flow(self, seed_range: SeedRange) -> Optional[SeedRange]:
        adj_start = max(self.source_start, seed_range.start)
        adj_end = min(self.source_end, seed_range.end)
        if adj_start < adj_end:
            r = adj_end - adj_start
            print(adj_start, adj_end, r)
            print(seed_range)
            print(self)
            res = SeedRange.from_start_end(adj_start, adj_end)
            print(res)
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


    def flow(self, seed_range: SeedRange) -> list[SeedRange]:
        result = [seed_range]
        for r in self.ranges:
            if range_seed := r.flow(seed_range):
                result.append(range_seed)
        return result


    # def minimize(self) -> LocationMap:
    #     combined_ranges = []
    #     for sorted_range in sorted(self.ranges, key=lambda r: r.source_start):
    #         if combined_ranges:
    #             last_combined = combined_ranges[-1]
    #             if sorted_range.source_start == last_combined.source_end:
    #                 last_combined.range_length += sorted_range.range_length
    #             elif sorted_range.source_start < last_combined.source_end:
    #                 raise Exception('Need to minimize range!')
    #             else:
    #                 combined_ranges.append(dataclasses.replace(sorted_range))
    #         else:
    #             combined_ranges.append(dataclasses.replace(sorted_range))
    #     print('Minimized from {} to {}'.format(len(self.ranges), len(combined_ranges)))
    #     return LocationMap(self.name, combined_ranges)


def part12(input_filename: str):
    with open(input_filename) as f:
        input = f.read()
        splitted_input = input.split('\n\n')
        seeds = parse_seeds(splitted_input[0])
        seed_ranges = parse_seed_ranges(splitted_input[0])
        location_maps = list(map(parse_map, splitted_input[1:]))
        # minimized_location_maps = list(map(lambda m: m.minimize(), location_maps))
        print(solve1(seeds, location_maps))
        print(solve2_bruteforce(seed_ranges, location_maps))
        #print(solve2(seed_ranges, location_maps))


def parse_seeds(line: str) -> list[int]:
    return list(map(int, line.removeprefix('seeds: ').split()))


def parse_seed_ranges(line: str) -> list[SeedRange]:
    seeds_str = line.removeprefix('seeds: ')
    numbers = list(map(int, seeds_str.split()))
    ranges = []
    for r in range(0, len(numbers), 2):
        [start, length] = numbers[r:r + 2]
        ranges.append(SeedRange(start, length))
    return ranges


def parse_map(text: str) -> LocationMap:
    splitted = text.split('\n')
    name = splitted[0]
    ranges = []
    for range_description in splitted[1:]:
        if range_description:
            range_components = list(map(int, range_description.split()))
            ranges.append(LocationRange(range_components[0], range_components[1], range_components[2]))
    print( ranges, 'before')
    ranges = list(sorted(ranges, key=lambda r: r.source_start))
    print(ranges)
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
