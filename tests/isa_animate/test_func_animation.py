"""
Test animation for function, including declaring and calling function.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       config, get_config, DEFAULT_FONT_SIZE,
                       RED, BLUE, GREEN, YELLOW, TEAL, WHITE,
                       UP, LEFT, RIGHT,
                       Text,
                       ElemUnit, FunctionUnit,
                       decl_func_unit, read_func_imm, function_call)

config.frame_height = 6
config.frame_width = 30

class TestFuncAnimation(Scene):
    """
    Test animation for function, including declaring and calling function.
    """
    def construct(self):
        # Read elements.
        r1_elem = ElemUnit(RED, 16, None, get_config("elem_fill_opacity"), DEFAULT_FONT_SIZE,
                           get_config("elem_value_format"), 0, False).move_to(UP * 4 + LEFT * 2)
        r2_elem = ElemUnit(BLUE, 16, None, get_config("elem_fill_opacity"), DEFAULT_FONT_SIZE,
                           get_config("elem_value_format"), 0, False).move_to(UP * 4 + RIGHT * 2)
        self.add(r1_elem, r2_elem)

        # Declare function.
        function_item = FunctionUnit("a*b+sum", WHITE, [16, 16, 16], [32, 4],
                                     ["a", "b", "sum"], ["sum", "flag"],
                                     DEFAULT_FONT_SIZE, get_config("elem_value_format"), None)
        function_animate = decl_func_unit(function_item)
        def_func_call_label = Text("def_func_call", color=YELLOW) \
            .move_to(function_item.func_rect.get_right() + RIGHT * 4)

        self.add(def_func_call_label)
        self.wait(duration=1)
        self.play(function_animate)
        self.wait(duration=1)
        self.remove(def_func_call_label)

        # Read immediate operands
        r3_elem = ElemUnit(GREEN, 16, None, get_config("elem_fill_opacity"), DEFAULT_FONT_SIZE,
                           get_config("elem_value_format"), 0, False) \
            .move_to(function_item.get_arg_pos(2, 0, 16))
        read_imm_animate = read_func_imm(r3_elem)
        read_imm_label = Text("read_func_imm", color=YELLOW) \
            .move_to(function_item.func_rect.get_right() + RIGHT * 4)

        # Play Animation.
        self.add(read_imm_label)
        self.wait(duration=1)
        self.play(read_imm_animate)
        self.wait(duration=1)
        self.remove(read_imm_label)

        res1_elem = ElemUnit(YELLOW, 32, None, get_config("elem_fill_opacity"),
                             DEFAULT_FONT_SIZE, get_config("elem_value_format"), 0, False)
        res2_elem = ElemUnit(TEAL, 4, None, get_config("elem_fill_opacity"),
                             DEFAULT_FONT_SIZE, get_config("elem_value_format"), 0, False)
        func_call_animate = function_call(
            function_item, [r1_elem, r2_elem, r3_elem], [res1_elem, res2_elem], [0, 0, 0], [0, 0])
        func_cal_label = Text("function_call", color=YELLOW) \
            .move_to(function_item.func_rect.get_right() + RIGHT * 4)

        # Play Animation.
        self.add(func_cal_label)
        self.wait(duration=1)
        self.play(func_call_animate)
        self.wait(duration=1)
        self.remove(func_cal_label)
