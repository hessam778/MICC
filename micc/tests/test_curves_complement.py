import unittest
import numpy as np
from micc.curves import CurvePair
from sys import stderr
from micc.utils import shift, invert


class ComplementaryCurvesTests(unittest.TestCase):

    def check_valid(self, true_loops, test_loops):
        valid = True
        for true_loop in true_loops:
            match = False
            for test_loop in test_loops:
                if set(true_loop) == set(int(v.real) for v in test_loop):
                    match = True
                    break
            if not match:
                stderr.write('broke it: '+str(true_loop)+'\n')
            valid &= match
        return valid

    def test_2(self):
        # polygonal boundaries (reference curve only)
        # [[(0.0, 3), (15.0, 1), (11.0, 1)], [(8.0, 3), (0.0, 1)], [(1.0, 1), (9.0, 3)], [(12.0, 1), (1.0, 3)], [(2.0, 1), (10.0, 3)], [(13.0, 1), (15.0, 3), (2.0, 3)], [(3.0, 1), (11.0, 3)], [(14.0, 3), (6.0, 1), (3.0, 3)], [(4.0, 1), (12.0, 3)], [(7.0, 1), (4.0, 3)], [(5.0, 1), (13.0, 3)], [(8.0, 1), (5.0, 3)], [(9.0, 1), (6.0, 3)], [(10.0, 1), (16.0, 1), (7.0, 3)], [(14.0, 1), (16.0, 3)]]
        # loops:
        true_loops = [(1, 12, 4, 7, 10, 2, 15, 11, 3, 6, 9), (0, 8, 5, 13, 15), (1, 12, 4, 7, 16, 14, 6, 9), (2, 15, 11, 3, 14, 16, 10), (0, 11, 3, 6, 9, 1, 12, 4, 7, 10, 2, 13, 5, 8), (0, 11, 3, 14, 16, 10, 2, 13, 5, 8)]
        true_loops = [shift([(i-1) % 17 for i in loop]) for loop in true_loops]
        # stderr.write('true loops:\n')
        # for loop in true_loops:
        #     stderr.write(str(loop)+'\n')
        test = CurvePair([[6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 1, 2, 3, 4, 17, 5],
                          [1, 2, 12, 13, 14, 15, 16, 5, 6, 7, 8, 9, 10, 11, 12, 3, 4]],
                         compute=True)

        test_loops = [c.arc_path for c in test.complementary_curves]
        valid = self.check_valid(true_loops, test_loops)
        self.assertTrue(valid)

    def test_3(self):
        # polygonal boundaries (reference curve only)
        # [[(0.0, 3), (5.0, 1), (1.0, 1)], [(6.0, 1), (7.0, 3), (0.0, 1)], [(2.0, 1), (1.0, 3)], [(3.0, 1), (15.0, 3), (2.0, 3)], [(14.0, 3), (13.0, 1), (3.0, 3)], [(4.0, 1), (16.0, 3)], [(14.0, 1), (4.0, 3)], [(15.0, 1), (5.0, 3)], [(16.0, 1), (6.0, 3)], [(7.0, 1), (8.0, 3)], [(8.0, 1), (9.0, 3)], [(9.0, 1), (10.0, 3)], [(10.0, 1), (11.0, 3)], [(11.0, 1), (12.0, 3)], [(12.0, 1), (13.0, 3)]]
        # loops:
        true_loops = [(0, 7, 8, 9, 10, 11, 12, 13, 3, 2, 1), (4, 14, 13, 12, 11, 10, 9, 8, 7, 6, 16), (1, 5, 15, 2), (0, 7, 8, 9, 10, 11, 12, 13, 3, 15, 5), (0, 1, 2, 3, 14, 4, 16, 6), (0, 5, 15, 3, 14, 4, 16, 6)]
        true_loops = [shift([(i-1) % 17 for i in loop]) for loop in true_loops]
        # for cycle in true_loops:
        #     stderr.write(str(cycle)+'\n')
        test = CurvePair([[17, 1, 2, 3, 4, 17, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16],
                          [1, 2, 12, 13, 14, 15, 16, 5, 6, 7, 8, 9, 10, 11, 12, 3, 4]],
                         compute=True)
        test_loops = [c.arc_path for c in test.complementary_curves]
        valid = self.check_valid(true_loops, test_loops)
        self.assertTrue(valid)

    def test_4(self):
        # polygonal boundaries (reference curve only)
        # [[(0.0, 3), (7.0, 1), (2.0, 1)], [(9.0, 1), (0.0, 1)], [(1.0, 1), (8.0, 1)], [(3.0, 1), (1.0, 3)], [(4.0, 1), (2.0, 3)], [(5.0, 1), (3.0, 3)], [(6.0, 1), (23.0, 3), (4.0, 3)], [(22.0, 3), (5.0, 3)], [(21.0, 3), (6.0, 3)], [(20.0, 3), (23.0, 1), (10.0, 1), (7.0, 3)], [(11.0, 1), (8.0, 3)], [(12.0, 1), (9.0, 3)], [(13.0, 1), (10.0, 3)], [(14.0, 1), (11.0, 3)], [(15.0, 1), (12.0, 3)], [(16.0, 1), (13.0, 3)], [(17.0, 1), (14.0, 3)], [(18.0, 1), (15.0, 3)], [(19.0, 1), (16.0, 3)], [(20.0, 1), (17.0, 3)], [(21.0, 1), (18.0, 3)], [(22.0, 1), (19.0, 3)]]
        # loops:
        true_loops = [(0, 7, 20, 17, 14, 11, 8, 1, 3, 5, 22, 19, 16, 13, 10, 23, 6, 21, 18, 15, 12, 9), (0, 9, 12, 15, 18, 21, 6, 4, 2), (0, 7, 10, 13, 16, 19, 22, 5, 3, 1, 8, 11, 14, 17, 20, 23, 6, 21, 18, 15, 12, 9), (1, 3, 5, 22, 19, 16, 13, 10, 20, 17, 14, 11, 8), (0, 9, 12, 15, 18, 21, 6, 23, 7), (2, 7, 23, 4), (1, 8, 11, 14, 17, 20, 7, 2, 4, 23, 10, 13, 16, 19, 22, 5, 3), (1, 8, 11, 14, 17, 20, 23, 4, 2, 7, 10, 13, 16, 19, 22, 5, 3)]
        true_loops = [shift([(i-1) % 24 for i in loop]) for loop in true_loops]
        test = CurvePair([[23, 22, 1, 2, 3, 4, 5, 22, 23, 24, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 24],
                          [1, 2, 3, 4, 19, 20, 21, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 20, 19, 5]],
                            compute=True)
        # for cycle in true_loops:
        #     stderr.write('real loop: '+str(cycle)+'\n')
        test_loops = [c.arc_path for c in test.complementary_curves]
        valid = self.check_valid(true_loops, test_loops)
        self.assertTrue(valid)

    def test_5(self):
        # polygonal boundaries (reference curve only)
        # [[(0.0, 3), (13.0, 1), (4.0, 1)], [(6.0, 3), (0.0, 1)], [(1.0, 1), (16.0, 1), (7.0, 3)], [(5.0, 1), (1.0, 3)], [(2.0, 1), (15.0, 1)], [(6.0, 1), (14.0, 3), (2.0, 3)], [(3.0, 1), (14.0, 1)], [(13.0, 3), (3.0, 3)], [(12.0, 3), (4.0, 3)], [(11.0, 3), (20.0, 1), (5.0, 3)], [(7.0, 1), (15.0, 3)], [(8.0, 1), (16.0, 3)], [(17.0, 1), (8.0, 3)], [(9.0, 1), (17.0, 3)], [(18.0, 1), (9.0, 3)], [(10.0, 1), (18.0, 3)], [(19.0, 1), (10.0, 3)], [(11.0, 1), (19.0, 3)], [(12.0, 1), (20.0, 3)]]
        # loops:
        true_loops = [(2, 14, 3, 13, 4, 12, 20, 11, 19, 10, 18, 9, 17, 8, 16, 7, 15), (0, 6, 14, 3, 13), (0, 4, 12, 20, 11, 19, 10, 18, 9, 17, 8, 16, 7, 15, 2, 6), (0, 4, 12, 20, 5, 1, 7, 15, 2, 6), (1, 5, 11, 19, 10, 18, 9, 17, 8, 16), (1, 7, 15, 2, 14, 3, 13, 4, 12, 20, 5)]
        true_loops = [shift([(i-1) % 21 for i in loop]) for loop in true_loops]

        test = CurvePair([[18, 21, 20, 19, 1, 2, 3, 4, 5, 6, 7, 8, 9, 19, 20, 21, 10, 11, 12, 13, 17],
                          [1, 2, 14, 15, 16, 17, 18, 10, 11, 12, 13, 16, 15, 14, 3, 4, 5, 6, 7, 8, 9]],
                            compute=True)
        # for cycle in true_loops:
        #     stderr.write(str(cycle)+'\n')
        test_loops = [c.arc_path for c in test.complementary_curves]
        valid = self.check_valid(true_loops, test_loops)
        self.assertTrue(valid)

    def test_6(self):
        true_loops = [(0, 9, 12, 1, 16, 6, 21, 10, 13, 22, 7, 17, 2, 11, 20, 5, 15), (0, 15, 5, 20, 11, 2, 17, 7, 22, 9, 19, 4, 14, 23, 8, 18, 3, 13), (0, 13, 10, 21, 6, 16, 1, 12, 9, 22, 7, 17, 2, 11, 20, 5, 15), (3, 13, 9, 19, 4, 14, 23, 8, 18), (0, 15, 5, 20, 11, 2, 17, 7, 22, 13, 3, 18, 8, 23, 14, 4, 19, 9), (1, 12, 9, 13, 10, 21, 6, 16), (1, 16, 6, 21, 10, 3, 18, 8, 23, 14, 4, 19, 12), (0, 22, 7, 17, 2, 11, 20, 5, 15)]
        true_loops = [shift([(i-1) % 24 for i in loop]) for loop in true_loops]
        test = CurvePair([[3, 4, 5, 6, 7, 8, 9, 10, 11, 22, 23, 24, 12, 16, 17, 18, 19, 20, 21, 24, 23, 22, 1, 2],
                          [13, 14, 15, 16, 17, 18, 19, 20, 21, 12, 15, 14, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]],
                            compute=True)
        # for cycle in true_loops:
        #     stderr.write('real loop: '+str(cycle)+'\n')
        test_loops = [c.arc_path for c in test.complementary_curves]
        valid = self.check_valid(true_loops, test_loops)
        self.assertTrue(valid)

    def test_7(self):
        true_loops = [(0, 11, 17, 14, 20, 10, 18, 15, 16, 13), (0, 11, 17, 14, 20, 10, 18, 15, 12, 1, 3, 5, 7, 9, 19, 16, 13), (2, 4, 6, 8, 20, 14, 17, 11), (1, 12, 19, 9, 7, 5, 3), (0, 2, 4, 6, 8, 10, 18, 15, 19, 9, 7, 5, 3, 1, 12, 16, 13), (0, 11, 17, 14, 20, 10, 18, 15, 19, 9, 7, 5, 3, 1, 12, 16, 13), (0, 2, 4, 6, 8, 10, 18, 15, 16, 13), (0, 13, 16, 19, 9, 7, 5, 3, 1, 12, 15, 18, 10, 8, 6, 4, 2)]
        true_loops = [shift([(i-1) % 21 for i in loop]) for loop in true_loops]
        test = CurvePair([[19, 18, 1, 2, 3, 4, 5, 6, 7, 8, 9, 18, 19, 20, 21, 14, 15, 16, 17, 21, 20],
                         [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 13, 12, 11, 10, 9]],
                          compute=True)
        # for cycle in true_loops:
        #     stderr.write('real loop: '+str(cycle)+'\n')
        test_loops = [c.arc_path for c in test.complementary_curves]
        valid = self.check_valid(true_loops, test_loops)
        self.assertTrue(valid)

if __name__ == '__main__':
    unittest.main()
