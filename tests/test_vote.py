import unittest

from run_leo import Account
from run_leo.core import import_leo_program


class TestVote(unittest.TestCase):
    def test_load_leo_program(self):
        prog = import_leo_program('./leo_examples/vote')()

        # Test if structs/records are successfully converted to class variables
        self.assertTrue(hasattr(prog, "ProposalInfo"))
        self.assertTrue(hasattr(prog, "Proposal"))
        self.assertTrue(hasattr(prog, "Ticket"))

        # Test if functions are successfully converted to class methods
        self.assertTrue(hasattr(prog, "propose"))
        self.assertTrue(hasattr(prog, "new_ticket"))
        self.assertTrue(hasattr(prog, 'agree'))
        self.assertTrue(hasattr(prog, 'disagree'))

        # create account
        proposer = Account.new()
        voter = Account.new()

        # Test leo method calls
        print("""
###############################################################################
########                                                               ########
########               STEP 0: Compile the vote program                ########
########                                                               ########
###############################################################################
""")
        print("""
###############################################################################
########                                                               ########
########                 STEP 1: Propose a new ballot                  ########
########                                                               ########
########                  ---------------------------                  ########
########                  |         |  Yes  |   No  |                  ########
########                  ---------------------------                  ########
########                  |  Votes  |       |       |                  ########
########                  ---------------------------                  ########
########                                                               ########
###############################################################################
""")
        propose_info = prog.ProposalInfo(
            title=2077160157502449938194577302446444,
            content=1452374294790018907888397545906607852827800436,
            proposer=proposer.address
        )
        prog.set_account(proposer)
        propose = prog.propose(propose_info)
        print(propose)

        # Have the second bidder place a bid of 90.
        print("""
###############################################################################
########                                                               ########
########               STEP 2: Issue a new ballot ticket               ########
########                                                               ########
########                  ---------------------------                  ########
########                  |         |  Yes  |   No  |                  ########
########                  ---------------------------                  ########
########                  |  Votes  |   0   |   0   |                  ########
########                  ---------------------------                  ########
########                                                               ########
###############################################################################
""")
        ticket = prog.new_ticket(2264670486490520844857553240576860973319410481267184439818180411609250173817,
                                 voter.address)
        print(ticket)

        print("""
###############################################################################
########                                                               ########
########            STEP 3: Vote 'Yes' on the ballot ticket            ########
########                                                               ########
########                  ---------------------------                  ########
########                  |         |  Yes  |   No  |                  ########
########                  ---------------------------                  ########
########                  |  Votes  |   1   |   0   |                  ########
########                  ---------------------------                  ########
########                                                               ########
###############################################################################
""")
        prog.set_account(voter)
        prog.agree(ticket)


if __name__ == '__main__':
    unittest.main()
