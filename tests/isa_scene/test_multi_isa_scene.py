"""
Test ISA scene with multiple instructions.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import MultiIsaScene # pylint: disable=wrong-import-position


class TestMultiIsaScene(MultiIsaScene):
    """
    Test ISA scene with multiple instructions.
    """
    def construct_isa_flow(self):
        # Parameters
        vl = 256
        esize = 32
        elements = vl // esize
        segments = vl // 128
        elempersegment = 128 // esize
        way = 2
        pairpersegment = elempersegment // way

        # Title
        self.draw_title("Shuffle instruction")
        subtitle = ["Buttom", "Top"]
        for part in range(0, way):
            self.start_section(subtitle[part])

            # Registers.
            if part == 0:
                zn_reg = self.decl_register("zn", vl, elements)
                zm_reg = self.decl_register("zm", vl, elements)
                src_reg = [zn_reg, zm_reg]
            zd_reg = self.decl_register("zd", vl, elements)

            # Behaviors
            for s in range(0, segments):
                for p in range(0, pairpersegment):
                    for w in range(0, way):
                        element = self.read_elem(
                            src_reg[w], s * elempersegment + part * pairpersegment + p,
                            color_hash=f"way{w}")
                        self.move_elem(element, zd_reg, s * elempersegment + p * way + w)

            if part < way - 1:
                self.end_section(wait=1, keep_objects=[zn_reg, zm_reg])
            else:
                self.end_section()

