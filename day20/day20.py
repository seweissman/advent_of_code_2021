from collections import defaultdict

SAMPLE_INPUT="""..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""

class Grid:
    def __init__(self, enhancement_str, grid):
        self.enhancement_str = enhancement_str
        self.grid = grid
        self.enhance_ct = 0

    @staticmethod
    def from_input(input_raw: str):
        input_lines = [line for line in input_raw.splitlines() if line]
        enhancement_str = input_lines[0]
        assert len(enhancement_str) == 512
        grid = defaultdict(lambda: defaultdict(lambda: "."))
        for i in range(1,len(input_lines)):
            line = input_lines[i]
            for j in range(len(line)):
                grid[i-1][j] = line[j]
        return Grid(enhancement_str, grid)

    def _enhance_pixel(self, row, col):
        enhancement_index = self._get_enhancement_index(row, col)
        return self.enhancement_str[enhancement_index]

    def _get_enhancement_index(self, row, col):
        pixels = ""
        for i in range(row-1, row+2):
            pixels += self.grid[i][col-1] + self.grid[i][col] + self.grid[i][col+1]   
        bin_pixels = "".join(["1" if p == "#" else "0" for p in pixels])
        enhancement_index = int(bin_pixels, base=2)
        return enhancement_index

    def enhance(self):
        self.enhance_ct += 1
        # Account for case where enhancement_str[0] = "#" and we have infinite lit pixels
        # every other enhancement
        if self.enhancement_str[0] == "#":
            if self.enhance_ct % 2 == 1:
                default_char = self.enhancement_str[0]
            else:
                default_char = self.enhancement_str[-1]
        else:
            default_char = "."
        new_grid = defaultdict(lambda: defaultdict(lambda: default_char))
        row_range, col_range = self._get_grid_range()
        for row in range(row_range[0]-2, row_range[1]+2):
            for col in range(col_range[0]-2, col_range[1]+2):
                p = self._enhance_pixel(row, col)
                new_grid[row][col] = p
                assert p == "#" or p == "."
        self.grid = new_grid

    def _get_grid_range(self):
        min_row = min(self.grid.keys())
        max_row = max(self.grid.keys())
        min_col = min([min(self.grid[r].keys()) for r in range(min_row, max_row + 1)])
        max_col = max([max(self.grid[r].keys()) for r in range(min_row, max_row + 1)])
        return (min_row, max_row+1),(min_col, max_col+1)

    def lit_pixels_ct(self):
        lit = 0
        for row in self.grid.values():
            lit += len([p for p in row.values() if p == "#"])
        return lit

    def print_grid(self, row_range=None, col_range=None):
        print("\n")
        if not row_range or not col_range:
            _row_range, _col_range = self._get_grid_range()
            if not row_range:
                row_range = _row_range
            if not col_range:
                col_range = _col_range
        for row in range(*row_range):
            row_str = "".join(self.grid[row][col] for col in range(*col_range))
            print(row_str)


def test_sample():
    grid = Grid.from_input(SAMPLE_INPUT)
    p = grid._enhance_pixel(2,2)
    assert p == "#"

    row_range, col_range = grid._get_grid_range()
    assert row_range == col_range == (0,5)

    p = grid._enhance_pixel(-1,-1)
    assert p == "."

    p = grid._enhance_pixel(-1,0)
    assert p == "#"

    p = grid._enhance_pixel(-1,1)
    assert p == "#"

    p = grid._enhance_pixel(0,0)
    assert p == "."

    p = grid._enhance_pixel(0,-1)
    assert p == "#"

    grid.enhance()
    grid.print_grid()
    grid.enhance()
    grid.print_grid()
    assert grid.lit_pixels_ct() == 35

    for i in range(48):
        grid.enhance()
    assert grid.lit_pixels_ct() == 3351

if __name__ == "__main__":
    with open("input.txt") as file:
        input_raw = file.read()
    
    grid = Grid.from_input(input_raw)
    #print(grid.enhancement_str)
    grid.print_grid(row_range=(0,10), col_range=(0,10))
    input_lines = input_raw.splitlines()
    lit_ct = 0
    for line in input_lines[2:]:
        lit_ct += len([p for p in line if p == "#"])
    print(grid._get_grid_range())
    print(grid.lit_pixels_ct())
    grid.enhance()
    grid.print_grid(row_range=(-3,13), col_range=(-3,13))

    print(grid.lit_pixels_ct())
    grid.enhance()
    print("Part1: ", grid.lit_pixels_ct())

    for i in range(48):
        grid.enhance()

    print("Part2: ", grid.lit_pixels_ct())

