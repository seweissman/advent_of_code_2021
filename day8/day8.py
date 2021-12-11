"""
--- Day 8: Seven Segment Search ---
You barely reach the safety of the cave when the whale smashes into the cave mouth, collapsing it. Sensors indicate another exit to this cave at a much greater depth, so you have no choice but to press on.

As your submarine slowly makes its way through the cave system, you notice that the four-digit seven-segment displays in your submarine are malfunctioning; they must have been damaged during the escape. You'll be in a lot of trouble without them, so you'd better figure out what's wrong.

Each digit of a seven-segment display is rendered by turning on or off any of seven segments named a through g:

  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
So, to render a 1, only segments c and f would be turned on; the rest would be off. To render a 7, only segments a, c, and f would be turned on.

The problem is that the signals which control the segments have been mixed up on each display. The submarine is still trying to display numbers by producing output on signal wires a through g, but those wires are connected to segments randomly. Worse, the wire/segment connections are mixed up separately for each four-digit display! (All of the digits within a display use the same connections, though.)

So, you might know that only signal wires b and g are turned on, but that doesn't mean segments b and g are turned on: the only digit that uses two segments is 1, so it must mean segments c and f are meant to be on. With just that information, you still can't tell which wire (b/g) goes to which segment (c/f). For that, you'll need to collect more information.

For each display, you watch the changing signals for a while, make a note of all ten unique signal patterns you see, and then write down a single four digit output value (your puzzle input). Using the signal patterns, you should be able to work out which pattern corresponds to which digit.

For example, here is what you might see in a single entry in your notes:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf
(The entry is wrapped here to two lines so it fits; in your notes, it will all be on a single line.)

Each entry consists of ten unique signal patterns, a | delimiter, and finally the four digit output value. Within an entry, the same wire/segment connections are used (but you don't know what the connections actually are). The unique signal patterns correspond to the ten different ways the submarine tries to render a digit using the current wire/segment connections. Because 7 is the only digit that uses three segments, dab in the above example means that to render a 7, signal lines d, a, and b are on. Because 4 is the only digit that uses four segments, eafb means that to render a 4, signal lines e, a, f, and b are on.

Using this information, you should be able to work out which combination of signal wires corresponds to each of the ten digits. Then, you can decode the four digit output value. Unfortunately, in the above example, all of the digits in the output value (cdfeb fcadb cdfeb cdbaf) use five segments and are more difficult to deduce.

For now, focus on the easy digits. Consider this larger example:

be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
fgae cfgab fg bagce
Because the digits 1, 4, 7, and 8 each use a unique number of segments, you should be able to tell which combinations of signals correspond to those digits. Counting only digits in the output values (the part after | on each line), in the above example, there are 26 instances of digits that use a unique number of segments (highlighted above).

In the output values, how many times do digits 1, 4, 7, or 8 appear?

--- Part Two ---
Through a little deduction, you should now be able to determine the remaining digits. Consider again the first example above:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf
After some careful analysis, the mapping between signal wires and segments only make sense in the following configuration:

 dddd
e    a
e    a
 ffff
g    b
g    b
 cccc
So, the unique signal patterns would correspond to the following digits:

acedgfb: 8
cdfbe: 5
gcdfa: 2
fbcad: 3
dab: 7
cefabd: 9
cdfgeb: 6
eafb: 4
cagedb: 0
ab: 1
Then, the four digits of the output value can be decoded:

cdfeb: 5
fcadb: 3
cdfeb: 5
cdbaf: 3
Therefore, the output value for this entry is 5353.

Following this same process for each entry in the second, larger example above, the output value of each entry can be determined:

fdgacbe cefdb cefbgd gcbe: 8394
fcgedb cgb dgebacf gc: 9781
cg cg fdcagb cbg: 1197
efabcd cedba gadfec cb: 9361
gecf egdcabf bgf bfgea: 4873
gebdcfa ecba ca fadegcb: 8418
cefg dcbef fcge gbcadfe: 4548
ed bcgafe cdgba cbgef: 1625
gbdfcae bgc cg cgb: 8717
fgae cfgab fg bagce: 4315
Adding all of the output values in this larger example produces 61229.

For each entry, determine all of the wire/segment connections and decode the four-digit output values. What do you get if you add up all of the output values?
"""

