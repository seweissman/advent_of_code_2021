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

SAMPLE_INPUT_PART2="""on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""

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

def cube_diff(range1, range2):
    #print("cube_diff", range1, range2)
    if not overlap(range1, range2):
        return [range1]
    x1_min, x1_max = range1[0]
    y1_min, y1_max = range1[1]
    z1_min, z1_max = range1[2]
    x2_min, x2_max = range2[0]
    y2_min, y2_max = range2[1]
    z2_min, z2_max = range2[2]
    cube_list = []
    #region a
    reg_a = ((x2_max + 1, x1_max),(y1_min, y1_max),(z1_min, z1_max))

    # region b
    reg_b = ((x1_min,min(x2_max, x1_max)),(y1_min,y1_max),(z1_min, z2_min-1))

    # region c
    reg_c = ((x1_min,min(x2_max, x1_max)),(y1_min, y2_min-1),(max(z2_min, z1_min),z1_max))

    # region d
    reg_d = ((x1_min, x2_min-1),(max(y2_min, y1_min),y1_max),(max(z2_min, z1_min), z1_max))

    # region e
    reg_e = ((max(x1_min, x2_min),min(x2_max, x1_max)),(max(y1_min,y2_min),min(y2_max, y1_max)),(z2_max+1, z1_max))

    # region f
    reg_f = ((max(x1_min, x2_min),min(x2_max, x1_max)),(y2_max+1, y1_max), (max(z1_min, z2_min),z1_max))

    regions = [reg_a, reg_b, reg_c, reg_d, reg_e, reg_f]
    #print("Regions", regions)
    for region in regions:
        if volume(region) > 0:
            cube_list.append(region)
    return cube_list

def test_cube_diff():
    cd = cube_diff(((9, 11), (9, 11), (10, 11)), ((9, 11), (9, 11), (9, 11)))
    assert cd == []

    cd = cube_diff(((9, 11), (9, 11), (9, 11)), ((9, 11), (9, 11), (10, 11)))
    assert cd == [((9,11),(9,11),(9,9))]

    cd = cube_diff(((9, 11), (10, 11), (9, 11)), ((9, 11), (9, 11), (9, 11)))
    assert cd == []

    cd = cube_diff(((9, 11), (9, 11), (9, 11)), ((9, 11), (10, 11), (9, 11)))
    assert cd == [((9,11),(9,9),(9,11))]

def overlap(range1, range2):
    x1_min, x1_max = range1[0]
    y1_min, y1_max = range1[1]
    z1_min, z1_max = range1[2]
    x2_min, x2_max = range2[0]
    y2_min, y2_max = range2[1]
    z2_min, z2_max = range2[2]
    if ((x2_min <= x1_min <= x2_max or x1_min <= x2_min <= x1_max) and 
        (y2_min <= y1_min <= y2_max or y1_min <= y2_min <= y1_max) and
        (z2_min <= z1_min <= z2_max or z1_min <= z2_min <= z1_max)):
        return ((max(x1_min, x2_min),min(x1_max, x2_max)),
                (max(y1_min, y2_min),min(y1_max, y2_max)),
                (max(z1_min, z2_min),min(z1_max, z2_max)))
    return None

def volume(cube_range, limit_range=None):
    if not cube_range:
        return 0
    x_min, x_max = cube_range[0]
    y_min, y_max = cube_range[1]
    z_min, z_max = cube_range[2]
    if x_max < x_min or y_max < y_min or z_max < z_min:
        return 0
    if limit_range:
        limit_x_min, limit_x_max = limit_range[0]
        limit_y_min, limit_y_max = limit_range[1]
        limit_z_min, limit_z_max = limit_range[2]
        if x_min > limit_x_max or y_min > limit_y_max or z_min > limit_y_max:
            return 0
        if x_max < limit_x_min or y_max < limit_x_min or z_max < limit_z_min:
            return 0
        x_min = max(x_min, limit_x_min)
        x_max = min(x_max, limit_x_max)
        y_min = max(y_min, limit_y_min)
        y_max = min(y_max, limit_y_max)
        z_min = max(z_min, limit_z_min)
        z_max = min(z_max, limit_z_max)
    vol = (x_max + 1 - x_min)*(y_max + 1 - y_min)*(z_max + 1 - z_min)
    assert vol >= 0
    return vol

def run_steps(reboot_steps):
    cube_list = [reboot_steps[0][1]]
    for state, new_cube in reboot_steps[1:]:
        print(state, new_cube) #, cube_list)
        cube_list_new = []
        if state == "on":
            cube_list_new += cube_list
            cube_union_list = [new_cube]
            for cube in cube_list:
                new_cube_union_list = []
                for union_cube in cube_union_list:
                    if overlap(union_cube, cube):
                        cube_remainders = cube_diff(union_cube, cube)
                        #print("remainders:", cube_remainders)
                        new_cube_union_list += cube_remainders
                    else:
                        new_cube_union_list.append(union_cube)
                cube_union_list = new_cube_union_list
            cube_list_new += cube_union_list
        if state == "off":
            for cube in cube_list:
                cube_diff_list = cube_diff(cube, new_cube)
                cube_list_new = cube_list_new + cube_diff_list

        cube_list = cube_list_new
    return cube_list

def test_sample_large_part2():
    reboot_steps = read_input(SAMPLE_INPUT_LARGE)
    cube_list = run_steps(reboot_steps)
    vol = sum([volume(cube, limit_range=((-50,50),(-50,50),(-50,50))) for cube in cube_list])
    assert vol == 590784

def test_sample_small_part2():
    reboot_steps = read_input(SAMPLE_INPUT_SMALL)
    cube_list = run_steps(reboot_steps)
    vol = sum([volume(cube) for cube in cube_list])
    assert vol == 39

def test_sample_part2():
    reboot_steps = read_input(SAMPLE_INPUT_PART2)
    cube_list = run_steps(reboot_steps)
    print(len(cube_list))
    vol = sum([volume(cube) for cube in cube_list])
    assert vol == 2758514936282235


if __name__ == "__main__":
    with open("input.txt") as file:
        input_raw = file.read()
    reboot_steps = read_input(input_raw)
    point_set = build_point_set(reboot_steps)
    print("Part 1:", len(point_set))

    cube_list = run_steps(reboot_steps)
    vol = sum([volume(cube) for cube in cube_list])
    print("Part2:", vol)    

