"""
Test ISA scene with single instruction.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import SingleIsaScene, set_config # pylint: disable=wrong-import-position


class TestSingleIsaSceneMem(SingleIsaScene):
    """
    Test ISA scene with single instruction.
    """
    def construct_isa_flow(self):
        # Parameters
        vl = 256
        esize = 32
        memsize = 32
        addrlen = 64
        mbytes = memsize // 8
        elements = vl // esize
        pl = vl // 8
        set_config("elem_value_format", "0x{:x}")

        # Title
        self.draw_title("Memory access with stride")

        # Registers.
        rn_reg = self.decl_register("rn", addrlen, value=0x100)
        rm_reg = self.decl_register("rm", addrlen, value=0x100, align_with=rn_reg)
        zt_reg = self.decl_register("zt", vl, elements, 1)
        ffr_reg = self.decl_register("ffr", pl, elements, align_with=rn_reg)

        # Function unit
        self.decl_function("addrgen", [addrlen, addrlen], addrlen,
                           name="base+offset", args_name=["base", "offset"],
                           func_callee=lambda x, y: x + y)
        self.decl_function("scale", [addrlen], addrlen,
                           name=f"offset*{mbytes}", args_name=["offset"],
                           func_callee=lambda x: x * mbytes)

        # Memory unit.
        addr_val = [rn_reg.reg_value + rm_reg.reg_value * mbytes + e * mbytes
                    for e in range(0, elements)]
        addr_e_val = [val + mbytes for val in addr_val]
        mem_range = [min(addr_val + addr_e_val), max(addr_val + addr_e_val)]
        self.decl_memory(addrlen, memsize, [mem_range], status_width=esize // 8, para_enable=True)

        # Behaviors
        base = self.read_elem(rn_reg)
        offset = self.read_elem(rm_reg)
        offset = self.function_call("scale", [offset])
        base = self.function_call("addrgen", [base, offset])

        for e in range(0, elements):
            data, status = self.read_memory(base, memsize,
                                            offset=mbytes * e, has_status_output=True)
            self.move_elem(data, zt_reg, e, width=memsize)
            self.move_elem(status, ffr_reg, e)

        self.end_section()
