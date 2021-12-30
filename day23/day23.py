
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
        amphipod, depth = self.get_next_amphipod_in_burrow(burrow_number)
        self.hallway[hallway_space] = amphipod
        self.burrows[burrow_number][depth] = "."
        move_ct = abs(hallway_space - burrow_hallway_positions[burrow_number]) + 1 + depth
        move_energy = move_ct * AMPHIPOD_ENERGY[amphipod]
        return move_energy

    def move_from_hallway_to_burrow(self, burrow_number, hallway_space):
        burrow_hallway_positions = [2,4,6,8]
        depth = self.get_next_empty_spot_in_burrow(burrow_number)
        amphipod = self.hallway[hallway_space]
        self.burrows[burrow_number][depth] = amphipod
        self.hallway[hallway_space] = "."
        move_ct = abs(hallway_space - burrow_hallway_positions[burrow_number]) + 1 + depth
        move_energy = move_ct * AMPHIPOD_ENERGY[amphipod]
        return move_energy

    def move_from_burrow_to_burrow(self, burrow_start, burrow_end):
        amphipod, start_depth = self.get_next_amphipod_in_burrow(burrow_start)
        end_depth = self.get_next_empty_spot_in_burrow(burrow_end)
        self.burrows[burrow_end][end_depth] = amphipod
        self.burrows[burrow_start][start_depth] = "."

        move_ct = abs(burrow_hallway_positions[burrow_start] - burrow_hallway_positions[burrow_end]) + 2 + start_depth + end_depth
        move_energy = move_ct * AMPHIPOD_ENERGY[amphipod]
        return move_energy
    
    def get_next_amphipod_in_burrow(self, burrow_num):
        burrow_size = len(self.burrows[burrow_num])
        for i in range(burrow_size):
            if self.burrows[burrow_num][i] != ".":
               return self.burrows[burrow_num][i],i
    
    def get_next_empty_spot_in_burrow(self, burrow_num):
        burrow_size = len(self.burrows[burrow_num])
        for i in range(burrow_size):
            if self.burrows[burrow_num][burrow_size - i - 1] == ".":
                return burrow_size - i - 1

    def is_empty_burrow(self, burrow_num):
        return all([burrow_contents == "." for burrow_contents in self.burrows[burrow_num]])

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

    def is_amphipod_already_in_home_burrow(self, burrow_num):
        amphipod, depth = self.get_next_amphipod_in_burrow(burrow_num)
        if all([["A","B","C","D"].index(self.burrows[burrow_num][d]) == burrow_num for d in range(depth, len(self.burrows[burrow_num]))]):
            return True
        return False

    def does_burrow_only_have_home_amphipods(self, burrow_num):
        if self.burrows[burrow_num][-1] == ".":
            return True
        amphipod, depth = self.get_next_amphipod_in_burrow(burrow_num)
        if all([["A","B","C","D"].index(self.burrows[burrow_num][d]) == burrow_num for d in range(depth, len(self.burrows[burrow_num]))]):
            return True
        return False
        

    def get_burrow_state(self):
        return tuple(self.hallway), (tuple(self.burrows[0]), 
                                     tuple(self.burrows[1]),
                                     tuple(self.burrows[2]),
                                     tuple(self.burrows[3]))

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
            if burrow.is_amphipod_already_in_home_burrow(burrow_num):
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
                        and burrow.has_room_burrow(other_burrow_num)
                        and burrow.does_burrow_only_have_home_amphipods(other_burrow_num)):
                        legal_moves.append(("btb", burrow_num, other_burrow_num))
    for hallway_space in range(0, 11):
        amphipod = burrow.hallway[hallway_space]
        if amphipod != ".":
            for burrow_num in range(0,4):
                if (burrow.is_burrow_reachable_from_hallway(burrow_num, hallway_space) 
                    and burrow.has_room_burrow(burrow_num)
                    and ["A","B","C","D"].index(amphipod) == burrow_num
                    and burrow.does_burrow_only_have_home_amphipods(burrow_num)):
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

def find_least_energy_solution(start_burrow: BurrowState, final_state):
    paths = []
    heappush(paths, (0, start_burrow.get_burrow_state()))
    seen = set()
    #import pdb; pdb.set_trace()
    n_paths = 0
    while paths:        
        cost, burrow_state = heappop(paths)
        if n_paths % 10000 == 0:
            print(cost, burrow_state)
        n_paths += 1
        if burrow_state in seen:
            continue
        # if burrow_state is final return cost
        if burrow_state[1] == final_state:
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


def test_sample_part1():
    burrows = [["B", "A"],["C", "D"],["B", "C"],["D","A"]]
    start_burrow = BurrowState(["."]*11, burrows)
    cost = find_least_energy_solution(start_burrow, (("A","A"),("B","B"),("C","C"),("D","D")))
    assert cost == 12521

def test_sample_part2_state_by_state():
    burrows = [["B", "D", "D", "A"],["C", "C", "B", "D"],["B", "B", "A", "C"],["D", "A", "C", "A"]]
    burrow = BurrowState(["."]*11, burrows)
    cost = 0
    moves = [
        ("bth",3,10),
        ("bth",3,0),
        ("bth",2,9),
        ("bth",2,7),
        ("bth",2,1),
        ("btb",1,2),
        ("btb",1,2),
        ("bth",1,5),
        ("bth",1,3),
        ("htb",1,5),
        ("htb",1,7),
        ("htb",1,9),
        ("btb",3,2),
        ("bth",3,9),
        ("htb",3,3),
        ("btb",0,1),
        ("btb",0,3),
        ("bth",0,3),
        ("htb",0,1),
        ("htb",0,0),
        ("htb",3,3),
        ("htb",0,9),
        ("htb",3,10),
    ]
    for move in moves:
        legal_moves = get_legal_moves(burrow)
        assert move in legal_moves
        move_cost = burrow.make_move(*move)
        cost += move_cost
    assert cost == 44169

def test_sample_part2_find():
    burrows = [["B", "D", "D", "A"],["C", "C", "B", "D"],["B", "B", "A", "C"],["D", "A", "C", "A"]]
    start_burrow = BurrowState(["."]*11, burrows)
    cost = find_least_energy_solution(start_burrow, (("A","A","A","A"),("B","B","B","B"),("C","C","C","C"),("D","D","D","D")))
    assert cost == 44169


if __name__ == "__main__":
    burrows = [["D", "C"],["C", "A"],["D", "A"],["B","B"]]
    start_burrow = BurrowState(["."]*11, burrows)
    cost = find_least_energy_solution(start_burrow, (("A","A"),("B","B"),("C","C"),("D","D")))
    print("Part 1: ", cost)


    burrows = [["D", "D", "D", "C"],["C", "C", "B", "A"],["D", "B", "A", "A"],["B","A", "C", "B"]]
    start_burrow = BurrowState(["."]*11, burrows)
    cost = find_least_energy_solution(start_burrow, (("A","A","A","A"),("B","B","B","B"),("C","C","C","C"),("D","D","D","D")))
    print("Part 2: ", cost)

