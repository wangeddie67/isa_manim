"""
Test animation for function, including declaring and calling function.
"""

import os
import sys
path = sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       config,
                       WHITE, BLUE, GREEN,
                       MemoryMap,
                       FadeIn, FadeOut)

config.frame_height = 6
config.frame_width = 30

class TestMemMapAnimation(Scene):
    """
    Test animation for function, including declaring and calling function.
    """
    def construct(self):
        # Read elements.
        mem_map = MemoryMap(color=WHITE, rd_color=BLUE, wr_color=GREEN,
                            width=16, align=16, left_addr=0, right_addr=0x80)
        self.play(FadeIn(mem_map))

        for i in range(0, 0x40, 8):
            new_mem_map = mem_map.add_rd_range(laddr=i, raddr=i + 8)
            new_mem_map = new_mem_map.add_wr_range(laddr=i + 0x40, raddr=i + 0x40 + 8)
            self.play(FadeOut(mem_map), FadeIn(new_mem_map))
            mem_map = new_mem_map
            self.wait()

        self.wait()
        self.play(FadeOut(mem_map))

        mem_map = MemoryMap(color=WHITE, rd_color=BLUE, wr_color=GREEN,
                            width=16, align=16)
        self.play(FadeIn(mem_map))

        for i in range(0, 0x80, 16):
            new_mem_map = mem_map.add_rd_range(laddr=i, raddr=i + 8)
            new_mem_map = new_mem_map.add_wr_range(laddr=i + 8, raddr=i + 16)
            self.play(FadeOut(mem_map), FadeIn(new_mem_map))
            mem_map = new_mem_map
            self.wait()

        self.wait()
        self.play(FadeOut(mem_map))
