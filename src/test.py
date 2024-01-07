import jsonpickle
from JackalBoard import *


def test_board():
    board = JackalBoard()
    response = board.start()
    while True:
        response = next_move(response, board)


def next_move(response: JackalBoardResponse, board: JackalBoard) -> JackalBoardResponse:
    print(jsonpickle.encode(response, unpicklable=False, indent=4))
    opts = [opt.id for opt in response.options]
    selected_opt = int(input())
    return board.perform_option(opts[selected_opt])


if __name__ == '__main__':
    test_board()
