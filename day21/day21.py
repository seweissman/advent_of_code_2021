from collections import defaultdict
class GameBoard:

    def __init__(self, initial_locs):

        self.n_players = len(initial_locs)
        self.player_locs = [l - 1 for l in initial_locs]
        self.player_scores = [0] * self.n_players
        self.die_state = 0
        self.die_rolls = 0

    def player_roll(self, i):
        self.player_locs[i] = (self.player_locs[i] + self.die_state + 1 + self.die_state + 2 + self.die_state + 3) % 10
        self.player_scores[i] += self.player_locs[i] + 1
        self.die_state += 3
        self.die_rolls += 3
        if self.player_scores[i] >= 1000:
            return True
        return False

    def run_game(self):
        rounds = 0
        while True:
            is_winner = self.player_roll(rounds % self.n_players)
            if is_winner:
                # return losing player score times number of die rolls
                return self.player_scores[(rounds+1) % self.n_players]*self.die_rolls
            rounds += 1


def test_sample():

    game = GameBoard([4,8])
    result = game.run_game()
    assert result == 739785

    n_paths_to_win1, n_paths_to_win2, win1_states, win2_states, all_states_p1, all_states_p2, end_states_p1, end_states_p2 \
        = find_paths_to_end(4, 8, 10)

    n_paths_to_win1_ex, n_paths_to_win2_ex, win1_states_ex, win2_states_ex, all_states_p1_ex, all_states_p2_ex, end_states_p1_ex, end_states_p2_ex \
        = find_paths_to_end_exhaust(4, 8, 10)

    # Round 1
    # 4,0
    # 8,0
    # rolls: 11, 12, 21, 22
    # rolls: 11, 12, 21, 22
    # 11 11 6,6  10,10 ---> 2 wins
    # 11 12 6,6  1, 1
    # 11 21 6,6  1, 1
    # 11 22 6,6  2, 2
    # 12 11 7,7  10,10 ---> 1 wins  ((6, 7), (9, 10), 1), x
    # 12 12 7,7  1,1 ---> 1 wins  ((6, 7), (0, 1), 1), x
    # 12 21 7,7  1,1 ---> 1 wins  ((6, 7), (0, 1), 1), x
    # 12 22 7,7  2,2 ---> 1 wins  ((6, 7), (1, 2), 1)}x
    # 21 11 7,7  10,10 ---> 1 wins  ((6, 7), (9, 10), 1), x
    # 21 12 7,7  1,1 ---> 1 wins ((6, 7), (0, 1), 1), x
    # 21 21 7,7  1,1 ---> 1 wins  ((6, 7), (0, 1), 1), x
    # 21 22 7,7  2,2 ---> 1 wins  ((6, 7), (1, 2), 1)}x
    # 22 11 8,8  10,10 ---> 1 wins ((7, 8), (9, 10), 1), x
    # 22 12 8,8  1,1 ---> 1 wins ((7, 8), (0, 1), 1), x
    # 22 21 8,8  1,1 ---> 1 wins  ((7, 8), (0, 1), 1), x
    # 22 22 8,8  2,2 ---> 1 wins  ((7, 8), (1, 2), 1), x




# 3 x 16 wins for 1 in round 2 = 48 wins for 1, + 12 wins in round 1 = 60
# 1 win for 2

