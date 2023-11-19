import sys
import unittest
import os
from PyQt5.QtWidgets import QApplication

from main_window.main_window import MainWindow
import random
from core.schema_classes import Primitive, Block
from settings import block_width, block_height
from hierarchy_window.hierarchy_window import HierarchyWindow


class MainWindowTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MainWindowTest, self).__init__(*args, **kwargs)

        app = QApplication(sys.argv)
        self.main_w = MainWindow()

        self.primitives = {}
        self.blocks = {}

    def test_checker_window(self):
        schem_files = os.listdir("./scheme_json_files/")
        for file in schem_files:
            self.main_w.checker.run_checker(file)

    def gen_prim(self):
        return Primitive('primitive', [], 50, 100, 100, 50)

    def gen_block(self, depth, prob_inner, prob_block, n_inner=2):
        max_depth = 3

        primitive = Primitive('primitive', [], 50, 100, 100, 50)
        block_top = Block('block', [], [], 100, 100, block_width, block_height)

        if depth < max_depth and random.random() < prob_inner:
            block_top.set_inner_block_list(
                [self.gen_block(depth + 1, prob_inner=prob_inner, prob_block=prob_block) if random.random() < prob_block
                 else primitive for i in range(1, n_inner)])
        print(depth)
        return block_top

    def gen_objects(self, n_prim=5, n_block=10, prob_inner=0.8, prob_block=0.5):

        for i in range(1, random.randrange(2, n_prim)):
            prim = self.gen_prim()

            self.primitives[prim] = True

        for i in range(1, random.randrange(2, n_block)):
            block = self.gen_block(depth=0, prob_inner=prob_inner, prob_block=prob_block)

            self.blocks[block] = True

    def test_hierarchy_window(self):
        app = QApplication(sys.argv)
        hier_wind = HierarchyWindow()

        self.gen_objects()
        hier_wind.get_hierarchy(self.primitives, self.blocks)


if __name__ == '__main__':
    unittest.main()

