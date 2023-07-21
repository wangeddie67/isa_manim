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
from .one_dim_reg_elem import OneDimRegElem
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
                 **kwargs):
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
            **kwargs: Arguments to new register rectangle.

        kwargs accept flowing arguments:

        * label_pos: position of label text. By default, the position of label text is defined as
          close to the left boundary of register rectangle.
        * font_size: Font size of label. By default, the font size is defined by configuration.

        """
        # Font size
        if "font_size" in kwargs:
            font_size = kwargs["font_size"]
            del kwargs["font_size"]
        else:
            font_size = DEFAULT_FONT_SIZE

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
        self.elem_width = float(width) / elements

        # Register rectangle
        self.reg_rect_list = [Rectangle(color=color,
                                        height=1.0,
                                        width=width * get_scene_ratio(),
                                        grid_xstep=self.elem_width * get_scene_ratio(),
                                        **kwargs).shift(DOWN * i)
                                for i in range(0, self.reg_count)]

        # Label text
        self.label_text_list = [Text(text=text[i],
                                     color=color,
                                     font_size=font_size)
                                for i in range(0, len(text))]
        if "label_pos" in kwargs:
            label_pos = np.ndarray(kwargs["label_pos"])
        else:
            for i in range(0, len(text)):
                label_pos = self.reg_rect_list[i].get_left() \
                    + self.label_text_list[i].get_left() + LEFT * 0.2
                self.label_text_list[i].move_to(label_pos)

        super().__init__(**kwargs)
        self.add(*self.reg_rect_list, *self.label_text_list)

    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    def get_max_boundary_width(self) -> float:
        """
        Return maximum scene width (left or right).

        Args:
            reg_idx: Index of register.
        """
        return max([self.reg_rect_list[reg_idx].width / 2 + self.label_text_list[reg_idx].width
                    for reg_idx in range(0, self.reg_count)])

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

        return self.reg_rect_list[reg_idx].get_right() \
            + LEFT * (index + 0.5) * elem_width * get_scene_ratio()


    def get_elem(self,
                 color: Color,
                 elem_width: float = -1.0,
                 reg_idx: int = 0,
                 index: int = 0,
                 value = None,
                 **kwargs) -> Rectangle:
        """
        Return a rectangle of specified item. 

        If not specified element width, new rectangle has same width as register.

        If specified element width, new rectangle and original rectangle are
        align right, if index is 0. Otherwise, move rectangle left by index.

        Args:
            color: Color of new rectangle.
            elem_width: Width of data element in bits.
            reg_idx: Index of register.
            index: Index of data element in register.
            value: Value of data element.
            **kwargs: Arguments to new elements.
        """
        if elem_width < 0:
            elem_width = self.elem_width

        return OneDimRegElem(color=color,
                             width=elem_width,
                             fill_opacity=0.5,
                             value=value,
                             **kwargs) \
            .move_to(self.get_elem_center(reg_idx=reg_idx, index=index, elem_width=elem_width))
