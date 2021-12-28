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


if __name__ == "__main__":
    game = GameBoard([7,8])
    result = game.run_game()
    print("Part 1: ", result)

    n_paths_to_win1, n_paths_to_win2 = find_paths_to_end((7,0), (8,0), 21)
    print("Part2: ", n_paths_to_win1, n_paths_to_win2)

    n_paths_to_win1, n_paths_to_win2 = find_paths_to_end((4,0), (8,0), 7)
    print("Test2: ", n_paths_to_win1, n_paths_to_win2)

