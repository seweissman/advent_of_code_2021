"""
--- Day 14: Extended Polymerization ---
The incredible pressures at this depth are starting to put a strain on your submarine. The submarine has polymerization equipment that would produce suitable materials to reinforce the submarine, and the nearby volcanically-active caves should even have the necessary input elements in sufficient quantities.

The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers a polymer template and a list of pair insertion rules (your puzzle input). You just need to work out what polymer would result after repeating the pair insertion process a few times.

For example:

NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
The first line is the polymer template - this is the starting point of the process.

The following section defines the pair insertion rules. A rule like AB -> C means that when elements A and B are immediately adjacent, element C should be inserted between them. These insertions all happen simultaneously.

So, starting with the polymer template NNCB, the first step simultaneously considers all three pairs:

The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and the second N.
The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.
The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.
Note that these pairs overlap: the second element of one pair is the first element of the next pair. Also, because all pairs are considered simultaneously, inserted elements are not considered to be part of a pair until the next step.

After the first step of this process, the polymer becomes NCNBCHB.

Here are the results of a few steps using the above rules:

Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB
This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073. After step 10, B occurs 1749 times, C occurs 298 times, H occurs 161 times, and N occurs 865 times; taking the quantity of the most common element (B, 1749) and subtracting the quantity of the least common element (H, 161) produces 1749 - 161 = 1588.

Apply 10 steps of pair insertion to the polymer template and find the most and least common elements in the result. What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?

--- Part Two ---
The resulting polymer isn't nearly strong enough to reinforce the submarine. You'll need to run more steps of the pair insertion process; a total of 40 steps should do it.

In the above example, the most common element is B (occurring 2192039569602 times) and the least common element is H (occurring 3849876073 times); subtracting these produces 2188189693529.

Apply 40 steps of pair insertion to the polymer template and find the most and least common elements in the result. What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?

"""
from collections import defaultdict

SAMPLE_INPUT="""
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""

class Polymer:

    def __init__(self, polymer_template, insertion_rules) -> None:
        self.insertion_rules = insertion_rules
        self.pair_cts = defaultdict(int)
        self.first_element = polymer_template[0]
        self.last_element = polymer_template[-1]
        all_pairs = ["".join(polymer_template[i:i+2]) for i in range(len(polymer_template) - 1)]
        for pair in all_pairs:
            self.pair_cts[pair] += 1

    def grow(self):
        new_pair_cts = defaultdict(int)
        for pair in self.pair_cts:
            if pair in self.pair_cts:
                new_pair_cts[pair[0] + self.insertion_rules[pair]] += self.pair_cts[pair]
                new_pair_cts[self.insertion_rules[pair] + pair[1]] += self.pair_cts[pair]
            else:
                new_pair_cts[pair] = self.pair_cts[pair]
        self.pair_cts = new_pair_cts

    def score(self):
        element_cts = defaultdict(int)
        for pair in self.pair_cts:
            element_cts[pair[0]] += self.pair_cts[pair]
            element_cts[pair[1]] += self.pair_cts[pair]
        # Account for double counting of all but first and last element of polymer string
        element_cts[self.first_element] += 1
        element_cts[self.last_element] += 1
        for element in element_cts:
            element_cts[element] //= 2

        # Find the most common and least common element and subtract counts for score
        elements = sorted([(v,k) for (k,v) in element_cts.items()])
        most_common_minus_least = elements[-1][0] - elements[0][0]
        return most_common_minus_least

    @staticmethod
    def from_input(input_raw):
        input_lines = [line.strip() for line in input_raw.splitlines() if line.strip()]
        polymer_template = input_lines[0]
        insertion_rules = [l.split(" -> ") for l in input_lines[1:]]
        insertion_rules = {x: y for (x,y) in insertion_rules}
        polymer = Polymer(polymer_template, insertion_rules)
        return polymer

def test_sample():
    polymer = Polymer.from_input(SAMPLE_INPUT)
    for i in range(10):
        polymer.grow()
    assert polymer.score() == 1588

def test_sample_part2():
    polymer = Polymer.from_input(SAMPLE_INPUT)
    for i in range(40):
        polymer.grow()
    assert polymer.score() == 2188189693529


if __name__ == "__main__":
    with open("./input.txt") as file:
        polymer = Polymer.from_input(file.read())
    for i in range(10):
        polymer.grow()
    print("Part 1:", polymer.score())

    for i in range(30):
        polymer.grow()
    print("Part 2:", polymer.score())

