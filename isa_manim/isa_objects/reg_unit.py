"""
Object for two dimension register

Two-dimension register provides an absolute graphic object for registers, including:

* Multiple vector registers in ARM.
* ZA matrix array in ARM.
* Matrix array in DSA.

Graphic object is a VGroup containing several Text objects and several Rectangle objects.

* Label text object presents the register name of each register.
* Height of register rectangle object must be 1.0 while width of register rectangle object presents 
  the width of register, 1.0 means 8 bit.

Graphic object structure:

* Label text and register rectangle are horizontal alignment.
"""

from typing import Any, List
import numpy as np
from manim import (VGroup, Rectangle, Text,
                   LEFT, RIGHT, DOWN, UP)
from colour import Color
from ..isa_config import get_scene_ratio

class RegUnit(VGroup):
    """
    Object for two-dimension register.

    Attributes:
        label_text_list: list of label text objects.
        reg_rect_list: list of register rectangle objects.
        reg_count: number of registers.
        reg_width: register width in bit of one register.
        elem_width: element width in bit.
        elements: number of elements of one register.
    """

    require_serialization = False
    """
    Animation related with this object does not need to be serialized.
    """

    def __init__(self,
                 text: List[str],
                 color: Color,
                 width: int,
                 elements: int,
                 nreg: int,
                 value: List[List[Any]],
                 font_size: int,
                 value_format: str
                 ):
        """
        Constructor an two-dimension register.

        Args:
            text: Register names which could be a string or a list of string.
            color: Color of register.
            width: Width of register, in bits.
            elements: Number of elements in one register.
            nreg: Number of registers, used to create 2D registers or a list of registers.
            value: Value of this element.
            font_size: Font size of label. By default, the font size is defined by configuration.
        """
        # Store parameters        
        self.reg_font_size = font_size
        self.reg_value_format = value_format
        self.reg_value = value
        self.reg_width = width

        # register count
        self.reg_count = nreg

        # Register width
        self.elem_width = width // elements

        # Register rectangle
        if elements > 1:
            self.reg_rect = Rectangle(color=color,
                                      height=nreg,
                                      width=width * get_scene_ratio(),
                                      grid_xstep=self.elem_width * get_scene_ratio(),
                                      grid_ystep=1.0,
                                      ).shift(DOWN * nreg // 2 + UP * 0.5)
        else:
            self.reg_rect = Rectangle(color=color,
                                      height=nreg,
                                      width=width * get_scene_ratio(),
                                      grid_ystep=1.0
                                      ).shift(DOWN * nreg // 2 + UP * 0.5)

        # Label text
        if isinstance(text, str):
            text = [text]
        self.label_text_list = [Text(text=text[i],
                                     color=color,
                                     font_size=font_size)
                                for i in range(0, len(text))]
        reg_rect_corner = self.reg_rect.get_corner(UP + LEFT)
        for i in range(0, len(text)):
            label_pos = reg_rect_corner + self.label_text_list[i].get_left() + LEFT * 0.2 \
                + i * DOWN + 0.5 * DOWN
            self.label_text_list[i].move_to(label_pos)

        super().__init__()
        self.add(*self.reg_rect, *self.label_text_list)

    # Property functions
    @property
    def reg_text(self) -> str:
        """
        Return text of register in a list or single element.
        """
        return [label_text.text for label_text in self.label_text_list]

    @property
    def reg_color(self) -> Color:
        """
        Return color of register.
        """
        return self.reg_rect[0].color

    # Override function
    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    # Get locations.
    def get_elem_center(self,
                        index: int,
                        reg_idx: int,
                        offset: int,
                        elem_width: float) -> np.ndarray:
        """
        Return center position of specified item.

        If not specified element width, return one elem as same as definition.
        Otherwise, return one element with specified width.

        Args:
            index: Index of elements.
            reg_idx: Index of register.
            offset: Offset of lower bits.
            elem_width: Width of element in bits.
        """
        elem_count = self.reg_width // self.elem_width
        if index >= elem_count:
            reg_idx = (reg_idx + index // elem_count) % self.reg_count
            index = index % elem_count
        else:
            reg_idx = reg_idx % self.reg_count

        return self.reg_rect.get_corner(UP + RIGHT) + reg_idx * DOWN + 0.5 * DOWN \
            + LEFT * index * self.elem_width * get_scene_ratio() + \
            + LEFT * offset * get_scene_ratio() + LEFT * 0.5 * elem_width * get_scene_ratio()

    # Get element value
    def get_elem_value(self,
                       index: int,
                       reg_idx: int) -> Any:
        """
        Return value of specified item.
        
        Args:
            reg_idx: Index of register.
            index: Index of elements.
        """
        if self.reg_value is None:
            return None

        if isinstance(self.reg_value, list):
            if isinstance(self.reg_value[0], list):
                sub_reg_value = self.reg_value[reg_idx % len(self.reg_value)]
                return sub_reg_value[index % len(sub_reg_value)]
            else:
                elem_count = self.reg_width // self.elem_width
                return self.reg_value[(reg_idx * elem_count + index) % len(self.reg_value)]
        else:
            return self.reg_value

    # Get element value
    def set_elem_value(self,
                       value: Any,
                       index: int,
                       reg_idx: int):
        """
        Return value of specified item.
        
        Args:
            index: Index of elements.
        """
        elem_count = self.reg_width // self.elem_width
        if self.reg_value is None:
            if elem_count == 1:
                self.reg_value = [None for _ in range(0, self.reg_count)]
            else:
                self.reg_value = [[None for _ in range(0, elem_count)]
                                  for _ in range(0, self.reg_count)]

        if isinstance(self.reg_value, list):
            if isinstance(self.reg_value[0], list):
                sub_reg_value = self.reg_value[reg_idx % len(self.reg_value)]
                sub_reg_value[index % len(sub_reg_value)] = value
            else:
                elem_count = self.reg_width // self.elem_width
                self.reg_value[(reg_idx * elem_count + index) % len(self.reg_value)] = value
        else:
            self.reg_value = value
