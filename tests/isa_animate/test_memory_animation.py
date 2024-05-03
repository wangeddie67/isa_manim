"""
Test animation for function, including declaring and calling function.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       config,
                       WHITE, BLUE, GREEN, YELLOW, PURPLE,
                       UP, LEFT, RIGHT,
                       Text,
                       RegElemUnit, MemoryUnit,
                       FadeIn,
                       decl_memory_unit, read_memory_without_addr, write_memory_without_addr)

config.frame_height = 6
config.frame_width = 30

class TestMemUnitAnimation(Scene):
    """
    Test animation for function, including declaring and calling function.
    """
    def construct(self):
        # Read elements.
        addr_elem = RegElemUnit(color=GREEN, width=64).move_to(UP * 4 + LEFT * 4)
        data_elem = RegElemUnit(color=BLUE, width=16).move_to(UP * 4 + RIGHT * 4)
        self.add(addr_elem, data_elem)

        # Declare memory.
        memory_unit = MemoryUnit(color=WHITE, addr_width=64, data_width=64, addr_align=64,
                                 mem_range=[[0, 0x1000]])
        memory_animate = decl_memory_unit(memory_unit)
        decl_memory_unit_label = Text("decl_memory_unit", color=YELLOW) \
            .move_to(memory_unit.mem_rect.get_right() + RIGHT * 4 + UP * 2)

        self.add(decl_memory_unit_label)
        self.play(memory_animate)
        self.wait(duration=2)
        self.remove(decl_memory_unit_label)

        # Write memory.
        write_memory_animate = write_memory_without_addr(mem_unit=memory_unit,
                                                         addr_item=addr_elem,
                                                         data_item=data_elem)
        write_memory_label = Text("write_memory", color=YELLOW) \
            .move_to(memory_unit.mem_rect.get_right() + RIGHT * 4 + UP * 2)

        # Play Animation.
        self.add(write_memory_label)
        self.play(write_memory_animate)
        self.wait(duration=2)
        self.remove(write_memory_label)

        addr_elem.move_to(UP * 4 + LEFT * 4)
        self.play(FadeIn(addr_elem))

        # Read memory.
        data_elem = RegElemUnit(color=PURPLE, width=64)
        read_memory_animate = read_memory_without_addr(mem_unit=memory_unit,
                                                       addr_item=addr_elem,
                                                       data_item=data_elem)
        read_memory_label = Text("read_memory", color=YELLOW) \
            .move_to(memory_unit.mem_rect.get_right() + RIGHT * 4 + UP * 2)

        # Play Animation.
        self.add(read_memory_label)
        self.play(read_memory_animate)

        self.play(data_elem.animate.move_to(UP * 4 + RIGHT * 4))
        self.wait(duration=2)
