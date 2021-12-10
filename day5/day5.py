"""
--- Day 5: Hydrothermal Venture ---
You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?
"""

SAMPLE_INPUT = \
"""
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""
from collections import defaultdict

def point_range(p1, p2):
    p1x, p1y = p1
    p2x, p2y = p2
    if p1x == p2x:
        x_inc = 0
    if p1y == p2y:
        y_inc = 0
    if p1x > p2x:
        x_inc = -1
    if p1x < p2x:
        x_inc = 1
    if p1y > p2y:
        y_inc = -1
    if p1y < p2y:
        y_inc = 1
    x, y = p1x, p1y
    while x != p2x or y != p2y:
        yield x, y
        x = x + x_inc
        y = y + y_inc
    yield p2x, p2y

def test_point_range():
    assert list(point_range((0,0), (0,0))) == [(0,0)]
    assert list(point_range((0,0), (5,0))) == [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0)]
    assert list(point_range((1,1), (5,1))) == [(1,1), (2,1), (3,1), (4,1), (5,1)]
    assert list(point_range((3,6), (6,3))) == [(3,6), (4,5), (5,4), (6,3)]

def add_line_to_grid(grid, start, end):
    for x, y in point_range(start, end):
        grid[x][y] += 1

def count_overlaps(grid):
    overlaps = 0
    for x in grid:
        for y in grid[x]:
            if grid[x][y] > 1:
                overlaps += 1
    return overlaps

def print_grid(grid, maxx, maxy):
    for x in range(0, maxx + 1):
        row = ""
        for y in range(0, maxy + 1):
            row += str(grid[x][y])
        print(row)

def test_build_grid():
    all_grid = defaultdict(lambda: defaultdict(int))
    non_diag_grid = defaultdict(lambda: defaultdict(int))
    maxx = maxy = 0
    lines = SAMPLE_INPUT.split("\n")
    lines = [line.strip() for line in lines]

    for line in lines:
        if line:
            start, end = line.split(" -> ")
            # print(start, end)
            startx, endx = [int(c) for c in start.split(",")]
            starty, endy = [int(c) for c in end.split(",")]
            if endx > maxx:
                maxx = endx
            if endy > maxy:
                maxy = endy
            if startx == starty or endx == endy:
                add_line_to_grid(non_diag_grid, (startx, endx), (starty, endy))
            add_line_to_grid(all_grid, (startx, endx), (starty, endy))
            # print_grid(grid, maxx, maxy)

    non_diag_overlaps = count_overlaps(non_diag_grid)
    assert(non_diag_overlaps == 5)

    all_overlaps = count_overlaps(all_grid)
    assert(all_overlaps == 12)


if __name__ == "__main__":
    with open("input.txt") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    grid = defaultdict(lambda: defaultdict(int))
    maxx = maxy = 0
    for line in lines:
        if line:
            start, end = line.split(" -> ")
            # print(start, end)
            startx, endx = [int(c) for c in start.split(",")]
            starty, endy = [int(c) for c in end.split(",")]
            if endx > maxx:
                maxx = endx
            if endy > maxy:
                maxy = endy
            add_line_to_grid(grid, (startx, endx), (starty, endy))
            # print_grid(grid, maxx, maxy)

    overlaps = count_overlaps(grid)
    print(overlaps)
