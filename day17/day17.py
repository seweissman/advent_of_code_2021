"""
--- Day 17: Trick Shot ---
You finally decode the Elves' message. HI, the message says. You continue searching for the sleigh keys.

Ahead of you is what appears to be a large ocean trench. Could the keys have fallen into it? You'd better send a probe to investigate.

The probe launcher on your submarine can fire the probe with any integer velocity in the x (forward) and y (upward, or downward if negative) directions. For example, an initial x,y velocity like 0,10 would fire the probe straight up, while an initial velocity like 10,-1 would fire the probe forward at a slight downward angle.

The probe's x,y position starts at 0,0. Then, it will follow some trajectory by moving in steps. On each step, these changes occur in the following order:

The probe's x position increases by its x velocity.
The probe's y position increases by its y velocity.
Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
Due to gravity, the probe's y velocity decreases by 1.
For the probe to successfully make it into the trench, the probe must be on some trajectory that causes it to be within a target area after any step. The submarine computer has already calculated this target area (your puzzle input). For example:

y = vt

y(t) = v0 + v0 - 1 + v0 - 2 + ... + v0 - t = (t+1)*v0 - t(t+1)/2

y(t) = v0t + v0 - t^2/2 - t/2

dy/dt = v0 - 1/2 - t = 0
t = v0 - 1/2


v0 = 9
t,y
1,9
2,17
3,24
4,30
5,35-
6,39
7,42
8,44
9,45

max = v0 * (v0+1)/2

-5 < (t + 1)*v0 - t(t+1)/2 < -10

target area: x=20..30, y=-10..-5
This target area means that you need to find initial x,y velocity values such that after any step, the probe's x position is at least 20 and at most 30, and the probe's y position is at least -10 and at most -5.

Given this target area, one initial velocity that causes the probe to be within the target area after any step is 7,2:

.............#....#............
.......#..............#........
...............................
S........................#.....
...............................
...............................
...........................#...
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTT#TT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
In this diagram, S is the probe's initial position, 0,0. The x coordinate increases to the right, and the y coordinate increases upward. In the bottom right, positions that are within the target area are shown as T. After each step (until the target area is reached), the position of the probe is marked with #. (The bottom-right # is both a position the probe reaches and a position in the target area.)

Another initial velocity that causes the probe to be within the target area after any step is 6,3:

...............#..#............
...........#........#..........
...............................
......#..............#.........
...............................
...............................
S....................#.........
...............................
...............................
...............................
.....................#.........
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................T#TTTTTTTTT
....................TTTTTTTTTTT
Another one is 9,0:

S........#.....................
.................#.............
...............................
........................#......
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTT#
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
One initial velocity that doesn't cause the probe to be within the target area after any step is 17,-4:

S..............................................................
...............................................................
...............................................................
...............................................................
.................#.............................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT..#.............................
....................TTTTTTTTTTT................................
...............................................................
...............................................................
...............................................................
...............................................................
................................................#..............
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
..............................................................#
The probe appears to pass through the target area, but is never within it after any step. Instead, it continues down and to the right - only the first few steps are shown.

If you're going to fire a highly scientific probe out of a super cool probe launcher, you might as well do it with style. How high can you make the probe go while still reaching the target area?

In the above example, using an initial velocity of 6,9 is the best you can do, causing the probe to reach a maximum y position of 45. (Any higher initial y velocity causes the probe to overshoot the target area entirely.)

Find the initial velocity that causes the probe to reach the highest y position and still eventually be within the target area after any step. What is the highest y position it reaches on this trajectory?
"""

import itertools

def gen_points(vx, vy):
    yield 0,0
    x = 0
    y = 0
    t = 0
    while True:
        if t <= vx:
            x += vx - t
        y += vy - t
        yield x,y
        t += 1

def test_gen_tools():
    pts = itertools.islice(gen_points(7, 2), 9)
    assert list(pts) == [(0,0), (7,2), (13,3), (18, 3), (22, 2), (25, 0), (27, -3), (28, -7), (28, -12)]

def find_every_velocity(xrange, yrange):
    """find every initial velocity such that at some time the probe reaches the target"""
    xlow, xhigh = xrange
    ylow, yhigh = yrange

    initial_velocities = []
    for vx in range(min(0, xlow), max(abs(xlow), abs(xhigh))+1):
        for vy in range(min(0, ylow), max(abs(ylow), abs(yhigh))+1):
            for x,y in gen_points(vx, vy):
                if xlow <= x <= xhigh and ylow <= y <= yhigh:
                    initial_velocities.append((vx, vy))
                # Stop generating points when x or y is out of range
                if x > xhigh or (y < 0 and y < ylow):
                    break
    return initial_velocities

SAMPLE_VELOCITY_OUTPUT = """
23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7
"""

def test_find_every_velocity():
    velocity_set_raw = [p for line in SAMPLE_VELOCITY_OUTPUT.splitlines() if line for p in line.split(" ") if p]
    velocity_set = set()
    for p in velocity_set_raw:
        x,y = p.split(",")
        velocity_set.add((int(x), int(y)))
    test_set = set(find_every_velocity((20, 30), (-10, -5)))
    assert velocity_set == test_set

if __name__ == "__main__":

    # Part 1

    # We don't need to code for this part.
    # x and y are independent so we only need to determine the max y velocity that will land in the
    # given range (-75, -49). Since the first y value after y passes through 0 is -v0 - 1, the max v0
    # is 74. The max height is v0 + v0 - 1 + v0 - 2 + ... + 1 = v0*(v0+1)/2. 74*75/2 = 2775

    # Part 2 input
    xrange=(241, 275)
    yrange=(-75, -49)
    velocity_set = set(find_every_velocity(xrange, yrange))
    print("Part 2:", len(velocity_set))
