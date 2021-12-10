"""
--- Day 4: Giant Squid ---
You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any sunlight. What you can see, however, is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random, and the chosen number is marked on all boards on which it appears. (Numbers may not appear on all boards.) If all numbers in any row or any column of a board are marked, that board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the boards are marked as follows (shown here adjacent to each other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
At this point, the third board wins because it has at least one complete row or column of marked numbers (in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first. What will your final score be if you choose that board?

--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?
"""

from collections import defaultdict


SAMPLE_INPUT= """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?
"""


def make_board(num_map, board_num, board_lines):
    board = defaultdict(lambda: defaultdict(str))
    for row, line in enumerate(board_lines):
        num_list = [s for s in line.split(" ") if s]
        for col, n in enumerate(num_list):
            board[row][col] = n
            num_map[n].add((board_num, row, col))
    return board

def read_input(input_lines):
    num_map = defaultdict(set)
    numbers = input_lines[0].split(",")
    board_ct = 0
    boards = []
    for i in range(1, len(input_lines)-1, 5):
        board_lines = input_lines[i:i+5]
        board = make_board(num_map, board_ct, board_lines)
        board_ct += 1
        boards.append(board)
    return numbers, num_map, boards

def check_board(board):
    """Check if this board is a winner"""
    row_scores = defaultdict(int)
    col_scores = defaultdict(int)
    for col in range(5):
        for row in range(5):
            if board[row][col] == "x":
                row_scores[row] += 1
                col_scores[col] += 1
                if row_scores[row] == 5 or col_scores[col] == 5:
                    return True
    return False
        
def score_board(winning_number, board):
    unmarked_sum = 0
    for col in range(5):
        for row in range(5):
            if board[row][col] != "x":
                unmarked_sum += int(board[row][col])
    score = int(winning_number)*unmarked_sum
    return score

def print_board(board):
    for row in range(5):
        print(" ".join([board[row][col] for col in range(5)]))

def run_game(input_lines):
    numbers, num_map, boards = read_input(input_lines)
    # print(numbers)
    winners = set()
    board_scores = []
    for n in numbers:
        # print("Playing: ", n)
        # look up where on the board this number occurs
        board_locations = num_map[n]
        for board, row, col in board_locations:
            boards[board][row][col] = "x"
        # for board in boards:
        #     print_board(board)
        #     print("\n")
        for i,board in enumerate(boards):
            if not i in winners and check_board(board):
                score = score_board(n, board)
                winners.add(i)
                board_scores.append((i, score))
    return board_scores
        
def test_sample_game():
    input_lines = [line.strip() for line in SAMPLE_INPUT.split("\n") if line]
    board_scores = run_game(input_lines)
    assert(board_scores[0][1] == 4512)
    assert(board_scores[-1][1] == 1924)


if __name__ == "__main__":
    with open("input.txt") as file:
        lines = [line.strip() for line in file]
        input_lines = [line for line in lines if line]
    # print(input_lines)
    scores = run_game(input_lines)
    print(scores)

