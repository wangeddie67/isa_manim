"""
Test animation for registers, including declaring, concatenating and replacing function.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       config,
                       WHITE, YELLOW,
                       UP, DOWN, LEFT, RIGHT,
                       Text, RegUnit,
                       decl_register, replace_register)

config.frame_height = 6
config.frame_width = 30

class TestRegAnimation(Scene):
    """
    Test animation for registers, including declaring, concatenating and replacing function.
    """
    def construct(self):
        # Declare Register.
        r1 = RegUnit(text="R1", color=WHITE, width=32).shift(LEFT * 6 + UP * 6)
        r2 = RegUnit(text="R2", color=WHITE, width=32).shift(UP * 6)
        r3 = RegUnit(text="R3", color=WHITE, width=32).shift(RIGHT * 6 + UP * 6)
        v1 = RegUnit(text="V1", color=WHITE, width=128, elements=4).shift(UP * 4)
        v2 = RegUnit(text="V2", color=WHITE, width=128, elements=4).shift(UP * 2)
        zn = RegUnit(text="Zn", color=WHITE, nreg=4, width=128, elements=8)

        # Animation
        decl_animation = decl_register(r1, r2, r3, v1, v2, zn)

        # label
        decl_register_label = Text("decl_register", color=YELLOW) \
            .move_to(v1.reg_rect.get_right() + RIGHT * 4)

        # Play Animation.
        self.wait()
        self.add(decl_register_label)
        self.play(decl_animation)
        self.wait(duration=2)
        self.remove(decl_register_label)

        # Replace Register
        v3 = RegUnit(text="V3", color=WHITE, width=64, elements=4)
        v4 = RegUnit(text="V4", color=WHITE, width=128, elements=4)

        # Animation
        replace_v3_animation = replace_register(old_vector=v1, new_vector=v3, align="right")
        replace_v4_animation = replace_register(old_vector=v2, new_vector=v4, align="center")

        # label
        replace_register_label = Text("replace_register", color=YELLOW) \
            .move_to(v1.reg_rect.get_right() + RIGHT * 4)

        # Play Animation.
        self.add(replace_register_label)
        self.play(replace_v3_animation, replace_v4_animation)
        self.wait(duration=2)
        self.remove(replace_register_label)
