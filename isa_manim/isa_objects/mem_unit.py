"""
Object for function call

Such object provides an absolute graphic object for function call, including pre-defined functions 
and operators.

Graphic object is a VGroup containing one Ellipse objects, several rectangle objects with dash line 
and several Text objects.
"""

from typing import List
import numpy as np
from manim import (VGroup, Text, Rectangle, DashedVMobject, RoundedRectangle, BraceBetweenPoints,
                   CubicBezier,
                   LEFT, RIGHT, UP, DOWN,
                   DEFAULT_FONT_SIZE)
from colour import Color
from ..isa_config import get_scene_ratio

class MemoryUnit(VGroup):
    """
    Object for function call.

    Attributes:
        args_width: width of arguments, in bit.
        res_width: Width of return value, in bit.
        func_ellipse: Ellipse of function.
        label_text: Text of function name/brief.
        args_rect_list: rectangle of arguments.
        args_text_list: text of arguments.
        res_rect: rectangle of return value.
    """

    require_serialization = True

    def __init__(self,
                 color: Color,
                 addr_width: int,
                 data_width: int,
                 **kwargs):
        """
        Constructor an function call.

        Args:
            text: Register name.
            color: Color of function call.
            args_width: Width of arguments, in bit
            res_width: Width of return value, in bit
            **kwargs: Arguments to function ellipse.

        kwargs:

            * args_value: Text of each argument.
            * font_size: Font size of value text.
        """
        # Font size
        if "font_size" in kwargs:
            font_size = kwargs["font_size"]
            del kwargs["font_size"]
        else:
            font_size = DEFAULT_FONT_SIZE

        # address width
        self.addr_width = addr_width
        # data width
        self.data_width = data_width

        # memory rectangle
        self.mem_rect = RoundedRectangle(
            color=color, height=3.0, width=4, **kwargs)

        # Label text
        self.label_text = Text(
            text="Mem", color=color, font_size=font_size) \
                .move_to(self.mem_rect.get_center() + UP * 0.5)
        self.range_text = Text(
            text="", color=color, font_size=font_size) \
                .move_to(self.mem_rect.get_center() + DOWN * 0.5)

        # Address rectangle
        self.addr_rect = DashedVMobject(
            Rectangle(color=color, height=1.0, width=addr_width * get_scene_ratio()))
        self.addr_rect.shift(
            LEFT * (1 + self.mem_rect.width / 2 + self.addr_rect.width / 2))
        self.addr_label_text = Text(
            text="Addr", color=color, font_size=font_size).move_to(self.addr_rect.get_center())

        # Data rectangle
        self.data_rect = DashedVMobject(
            Rectangle(color=color, height=1.0, width=data_width * get_scene_ratio()))
        self.data_rect.shift(
            RIGHT * (1 + self.mem_rect.width / 2 + self.data_rect.width / 2))
        self.data_label_text = Text(
            text="Data", color=color, font_size=font_size).move_to(self.data_rect.get_center())
        
        self.mem_map_width = self.addr_rect.width + self.data_rect.width + self.mem_rect.width + 2
        self.mem_map_rect = Rectangle(color=color, height=1.0, width=self.mem_map_width, **kwargs)
        self.mem_map_rect.shift(self.addr_rect.get_left() - self.mem_map_rect.get_left())
        self.mem_map_rect.shift(DOWN * 3)

        self.mem_map_left_brace = CubicBezier(
            self.mem_map_rect.get_left() + UP * 0.7, self.mem_map_rect.get_left() + UP * 1.25,
            self.mem_rect.get_left() + DOWN * 2.25, self.mem_rect.get_left() + DOWN * 1.5)
        self.mem_map_right_brace = CubicBezier(
            self.mem_map_rect.get_right() + UP * 0.7, self.mem_map_rect.get_right() + UP * 1.25,
            self.mem_rect.get_right() + DOWN * 2.25, self.mem_rect.get_right() + DOWN * 1.5)

        super().__init__(**kwargs)
        self.add(self.mem_rect, self.label_text,
                 self.addr_rect, self.addr_label_text, self.data_rect, self.data_label_text,
                 self.mem_map_rect, self.mem_map_left_brace, self.mem_map_right_brace)

    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    def get_addr_pos(self, width: int = None) -> np.ndarray:
        """
        Return center position of access address.

        Args:
            width: Width of address in bit.
        """
        if width:
            return self.addr_rect.get_right() + LEFT * width * get_scene_ratio() / 2
        else:
            return self.addr_rect.get_center()

    def get_data_pos(self, width: int = None) -> np.ndarray:
        """
        Return center position of write data.

        Args:
            width: Width of write data in bit.
        """
        if width:
            return self.data_rect.get_right() + LEFT * width * get_scene_ratio() / 2
        else:
            return self.data_rect.get_center()
