import unittest

from run_leo import Account
from run_leo.core import import_leo_program


class TestAuction(unittest.TestCase):
    def test_load_leo_program(self):
        prog = import_leo_program('./leo_examples/auction')()

        # Test if structs/records are successfully converted to class variables
        self.assertTrue(hasattr(prog, "Bid"))

        # Test if functions are successfully converted to class methods
        self.assertTrue(hasattr(prog, "place_bid"))
        self.assertTrue(hasattr(prog, "resolve"))
        self.assertTrue(hasattr(prog, 'finish'))

        # create bidder and auctioneer account
        bidder1 = Account(address='aleo1yzlta2q5h8t0fqe0v6dyh9mtv4aggd53fgzr068jvplqhvqsnvzq7pj2ke',
                          private_key='APrivateKey1zkpG9Af9z5Ha4ejVyMCqVFXRKknSm8L1ELEwcc4htk9YhVK')
        bidder2 = Account(address='aleo1esqchvevwn7n5p84e735w4dtwt2hdtu4dpguwgwy94tsxm2p7qpqmlrta4',
                          private_key='APrivateKey1zkpAFshdsj2EqQzXh5zHceDapFWVCwR6wMCJFfkLYRKupug')
        auctioneer = Account(address="aleo1fxs9s0w97lmkwlcmgn0z3nuxufdee5yck9wqrs0umevp7qs0sg9q5xxxzh",
                             private_key="APrivateKey1zkp5wvamYgK3WCAdpBQxZqQX8XnuN2u11Y6QprZTriVwZVc")

        # Test leo method calls
        print("""
###############################################################################
########                                                               ########
########            STEP 0: Initialize a new 2-party auction           ########
########                                                               ########
########                -------------------------------                ########
########                |  OPEN   |    A    |    B    |                ########
########                -------------------------------                ########
########                |   Bid   |         |         |                ########
########                -------------------------------                ########
########                                                               ########
###############################################################################
""")
        # Have the first bidder place a bid of 10.
        print(""""
###############################################################################
########                                                               ########
########          STEP 1: The first bidder places a bid of 10          ########
########                                                               ########
########                -------------------------------                ########
########                |  OPEN   |    A    |    B    |                ########
########                -------------------------------                ########
########                |   Bid   |   10    |         |                ########
########                -------------------------------                ########
########                                                               ########
###############################################################################
""")
        prog.set_account(bidder1)
        bid1 = prog.place_bid(bidder1.address, 10)
        print(bid1)

        # Have the second bidder place a bid of 90.
        print("""
###############################################################################
########                                                               ########
########         STEP 2: The second bidder places a bid of 90          ########
########                                                               ########
########                -------------------------------                ########
########                |  OPEN   |    A    |    B    |                ########
########                -------------------------------                ########
########                |   Bid   |   10    |   90    |                ########
########                -------------------------------                ########
########                                                               ########
###############################################################################
""")
        prog.set_account(bidder2)
        bid2 = prog.place_bid(bidder2.address, 90)
        print(bid2)

        # Have the auctioneer select the winning bid.
        print("""
###############################################################################
########                                                               ########
########       STEP 3: The auctioneer selects the winning bidder       ########
########                                                               ########
########                -------------------------------                ########
########                |  OPEN   |    A    |  → B ←  |                ########
########                -------------------------------                ########
########                |   Bid   |   10    |  → 90 ← |                ########
########                -------------------------------                ########
########                                                               ########
###############################################################################
""")
        prog.set_account(auctioneer)
        win_bid = prog.resolve(bid1, bid2)
        print(win_bid)

        # Have the auctioneer finish the auction.
        print("""
###############################################################################
########                                                               ########
########         STEP 3: The auctioneer completes the auction.         ########
########                                                               ########
########                -------------------------------                ########
########                |  CLOSE  |    A    |  → B ←  |                ########
########                -------------------------------                ########
########                |   Bid   |   10    |  → 90 ← |                ########
########                -------------------------------                ########
########                                                               ########
###############################################################################
""")
        bid = prog.finish(win_bid)
        print(bid)


if __name__ == '__main__':
    unittest.main()
