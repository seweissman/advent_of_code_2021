"""
--- Day 12: Passage Pathing ---
With your submarine's subterranean subsystems subsisting suboptimally, the only way you're getting out of this cave anytime soon is by finding a path yourself. Not just a path - the only way to know if you've found the best path is to find all of them.

Fortunately, the sensors are still mostly working, and so you build a rough map of the remaining caves (your puzzle input). For example:

start-A
start-b
A-c
A-b
b-d
A-end
b-end
This is a list of how all of the caves are connected. You start in the cave named start, and your destination is the cave named end. An entry like b-d means that cave b is connected to cave d - that is, you can move between them.

So, the above cave system looks roughly like this:

    start
    /   \
c--A-----b--d
    \   /
     end
Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves more than once. There are two types of caves: big caves (written in uppercase, like A) and small caves (written in lowercase, like b). It would be a waste of time to visit any small cave more than once, but big caves are large enough that it might be worth visiting them multiple times. So, all paths you find should visit small caves at most once, and can visit big caves any number of times.

Given these rules, there are 10 paths through this example cave system:

start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end
(Each line in the above list corresponds to a single path; the caves visited by that path are listed in the order they are visited and separated by commas.)

Note that in this cave system, cave d is never visited by any path: to do so, cave b would need to be visited twice (once on the way to cave d and a second time when returning from cave d), and since cave b is small, this is not allowed.

Here is a slightly larger example:

dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
The 19 paths through it are as follows:

start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end
Finally, this even larger example has 226 paths through it:

fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
How many paths through this cave system are there that visit small caves at most once?
"""
from collections import defaultdict

SAMPLE_INPUT_SMALL= \
"""
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

def test_small():
    input_lines = [line for line in SAMPLE_INPUT_SMALL.splitlines() if line]
    graph = build_graph(input_lines)
    assert count_paths(graph, "start") == 10
    assert count_paths_part2(graph, "start") == 36

SAMPLE_INPUT_MEDIUM = \
"""
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""

def test_medium():
    input_lines = [line for line in SAMPLE_INPUT_MEDIUM.splitlines() if line]
    graph = build_graph(input_lines)
    assert count_paths(graph, "start") == 19
    assert count_paths_part2(graph, "start") == 103

SAMPLE_INPUT_LARGE = \
"""
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""

def test_large():
    input_lines = [line for line in SAMPLE_INPUT_LARGE.splitlines() if line]
    graph = build_graph(input_lines)
    assert count_paths(graph, "start") == 226
    assert count_paths_part2(graph, "start") == 3509

def is_lowercase(x):
    return x.lower() == x

def build_graph(input_lines):
    graph = defaultdict(set)
    for line in input_lines:
        i,j = line.split("-")
        if i != "end" and j != "start":
            graph[i].add(j)
        if j != "end" and i != "start":
            graph[j].add(i)
    return graph

def count_paths(graph, start, visited=None):
    if not visited:
        visited = set()
    visited.add(start)
    if start == "end":
        return 1
    path_ct = 0
    for adj_node in graph[start]:
        if not is_lowercase(adj_node) or (is_lowercase(adj_node) and not adj_node in visited):
            ct = count_paths(graph, adj_node, visited.copy())
            path_ct += ct
    return path_ct

def count_paths_part2(graph, start, visit_count=None):
    if not visit_count:
        visit_count = defaultdict(int)
    if is_lowercase(start):
        visit_count[start] += 1
    if start == "end":
        return 1
    path_ct = 0
    for adj_node in graph[start]:
        if (not is_lowercase(adj_node) 
            or (is_lowercase(adj_node) and not adj_node in visit_count)
            or (is_lowercase(adj_node) and 2 not in visit_count.values())):
            ct = count_paths_part2(graph, adj_node, visit_count.copy())
            path_ct += ct
    return path_ct


if __name__ == "__main__":
    with open("input.txt") as file:
        input_lines = file.read().splitlines()
    graph = build_graph(input_lines)
    print(graph)
    print("Part1:", count_paths(graph, "start"))
    print("Part2:", count_paths_part2(graph, "start"))
