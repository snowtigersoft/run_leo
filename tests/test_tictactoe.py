import unittest
from run_leo.core import import_leo_program


class TestLeoProgram(unittest.TestCase):
    no_left_piece = True

    def echo(self, step, player, board, win):
        self.no_left_piece = True

        def piece(row, col):
            if board[f'r{row}'][f'c{col}'] == 0:
                self.no_left_piece = False
                return ' '
            elif board[f'r{row}'][f'c{col}'] == 1:
                return 'x'
            else:
                return 'o'
        title = 'Creating a new game of Tic-Tac-Toe' if step == 0 else f'Player {player} makes the {step} move.        '
        print(f"""
###############################################################################
########                                                               ########
########          STEP {step}: {title}           ########
########                                                               ########
########                         | {piece(1, 1)} | {piece(1, 2)} | {piece(1, 3)} |                         ########
########                         | {piece(2, 1)} | {piece(2, 2)} | {piece(2, 3)} |                         ########
########                         | {piece(3, 1)} | {piece(3, 2)} | {piece(3, 3)} |                         ########
########                                                               ########
###############################################################################
""")
        if not win:
            if self.no_left_piece:
                print("""
###############################################################################
########                                                               ########
########               Game Complete! Players 1 & 2 Tied               ########
########                                                               ########
###############################################################################
""")
            return
        print(f"""
###############################################################################
########                                                               ########
########               Game Complete! Player {win} WIN                     ########
########                                                               ########
###############################################################################
""")

    def test_load_leo_program(self):
        ttt = import_leo_program('./leo_examples/tictactoe')()

        # Test if structs are successfully converted to class variables
        self.assertTrue(hasattr(ttt, "Row"))
        self.assertTrue(hasattr(ttt, "Board"))

        # Test if functions are successfully converted to class methods
        self.assertTrue(hasattr(ttt, "new"))
        self.assertTrue(hasattr(ttt, "make_move"))

        # Test class method calls
        board = ttt.new()
        print(board)
        self.echo(0, 0, board, 0)

        board, win = ttt.make_move(1, 1, 1, board)
        print((board, win))
        self.echo(1, 1, board, win)

        board, win = ttt.make_move(2, 2, 2, board)
        print((board, win))
        self.echo(2, 2, board, win)

        board, win = ttt.make_move(1, 3, 1, board)
        print((board, win))
        self.echo(3, 1, board, win)

        board, win = ttt.make_move(2, 2, 1, board)
        print((board, win))
        self.echo(4, 2, board, win)

        board, win = ttt.make_move(1, 2, 3, board)
        print((board, win))
        self.echo(5, 1, board, win)

        board, win = ttt.make_move(2, 1, 2, board)
        print((board, win))
        self.echo(6, 2, board, win)

        board, win = ttt.make_move(1, 3, 2, board)
        print((board, win))
        self.echo(7, 1, board, win)

        board, win = ttt.make_move(2, 3, 3, board)
        print((board, win))
        self.echo(8, 2, board, win)

        board, win = ttt.make_move(1, 1, 3, board)
        print((board, win))
        self.echo(9, 1, board, win)


if __name__ == '__main__':
    unittest.main()