# Round 2
    # 6,6  1, 1
    # rolls: 11, 12, 21, 22
    # rolls: 11, 12, 21, 22
    # 11 11 8,14  3,4 ---> 1 wins  ((7, 14), (2, 4), 2), 
    # 11 12 8,14  4,5 ---> 1 wins  ((7, 14), (3, 5), 2), 
    # 11 21 8,14  4,5 ---> 1 wins  ((7, 14), (3, 5), 2), 
    # 11 22 8,14  5,6 ---> 1 wins ((7, 14), (4, 6), 2), 
    # 12 11 9,15  3,4 ---> 1 wins ((8, 15), (2, 4), 2), 
    # 12 12 9,15  4,5 ---> 1 wins ((8, 15), (3, 5), 2), 
    # 12 21 9,15  4,5 ---> 1 wins ((8, 15), (3, 5), 2), 
    # 12 22 9,15  5,6 ---> 1 wins  ((8, 15), (4, 6), 2),
    # 21 11 9,15  3,4 ---> 1 wins  ((8, 15), (2, 4), 2), 
    # 21 12 9,15  4,5 ---> 1 wins  ((8, 15), (3, 5), 2), 
    # 21 21 9,15  4,5 ---> 1 wins  ((8, 15), (3, 5), 2), 
    # 21 22 9,15  5,6 ---> 1 wins  ((8, 15), (4, 6), 2), 
    # 22 11 10,16  3,4 ---> 1 wins   {((9, 16), (2, 4), 2), 
    # 22 12 10,16  4,5 ---> 1 wins   ((9, 16), (3, 5), 2), 
    # 22 21 10,16  4,5 ---> 1 wins   ((9, 16), (3, 5), 2), 
    # 22 22 10,16  5,6 ---> 1 wins   ((9, 16), (4, 6), 2), 

    # 6,6  2, 2
    # rolls: 11, 12, 21, 22
    # rolls: 11, 12, 21, 22
    # 11 11 8,14  4,6 ---> 1 wins  ((7, 14), (3, 6), 2),  x
    # 11 12 8,14  5,7 ---> 1 wins ((7, 14), (4, 7), 2),  x
    # 11 21 8,14  5,7 ---> 1 wins ((7, 14), (4, 7), 2), x
    # 11 22 8,14  6,8 ---> 1 wins ((7, 14), (5, 8), 2),  x
    # 12 11 9,15  4,6 ---> 1 wins ((8, 15), (3, 6), 2), x
    # 12 12 9,15  5,7 ---> 1 wins ((8, 15), (4, 7), 2),  x
    # 12 21 9,15  5,7 ---> 1 wins ((8, 15), (4, 7), 2), x
    # 12 22 9,15  6,8 ---> 1 wins  ((8, 15), (5, 8), 2), x
    # 21 11 9,15  4,6 ---> 1 wins  ((8, 15), (3, 6), 2), x
    # 21 12 9,15  5,7 ---> 1 wins  ((8, 15), (4, 7), 2), x 
    # 21 21 9,15  5,7 ---> 1 wins  ((8, 15), (4, 7), 2),  x
    # 21 22 9,15  6,8 ---> 1 wins  ((8, 15), (5, 8), 2), x
    # 22 11 10,16  4,6 ---> 1 wins   ((9, 16), (3, 6), 2), x
    # 22 12 10,16  5,7 ---> 1 wins   ((9, 16), (4, 7), 2), x
    # 22 21 10,16  5,7 ---> 1 wins   ((9, 16), (4, 7), 2),  x
    # 22 22 10,16  6,8 ---> 1 wins  ((9, 16), (5, 8), 2),  x

    print("Paths:", n_paths_to_win1_ex, n_paths_to_win1)
    assert n_paths_to_win1 == n_paths_to_win1_ex
    assert n_paths_to_win2 == n_paths_to_win2_ex
    assert win1_states == win1_states_ex
    assert win2_states == win2_states_ex
    
