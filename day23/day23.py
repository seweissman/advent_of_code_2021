SAMPLE_INPUT="""#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

AMPHIPOD_ENERGY = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

burrow_hallway_positions = [2,4,6,8]


class BurrowState:
    def __init__(self, hallway, burrows):
        self.hallway = list(hallway)
        self.burrows = []
        for b in burrows:
            self.burrows.append(list(b))

    def move_from_burrow_to_hallway(self, burrow_number, hallway_space):
        if self.burrows[burrow_number][0] != ".":
            amphipod = self.burrows[burrow_number][0]
            self.hallway[hallway_space] = self.burrows[burrow_number][0]
            self.burrows[burrow_number][0] = "."
            move_ct = abs(hallway_space - burrow_hallway_positions[burrow_number]) + 1
            move_energy = move_ct * AMPHIPOD_ENERGY[amphipod]
            return move_energy
        else:
            amphipod = self.burrows[burrow_number][1]
            self.hallway[hallway_space] = self.burrows[burrow_number][1]
            self.burrows[burrow_number][1] = "."
            move_ct = abs(hallway_space - burrow_hallway_positions[burrow_number]) + 2
            move_energy = move_ct * AMPHIPOD_ENERGY[amphipod]
            return move_energy

    def move_from_hallway_to_burrow(self, burrow_number, hallway_space):
        burrow_hallway_positions = [2,4,6,8]
        if self.burrows[burrow_number][1] == ".":
            amphipod = self.hallway[hallway_space]
            self.burrows[burrow_number][1] = amphipod
            self.hallway[hallway_space] = "."
            move_ct = abs(hallway_space - burrow_hallway_positions[burrow_number]) + 2
            move_energy = move_ct * AMPHIPOD_ENERGY[amphipod]
            return move_energy
        else:
            amphipod = self.hallway[hallway_space]
            self.burrows[burrow_number][0] = amphipod
            self.hallway[hallway_space] = "."
            move_ct = abs(hallway_space - burrow_hallway_positions[burrow_number]) + 1
            move_energy = move_ct * AMPHIPOD_ENERGY[amphipod]
            return move_energy

    def move_from_burrow_to_burrow(self, burrow_start, burrow_end):
        if self.burrows[burrow_start][0] != ".":
            burrow_start_depth = 0
        else:
            burrow_start_depth = 1
        
        if self.burrows[burrow_end][1] == ".":
            burrow_end_depth = 1
        else:
            burrow_end_depth = 0
        
        amphipod = self.burrows[burrow_start][burrow_start_depth]
        self.burrows[burrow_end][burrow_end_depth] = amphipod
        self.burrows[burrow_start][burrow_start_depth] = "."

        move_ct = abs(burrow_hallway_positions[burrow_start] - burrow_hallway_positions[burrow_end]) + 2 + burrow_start_depth + burrow_end_depth
        move_energy = move_ct * AMPHIPOD_ENERGY[amphipod]
        return move_energy
    
    def get_next_amphipod_in_burrow(self, burrow_num):
        if self.burrows[burrow_num][0] != ".":
            return self.burrows[burrow_num][0],0
        if self.burrows[burrow_num][1] != ".":
            return self.burrows[burrow_num][1],1

    def is_empty_burrow(self, burrow_num):
        return self.burrows[burrow_num][0] == "." and self.burrows[burrow_num][1] == "."

    def has_room_burrow(self, burrow_num):
        return self.burrows[burrow_num][0] == "."

    def is_hallway_reachable_from_burrow(self, burrow_num, hallway_space):
        burrow_hallway_space = burrow_hallway_positions[burrow_num]
        min_space = min(hallway_space, burrow_hallway_space)
        max_space = max(hallway_space, burrow_hallway_space)
        return all([self.hallway[sp] == "." for sp in range(min_space, max_space + 1)])

    def is_burrow_reachable_from_hallway(self, burrow_num, hallway_space):
        burrow_hallway_space = burrow_hallway_positions[burrow_num]
        min_space = min(hallway_space, burrow_hallway_space)
        max_space = max(hallway_space, burrow_hallway_space)
        if hallway_space == min_space:
            min_space += 1
        else:
            max_space -= 1
        return all([self.hallway[sp] == "." for sp in range(min_space, max_space + 1)])


    def get_burrow_state(self):
        return tuple(self.hallway),((self.burrows[0][0], self.burrows[0][1]), 
                                    (self.burrows[1][0], self.burrows[1][1]),
                                    (self.burrows[2][0], self.burrows[2][1]),
                                    (self.burrows[3][0], self.burrows[3][1]))

    def make_move(self,move_type, n1, n2):
        if move_type == "bth":
            cost = self.move_from_burrow_to_hallway(n1, n2)
        elif move_type == "btb":
            cost = self.move_from_burrow_to_burrow(n1, n2)
        else: # move_type == htb
            cost = self.move_from_hallway_to_burrow(n1, n2)
        return cost


def test_move_amphipods():
    burrows = [["B", "A"],["C", "D"],["B", "C"],["D","A"]]
    burrow = BurrowState(["."]*11, burrows)

    is_reachable = burrow.is_hallway_reachable_from_burrow(2, 3)
    assert is_reachable == True

    energy = burrow.move_from_burrow_to_hallway(2, 3)
    assert energy == 40

    is_reachable = burrow.is_hallway_reachable_from_burrow(0, 3)
    assert is_reachable == False

    is_reachable = burrow.is_hallway_reachable_from_burrow(0, 10)
    assert is_reachable == False

    is_reachable = burrow.is_hallway_reachable_from_burrow(0, 0)
    assert is_reachable == True

    energy = burrow.move_from_burrow_to_burrow(1,2)
    assert energy == 400

    energy = burrow.move_from_burrow_to_hallway(1,5)
    assert energy == 3000

    energy = burrow.move_from_hallway_to_burrow(1, 3)
    assert energy == 30

from heapq import heappop, heappush

def get_legal_moves(burrow):
    legal_moves = []
    for burrow_num in range(4):
        if not burrow.is_empty_burrow(burrow_num):
            amphipod, depth = burrow.get_next_amphipod_in_burrow(burrow_num)
            if (["A","B","C","D"].index(amphipod) == burrow_num 
                and (depth == 1 or (depth == 0 and burrow.burrows[burrow_num][1] == amphipod))):
                continue
            for hallway_space in range(len(burrow.hallway)):
                if hallway_space in burrow_hallway_positions:
                    continue
                if burrow.is_hallway_reachable_from_burrow(burrow_num, hallway_space):
                    legal_moves.append(("bth", burrow_num, hallway_space))
            for other_burrow_num in range(4):
                if burrow_num != other_burrow_num:
                    if (["A","B","C","D"].index(amphipod) == other_burrow_num
                        and burrow.is_hallway_reachable_from_burrow(burrow_num, 
                                                        burrow_hallway_positions[other_burrow_num])
                        and burrow.has_room_burrow(other_burrow_num)):
                        legal_moves.append(("btb", burrow_num, other_burrow_num))
    for hallway_space in range(0, 11):
        amphipod = burrow.hallway[hallway_space]
        if amphipod != ".":
            for burrow_num in range(0,4):
                if (burrow.is_burrow_reachable_from_hallway(burrow_num, hallway_space) 
                    and burrow.has_room_burrow(burrow_num)
                    and ["A","B","C","D"].index(amphipod) == burrow_num):
                    legal_moves.append(("htb", burrow_num, hallway_space))
    return legal_moves

def test_legal_moves():
    hallway = [".",".",".","B",".",".",".",".",".",".","."]
    burrows = [["B","A"],[".","D"],["C","C"],["D","A"]]
    burrow = BurrowState(hallway, burrows)
    legal_moves = get_legal_moves(burrow)
    print(legal_moves)
    burrow.make_move("bth",1,5)
    print(burrow.get_burrow_state())
    #import pdb; pdb.set_trace()
    legal_moves = get_legal_moves(burrow)
    print(legal_moves)

def find_least_energy_solution(start_burrow: BurrowState):
    paths = []
    heappush(paths, (0, start_burrow.get_burrow_state()))
    seen = set()
    #import pdb; pdb.set_trace()
    while paths:
        cost, burrow_state = heappop(paths)
        #print(cost, burrow_state)
        if burrow_state in seen:
            continue
        # if burrow_state is final return cost
        if burrow_state[1] == (("A","A"),("B","B"),("C","C"),("D","D")):
            return cost
        seen.add(burrow_state)
        burrow = BurrowState(burrow_state[0], burrow_state[1])
        legal_moves = get_legal_moves(burrow)
        #print(burrow_state, legal_moves)
        for move_type, n1, n2 in legal_moves:
            burrow = BurrowState(burrow_state[0], burrow_state[1])
            move_cost = burrow.make_move(move_type, n1, n2)
            new_cost = cost + move_cost

            heappush(paths, (new_cost, burrow.get_burrow_state()))

    import pdb; pdb.set_trace()

def test_sample():
    burrows = [["B", "A"],["C", "D"],["B", "C"],["D","A"]]
    start_burrow = BurrowState(["."]*11, burrows)
    cost = find_least_energy_solution(start_burrow)
    assert cost == 12521

if __name__ == "__main__":
    burrows = [["D", "C"],["C", "A"],["D", "A"],["B","B"]]
    start_burrow = BurrowState(["."]*11, burrows)
    cost = find_least_energy_solution(start_burrow)
    print("Part 1: ", cost)
