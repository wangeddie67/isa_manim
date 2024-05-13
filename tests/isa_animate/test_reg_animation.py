"""
Test animation for registers, including declaring, concatenating and replacing function.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       config, get_config, DEFAULT_FONT_SIZE,
                       WHITE, YELLOW,
                       UP, LEFT, RIGHT,
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
        r1 = RegUnit(["R1"], WHITE, 32, 1, 1, None,
                     DEFAULT_FONT_SIZE, get_config("elem_value_format")).shift(LEFT * 6 + UP * 6)
        r2 = RegUnit(["R2"], WHITE, 32, 1, 1, None,
                     DEFAULT_FONT_SIZE, get_config("elem_value_format")).shift(UP * 6)
        r3 = RegUnit(["R3"], WHITE, 32, 1, 1, None,
                     DEFAULT_FONT_SIZE, get_config("elem_value_format")).shift(RIGHT * 6 + UP * 6)
        v1 = RegUnit(["V1"], WHITE, 128, 4, 1, None,
                     DEFAULT_FONT_SIZE, get_config("elem_value_format")).shift(UP * 4)
        v2 = RegUnit(["V2"], WHITE, 128, 4, 1, None,
                     DEFAULT_FONT_SIZE, get_config("elem_value_format")).shift(UP * 2)
        zn = RegUnit(["Zn"], WHITE, 128, 4, 4, None,
                     DEFAULT_FONT_SIZE, get_config("elem_value_format"))

        # Animation
        decl_animation = decl_register(r1, r2, r3, v1, v2, zn)

        # label
        decl_register_label = Text("decl_register", color=YELLOW) \
            .move_to(v1.reg_rect.get_right() + RIGHT * 4)

        # Play Animation.
        self.wait()
        self.add(decl_register_label)
        self.wait(duration=1)
        self.play(decl_animation)
        self.wait(duration=1)
        self.remove(decl_register_label)

        # Replace Register
        v3 = RegUnit(["V3"], WHITE, 64, 4, 1, None,
                     DEFAULT_FONT_SIZE, get_config("elem_value_format"))
        v4 = RegUnit(["V4"], WHITE, 128, 8, 1, None,
                     DEFAULT_FONT_SIZE, get_config("elem_value_format"))

        # Animation
        replace_v3_animation = replace_register(v1, v3, 0)
        replace_v4_animation = replace_register(v2, v4, 0)

        # label
        replace_register_label = Text("replace_register", color=YELLOW) \
            .move_to(v1.reg_rect.get_right() + RIGHT * 4)

        # Play Animation.
        self.add(replace_register_label)
        self.wait(duration=1)
        self.play(replace_v3_animation, replace_v4_animation)
        self.wait(duration=1)
        self.remove(replace_register_label)
