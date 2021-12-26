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

class DiracGameBoard:

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

# x_loc, x_score
# y_loc, y_score

# [. . . x . . . . . .]
# [. . . . . . . x . .]

# [. . . x . . y . . .]
# [. . y . . . . x . .]


#winning states for y:
#21 22 23 24 25 
# (3, 23) (4, 23) (5, 23) (6, 23) (7, 23) (8, 23) (9, 23)
# (4, 24) (5, 24) (6, 24) (7, 24) (8, 24) (9, 24)
# (5, 25) (6, 25) (7, 25) (8, 25) (9, 25)
# (6, 26) (7, 26) (8, 26) (9, 26)
# (8, 27) (0, 27) (7, 27) 
# (9, 28) (8, 28) 
# (9, 29) 

#(8, 25) -> ([5,4,3,2,1,10,9] ,17)

# 

# 3 X 1, 4 X 3, 5 X 6, 6 X 7, 7 X 6, 8 x 3, 9 x 1
# 1 1 1 = 3
# 1 1 2 = 4
# 1 1 3 = 5
# 1 2 1 = 4
# 1 2 2 = 5
# 1 2 3 = 6
# 1 3 1 = 5
# 1 3 2 = 6
# 1 3 3 = 7
# 2 1 1 = 4
# 2 1 2 = 5
# 2 1 3 = 6
# 2 2 1 = 5
# 2 2 2 = 6
# 2 2 3 = 7
# 2 3 1 = 6
# 2 3 2 = 7
# 2 3 3 = 8
# 3 1 1 = 5
# 3 1 2 = 6
# 3 1 3 = 7
# 3 2 1 = 6
# 3 2 2 = 7
# 3 2 3 = 8
# 3 3 1 = 7 
# 3 3 2 = 8
# 3 3 3 = 9

# 2 1
# 2 2
# 2 3
# 3 1
# 3 2
# 3 3

def test_sample():

    game = GameBoard([4,8])
    result = game.run_game()
    assert result == 739785

    all_locs_p1 = find_all_locs(4)
    print("4", len(all_locs_p1))
    end_locs_p1 = [(loc, score, round) for (loc, score, round) in all_locs_p1 if score >= 21]
    print("4 end locs", len(end_locs_p1))
    all_locs_p2 = find_all_locs(8)
    print("8", len(all_locs_p2))
    end_locs_p2 = [(loc, score, round) for (loc, score, round) in all_locs_p2 if score >= 21]
    print("8 end locs", len(end_locs_p2))

    end_game_states = set()
    for loc1, score1, round1 in end_locs_p1:
        for loc2, score2, round2 in all_locs_p2:
            if round1 == round2 and score1 >= 21:
                end_game_states.add(((loc1, score1), (loc2, score2), round1))

    for loc2, score2, round2 in end_locs_p2:
        for loc1, score1, round1 in all_locs_p1:
            if round1 == round2 and score1 < 21 and score2 >= 21:
                end_game_states.add(((loc1, score1), (loc2, score2), round1))

    print("Number of end game states: ", len(end_game_states))


    paths_to_end = defaultdict(int)
    states = []
    for state in end_game_states:
        states.append(state)
        paths_to_end[state] = 1
    
    #print(paths_to_end)

    seen = set()
    while states:
        p1_state, p2_state, round = states.pop()
        loc1, score1 = p1_state
        loc2, score2 = p2_state
        seen.add((p1_state, p2_state, round))
        if round == 0 or ((loc1, score1, round) not in all_locs_p1) or ((loc2, score2, round) not in all_locs_p2):
            continue
        prev_round = round - 1
        for roll1, mult1 in [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]:
            prev_loc1 = (loc1 - roll1) % 10
            prev_score1 = score1 - (loc1 + 1)
            for roll2, mult2 in [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]:
                prev_loc2 = (loc2 - roll2) % 10
                prev_score2 = score2 - (loc2 + 1)
                paths_to_end[((prev_loc1, prev_score1), (prev_loc2, prev_score2), prev_round)] += mult1*mult2*paths_to_end[(p1_state, p2_state, round)]
                new_state = ((prev_loc1, prev_score1),(prev_loc2, prev_score2), prev_round)
                if new_state not in seen:
                    states.append(new_state)

    # for p1_state, p2_state, round in paths_to_end:
    #     if round == 0:
    #         print(p1_state, p2_state, paths_to_end[p1_state, p2_state, round])
    print("Paths:", paths_to_end[((3, 0), (7, 0), 0)])

def find_all_locs(start):
    seen = set()
    stack = [(start-1, 0, 0)]
    while stack:
        loc, score, round = stack.pop()
        seen.add((loc, score, round))
        if score >= 21:
            continue
        for i in range(1,4):
            for j in range(1, 4):
                for k in range(1, 4):
                    roll = i + j + k
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

