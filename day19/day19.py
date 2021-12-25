import numpy as np

def rotate(points, origin, angle):
    return (points - origin) * np.exp(complex(0, angle)) + origin

rx = np.array([[1, 0, 0 ],
              [0, 0, -1],
              [0, 1, 0]])

ry = np.array([[0, 0, 1 ],
              [0, 1, 0],
              [-1, 0, 0]])

rz = np.array([[0, -1, 0 ],
              [1, 0, 0],
              [0, 0, 1]])

SAMPLE_INPUT_RAW="""--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""


def read_input(input_raw):
    sections_raw = input_raw.split("\n\n")
    return [read_points(section_raw) for section_raw in sections_raw]
    
def read_points(section_raw):
    points = [[int(v) for v in line.split(",")] for line in section_raw.splitlines()[1:]]
    return points

import math

def point_distances(i,points, dist_map):
    for pt1 in points:
        dists = set()
        for pt2 in points:
            if pt1 != pt2:      
                dist = math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2 + (pt1[2] - pt2[2])**2)
                dists.add(dist)
        dist_map[tuple([i] + pt1)] = dists

from collections import defaultdict

# https://github.com/akshayb6/trilateration-in-3d/blob/master/trilateration.py#L7
def trilaterate3D(distances):
    p1=np.array(distances[0][:3])
    p2=np.array(distances[1][:3])
    p3=np.array(distances[2][:3])       
    p4=np.array(distances[3][:3])
    r1=distances[0][-1]
    r2=distances[1][-1]
    r3=distances[2][-1]
    r4=distances[3][-1]
    e_x=(p2-p1)/np.linalg.norm(p2-p1)
    i=np.dot(e_x,(p3-p1))
    e_y=(p3-p1-(i*e_x))/(np.linalg.norm(p3-p1-(i*e_x)))
    e_z=np.cross(e_x,e_y)
    d=np.linalg.norm(p2-p1)
    j=np.dot(e_y,(p3-p1))
    x=((r1**2)-(r2**2)+(d**2))/(2*d)
    y=(((r1**2)-(r3**2)+(i**2)+(j**2))/(2*j))-((i/j)*(x))
    z1=np.sqrt(r1**2-x**2-y**2)
    z2=np.sqrt(r1**2-x**2-y**2)*(-1)
    ans1=p1+(x*e_x)+(y*e_y)+(z1*e_z)
    ans2=p1+(x*e_x)+(y*e_y)+(z2*e_z)
    dist1=np.linalg.norm(p4-ans1)
    dist2=np.linalg.norm(p4-ans2)
    if np.abs(r4-dist1)<np.abs(r4-dist2):
        return ans1
    else: 
        return ans2

def test_sample():
    section_points = read_input(SAMPLE_INPUT_RAW)
    #print("Section points:", section_points)
    relative_locations = []
    for i in range(len(section_points)):
        points0 = section_points[i]
        point_dists0 = {}
        point_distances(i,points0, point_dists0)
        for j in range(i+1, len(section_points)):
            points1 = section_points[j]
            point_dists1 = {}
            point_distances(j,points1, point_dists1)
            shared_points = []
            for pt0 in point_dists0:
                for pt1 in point_dists1:
                    if len(point_dists0[pt0].intersection(point_dists1[pt1])) >= 11:
                        shared_points.append((pt0, pt1))
            if shared_points:
                offset, rotation = find_orientation(shared_points)
                relative_locations.append((i,j,offset,rotation))
                for pti, ptj in shared_points:
                    assert np.array_equal(pti[1:], rotate_and_translate(np.array(ptj[1:]), offset, rotation))
                    assert np.array_equal(ptj[1:], unrotate_and_translate(np.array(pti[1:]), offset, rotation))

    print(relative_locations)
    find_locations_relative_to_zero(relative_locations, len(section_points))


def find_orientation(shared_points):
    """For some rotation, all shared points between scanner i and scanner j will have the same offset"""
    for nrx in range(4):
        for nry in range(4):
            for nrz in range(4):
                point_offsets = [(pt1[1:] - rotate_and_translate(pt2[1:], np.array([0,0,0]), (nrx, nry, nrz))) 
                                    for (pt1,pt2) in shared_points]
                point_offsets_set = {tuple(pt) for pt in point_offsets}
                if len(point_offsets_set) == 1:
                    return point_offsets[0], np.array([nrx,  nry, nrz])
                #print(len()

def test_rotate_point():
    for nrx in range(4):
        for nry in range(4):
            for nrz in range(4):
                new_pt = rotate_and_translate([-336, 658, 858], (68, -1246, -43), (nrx, nry, nrz)) 
                if (list(new_pt) == [404, -588, -901]):
                    assert (nrx,nry,nrz) in [(2,0,2), (0,2,0)]

def test_undo_rotation():
    pt = [-336, 658, 858]
    new_pt = rotate_and_translate(pt,[0,0,0],[1,2,3])
    old_pt = unrotate_and_translate(new_pt, [0,0,0], [1,2,3])
    assert np.array_equal(pt, old_pt.astype(int))
    
def find_locations_relative_to_zero(relative_locations, n):
    for i in range(1,n):
        # if i == 2:
        #     import pdb; pdb.set_trace()
        seen = set()
        loc = np.array([0, 0, 0])
        pt = i
        stack = [[pt, loc]]
        while stack:
            #print("Stack", i, stack)
            pt, loc = stack.pop()
            if pt == 0:
                print("Found path: ", i, loc)
                break
            seen.add(pt)
            for pti, ptj, offset, rotations in relative_locations:
                if pti == pt and ptj not in seen:
                    stack.append([ptj, unrotate_and_translate(loc, offset, rotations)])
                if ptj == pt and pti not in seen:
                    stack.append([pti, rotate_and_translate(loc, offset, rotations)])


def connected_components(point_map):
    components = []
    key_set = set(point_map.keys())
    ct = 0
    for pt in key_set:
        if pt not in point_map:
            continue
        component = set()
        points_to_check = []
        component.add(pt)
        points_to_check.append(pt)
        while points_to_check:
            pt = points_to_check.pop()
            for other_point in point_map[pt]:
                points_to_check.append(other_point)
            component = component.union(point_map[pt])
            #print(points_to_check)
            del point_map[pt]
        ct += 1
        #print(len(component))
        components.append(component)
    print("Component ct", ct)
    #print("Components:", components)
    return components

from heapq import heappush, heappop

def shortest_path(n_points, distances):
    costs = {}
    for i in range(n_points):
        for j in range(i+1, n_points):
            #if i == 20 and j == 21:
            #    import pdb; pdb.set_trace()
            q = []
            heappush(q, (0, i))
            seen = set()
            while q:
                cost, k = heappop(q)
                seen.add(k)
                if k == j:
                    costs[(i,j)] = cost
                    break
                for p in distances:
                    if p[0] == k and p[1] not in seen:
                        heappush(q, (cost + distances[p], p[1]))
                    if p[1] == k and p[0] not in seen:
                        heappush(q, (cost + distances[p], p[0]))
    return costs

def rotate_and_translate(pt, offset, rotation):
    dx, dy, dz = offset
    nrx, nry, nrz = rotation
    xmat = np.linalg.matrix_power(rx, nrx)
    ymat = np.linalg.matrix_power(ry, nry)
    zmat = np.linalg.matrix_power(rz, nrz)
    pt_rotated = xmat.dot(ymat.dot(zmat.dot(pt)))
    return pt_rotated + [dx, dy, dz]

def unrotate_and_translate(pt, offset, rotation):
    dx, dy, dz = offset
    nrx, nry, nrz = rotation
    pt_translated = pt - [dx, dy, dz]

    xmat = np.linalg.matrix_power(rx, -nrx)
    ymat = np.linalg.matrix_power(ry, -nry)
    zmat = np.linalg.matrix_power(rz, -nrz)
    pt_rotated = zmat.dot(ymat.dot(xmat.dot(pt_translated)))
    return pt_rotated


if __name__ == "__main__":
    with open("input.txt") as file:
        section_points = read_input(file.read())
    #print(section_points)
    point_dists_map = {}
    point_map = defaultdict(set)
    for i in range(len(section_points)):
        points = section_points[i]
        point_distances(i,points, point_dists_map)
    #print(point_dists_map)
    for pt0, pt0_dists in point_dists_map.items():
        for pt1, pt1_dists in point_dists_map.items():
            if pt0 != pt1:
                point_map[pt0]
                point_map[pt1]
                if len(pt1_dists.intersection(pt0_dists)) > 3:
                    # print(pt0, pt1, len(pt1_dists.intersection(pt0_dists)))
                    point_map[pt0].add(pt1)
                    point_map[pt1].add(pt0)
    components = connected_components(point_map)
    # for component in components:
    #     for p1 in component:
    #         for p2 in component:
    #             if p1 != p2:
    #                 print(p1, p2, abs(p1[1]) + abs(p1[2]) + abs(p1[3]) + abs(p2[1]) + abs(p2[2]) + abs(p2[3]))
    #     if len(component) > 1:
    #         print("\n\n")
    print("Part 1:", len(components))
    taxi_distances = defaultdict(set)
    for component in components:
        for p1 in component:
            for p2 in component:
                if p1 != p2:
                    d = abs(p1[1]) + abs(p1[2]) + abs(p1[3]) + abs(p2[1]) + abs(p2[2]) + abs(p2[3])
                    taxi_distances[tuple(sorted([p1[0],p2[0]]))].add(d)
    farthest_scanners = max([min(distance_set) for distance_set in taxi_distances.values()])
    distances = {}
    for pair, distance_set in taxi_distances.items():
        print(pair, min(distance_set))
        distances[pair] = min(distance_set)
        #print(pair, min(distance_set))
    costs = shortest_path(len(points), distances)
    print("Costs:", costs)
    print("Part 2:", max(costs.values()))




