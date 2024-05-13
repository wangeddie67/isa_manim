"""
Test animation for elements, including reading and assigning elements.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       config, get_config, DEFAULT_FONT_SIZE,
                       WHITE, BLUE, GREEN, PURPLE, YELLOW,
                       UP, LEFT, RIGHT,
                       Text,
                       RegUnit, ElemUnit,
                       read_elem, assign_elem)

config.frame_height = 6
config.frame_width = 30

class TestElemAnimation(Scene):
    """
    Test animation for elements, including reading and assigning elements.
    """
    def construct(self):
        # Declare Register.
        scalar_reg = RegUnit(["Rn"], WHITE, 32, 1, 1, None, DEFAULT_FONT_SIZE,
                             get_config("elem_value_format")).shift(UP * 4 + LEFT * 2)
        vector_reg = RegUnit(["Vn"], WHITE, 128, 8, 1, None, DEFAULT_FONT_SIZE,
                             get_config("elem_value_format")).shift(UP * 2 + LEFT * 2)
        vector_2d_reg = RegUnit(["Zn"], WHITE, 128, 4, 4, None, DEFAULT_FONT_SIZE,
                                get_config("elem_value_format")).shift(LEFT * 2)

        # Play Animation.
        self.add(scalar_reg, vector_reg, vector_2d_reg)
        self.wait()

        # Elements.
        scalar_elem = ElemUnit(BLUE, 16, None, get_config("elem_fill_opacity"),
                               DEFAULT_FONT_SIZE, get_config("elem_value_format"), 0, False)
        vector_elem = ElemUnit(GREEN, 16, None, get_config("elem_fill_opacity"),
                               DEFAULT_FONT_SIZE, get_config("elem_value_format"), 0, False)
        vector_2d_elem = ElemUnit(PURPLE, 16, None, get_config("elem_fill_opacity"),
                                  DEFAULT_FONT_SIZE, get_config("elem_value_format"), 0, False)

        # Read elements
        read_scalar_animate = read_elem(scalar_reg, scalar_elem, 0, 0, 16)
        read_vector_animate = read_elem(vector_reg, vector_elem, 2, 0, 0)
        read_vector_2d_animate = read_elem(vector_2d_reg, vector_2d_elem, 20, 0, 0)

        # Label
        read_elem_label = Text("read_elem", color=YELLOW) \
            .move_to(scalar_reg.reg_rect.get_right() + RIGHT * 4)
        self.add(read_elem_label)

        # Play Animation.
        self.add(read_elem_label)
        self.wait(duration=1)
        self.play(read_scalar_animate, read_vector_animate, read_vector_2d_animate)
        self.wait(duration=1)
        self.remove(read_elem_label)

        # Assign elements.
        new_vector_2d_elem = ElemUnit(BLUE, 16, None, get_config("elem_fill_opacity"),
                                      DEFAULT_FONT_SIZE, get_config("elem_value_format"), 0, False)
        assign_scalar_animate = assign_elem(vector_2d_elem, new_vector_2d_elem, scalar_reg, 0, 0, 0)
        new_scalar_elem = ElemUnit(GREEN, 8, None, get_config("elem_fill_opacity"),
                                   DEFAULT_FONT_SIZE, get_config("elem_value_format"), 0, False)
        assign_vector_animate = assign_elem(scalar_elem, new_scalar_elem, vector_reg, 4, 0, 0)
        new_vector_elem = ElemUnit(PURPLE, 32, None, get_config("elem_fill_opacity"),
                                   DEFAULT_FONT_SIZE, get_config("elem_value_format"), 0, False)
        assign_vector_2d_animate = assign_elem(vector_elem, new_vector_elem, vector_2d_reg, 7, 0, 0)

        assign_elem_label = Text("assign_elem", color=YELLOW) \
            .move_to(scalar_reg.reg_rect.get_right() + RIGHT * 4)
        self.add(assign_elem_label)

        # Play Animation.
        self.add(assign_elem_label)
        self.wait(duration=1)
        self.play(assign_scalar_animate, assign_vector_animate, assign_vector_2d_animate)
        self.wait(duration=1)
        self.remove(assign_elem_label)
