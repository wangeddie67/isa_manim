"""
Test object for register element.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       Dot, BraceBetweenPoints, Text, Arrow,
                       config,
                       RED, GREEN, BLUE, YELLOW,
                       LEFT, RIGHT, UP, DOWN,
                       RegElemUnit)

config.frame_height = 6
config.frame_width = 24

class TestOneDimRegElem(Scene):
    """
    Test object for register element.
    """
    def construct(self):
        elem = RegElemUnit(color=RED, width=16, value="0x5F5F")
        dots = [Dot(color=GREEN)]
        self.add(elem, *dots)

        down_brace = BraceBetweenPoints(elem.elem_rect.get_left() + DOWN * 0.5,
                                        elem.elem_rect.get_right() + DOWN * 0.5,
                                        color=GREEN)
        down_brace_text = \
            down_brace.get_text("Scene : " + str(elem.elem_rect.width)).set_color(GREEN)
        self.add(down_brace, down_brace_text)

        up_brace = BraceBetweenPoints(elem.elem_rect.get_left() + UP * 0.5,
                                      elem.elem_rect.get_right() + UP * 0.5,
                                      color=BLUE,
                                      direction=UP)
        up_brace_text = up_brace.get_text("Bit width : " + str(elem.elem_width)).set_color(BLUE)
        self.add(up_brace, up_brace_text)

        right_brace = BraceBetweenPoints(elem.elem_rect.get_right() + UP * 0.5,
                                         elem.elem_rect.get_right() + DOWN * 0.5,
                                         color=GREEN,
                                         direction=RIGHT)
        right_brace_text = right_brace.get_text("Scene : 1.0").set_color(GREEN)
        self.add(right_brace, right_brace_text)

        elem_rect_label = Text("elem_rect", color=YELLOW) \
            .move_to(elem.elem_rect.get_left() + LEFT * 4)
        elem_rect_arrow = Arrow(
            elem_rect_label.get_right(), elem.elem_rect.get_left(), color=YELLOW)
        self.add(elem_rect_label, elem_rect_arrow)

        value_text_label = Text("value_text", color=YELLOW) \
            .move_to(elem.elem_rect.get_left() + LEFT * 4 + DOWN * 1.0)
        value_text_arrow = Arrow(
            value_text_label.get_right(), elem.value_text.get_bottom(), color=YELLOW)
        self.add(value_text_label, value_text_arrow)
