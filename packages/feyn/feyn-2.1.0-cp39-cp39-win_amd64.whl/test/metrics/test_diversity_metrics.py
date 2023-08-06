import pytest
import unittest
from feyn.metrics._diversity import levenshtein_distance, tree_edit_distance

from feyn._context import Context
from feyn._program import Program


class TestDiversity(unittest.TestCase):
    def setUp(self):
        features = list("abcde")
        self.output = "output"

        self.ctx = Context()
        self.ctx.registers.append(self.output)
        self.ctx.registers += features

        # Define programs
        # Programs p5 and p6 have the same structure as the example in the paper by Zhang and Shasha 1989 on tree edit distance algorithm
        self.p1 = Program(self.ctx.query_to_codes(self.output, "(inverse('a'*'b'))+'c'")[1], -1, True)
        self.p2 = Program(self.ctx.query_to_codes(self.output, "('a'+'c') + 'b'")[1], -1, True)
        self.p3 = Program(self.ctx.query_to_codes(self.output, "'a'+'a'")[1], -1, True)
        self.p4 = Program(self.ctx.query_to_codes(self.output, "'b'*'c'")[1], -1, True)
        self.p5 = Program(self.ctx.query_to_codes(self.output, "('a'*inverse('b'))+'e'")[1], -1, True)
        self.p6 = Program(self.ctx.query_to_codes(self.output, "inverse('a'*'b')+'e'")[1], -1, True)

        # Convert programs to models
        self.m1 = self.ctx.to_model(self.p1, self.output)
        self.m2 = self.ctx.to_model(self.p2, self.output)
        self.m3 = self.ctx.to_model(self.p3, self.output)
        self.m4 = self.ctx.to_model(self.p4, self.output)
        self.m5 = self.ctx.to_model(self.p5, self.output)
        self.m6 = self.ctx.to_model(self.p6, self.output)

    def test_levenshtein_distance(self):
        assert self.m1 is not None
        assert self.m2 is not None
        distance = levenshtein_distance(self.m1, self.m2)
        self.assertEqual(distance, 4)

    def test_tree_edit_distance(self):
        assert self.m1 is not None
        assert self.m2 is not None
        assert self.m3 is not None
        assert self.m4 is not None
        assert self.m5 is not None
        assert self.m6 is not None
        self.assertEqual(tree_edit_distance(self.m1, self.m2), 4)
        self.assertEqual(tree_edit_distance(self.m3, self.m4), 3)
        self.assertEqual(tree_edit_distance(self.m5, self.m6), 2) # Same example as in paper
