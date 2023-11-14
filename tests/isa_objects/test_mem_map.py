"""
Test object for function unit.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       Dot,
                       config,
                       WHITE, GREEN, YELLOW,
                       UP,
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
                             right_addr=0x64).shift(UP * 1.5)
        dots = [Dot(color=GREEN).shift(UP * 1.5)]
        self.add(mem_unit, *dots)

        mem_unit = MemoryMap(color=WHITE,
                             rd_color=GREEN,
                             wr_color=YELLOW,
                             width=10,
                             align=16,
                             left_addr=0,
                             right_addr=0x80,
                             rd_range=[(16 * i, 16 * i + 8) for i in range(0, 8)],
                             wr_range=[(16 * i + 8, 16 * i + 16) for i in range(0, 8)]) \
            .shift(UP * -1)
        dots = [Dot(color=GREEN).shift(UP * -1)]
        self.add(mem_unit, *dots)

        mem_unit = MemoryMap(color=WHITE, rd_color=GREEN, wr_color=YELLOW,
                             width=10, align=16, left_addr=0, right_addr=0x100,
                             rd_range=[(0, 128)],
                             wr_range=[(128, 256)]).shift(UP * -3.5)
        dots = [Dot(color=GREEN).shift(UP * -3.5)]
        self.add(mem_unit, *dots)
