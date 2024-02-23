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

        zn = self.decl_vector(text="Zn", width=vl)
        zm = self.decl_vector(text="Zm", width=vl)
        zda = self.decl_vector(text="Zda", width=vl)

        for i in range(0, 4):
            sum_ = self.read_elem(vector=zda, size=esize, index=i, color_hash="sum_")

            for j in range(0, 2):
                opa = self.read_elem(
                    vector=zn, size=esize // 2, index = 2 * i + j, color_hash="opa" + str(j))
                opb = self.read_elem(
                    vector=zm, size=esize // 2, index = 2 * i + j, color_hash="opb" + str(j))
                prod = self.function_call(
                    func="*(a, b)", args=[opa, opb], res_size=esize, res_color_hash="prod" + str(j),
                    func_isa_hash="prod" + str(j), func_args_name=["a", "b"])
                sum__ = self.function_call(
                    func="+(a, b)", args=[prod, sum_], res_size=esize, res_color_hash="add" + str(j),
                    func_isa_hash="add" + str(j), func_args_name=["a", "b"])
                sum_ = sum__

            self.move_elem(elem=sum_, vector=zda, index=i)

            if i == 0:
                self.end_section(wait=1, fade_out=False)

        self.end_section(wait=2)
