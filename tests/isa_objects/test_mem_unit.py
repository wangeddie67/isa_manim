"""
Test object for function unit.
"""

import os
import sys
path = sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       Dot, BraceBetweenPoints, Text, Arrow,
                       config,
                       WHITE, GREEN, YELLOW,
                       LEFT, RIGHT, UP, DOWN,
                       MemoryUnit)

config.frame_height = 6
config.frame_width = 24

class TestMemoryUnit(Scene):
    """
    Test object for function unit.
    """
    def construct(self):
        mem_unit = MemoryUnit(color=WHITE, addr_width=64, data_width=32)
        dots = [Dot(color=GREEN)]
        self.add(mem_unit, *dots)

        mem_up_brace = BraceBetweenPoints(mem_unit.mem_rect.get_left() + UP * 1.5,
                                          mem_unit.mem_rect.get_right() + UP * 1.5,
                                          color=GREEN,
                                          direction=UP)
        mem_up_brace_text = \
            mem_up_brace.get_text("Scene : " + str(mem_unit.mem_rect.width)).set_color(GREEN)
        self.add(mem_up_brace, mem_up_brace_text)

        addr_up_brace = BraceBetweenPoints(mem_unit.addr_rect.get_left() + UP * 1.5,
                                           mem_unit.addr_rect.get_right() + UP * 1.5,
                                           color=GREEN,
                                           direction=UP)
        addr_up_brace_text = \
            addr_up_brace.get_text("Scene : " + str(mem_unit.addr_rect.width)).set_color(GREEN)
        self.add(addr_up_brace, addr_up_brace_text)

        addr_up_space_brace = BraceBetweenPoints(mem_unit.addr_rect.get_right() + UP * 1.5,
                                                 mem_unit.addr_rect.get_right() + UP * 1.5 + RIGHT,
                                                 color=GREEN,
                                                 direction=UP)
        addr_up_space_brace_text = addr_up_space_brace.get_text("1.0").set_color(GREEN)
        self.add(addr_up_space_brace, addr_up_space_brace_text)

        data_up_brace = BraceBetweenPoints(mem_unit.data_rect.get_left() + UP * 1.5,
                                           mem_unit.data_rect.get_right() + UP * 1.5,
                                           color=GREEN,
                                           direction=UP)
        data_up_brace_text = \
            data_up_brace.get_text("Scene : " + str(mem_unit.data_rect.width)).set_color(GREEN)
        self.add(data_up_brace, data_up_brace_text)

        data_up_space_brace = BraceBetweenPoints(mem_unit.data_rect.get_left() + UP * 1.5 + LEFT,
                                                 mem_unit.data_rect.get_left() + UP * 1.5,
                                                 color=GREEN,
                                                 direction=UP)
        data_up_space_brace_text = data_up_space_brace.get_text("1.0").set_color(GREEN)
        self.add(data_up_space_brace, data_up_space_brace_text)

        addr_down_brace = BraceBetweenPoints(mem_unit.addr_rect.get_left() + DOWN * 0.5,
                                             mem_unit.addr_rect.get_right() + DOWN * 0.5,
                                             color=GREEN)
        addr_down_brace_text = \
            addr_down_brace.get_text("Bit width : " + str(mem_unit.addr_width)).set_color(GREEN)
        self.add(addr_down_brace, addr_down_brace_text)

        data_down_brace = BraceBetweenPoints(mem_unit.data_rect.get_left() + DOWN * 0.5,
                                             mem_unit.data_rect.get_right() + DOWN * 0.5,
                                             color=GREEN)
        data_down_brace_text = \
            data_down_brace.get_text("Bit width : " + str(mem_unit.data_width)).set_color(GREEN)
        self.add(data_down_brace, data_down_brace_text)

        mem_map_down_brace = BraceBetweenPoints(mem_unit.mem_map_rect.get_left() + DOWN * 0.5,
                                                mem_unit.mem_map_rect.get_right() + DOWN * 0.5,
                                                color=GREEN)
        mem_map_down_brace_text = \
            mem_map_down_brace.get_text("Scene : " + str(mem_unit.mem_map_rect.width)) \
                .set_color(GREEN)
        self.add(mem_map_down_brace, mem_map_down_brace_text)

        right_brace = BraceBetweenPoints(mem_unit.data_rect.get_right() + UP * 1.5,
                                         mem_unit.data_rect.get_right() + UP * 0.5,
                                         color=GREEN,
                                         direction=RIGHT)
        right_brace_text = right_brace.get_text("Scene : 1.0").set_color(GREEN)

        args_right_brace = BraceBetweenPoints(mem_unit.data_rect.get_right() + UP * 0.5,
                                              mem_unit.data_rect.get_right() + DOWN * 0.5,
                                              color=GREEN,
                                              direction=RIGHT)
        args_right_brace_text = args_right_brace.get_text("Scene : 1.0").set_color(GREEN)

        args_space_brace = BraceBetweenPoints(mem_unit.data_rect.get_right() + DOWN * 0.5,
                                              mem_unit.data_rect.get_right() + DOWN * 1.5,
                                              color=GREEN,
                                              direction=RIGHT)
        args_space_brace_text = args_space_brace.get_text("Scene : 1.0").set_color(GREEN)

        res_right_brace = BraceBetweenPoints(mem_unit.data_rect.get_right() + DOWN * 1.5,
                                             mem_unit.mem_map_rect.get_right() + UP * 0.5,
                                             color=GREEN,
                                             direction=RIGHT)
        res_right_brace_text = res_right_brace.get_text("Scene : 1.0").set_color(GREEN)

        res_space_brace = BraceBetweenPoints(mem_unit.mem_map_rect.get_right() + UP * 0.5,
                                             mem_unit.mem_map_rect.get_right() + DOWN * 0.5,
                                             color=GREEN,
                                             direction=RIGHT)
        res_space_brace_text = res_space_brace.get_text("Scene : 1.0").set_color(GREEN)
        self.add(
            right_brace, right_brace_text, args_right_brace, args_right_brace_text,
            res_right_brace, res_right_brace_text,
            args_space_brace, args_space_brace_text, res_space_brace, res_space_brace_text)

        mem_rect_label = Text("mem_rect", color=YELLOW) \
            .move_to(mem_unit.mem_rect.get_left() + LEFT * 4 + UP * 4.5)
        mem_rect_arrow = Arrow(
            mem_rect_label.get_right(), mem_unit.mem_rect.get_left(), color=YELLOW)
        self.add(mem_rect_label, mem_rect_arrow)

        # label_text_label = Text("label_text", color=YELLOW) \
        #     .move_to(mem_unit.label_text.get_left() + LEFT * 4 + UP * 5)
        # label_text_arrow = Arrow(
        #     label_text_label.get_right(), mem_unit.label_text.get_left(), color=YELLOW)
        # self.add(label_text_label, label_text_arrow)

        addr_rect_label = Text("addr_rect", color=YELLOW) \
            .move_to(mem_unit.addr_rect.get_top() + UP * 3 + LEFT * 2)
        addr_rect_arrow = Arrow(
            addr_rect_label.get_bottom(), mem_unit.addr_rect.get_top() + LEFT, color=YELLOW)
        self.add(addr_rect_label, addr_rect_arrow)

        data_rect_label = Text("data_rect", color=YELLOW) \
            .move_to(mem_unit.data_rect.get_top() + UP * 3 + RIGHT * 2)
        data_rect_arrow = Arrow(
            data_rect_label.get_bottom(), mem_unit.data_rect.get_top() + RIGHT, color=YELLOW)
        self.add(data_rect_label, data_rect_arrow)

        mem_map_label = Text("mem_map_rect", color=YELLOW) \
            .move_to(mem_unit.mem_map_rect.get_bottom() + DOWN * 2 + RIGHT * 5)
        mem_map_arrow = Arrow(
            mem_map_label.get_left(), mem_unit.mem_map_rect.get_bottom() + RIGHT, color=YELLOW)
        self.add(mem_map_label, mem_map_arrow)
