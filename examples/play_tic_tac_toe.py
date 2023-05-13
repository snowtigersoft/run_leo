from run_leo import import_leo_program


class TicTacToe:
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

    @staticmethod
    def get_board_point(player):
        while True:
            user_input = input(f"Player {player}: "
                               f"Please enter two numbers between 1 and 3, separated by a space (e.g., 1 2): ")
            try:
                x, y = map(int, user_input.split())
                if 1 <= x <= 3 and 1 <= y <= 3:
                    return x, y
                else:
                    print("Both numbers should be between 1 and 3. Please try again.")
            except ValueError:
                print("Invalid input format. Please try again.")

    def play(self):
        player = 1
        win = 0
        step = 1
        ttt = import_leo_program('../tests/leo_examples/tictactoe')()

        print("Init, waiting...")

        board = ttt.new()
        self.echo(0, 0, board, 0)

        while not win and not self.no_left_piece:
            row, col = self.get_board_point(player)
            board, win = ttt.make_move(player, int(row), int(col), board)
            self.echo(step, player, board, win)
            step += 1
            player = 2 if player == 1 else 1


if __name__ == '__main__':
    TicTacToe().play()
