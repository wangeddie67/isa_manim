"""
Test object for function unit.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       Dot, BraceBetweenPoints, Text, Arrow,
                       config, get_config, DEFAULT_FONT_SIZE,
                       WHITE, GREEN, BLUE, YELLOW,
                       LEFT, RIGHT, UP, DOWN,
                       FunctionUnit)

config.frame_height = 6
config.frame_width = 24

class TestFunctionUnit(Scene):
    """
    Test object for function unit.
    """
    def construct(self):
        function = FunctionUnit(
            "FMA (a * b + c)", WHITE, [16, 16, 32], [32, 4], ["a", "b", "c"], ["sum", "flag"],
            DEFAULT_FONT_SIZE, get_config("elem_value_format"), None)
        dots = [Dot(color=GREEN)]
        self.add(function, *dots)

        func_down_brace = BraceBetweenPoints(function.func_rect.get_left() + DOWN * 0.5,
                                             function.func_rect.get_right() + DOWN * 0.5,
                                             color=GREEN)
        func_down_brace_text = \
            func_down_brace.get_text("Scene : " + str(function.func_rect.width)) \
            .set_color(GREEN).shift(UP * 0.25)
        self.add(func_down_brace, func_down_brace_text)

        for i, (arg_width, arg_rect) in enumerate(zip(function.func_args_width_list,
                                                      function.args_rect_list)):
            arg_up_brace = BraceBetweenPoints(arg_rect.get_left() + UP * 0.5,
                                              arg_rect.get_right() + UP * 0.5,
                                              color=BLUE,
                                              direction=UP)
            if i == 0:
                arg_up_brace_text = arg_up_brace.get_text("Bit width : " + str(arg_width)) \
                    .set_color(BLUE).shift(LEFT * 1.0)
            else:
                arg_up_brace_text = arg_up_brace.get_text(str(arg_width)).set_color(BLUE)
            self.add(arg_up_brace, arg_up_brace_text)

            arg_down_brace = BraceBetweenPoints(arg_rect.get_left() + DOWN * 0.5,
                                                arg_rect.get_right() + DOWN * 0.5,
                                                color=GREEN)
            if i == 0:
                arg_down_brace_text = arg_down_brace.get_text("Scene : " + str(arg_rect.width)) \
                    .set_color(GREEN).shift(UP * 0.25 + LEFT * 1.0)
            else:
                arg_down_brace_text = arg_down_brace.get_text(str(arg_rect.width)) \
                    .set_color(GREEN).shift(UP * 0.25)
            self.add(arg_down_brace, arg_down_brace_text)

            if i > 0:
                arg_space_down_brace = BraceBetweenPoints(
                    function.args_rect_list[i - 1].get_right() + DOWN * 0.5,
                    function.args_rect_list[i].get_left() + DOWN * 0.5,
                    color=GREEN)
                arg_space_down_brace_text = \
                    arg_space_down_brace.get_text("1.0").set_color(GREEN).shift(UP * 0.25)
                self.add(arg_space_down_brace, arg_space_down_brace_text)

        for i, (res_width, res_rect) in enumerate(zip(function.func_res_width_list,
                                                      function.res_rect_list)):
            res_up_brace = BraceBetweenPoints(res_rect.get_left() + UP * 0.5,
                                              res_rect.get_right() + UP * 0.5,
                                              color=BLUE)
            if i == 0:
                res_up_brace_text = res_up_brace.get_text("Bit width : " + str(res_width)) \
                    .set_color(BLUE).shift(UP * 0.25 + LEFT * 1.0)
            else:
                res_up_brace_text = res_up_brace.get_text(str(res_width)) \
                    .set_color(BLUE).shift(UP * 0.25)
            self.add(res_up_brace, res_up_brace_text)

            res_down_brace = BraceBetweenPoints(res_rect.get_left() + DOWN * 0.5,
                                                res_rect.get_right() + DOWN * 0.5,
                                                color=GREEN)
            if i == 0:
                res_down_brace_text = res_down_brace.get_text("Scene : " + str(res_rect.width)) \
                    .set_color(GREEN).shift(UP * 0.25 + LEFT * 1.0)
            else:
                res_down_brace_text = res_down_brace.get_text(str(res_rect.width)) \
                    .set_color(GREEN).shift(UP * 0.25)
            self.add(res_down_brace, res_down_brace_text)

            if i > 0:
                res_space_down_brace = BraceBetweenPoints(
                    function.res_rect_list[i - 1].get_right() + DOWN * 0.5,
                    function.res_rect_list[i].get_left() + DOWN * 0.5,
                    color=GREEN)
                res_space_down_brace_text = \
                    res_space_down_brace.get_text("1.0").set_color(GREEN).shift(UP * 0.25)
                self.add(res_space_down_brace, res_space_down_brace_text)

        right_brace = BraceBetweenPoints(function.func_rect.get_right() + UP * 0.5,
                                         function.func_rect.get_right() + DOWN * 0.5,
                                         color=GREEN,
                                         direction=RIGHT)
        right_brace_text = right_brace.get_text("Scene : 1.0").set_color(GREEN)

        args_right_brace = BraceBetweenPoints(function.func_rect.get_right() + UP * 2.5,
                                              function.func_rect.get_right() + UP * 1.5,
                                              color=GREEN,
                                              direction=RIGHT)
        args_right_brace_text = args_right_brace.get_text("Scene : 1.0").set_color(GREEN)

        args_space_brace = BraceBetweenPoints(function.func_rect.get_right() + UP * 1.5,
                                              function.func_rect.get_right() + UP * 0.5,
                                              color=GREEN,
                                              direction=RIGHT)
        args_space_brace_text = args_space_brace.get_text("Scene : 1.0").set_color(GREEN)

        res_right_brace = BraceBetweenPoints(function.func_rect.get_right() + DOWN * 1.5,
                                             function.func_rect.get_right() + DOWN * 2.5,
                                             color=GREEN,
                                             direction=RIGHT)
        res_right_brace_text = res_right_brace.get_text("Scene : 1.0").set_color(GREEN)

        res_space_brace = BraceBetweenPoints(function.func_rect.get_right() + DOWN * 0.5,
                                             function.func_rect.get_right() + DOWN * 1.5,
                                             color=GREEN,
                                             direction=RIGHT)
        res_space_brace_text = res_space_brace.get_text("Scene : 1.0").set_color(GREEN)
        self.add(
            right_brace, right_brace_text, args_right_brace, args_right_brace_text,
            res_right_brace, res_right_brace_text,
            args_space_brace, args_space_brace_text, res_space_brace, res_space_brace_text)

        func_rect_label = Text("func_rect", color=YELLOW) \
            .move_to(function.func_rect.get_left() + LEFT * 4 + UP * 0.5)
        func_rect_arrow = Arrow(
            func_rect_label.get_right(), function.func_rect.get_left(), color=YELLOW)
        self.add(func_rect_label, func_rect_arrow)

        label_text_label = Text("name_text", color=YELLOW) \
            .move_to(function.func_rect.get_left() + LEFT * 4 + DOWN * 0.5)
        label_text_arrow = Arrow(
            label_text_label.get_right(), function.name_text.get_left(), color=YELLOW)
        self.add(label_text_label, label_text_arrow)

        res_rect_label = Text("res_rect_list", color=YELLOW) \
            .move_to(function.res_rect_list[0].get_left() + LEFT * 4 + DOWN * 0.5)
        res_rect_arrow = Arrow(
            res_rect_label.get_right(), function.res_rect_list[0].get_left(), color=YELLOW)
        self.add(res_rect_label, res_rect_arrow)

        res_text_label = Text("res_text_list", color=YELLOW) \
            .move_to(function.res_rect_list[0].get_left() + LEFT * 4 + UP * 0.5)
        res_text_arrow = Arrow(
            res_text_label.get_right(), function.res_text_list[0].get_left(), color=YELLOW)
        self.add(res_text_label, res_text_arrow)

        args_rect_label = Text("args_rect_list", color=YELLOW) \
            .move_to(function.args_rect_list[0].get_left() + LEFT * 4 + UP * 0.5)
        args_rect_arrow = Arrow(
            args_rect_label.get_right(), function.args_rect_list[0].get_left(), color=YELLOW)
        self.add(args_rect_label, args_rect_arrow)

        args_text_label = Text("args_text_list", color=YELLOW) \
            .move_to(function.args_rect_list[0].get_left() + LEFT * 4 + DOWN * 0.5)
        args_text_arrow = Arrow(
            args_text_label.get_right(), function.args_text_list[0].get_left(), color=YELLOW)
        self.add(args_text_label, args_text_arrow)
