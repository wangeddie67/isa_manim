"""
Test object for function unit.
"""

import os
import sys
path = sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       Dot, BraceBetweenPoints, Text, Arrow,
                       config,
                       WHITE, GREEN, YELLOW,
                       LEFT, RIGHT, UP, DOWN,
                       MemoryMap)

config.frame_height = 6
config.frame_width = 24

class TestMemoryMap(Scene):
    """
    Test object for function unit.
    """
    def construct(self):
        mem_unit = MemoryMap(color=WHITE,
                             rd_color=GREEN,
                             wr_color=YELLOW,
                             width=10,
                             align=16).shift(UP * 4)
        dots = [Dot(color=GREEN).shift(UP * 4)]
        self.add(mem_unit, *dots)

        mem_unit = MemoryMap(color=WHITE,
                             rd_color=GREEN,
                             wr_color=YELLOW,
                             width=10,
                             align=16,
                             left_addr=0,
                             right_addr=0x64).shift(UP * 2)
        dots = [Dot(color=GREEN).shift(UP * 2)]
        self.add(mem_unit, *dots)

        mem_unit = MemoryMap(color=WHITE,
                             rd_color=GREEN,
                             wr_color=YELLOW,
                             width=10,
                             align=16,
                             left_addr=0,
                             right_addr=0x80,
                             rd_range=[(16 * i, 16 * i + 8) for i in range(0, 4)],
                             wr_range=[(16 * i + 8, 16 * i + 16) for i in range(0, 4)]) \
            .shift(UP * 0)
        dots = [Dot(color=GREEN).shift(UP * 0)]
        self.add(mem_unit, *dots)

        mem_unit = MemoryMap(color=WHITE, rd_color=GREEN, wr_color=YELLOW,
                             width=10, align=16, left_addr=0, right_addr=0x80,
                             rd_range=[(0, 64)],
                             wr_range=[(0 + 128, 64 + 128)]).shift(UP * -2)
        dots = [Dot(color=GREEN).shift(UP * -2)]
        self.add(mem_unit, *dots)
