import unittest
from run_leo import LeoParser


class TestLeoParser(unittest.TestCase):
    def test_parse_example(self):
        example_leo_code = """
program test.aleo {
    struct Row {
        // comment 1 c1: u8
        c1: u8,
        c2: u8,
        c3: u8
    }

    struct Board {
        r1: Row,
        r2: Row,
        r3: Row,
    }
    
    record Ok {
        cat: u8
    }

    function check_for_win(b: Board, p: u8) -> bool {
    }

    transition make_move(player: u8, row: u8, col: u8, board: Board) -> (Board, u8) {
        // Check that inputs are valid.
        assert(player == 1u8 || player == 2u8);
    }
    
    transition play(public board: Board, board2: Board) -> bool {
        // Check that inputs are valid.
        assert(player == 1u8 || player == 2u8);
    }
    
    // Returns an updated board state record that has been started. This board cannot be used to start any other games.
    // Returns a dummy move record owned by the opponent.
    // This function commits a given board to a game with an opponent and creates the initial dummy move.
    transition offer_battleship(
        // The board record to start a game with.
        board: board.leo/board_state.record,
    ) -> (board.leo/board_state.record, move.leo/move.record) {
        let state: board_state = board.leo/start_board(board);
        let dummy: move = move.leo/start_game(board.player_2);

        return (state, dummy);
    }
}
"""

        parser = LeoParser(example_leo_code)

        self.assertEqual(len(parser.structs), 2)
        self.assertEqual(parser.structs[0].name, "Row")
        self.assertEqual(parser.structs[0].fields, [("private", "c1", "u8"), ("private", "c2", "u8"), ("private", "c3", "u8")])

        self.assertEqual(parser.structs[1].name, "Board")
        self.assertEqual(parser.structs[1].fields, [("private", "r1", "Row"), ("private", "r2", "Row"), ("private", "r3", "Row")])

        self.assertEqual(len(parser.records), 1)
        self.assertEqual(parser.records[0].name, "Ok")
        self.assertEqual(parser.records[0].fields, [("private", "cat", "u8")])

        self.assertEqual(len(parser.functions), 3)
        self.assertEqual(parser.functions[0].name, "make_move")
        self.assertEqual(parser.functions[0].input_params, [("private", "player", "u8"), ("private", "row", "u8"),
                                                            ("private", "col", "u8"), ("private", "board", "Board")])
        self.assertEqual(parser.functions[0].output_params, ['Board', 'u8'])

        self.assertEqual(parser.functions[1].name, "play")
        self.assertEqual(parser.functions[1].input_params, [("public", "board", "Board"), ("private", "board2", "Board")])
        self.assertEqual(parser.functions[1].output_params, ['bool'])

        self.assertEqual(parser.functions[2].name, "offer_battleship")
        self.assertEqual(parser.functions[2].input_params, [("private", "board", "board__board_state")])
        self.assertEqual(parser.functions[2].output_params, ['board__board_state', 'move__move'])


if __name__ == "__main__":
    unittest.main()
