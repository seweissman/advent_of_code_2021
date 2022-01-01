import numpy as np

SAMPLE_INPUT = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""
def read_input(input_lines):
    return np.array([list(line) for line in input_lines])

def test_sample():
    input_lines = SAMPLE_INPUT.splitlines()
    cucumber_grid = read_input(input_lines)
    #print(cucumber_grid)
    steps = 0
    while True:
        steps += 1

        new_grid = step_grid(cucumber_grid)
        if np.array_equal(cucumber_grid, new_grid):
            break
        cucumber_grid = new_grid
    assert steps == 58

def step_grid(cucumber_grid: np.array):
    nrows, ncols = cucumber_grid.shape
    new_grid = np.full((nrows, ncols), ".")

    for r in range(nrows):
        for c in range(ncols):
            char = cucumber_grid[(r,c)]
            # east facing cucumber
            if char == ">":
                if cucumber_grid[(r, (c+1)%ncols)] == ".":
                    new_grid[(r, (c+1)%ncols)] = ">"
                else:
                    new_grid[(r,c)] = ">"
            if char == "v":
                new_grid[(r,c)] = "v"

    cucumber_grid = new_grid
    new_grid = np.full((nrows, ncols), ".")

    for r in range(nrows):
        for c in range(ncols):
            char = cucumber_grid[(r,c)]
            # south facing cucumber
            if char == "v":
                if cucumber_grid[((r+1)%nrows, c)] == ".":
                    new_grid[((r+1)%nrows, c)] = "v"
                else:
                    new_grid[(r,c)] = "v"
            if char == ">":
                new_grid[(r,c)] = ">"

    return new_grid

if __name__ == "__main__":
    with open("input.txt") as file:
        input_lines = file.read().splitlines()
    cucumber_grid = read_input(input_lines)
    steps = 0
    while True:
        steps += 1

        new_grid = step_grid(cucumber_grid)
        if np.array_equal(cucumber_grid, new_grid):
            break
        cucumber_grid = new_grid
    print("Part1: ", steps)
