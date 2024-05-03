"""
Test animation for elements, including reading and assigning elements.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       config,
                       WHITE, BLUE, GREEN, PURPLE, YELLOW,
                       UP, LEFT, RIGHT,
                       Text,
                       OneDimReg, RegUnit, RegElemUnit,
                       read_elem, assign_elem)

config.frame_height = 6
config.frame_width = 30

class TestElemAnimation(Scene):
    """
    Test animation for elements, including reading and assigning elements.
    """
    def construct(self):
        # Declare Register.
        scalar_reg = OneDimReg(text="Rn", color=WHITE, width=32).shift(UP * 4 + LEFT * 2)
        vector_reg = OneDimReg(text="Vn", color=WHITE, width=128).shift(UP * 2 + LEFT * 2)
        vector_2d_reg = RegUnit(text="Zn", color=WHITE, nreg=4, width=128).shift(LEFT * 2)

        # Play Animation.
        self.wait()
        self.add(scalar_reg, vector_reg, vector_2d_reg)
        self.wait()

        # Elements.
        scalar_elem = RegElemUnit(color=BLUE, width=16)
        vector_elem = RegElemUnit(color=GREEN, width=16)
        vector_2d_elem = RegElemUnit(color=PURPLE, width=16)

        # Read elements
        read_scalar_animate = read_elem(vector=scalar_reg, elem=scalar_elem)
        read_vector_animate = read_elem(vector=vector_reg, elem=vector_elem, index=2)
        read_vector_2d_animate = read_elem(vector=vector_2d_reg, elem=vector_2d_elem, index=20)

        # Label
        read_elem_label = Text("read_elem", color=YELLOW) \
            .move_to(scalar_reg.reg_rect.get_right() + RIGHT * 4)
        self.add(read_elem_label)

        # Play Animation.
        self.play(read_scalar_animate, read_vector_animate, read_vector_2d_animate)
        self.wait(duration=2)
        self.remove(read_elem_label)

        # Assign elements.
        new_vector_2d_elem = RegElemUnit(color=vector_2d_elem.elem_color, width=16)
        assign_scalar_animate = assign_elem(old_elem=vector_2d_elem,
                                            new_elem=new_vector_2d_elem,
                                            vector=scalar_reg)
        new_scalar_elem = RegElemUnit(color=scalar_elem.elem_color, width=8)
        assign_vector_animate = assign_elem(old_elem=scalar_elem,
                                            new_elem=new_scalar_elem,
                                            vector=vector_reg,
                                            index=4)
        new_vector_elem = RegElemUnit(color=vector_elem.elem_color, width=32)
        assign_vector_2d_animate = assign_elem(old_elem=vector_elem,
                                               new_elem=new_vector_elem,
                                               vector=vector_2d_reg,
                                               index=7)

        assign_elem_label = Text("assign_elem", color=YELLOW) \
            .move_to(scalar_reg.reg_rect.get_right() + RIGHT * 4)
        self.add(assign_elem_label)

        # Play Animation.
        self.play(assign_scalar_animate, assign_vector_animate, assign_vector_2d_animate)
        self.wait(duration=2)

