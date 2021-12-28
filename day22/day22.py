SAMPLE_INPUT_SMALL = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""

SAMPLE_INPUT_LARGE = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682"""


def read_input(input_raw:str):
    reboot_steps = []
    for line in input_raw.splitlines():
        state,ranges_str = line.split(" ")
        ranges = ranges_str.split(",")
        ranges = [range.split("..") for range in [range.split("=")[1] for range in ranges]]
        ranges = tuple([(int(r_start), int(r_end)) for (r_start, r_end) in ranges])
        reboot_steps.append((state, ranges))
    return reboot_steps

def build_point_set(reboot_steps):
    point_set = set()
    for state, ranges in reboot_steps:
        x_min, x_max = ranges[0]
        y_min, y_max = ranges[1]
        z_min, z_max = ranges[2]
        # check if cube is in the range we care about
        if x_min > 50 or x_max < -50 or y_min > 50 or y_max < -50 or z_min > 50 or z_max < -50:
            continue
        #print("Processing: ", state, ranges)
        x_min = max(-50, x_min)
        y_min = max(-50, y_min)
        z_min = max(-50, z_min)
        x_max = min(50, x_max)
        y_max = min(50, y_max)
        z_max = min(50, z_max)
        #print(x_min, x_max, y_min, y_max, z_min, z_max)
        cube_points = set()
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                for z in range(z_min, z_max + 1):
                    cube_points.add((x, y, z))
        #print(len(cube_points))
        if state == "on":
            point_set = point_set.union(cube_points)
        if state == "off":
            point_set = point_set.difference(cube_points)
        #print(len(point_set))
    return point_set

def test_sample_small():
    reboot_steps = read_input(SAMPLE_INPUT_SMALL)
    assert len(reboot_steps) == 4
    point_set = build_point_set(reboot_steps)
    assert len(point_set) == 39

def test_sample_large():
    reboot_steps = read_input(SAMPLE_INPUT_LARGE)
    assert len(reboot_steps) == 22
    point_set = build_point_set(reboot_steps)
    assert len(point_set) == 590784

if __name__ == "__main__":
    with open("input.txt") as file:
        input_raw = file.read()
    reboot_steps = read_input(input_raw)
    point_set = build_point_set(reboot_steps)
    print("Part 1:", len(point_set))