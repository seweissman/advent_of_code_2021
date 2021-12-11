"""
--- Day 9: Smoke Basin ---
These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678
Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?

--- Part Two ---
Next, you need to find the largest basins so you know what areas are most important to avoid.

A basin is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point. The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678
The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678
The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
Find the three largest basins and multiply their sizes together. In the above example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?
"""

import numpy as np

SAMPLE_INPUT = \
"""
2199943210
3987894921
9856789892
8767896789
9899965678
"""

def test_part1():
    input_lines = [line.strip() for line in SAMPLE_INPUT.split("\n") if line.strip()]
    height_array = read_input(input_lines)
    low_points = find_low_points(height_array)
    low_vals = [height_array[p] for p in low_points]
    assert low_vals == [1, 0, 5, 5]
    risk_level = sum([v + 1 for v in low_vals])
    assert risk_level == 15

def test_part2():
    input_lines = [line.strip() for line in SAMPLE_INPUT.split("\n") if line.strip()]
    height_array = read_input(input_lines)
    low_points = find_low_points(height_array)
    basins = [find_basin(p, height_array) for p in low_points]
    basin_sizes = [len(basin) for basin in basins]
    top3 = sorted(basin_sizes)[-3:]
    assert top3 == [9,9,14]
    assert np.prod(top3) == 1134

def get_adjacent_points(a, p):
    i, j = p
    adjacent_points = []
    if i > 0:
        adjacent_points.append((i-1,j))
    if i < a.shape[0] - 1:
        adjacent_points.append((i+1,j))
    if j > 0:
        adjacent_points.append((i,j-1))
    if j < a.shape[1] - 1:
        adjacent_points.append((i,j+1))
    return adjacent_points

def find_low_points(height_array):
    low_points = []
    for i in range(height_array.shape[0]):
        for j in range(height_array.shape[1]):
            adjacent_points = get_adjacent_points(height_array, (i,j))
            surrounding_vals = [height_array[p] for p in adjacent_points]
            if all([v > height_array[i][j] for v in surrounding_vals]):
                low_points.append((i,j))
    return low_points

def find_basin(p, height_array):
    basin_points = {p}
    while True:
        new_basin_points = set()
        for basin_point in basin_points:
            adjacent_points = get_adjacent_points(height_array, basin_point)
            for adjacent_point in adjacent_points:
                if (adjacent_point not in basin_points 
                        and height_array[adjacent_point] > height_array[basin_point]
                        and height_array[adjacent_point] != 9):
                    new_basin_points.add(adjacent_point)
        if not new_basin_points:
            break
        basin_points = basin_points.union(new_basin_points)
    return basin_points
        

def read_input(input_lines):
    a = np.array([[int(d) for d in line] for line in input_lines])
    return a


if __name__ == "__main__":
    with open("input.txt") as file:
        input_lines = [line.strip() for line in file.readlines() if line.strip()]
    height_array = read_input(input_lines)
    low_points = find_low_points(height_array)
    low_vals = [height_array[p] for p in low_points]
    risk_level = sum([v + 1 for v in low_vals])
    print("Part1:", risk_level)

    basins = [find_basin(p, height_array) for p in low_points]
    basin_sizes = [len(basin) for basin in basins]
    top3 = sorted(basin_sizes)[-3:]
    print("Part2:", np.prod(top3))
