import unittest
from run_leo import LeoParser


class TestLeoParser(unittest.TestCase):
    def test_parse_example(self):
        example_leo_code = """
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
        """

        parser = LeoParser(example_leo_code)

        self.assertEqual(len(parser.structs), 3)
        self.assertEqual(parser.structs[0].name, "Row")
        self.assertEqual(parser.structs[0].fields, [("c1", "u8"), ("c2", "u8"), ("c3", "u8")])

        self.assertEqual(parser.structs[1].name, "Board")
        self.assertEqual(parser.structs[1].fields, [("r1", "Row"), ("r2", "Row"), ("r3", "Row")])

        self.assertEqual(parser.structs[2].name, "Ok")
        self.assertEqual(parser.structs[2].fields, [("cat", "u8")])

        self.assertEqual(len(parser.functions), 2)
        self.assertEqual(parser.functions[0].name, "make_move")
        self.assertEqual(parser.functions[0].input_params, [("private", "player", "u8"), ("private", "row", "u8"),
                                                            ("private", "col", "u8"), ("private", "board", "Board")])

        self.assertEqual(parser.functions[1].name, "play")
        self.assertEqual(parser.functions[1].input_params, [("public", "board", "Board"), ("private", "board2", "Board")])


if __name__ == "__main__":
    unittest.main()