SAMPLE_INPUT=\
"""
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""

from collections import namedtuple, defaultdict

Entry = namedtuple("Entry", ["signal_patterns", "output_patterns"])

def count_1478(pattern_list):
    count = 0
    for pattern in pattern_list:
        if len(pattern) in [2, 3, 4, 7]:
            count += 1
    return count

def find_segments(signal_patterns):
    
    # How many times does each segment occur in the 10 digits
    # a : 7
    # b : 6
    # c : 8
    # d : 7
    # e : 4
    # f : 9
    # g : 7
    # We can find segments b e and f because they have unique counts

    segment_ct = defaultdict(int)
    segment_map = {}
    for segment in "abcdefg":
        segment_map[segment] = ""
    
    for pattern in signal_patterns:
        for segment in pattern:
            segment_ct[segment] += 1
    
    for segment, ct in segment_ct.items():
        if ct == 6:
            segment_map["b"] = segment
        if ct == 4:
            segment_map["e"] = segment
        if ct == 9:
            segment_map["f"] = segment

    # We can derive segments c, a and d from the unique 1,7,4 patterns using known segments

    for pattern in signal_patterns:
        if len(pattern) == 2:
            one_pattern = pattern
        if len(pattern) == 4:
            four_pattern = pattern
        if len(pattern) == 3:
            seven_pattern = pattern
    
    segment_map["c"] = list(set(one_pattern) - set(segment_map["f"]))[0]
    segment_map["a"] = list(set(seven_pattern) - {segment_map["c"], segment_map["f"]})[0]
    segment_map["d"] = list(set(four_pattern) - {segment_map["b"], segment_map["c"], segment_map["f"]})[0]

    # g is the only segment remaining
    
    segment_map["g"] = list(set("abcdefg") - set(segment_map.values()))[0]
    return segment_map

def pattern_to_digit(pattern, segment_map):
    reverse_segment_map = {value:key for key,value in segment_map.items()}
    decode_pattern = {reverse_segment_map[segment] for segment in pattern}
    if decode_pattern == set("abcfeg"):
        return 0
    if decode_pattern == set("cf"):
        return 1
    if decode_pattern == set("acdeg"):
        return 2
    if decode_pattern == set("acdfg"):
        return 3
    if decode_pattern == set("bcdf"):
        return 4
    if decode_pattern == set("abdfg"):
        return 5
    if decode_pattern == set("abdefg"):
        return 6
    if decode_pattern == set("acf"):
        return 7
    if decode_pattern == set("abcdefg"):
        return 8
    if decode_pattern == set("abcdfg"):
        return 9

def read_input(input_lines):
    entries = []
    for line in input_lines:
        line = line.strip()
        if not line:
            continue
        signal_patterns, output_patterns = line.split(" | ")
        signal_patterns = signal_patterns.split(" ")
        output_patterns = output_patterns.split(" ")
        entry = Entry(signal_patterns=signal_patterns, output_patterns=output_patterns)
        entries.append(entry)
    return entries

def test_sample_part1():
    input_lines = SAMPLE_INPUT.split("\n")
    entries = read_input(input_lines)

    ct = sum([count_1478(entry.output_patterns) for entry in entries])
    assert ct == 26

def test_find_segments():
    signal_patterns = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab".split(" ")
    segment_map = find_segments(signal_patterns)
    assert segment_map["a"] == "d"
    assert segment_map["b"] == "e"
    assert segment_map["c"] == "a"
    assert segment_map["d"] == "f"
    assert segment_map["e"] == "g"
    assert segment_map["f"] == "b"
    assert segment_map["g"] == "c"

def test_pattern_to_digit():
    signal_patterns = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab".split(" ")
    segment_map = find_segments(signal_patterns)
    assert pattern_to_digit("cdfeb", segment_map) == 5
    assert pattern_to_digit("fcadb", segment_map) == 3
    assert pattern_to_digit("cbdfe", segment_map) == 5
    assert pattern_to_digit("cdbaf", segment_map) == 3

def test_sample_part2():
    input_lines = SAMPLE_INPUT.split("\n")
    entries = read_input(input_lines)
    entry_sum = 0
    for entry in entries:
        segment_map = find_segments(entry.signal_patterns)
        digits = [pattern_to_digit(pattern, segment_map) for pattern in entry.output_patterns]
        value = sum([10**(3-i)*d for i,d in enumerate(digits)])
        entry_sum += value
    assert entry_sum == 61229


if __name__ == "__main__":
    with open("input.txt") as file:
        input_lines = file.readlines()
    input_lines = [line.strip() for line in input_lines]
    entries = read_input(input_lines)
    ct = sum([count_1478(entry.output_patterns) for entry in entries])
    print("part1:", ct)

    entry_sum = 0
    for entry in entries:
        segment_map = find_segments(entry.signal_patterns)
        digits = [pattern_to_digit(pattern, segment_map) for pattern in entry.output_patterns]
        value = sum([10**(3-i)*d for i,d in enumerate(digits)])
        entry_sum += value
    print("part2:", entry_sum)

