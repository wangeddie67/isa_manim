"""
Test ISA scene with single instruction.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import SingleIsaScene # pylint: disable=wrong-import-position


class TestSingleIsaScene(SingleIsaScene):
    """
    Test ISA scene with single instruction.
    """
    def construct_isa_flow(self):
        # Title
        self.draw_title("DOT Instruction")

        vl = 128
        esize = 32
        elements = vl // esize
        way = 2

        zn = self.decl_register("Zn", vl, elements * way)
        zm = self.decl_register("Zm", vl, elements * way)
        zd = self.decl_register("Zda", vl, elements)

        self.decl_func_group(elements, "dot", [esize // way, esize // way, esize], esize,
                             func_name="a*b+sum", args_name=["a", "b", "sum"], force_hw_ratio=True)

        for i in range(0, elements):
            dot_sum = self.read_elem(zd, i)

            for j in range(0, 2):
                opa = self.read_elem(zn, way * i + j)
                opb = self.read_elem(zm, way * 2 + j)
                dot_sum = self.function_call(f"dot{i}", [opa, opb, dot_sum])

            self.move_elem(dot_sum, zd, i)

            if i == 0:
                self.end_section(wait=1, fade_out=False)

        self.end_section(wait=2)