def find_paths_to_end_exhaust(start1, start2, winning_score):
    stack = [((start1 - 1, 0), (start2 - 1, 0), 0)]
    paths_to_win1 = 0
    win1_states = set()
    paths_to_win2 = 0
    win2_states = set()
    all_states1 = set()
    all_states2 = set()
    end_states1 = set()
    end_states2 = set()
    while stack:
        state1, state2, round = stack.pop()
        all_states1.add((state1[0], state1[1], round))
        all_states2.add((state2[0], state2[1], round))
        loc1, score1 = state1
        loc2, score2, = state2
        if score1 >= winning_score:
            end_states1.add((state1[0], state1[1], round))
            end_states2.add((state2[0], state2[1], round))
            paths_to_win1 += 1
            win1_states.add((state1, state2, round))
            continue
        else:
            if score2 >= winning_score:
                paths_to_win2 += 1
                end_states1.add((state1[0], state1[1], round))
                end_states2.add((state2[0], state2[1], round))
                win2_states.add((state1, state2, round))
                continue
        for r1_1 in (1,2):
            for r1_2 in (1,2):
                roll1 = r1_1 + r1_2
                new_loc1 = (loc1 + roll1) % 10
                new_score1 = score1 + new_loc1 + 1
                for r2_1 in (1,2):
                    for r2_2 in (1,2):
                        roll2 = r2_1 + r2_2
                        new_loc2 = (loc2 + roll2) % 10
                        new_score2 = score2 + new_loc2 + 1
                        stack.append(((new_loc1, new_score1), (new_loc2, new_score2), round+1))
    print("Paths to win: ", paths_to_win1, paths_to_win2)
    print("N winning states", len(win1_states), len(win2_states))
    print("All states", len(all_states1), len(all_states2))
    print([(state1, state2, round) for (state1, state2, round) in win1_states if round == 1])
    #print(win1_states)
    return (paths_to_win1, paths_to_win2, win1_states, win2_states, 
            all_states1, all_states2, end_states1, end_states2)


THREE_ROLLS =  [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]
TWO_ROLLS =  [(2, 1), (3, 2), (4, 1)]

