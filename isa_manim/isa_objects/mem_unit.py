"""
Object for memory unit.

Such object provides an absolute graphic object for memory unit.

Graphic object is a VGroup containing one Round rectangle objects, several rectangle objects, two
Cubic Bezier lines and several Text objects.
"""

import numpy as np
from manim import (VGroup, Text, Rectangle, DashedVMobject, RoundedRectangle,
                   CubicBezier,
                   LEFT, RIGHT, UP, DOWN,
                   DEFAULT_FONT_SIZE)
from colour import Color
from ..isa_config import get_scene_ratio
from .mem_map import MemoryMap

class MemoryUnit(VGroup):
    """
    Object for memory unit.

    Attributes:
        addr_width: width of address, in bit.
        data_width: Width of data, in bit.
        mem_rect: Round rectangle of memory unit.
        label_text: Text of memory.
        addr_rect: rectangle of address argument.
        data_rect: rectangle of data argument.
        mem_map_rect: rectangle of memory map. Provides the position of memory map.
        mem_map_left_brace: left brace of memory map.
        mem_map_right_brace: right brace of memory map. 
    """

    require_serialization = True

    def __init__(self,
                 color: Color,
                 addr_width: int,
                 data_width: int,
                 font_size = DEFAULT_FONT_SIZE):
        """
        Constructor an function call.

        Args:
            color: Color of memory unit.
            addr_width: Width of address, in bit
            data_width: Width of data, in bit
            font_size: Font size of value text.
        """
        # address width
        self.addr_width = addr_width
        # data width
        self.data_width = data_width

        # memory rectangle
        self.mem_rect = RoundedRectangle(color=color, height=3.0, width=4)

        # Label text
        self.label_text = Text(
            text="Mem", color=color, font_size=font_size) \
                .move_to(self.mem_rect.get_center())

        # Address rectangle
        self.addr_rect = DashedVMobject(
            Rectangle(color=color, height=1.0, width=addr_width * get_scene_ratio()))
        self.addr_rect.shift(
            LEFT * (1 + self.mem_rect.width / 2 + self.addr_rect.width / 2))
        self.addr_label_text = Text(text="Addr", color=color, font_size=font_size) \
            .move_to(self.addr_rect.get_center() + UP)

        # Data rectangle
        self.data_rect = DashedVMobject(
            Rectangle(color=color, height=1.0, width=data_width * get_scene_ratio()))
        self.data_rect.shift(
            RIGHT * (1 + self.mem_rect.width / 2 + self.data_rect.width / 2))
        self.data_label_text = Text(text="Data", color=color, font_size=font_size) \
            .move_to(self.data_rect.get_center() + UP)

        self.mem_map_width = self.addr_rect.width + self.data_rect.width + self.mem_rect.width + 2
        self.mem_map_rect = Rectangle(color=color, height=1.0, width=self.mem_map_width)
        self.mem_map_rect.shift(self.addr_rect.get_left() - self.mem_map_rect.get_left())
        self.mem_map_rect.shift(DOWN * 3)

        self.mem_map_left_brace = CubicBezier(
            self.mem_map_rect.get_left() + UP * 0.7, self.mem_map_rect.get_left() + UP * 1.25,
            self.mem_rect.get_left() + DOWN * 2.25, self.mem_rect.get_left() + DOWN * 1.5)
        self.mem_map_right_brace = CubicBezier(
            self.mem_map_rect.get_right() + UP * 0.7, self.mem_map_rect.get_right() + UP * 1.25,
            self.mem_rect.get_right() + DOWN * 2.25, self.mem_rect.get_right() + DOWN * 1.5)

        self.mem_map_object : MemoryMap = None

        super().__init__()
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
