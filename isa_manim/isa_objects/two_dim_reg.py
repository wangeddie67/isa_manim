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

from typing import Union, List
import numpy as np
from manim import (VGroup, Rectangle, Text,
                   LEFT, DOWN,
                   DEFAULT_FONT_SIZE)
from colour import Color
from ..isa_config import get_scene_ratio

class TwoDimReg(VGroup):
    """
    Object for two-dimension register.

    Attributes:
        label_text_list: list of label text objects.
        reg_rect_list: list of register rectangle objects.
        reg_count: number of registers.
        reg_width: register width in bit of one register.
        elem_width: element width in bit.
        elements: number of elements of one register.
        value: Value of this register, which should be an integer or UInt defined by isa_sim_utils.
    """

    require_serialization = False
    """
    Animation related with this object does not need to be serialized.
    """

    def __init__(self,
                 text: Union[str, List[str]],
                 color: Color,
                 nreg: int,
                 width: int,
                 elements: int = 1,
                 value: list = None,
                 font_size = DEFAULT_FONT_SIZE,
                 label_pos = None):
        """
        Constructor an two-dimension register.

        Args:
            text: Register names which could be a string or a list of string.
            color: Color of register.
            nreg: Number of registers.
            width: Width of register, in bits.
            elements: Number of elements in one register.
            value: Value of this register, which should be an integer or UInt defined by
                isa_sim_utils.
            font_size: Font size of label. By default, the font size is defined by configuration.
            label_pos: position of label text. By default, the position of label text is defined as
                close to the left boundary of register rectangle.

        """
        # Element value
        if not isinstance(value, list):
            self.value_list = [value]
        else:
            self.value_list = value

        # register count
        self.reg_count = nreg

        # element number:
        self.elements = elements

        # Register width
        self.reg_width = width
        self.elem_width = width // elements

        # Register rectangle
        if elements > 1:
            self.reg_rect_list = [Rectangle(color=color,
                                            height=1.0,
                                            width=width * get_scene_ratio(),
                                            grid_xstep=self.elem_width * get_scene_ratio()
                                            ).shift(DOWN * i)
                                    for i in range(0, self.reg_count)]
        else:
            self.reg_rect_list = [Rectangle(color=color,
                                            height=1.0,
                                            width=width * get_scene_ratio()).shift(DOWN * i)
                                    for i in range(0, self.reg_count)]

        # Label text
        if isinstance(text, str):
            text = [text]
        self.label_text_list = [Text(text=text[i],
                                     color=color,
                                     font_size=font_size)
                                for i in range(0, len(text))]
        if label_pos is not None:
            label_pos = np.ndarray(label_pos)
        else:
            for i in range(0, len(text)):
                label_pos = self.reg_rect_list[i].get_left() \
                    + self.label_text_list[i].get_left() + LEFT * 0.2
                self.label_text_list[i].move_to(label_pos)

        super().__init__()
        self.add(*self.reg_rect_list, *self.label_text_list)

    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    def get_elem_center(self,
                        reg_idx: int,
                        index: int,
                        elem_width: float = -1.0) -> np.ndarray:
        """
        Return center position of specified item.

        If not specified element width, return one elem as same as definition.
        Otherwise, return one element with specified width.

        Args:
            reg_idx: Index of register.
            index: Index of elements.
            elem_width: Width of element in bits.
        """
        if elem_width < 0:
            elem_width = self.elem_width

        elem_count = self.reg_width // elem_width
        if index >= elem_count:
            reg_idx = (reg_idx + index // elem_count) % self.reg_count
            index = index % elem_count
        else:
            reg_idx = reg_idx % self.reg_count

        return self.reg_rect_list[reg_idx].get_right() \
            + LEFT * (index + 0.5) * elem_width * get_scene_ratio()
