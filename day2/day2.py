"""
--- Day 2: Dive! ---
Now, you need to figure out how to pilot this thing.

It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

forward X increases the horizontal position by X units.
down X increases the depth by X units.
up X decreases the depth by X units.
Note that since you're on a submarine, down and up affect your depth, and so they have the opposite result of what you might expect.

The submarine seems to already have a planned course (your puzzle input). You should probably figure out where it's going. For example:

forward 5
down 5
forward 8
up 3
down 8
forward 2
Your horizontal position and depth both start at 0. The steps above would then modify them as follows:

forward 5 adds 5 to your horizontal position, a total of 5.
down 5 adds 5 to your depth, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13.
up 3 decreases your depth by 3, resulting in a value of 2.
down 8 adds 8 to your depth, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15.
After following these instructions, you would have a horizontal position of 15 and a depth of 10. (Multiplying these together produces 150.)

Calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?

--- Part Two ---
Based on your calculations, the planned course doesn't seem to make any sense. You find the submarine manual and discover that the process is actually slightly more complicated.

In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at 0. The commands also mean something entirely different than you first thought:

down X increases your aim by X units.
up X decreases your aim by X units.
forward X does two things:
It increases your horizontal position by X units.
It increases your depth by your aim multiplied by X.
Again note that since you're on a submarine, down and up do the opposite of what you might expect: "down" means aiming in the positive direction.

Now, the above example does something different:

forward 5 adds 5 to your horizontal position, a total of 5. Because your aim is 0, your depth does not change.
down 5 adds 5 to your aim, resulting in a value of 5.
forward 8 adds 8 to your horizontal position, a total of 13. Because your aim is 5, your depth increases by 8*5=40.
up 3 decreases your aim by 3, resulting in a value of 2.
down 8 adds 8 to your aim, resulting in a value of 10.
forward 2 adds 2 to your horizontal position, a total of 15. Because your aim is 10, your depth increases by 2*10=20 to a total of 60.
After following these new instructions, you would have a horizontal position of 15 and a depth of 60. (Multiplying these produces 900.)

Using this new interpretation of the commands, calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?
"""

SAMPLE_INSTRUCTIONS = [
"forward 5",
"down 5",
"forward 8",
"up 3",
"down 8",
"forward 2"
]

def run_instruction_part1(instruction, position):
    direction, distance = instruction.split(" ")
    x, depth = position
    distance = int(distance)
    if direction == "forward":
        return x + distance, depth
    if direction == "down":
        return x, depth + distance
    if direction == "up":
        return x, depth - distance
    return position

def run_instruction_part2(instruction, position):
    direction, distance = instruction.split(" ")
    x, depth, aim = position
    distance = int(distance)
    if direction == "forward":
        return x + distance, depth + (aim * distance), aim
    if direction == "down":
        return x, depth, aim + distance
    if direction == "up":
        return x, depth, aim - distance
    return position

def run_course(instruction_list, position=(0, 0), instruction_fn=run_instruction_part1):
    for instruction in instruction_list:
        position = instruction_fn(instruction, position)
    return position

def test_part1():
    position = run_course(SAMPLE_INSTRUCTIONS)
    assert(position == (15, 10))
    assert(position[0]*position[1] == 150)


def test_part2():
    position = run_course(SAMPLE_INSTRUCTIONS, position=(0,0,0), instruction_fn=run_instruction_part2)
    x, depth, aim = position
    assert((x, depth) == (15, 60))
    assert(x*depth == 900)

if __name__ == "__main__":
    with open("input.txt") as file:
        instructions = [line.strip() for line in file]
    part1 = run_course(instructions)
    print("Part1:", part1, part1[0] * part1[1])

    part2 = run_course(instructions, position=(0,0,0), instruction_fn=run_instruction_part2)
    print("Part2:", part2, part2[0] * part2[1])
