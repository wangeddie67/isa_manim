"""
Test animation for function, including declaring and calling function.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       config, get_config, DEFAULT_FONT_SIZE,
                       WHITE, BLUE, GREEN, YELLOW, PURPLE, RED,
                       UP, LEFT, RIGHT,
                       Text,
                       RegUnit, ElemUnit, MemoryUnit,
                       FadeIn, AnimationGroup,
                       decl_memory_unit, read_memory, write_memory)

config.frame_height = 6
config.frame_width = 30

class TestMemUnitAnimationParallel(Scene):
    """
    Test animation for function, including declaring and calling function.
    """
    def construct(self):
        # Read elements.
        addr_reg = RegUnit(["Addr"], WHITE, 64, 1, 1, None,
                           DEFAULT_FONT_SIZE, get_config("elem_value_format")) \
                    .shift(UP * 6 + LEFT * 4)
        data_reg = RegUnit(["Data"], WHITE, 128, 8, 1, None,
                           DEFAULT_FONT_SIZE, get_config("elem_value_format")) \
                    .shift(UP * 4)
        addr_elem = ElemUnit(GREEN, 64, 0x40, get_config("elem_fill_opacity"), DEFAULT_FONT_SIZE,
                             get_config("elem_value_format"), 0, False) \
                    .move_to(addr_reg.get_elem_pos(0, 0, 0, 64))
        data_elem_list = [ElemUnit(BLUE, 16, None,
                             get_config("elem_fill_opacity"), DEFAULT_FONT_SIZE,
                             get_config("elem_value_format"), 0, False) \
                    .move_to(data_reg.get_elem_pos(i, 0, 0, 16))
                    for i in range(0, data_reg.elem_count)]
        self.add(addr_reg, data_reg, addr_elem, *data_elem_list)

        # Declare memory.
        memory_unit = MemoryUnit(WHITE, 64, 64, 64, [[0, 0x100]], DEFAULT_FONT_SIZE,
                                 get_config("elem_value_format"), True, 4, 0)
        memory_animate = decl_memory_unit(memory_unit)
        decl_memory_unit_label = Text("decl_memory_unit", color=YELLOW) \
            .move_to(memory_unit.mem_rect.get_right() + RIGHT * 4 + UP * 2)

        self.add(decl_memory_unit_label)
        self.wait(duration=1)
        self.play(memory_animate)
        self.wait(duration=1)
        self.remove(decl_memory_unit_label)

        # Write memory.
        status_elem = ElemUnit(RED, 4, None, get_config("elem_fill_opacity"), DEFAULT_FONT_SIZE,
                               get_config("elem_value_format"), 0, False)
        write_memory_animate_list = [write_memory(
            memory_unit, addr_elem, data_elem, status_elem if i == 0 else None,
            memory_unit.get_addr_mark(addr_elem.elem_value, addr_elem.elem_color),
            memory_unit.get_wt_mem_mark(addr_elem.elem_value + data_elem.elem_width // 8 * i * 2,
                                    addr_elem.elem_value + data_elem.elem_width // 8 * (i * 2 + 1),
                                    data_elem.elem_color),
            i == 0)
                    for i, data_elem in enumerate(data_elem_list)]
        write_memory_label = Text("write_memory", color=YELLOW) \
            .move_to(memory_unit.mem_rect.get_right() + RIGHT * 4 + UP * 2)

        # Play Animation.
        self.add(write_memory_label)
        self.wait(duration=1)
        self.play(AnimationGroup(*write_memory_animate_list))
        self.wait(duration=1)
        self.remove(write_memory_label, status_elem)

        addr_elem = ElemUnit(GREEN, 64, 0x40, get_config("elem_fill_opacity"), DEFAULT_FONT_SIZE,
                             get_config("elem_value_format"), 0, False) \
                    .move_to(addr_reg.get_elem_pos(0, 0, 0, 64))
        self.play(FadeIn(addr_elem))

        # Read memory.
        data_elem_list = [ElemUnit(PURPLE, 16, None,
                            get_config("elem_fill_opacity"), DEFAULT_FONT_SIZE,
                            get_config("elem_value_format"), 0, False) \
                    .move_to(data_reg.get_elem_pos(i, 0, 0, 16))
                    for i in range(0, data_reg.elem_count)]
        status_elem = ElemUnit(RED, 4, None, get_config("elem_fill_opacity"), DEFAULT_FONT_SIZE,
                               get_config("elem_value_format"), 0, False)
        write_memory_animate_list = [read_memory(
            memory_unit, addr_elem, data_elem, status_elem if i == 0 else None,
            memory_unit.get_addr_mark(addr_elem.elem_value, addr_elem.elem_color),
            memory_unit.get_rd_mem_mark(addr_elem.elem_value + data_elem.elem_width // 8 * i * 2,
                                    addr_elem.elem_value + data_elem.elem_width // 8 * (i * 2 + 1),
                                    data_elem.elem_color),
            i == 0)
                    for i, data_elem in enumerate(data_elem_list)]
        read_memory_label = Text("read_memory", color=YELLOW) \
            .move_to(memory_unit.mem_rect.get_right() + RIGHT * 4 + UP * 2)

        # Play Animation.
        self.add(read_memory_label)
        self.wait(duration=1)
        self.play(AnimationGroup(*write_memory_animate_list))
        # self.play(data_elem.animate.move_to(data_reg.get_elem_pos(0, 0, 0, 64)))
        self.wait(duration=1)
        self.remove(read_memory_label, status_elem)
