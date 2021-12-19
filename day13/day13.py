"""
--- Day 13: Transparent Origami ---
You reach another volcanically active part of the cave. It would be nice if you could do some kind of thermal imaging so you could tell ahead of time which caves are too hot to safely enter.

Fortunately, the submarine seems to be equipped with a thermal camera! When you activate it, you are greeted with:

Congratulations on your purchase! To activate this infrared thermal imaging
camera system, please enter the code found on page 1 of the manual.
Apparently, the Elves have never used this feature. To your surprise, you manage to find the manual; as you go to open it, page 1 falls out. It's a large sheet of transparent paper! The transparent paper is marked with random dots and includes instructions on how to fold it up (your puzzle input). For example:

6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
The first section is a list of dots on the transparent paper. 0,0 represents the top-left coordinate. The first value, x, increases to the right. The second value, y, increases downward. So, the coordinate 3,0 is to the right of 0,0, and the coordinate 0,7 is below 0,0. The coordinates in this example form the following pattern, where # is a dot on the paper and . is an empty, unmarked position:

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........
Then, there is a list of fold instructions. Each instruction indicates a line on the transparent paper and wants you to fold the paper up (for horizontal y=... lines) or left (for vertical x=... lines). In this example, the first fold instruction is fold along y=7, which designates the line formed by all of the positions where y is 7 (marked here with -):

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
-----------
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........
Because this is a horizontal line, fold the bottom half up. Some of the dots might end up overlapping after the fold is complete, but dots will never appear exactly on a fold line. The result of doing this fold looks like this:

#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........
Now, only 17 dots are visible.

Notice, for example, the two dots in the bottom left corner before the transparent paper is folded; after the fold is complete, those dots appear in the top left corner (at 0,0 and 0,1). Because the paper is transparent, the dot just below them in the result (at 0,3) remains visible, as it can be seen through the transparent paper.

Also notice that some dots can end up overlapping; in this case, the dots merge together and become a single dot.

The second fold instruction is fold along x=5, which indicates this line:

#.##.|#..#.
#...#|.....
.....|#...#
#...#|.....
.#.#.|#.###
.....|.....
.....|.....
Because this is a vertical line, fold left:

#####
#...#
#...#
#...#
#####
.....
.....
The instructions made a square!

The transparent paper is pretty big, so for now, focus on just completing the first fold. After the first fold in the example above, 17 dots are visible - dots that end up overlapping after the fold is completed count as a single dot.

How many dots are visible after completing just the first fold instruction on your transparent paper?
"""

import numpy as np

SAMPLE_INPUT = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

def read_input(input_raw):
    input_lines = [line.strip() for line in input_raw.splitlines() if line.strip()]

    points = [line.split(",") for line in input_lines if "," in line]
    folds = [line.split(" ")[-1] for line in input_lines if "=" in line]

    points = [(int(x), int(y)) for (x,y) in points]
    folds = [f.split("=") for f in folds]
    folds = [(axis, int(ct)) for (axis, ct) in folds]
    return points, folds

def fold_sheet(sheet, axis, n):
    if axis == "x":
        left = sheet[:,0:n]
        right = sheet[:,n+1:]
        return left | np.flip(right, 1)
    if axis == "y":
        top = sheet[0:n,:]
        bottom = sheet[n+1:,:]
        return top | np.flip(bottom, 0)

def build_sheet(points):
    maxx = max([x for (x,_) in points])
    maxy = max([y for (_,y) in points])
    dimy = maxx + 1
    dimx = maxy + 1
    # Make sure dimensions are odd so that we can fold evenly
    if dimy % 2 == 0:
        dimy += 1
    if dimx % 2 == 0:
        dimx += 1
    sheet = np.zeros((dimx, dimy), dtype=bool)    
    for x,y in points:
        sheet[(y,x)] = True
    return sheet

def test_sample():
    points, folds = read_input(SAMPLE_INPUT)
    fold = folds[0]

    sheet = build_sheet(points)
    sheet = fold_sheet(sheet, fold[0], fold[1])
    num_true = sum([1 for v in sheet.flatten() if v])
    assert num_true == 17


if __name__ == "__main__":
    with open("./input.txt") as file:
        points, folds = read_input(file.read())

    sheet = build_sheet(points)
    fold = folds[0]
    sheet = fold_sheet(sheet, fold[0], fold[1])
    num_true = sum([1 for v in sheet.flatten() if v])
    print("Part1: ", num_true)

    for fold in folds[1:]:
        sheet = fold_sheet(sheet, fold[0], fold[1])

    # For Part2, Print out code
    for row in range(0, sheet.shape[0]):
        print("".join(["#" if v else "." for v in sheet[row]]))