def find_paths_to_end(start1, start2, winning_score):
    all_states_p1 = find_all_states(start1, winning_score)
    print("p1 all locs", len(all_states_p1))
    end_states_p1 = {(loc, score, round) for (loc, score, round) in all_states_p1 if score >= winning_score}
    print("p1 end locs", len(end_states_p1))
    all_states_p2 = find_all_states(start2, winning_score)
    print("p2 all locs", len(all_states_p2))
    end_states_p2 = {(loc, score, round) for (loc, score, round) in all_states_p2 if score >= winning_score}
    print("p2 end locs", len(end_states_p2))

    # end states where player 1 wins
    win1_states = set()
    for loc1, score1, round1 in end_states_p1:
        for loc2, score2, round2 in all_states_p2:
            if round1 == round2 and score1 >= winning_score:
                win1_states.add(((loc1, score1), (loc2, score2), round1))

    win2_states = set()
    for loc2, score2, round2 in end_states_p2:
        for loc1, score1, round1 in all_states_p1:
            if round1 == round2 and score1 < winning_score and score2 >= winning_score:
                win2_states.add(((loc1, score1), (loc2, score2), round1))

    #calc_paths_to_end(paths_to_end, winning_states)
    paths_to_end1 = defaultdict(int)
    states = set()
    for state in win1_states:
        states.add(state)
        paths_to_end1[state] = 1

    seen = set()
    while states:
        print("\n\nIteration:")
        print("Paths to end: ", paths_to_end1[((3, 0), (7, 0), 0)])
        new_states = set()
        for state in states:
            p1_state, p2_state, round = state
            loc1, score1 = p1_state
            loc2, score2 = p2_state
            if round == 0 or ((loc1, score1, round) not in all_states_p1) or ((loc2, score2, round) not in all_states_p2):
                continue
            #print(state)
            prev_round = round - 1
            for roll1, mult1 in TWO_ROLLS:
                prev_loc1 = (loc1 - roll1) % 10
                prev_score1 = score1 - (loc1 + 1)
                for roll2, mult2 in TWO_ROLLS:
                    prev_loc2 = (loc2 - roll2) % 10
                    prev_score2 = score2 - (loc2 + 1)
                    new_state = ((prev_loc1, prev_score1),(prev_loc2, prev_score2), prev_round)
                    new_states.add(new_state)
        #print("New states:", new_states)
        for new_state1, new_state2, new_round in sorted(new_states, key=lambda s: -1*s[2]):
            if (new_state1, new_state2, new_round) in seen:
                continue
            new_loc1, new_score1 = new_state1
            new_loc2, new_score2 = new_state2
            for roll1, mult1 in TWO_ROLLS:
                loc1 = (new_loc1 + roll1) % 10
                score1 = new_score1 + (loc1 + 1)
                for roll2, mult2 in TWO_ROLLS:
                    loc2 = (new_loc2 + roll2) % 10
                    score2 = new_score2 + (loc2 + 1)
                    if (
                        (((new_loc1, new_score1), new_round) == ((3, 0), 0) and ((new_loc2, new_score2), new_round) == ((7, 0), 0)) or
                        (((new_loc1, new_score1), new_round) == ((5, 6), 1) and ((new_loc2, new_score2), new_round) == ((1, 2), 1)) 
                        ):
                        amount_to_add = mult1*mult2*paths_to_end1[((loc1, score1), (loc2, score2), new_round + 1)]
                        #print("loc1", "loc2", new_loc1, new_loc2, loc1, score1, loc2, score2, roll1, roll2, "Adding: ", amount_to_add)
                        #print("Adding:", amount_to_add)

                    paths_to_end1[((new_loc1, new_score1), (new_loc2, new_score2), new_round)] += mult1*mult2*paths_to_end1[((loc1, score1), (loc2, score2), new_round + 1)]

        states = new_states
        seen = seen.union(new_states)

    paths_to_end2 = defaultdict(int)
    states = []
    for state in win2_states:
        states.append(state)
        paths_to_end2[state] = 1

    seen = set()
    while states:
        p1_state, p2_state, round = states.pop()
        loc1, score1 = p1_state
        loc2, score2 = p2_state
        seen.add((p1_state, p2_state, round))
        if round == 0 or ((loc1, score1, round) not in all_states_p1) or ((loc2, score2, round) not in all_states_p2):
            continue
        prev_round = round - 1
        for roll1, mult1 in TWO_ROLLS:
            prev_loc1 = (loc1 - roll1) % 10
            prev_score1 = score1 - (loc1 + 1)
            for roll2, mult2 in TWO_ROLLS:
                prev_loc2 = (loc2 - roll2) % 10
                prev_score2 = score2 - (loc2 + 1)
                assert paths_to_end2[(p1_state, p2_state, round)] != 0
                paths_to_end2[((prev_loc1, prev_score1), (prev_loc2, prev_score2), prev_round)] += mult1*mult2*paths_to_end2[(p1_state, p2_state, round)]
                new_state = ((prev_loc1, prev_score1),(prev_loc2, prev_score2), prev_round)
                if new_state not in seen:
                    states.append(new_state)

    # for p1_state, p2_state, round in paths_to_end:
    #     if round == 0:
    #         print(p1_state, p2_state, paths_to_end[p1_state, p2_state, round])
    print("Paths to end: ", paths_to_end1[((3, 0), (7, 0), 0)])

    print("Paths:", paths_to_end2[((start1-1, 0), (start2-1, 0), 0)])
    #print(paths_to_end)
    return (paths_to_end1[((start1-1, 0), (start2-1, 0), 0)], paths_to_end2[((start1-1, 0), (start2-1, 0), 0)], win1_states, win2_states, 
            all_states_p1, all_states_p2, end_states_p1, end_states_p2)

#def calc_paths_to_end()


def find_all_states(start, winning_score):
    seen = set()
    stack = [(start-1, 0, 0)]
    while stack:
        loc, score, round = stack.pop()
        seen.add((loc, score, round))
        if score >= winning_score:
            continue
        for i in range(1,3):
            for j in range(1, 3):
                roll = i + j
                new_loc = (loc + roll) % 10
                new_score = score + new_loc + 1
                new_round = round + 1
                if (new_loc, new_score, new_round) not in seen:
                    stack.append((new_loc, new_score, new_round))
    return seen


if __name__ == "__main__":
    game = GameBoard([7,8])
    result = game.run_game()
    print("Part 1: ", result)

