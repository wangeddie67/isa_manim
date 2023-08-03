"""
Test ISA scene with single instruction.
"""

import os
import sys
path = sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import SingleIsaScene # pylint: disable=wrong-import-position


class TestSingleIsaSceneMem(SingleIsaScene):
    """
    Test ISA scene with single instruction.
    """
    def construct_isa_flow(self):
        # Title
        self.draw_title("CPY* Instruction, forward, option A")

        xs_i = 24
        xd_i = 0
        xn_i = 72
        step = 16

        xs_reg = self.decl_scalar(text="Xs", width=64)
        xd_reg = self.decl_scalar(text="Xd", width=64)
        xn_reg = self.decl_vector(text="Xn", width=64)

        xs_item = self.read_elem(vector=xs_reg, size=64, value=xs_i)
        xd_item = self.read_elem(vector=xd_reg, size=64, value=xd_i)
        xn_item = self.read_elem(vector=xn_reg, size=64, value=xn_i)
        self.wait()

        # CPYP
        xs_i = xs_i + xn_i
        xd_i = xd_i + xn_i
        xn_i = -xn_i

        xs_item = self.data_convert(elem=xs_item, size=64, value=xs_i)
        xd_item = self.data_convert(elem=xd_item, size=64, value=xd_i)
        xn_item = self.data_convert(elem=xn_item, size=64, value=xn_i)
        self.end_section(fade_out=False)

        # CPYM
        while -xn_i >= step:
            rd_addr_item = self.function_call(
                func="read_addr", args=[xs_item, xn_item], res_size=64, value=xs_i + xn_i,
                isa_hash="read_addr")
            data_item = self.read_memory(addr=rd_addr_item, size=step * 8, color_hash="data_item")
            wr_addr_item = self.function_call(
                func="write_addr", args=[xd_item, xn_item], res_size=64, value=xd_i + xn_i,
                isa_hash="write_addr")
            self.write_memory(addr=wr_addr_item, data=data_item)

            xn_i = xn_i + step
            xn_item = self.data_convert(elem=xn_item, size=64, value=xn_i)
            self.end_section(fade_out=False)

        # CPYE
        rd_addr_item = self.function_call(
            func="read_addr", args=[xs_item, xn_item], res_size=64, value=xs_i + xn_i,
            isa_hash="read_addr")
        data_item = self.read_memory(addr=rd_addr_item, size=-xn_i * 8, color_hash="data_item")
        wr_addr_item = self.function_call(
            func="write_addr", args=[xd_item, xn_item], res_size=64, value=xd_i + xn_i,
            isa_hash="write_addr")
        self.write_memory(addr=wr_addr_item, data=data_item)

        xn_item = self.data_convert(elem=xn_item, size=64, value=0)

        self.end_section(wait=2)
