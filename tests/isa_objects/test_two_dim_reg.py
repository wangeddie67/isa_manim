"""
Test object for register with two dimensions.
"""

import os
import sys
path = sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       Dot, BraceBetweenPoints, Text, Arrow,
                       config,
                       WHITE, GREEN, BLUE, YELLOW,
                       RIGHT, UP, DOWN,
                       TwoDimReg)

config.frame_height = 6
config.frame_width = 24

class TestTwoDimReg(Scene):
    """
    Test object for register with two dimensions.
    """
    def construct(self):
        vector = TwoDimReg(
            text=["V8", "V9", "V10", "V11"], nreg=4, color=WHITE, width=128, elements=8)
        dots = [Dot(color=GREEN)]
        self.add(vector, *dots)

        down_brace = BraceBetweenPoints(vector.reg_rect_list[-1].get_left() + DOWN * 0.5,
                                        vector.reg_rect_list[-1].get_right() + DOWN * 0.5,
                                        color=GREEN)
        down_brace_text = \
            down_brace.get_text("Scene : " + str(vector.reg_rect_list[0].width)).set_color(GREEN)
        self.add(down_brace, down_brace_text)

        up_brace = BraceBetweenPoints(vector.reg_rect_list[0].get_left() + UP * 0.5,
                                      vector.reg_rect_list[0].get_right() + UP * 0.5,
                                      color=BLUE,
                                      direction=UP)
        up_brace_text = up_brace.get_text("Bit width : " + str(vector.reg_width)).set_color(BLUE)
        self.add(up_brace, up_brace_text)

        right_brace = BraceBetweenPoints(vector.reg_rect_list[0].get_right() + UP * 0.5,
                                         vector.reg_rect_list[-1].get_right() + DOWN * 0.5,
                                         color=GREEN,
                                         direction=RIGHT)
        right_brace_text = right_brace.get_text("Scene : " + str(vector.reg_count)).set_color(GREEN)
        self.add(right_brace, right_brace_text)

        reg_rect_label = Text("reg_rect_list", color=YELLOW).move_to(UP * 2.5 + RIGHT * 4)
        reg_rect_arrow = Arrow(reg_rect_label.get_bottom(),
                               vector.reg_rect_list[0].get_top() + RIGHT * 2,
                               color=YELLOW)
        self.add(reg_rect_label, reg_rect_arrow)

        label_text_label = Text("label_text_list", color=YELLOW) \
            .move_to(vector.label_text_list[0].get_center() + UP * 2.5)
        label_text_arrow = Arrow(
            label_text_label.get_bottom(), vector.label_text_list[0].get_top(), color=YELLOW)
        self.add(label_text_label, label_text_arrow)
