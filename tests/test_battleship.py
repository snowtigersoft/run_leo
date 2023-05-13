import unittest

from run_leo import Account
from run_leo.core import import_leo_program


class TestBattleship(unittest.TestCase):

    def test_load_leo_program(self):
        bs = import_leo_program('./leo_examples/battleship')()

        # Test if structs are successfully converted to class variables
        self.assertTrue(hasattr(bs, "board__board_state"))
        self.assertTrue(hasattr(bs, "move__move"))

        # Test if functions are successfully converted to class methods
        self.assertTrue(hasattr(bs, "initialize_board"))
        self.assertTrue(hasattr(bs, "offer_battleship"))
        self.assertTrue(hasattr(bs, "start_battleship"))
        self.assertTrue(hasattr(bs, "play"))

        # create new accounts
        account1 = Account.new()
        account2 = Account.new()

        # Test class method calls
        print("""
###############################################################################
########                                                               ########
########                 STEP 1: Initializing Player 1                 ########
########                                                               ########
###############################################################################
""")
        bs.set_account(account1)
        print("✅ Successfully initialized Player 1.")

        print("""
###############################################################################
########                                                               ########
########           STEP 2: Player 1 Places Ships On The Board          ########
########                                                               ########
###############################################################################
""")
        board_state1 = bs.initialize_board(34084860461056, 551911718912, 7, 1157425104234217472, account2.address)
        print(board_state1)

        print("""
###############################################################################
########                                                               ########
########         STEP 3: Player 1 Passes The Board To Player 2         ########
########                                                               ########
###############################################################################
""")
        board_state1, move1 = bs.offer_battleship(board_state1)
        print((board_state1, move1))

        print("""
###############################################################################
########                                                               ########
########           STEP 4: Player 2 Places Ships On The Board          ########
########                                                               ########
###############################################################################
""")
        bs.set_account(account2)
        board_state2 = bs.initialize_board(31, 2207646875648, 224, 9042383626829824, account1.address)
        print(board_state2)

        print("""
###############################################################################
########                                                               ########
########          STEP 5: Passing The Board Back To Player 1           ########
########                                                               ########
###############################################################################
""")
        board_state2, move2 = bs.start_battleship(board_state2, move1)
        print((board_state2, move2))

        print("""
###############################################################################
########                                                               ########
########               STEP 6: Player 1 Takes The 1st Turn             ########
########                                                               ########
###############################################################################
""")
        bs.set_account(account1)
        board_state1, move1 = bs.play(board_state1, move2, 1)
        print((board_state1, move1))

        print("""
###############################################################################
########                                                               ########
########               STEP 7: Player 2 Takes The 2nd Turn             ########
########                                                               ########
###############################################################################
""")
        bs.set_account(account2)
        board_state2, move2 = bs.play(board_state2, move1, 2048)
        print((board_state2, move2))

        print("""
###############################################################################
########                                                               ########
########              STEP 8: Player 1 Takes The 3rd Turn              ########
########                                                               ########
###############################################################################
""")
        bs.set_account(account1)
        board_state1, move1 = bs.play(board_state1, move2, 2)
        print((board_state1, move1))

        print("""
###############################################################################
########                                                               ########
########               STEP 9: Player 2 Takes The 4th Turn             ########
########                                                               ########
###############################################################################
""")
        bs.set_account(account2)
        board_state2, move2 = bs.play(board_state2, move1, 4)
        print((board_state2, move2))


if __name__ == '__main__':
    unittest.main()
