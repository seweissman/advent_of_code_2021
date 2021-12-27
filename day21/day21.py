from functools import cache

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

    paths1, paths2 = find_paths_to_end((4, 0), (8, 0), 21)
    assert paths1 == 444356092776315
    assert paths2 == 341960390180808


@cache
def find_paths_to_end(state1, state2, winning_score):
    loc1, score1 = state1
    loc2, score2 = state2

    wins1 = 0
    wins2 = 0
    for roll1 in TWO_ROLLS:
        for roll2 in TWO_ROLLS:
            new_loc1 = (loc1 + roll1 - 1) % 10 + 1
            new_score1 = score1 + new_loc1
            if new_score1 >= winning_score:
                wins1 += 1
                break
            new_loc2 = (loc2 + roll2 - 1) % 10 + 1
            new_score2 = score2 + new_loc2
            if new_score2 >= winning_score:
                wins2 += 1
                continue
            sub_wins1, sub_wins2 = find_paths_to_end((new_loc1, new_score1), (new_loc2, new_score2), winning_score)
            wins1 += sub_wins1
            wins2 += sub_wins2
    return wins1, wins2

THREE_ROLLS =  [3, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 8, 8, 8, 9]
TWO_ROLLS = [2, 3, 3, 4]

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
-        #print("New states:", new_states)
-        for new_state1, new_state2, new_round in sorted(new_states, key=lambda s: -1*s[2]):
-            if (new_state1, new_state2, new_round) in seen:
-                continue
-            new_loc1, new_score1 = new_state1
-            new_loc2, new_score2 = new_state2
-            for roll1, mult1 in TWO_ROLLS:
-                loc1 = (new_loc1 + roll1) % 10
-                score1 = new_score1 + (loc1 + 1)
-                for roll2, mult2 in TWO_ROLLS:
-                    loc2 = (new_loc2 + roll2) % 10
-                    score2 = new_score2 + (loc2 + 1)
-                    if (
-                        (((new_loc1, new_score1), new_round) == ((3, 0), 0) and ((new_loc2, new_score2), new_round) == ((7, 0), 0)) or
-                        (((new_loc1, new_score1), new_round) == ((5, 6), 1) and ((new_loc2, new_score2), new_round) == ((1, 2), 1))
-                        ):
-                        amount_to_add = mult1*mult2*paths_to_end1[((loc1, score1), (loc2, score2), new_round + 1)]
-                        #print("loc1", "loc2", new_loc1, new_loc2, loc1, score1, loc2, score2, roll1, roll2, "Adding: ", amount_to_add)
-                        #print("Adding:", amount_to_add)
-
-                    paths_to_end1[((new_loc1, new_score1), (new_loc2, new_score2), new_round)] += mult1*mult2*paths_to_end1[((loc1, score1), (loc2, score2), new_round + 1)]
-
-        states = new_states
-        seen = seen.union(new_states)
-


if __name__ == "__main__":
    game = GameBoard([7,8])
    result = game.run_game()
    print("Part 1: ", result)

    n_paths_to_win1, n_paths_to_win2 = find_paths_to_end((7,0), (8,0), 21)
    print("Part2: ", n_paths_to_win1, n_paths_to_win2)

    n_paths_to_win1, n_paths_to_win2 = find_paths_to_end((4,0), (8,0), 7)
    print("Test2: ", n_paths_to_win1, n_paths_to_win2)


# -    # Round 1
# -    # 4,0
# -    # 8,0
# -    # rolls: 11, 12, 21, 22
# -    # rolls: 11, 12, 21, 22
# -    # 11 11 6,6  10,10 ---> 2 wins
# -    # 11 12 6,6  1, 1
# -    # 11 21 6,6  1, 1
# -    # 11 22 6,6  2, 2
# -    # 12 11 7,7  10,10 ---> 1 wins  ((6, 7), (9, 10), 1), x
# -    # 21 11 7,7  10,10 ---> 1 wins  ((6, 7), (9, 10), 1), x
# -    # 22 11 8,8  10,10 ---> 1 wins ((7, 8), (9, 10), 1), x

# -
# -# Round 2
# -    # 6,6  1, 1
# -    # rolls: 11, 12, 21, 22
# -    # rolls: 11, 12, 21, 22
# -    # 11 11 8,14  3,4 ---> 1 wins  ((7, 14), (2, 4), 2),
# -    # 12 11 9,15  3,4 ---> 1 wins ((8, 15), (2, 4), 2),
# -    # 21 11 9,15  3,4 ---> 1 wins  ((8, 15), (2, 4), 2),
# -    # 22 11 10,16  3,4 ---> 1 wins   {((9, 16), (2, 4), 2),
# -
# -    # 6,6  2, 2
# -    # rolls: 11, 12, 21, 22
# -    # rolls: 11, 12, 21, 22
# -    # 11 11 8,14  4,6 ---> 1 wins  ((7, 14), (3, 6), 2),  x
# -    # 12 11 9,15  4,6 ---> 1 wins ((8, 15), (3, 6), 2), x
# -    # 21 11 9,15  4,6 ---> 1 wins  ((8, 15), (3, 6), 2), x
# -    # 22 11 10,16  4,6 ---> 1 wins   ((9, 16), (3, 6), 2), x
