"""
One dimension register object.
"""

import numpy as np
from manim import VGroup, Rectangle, Text
from manim import LEFT
from manim import DEFAULT_FONT_SIZE
from colour import Color
from .one_dim_reg_elem import OneDimRegElem

class OneDimReg(VGroup):
    """
    One-dimension register provides an absolute graphic object for registers, 
    including:
    - general purpose registers.
    - predicate registers for ARM.
    - SIMD&FP registers for ARM
    - SVE registers for ARM.

    Graphic object is a VGroup containing several Text objects and one Rectangle
    object.
    - Label text object presents the register name.
    - List of value text object presents the register value of each element.
      If number of value text must be as same as the number of elements.
    - Height of register rectangle object must be 1.0 while width of register
    rectangle object presents the width of register, 1.0 means 1 byte.

    Graphic object structure:
    - Label text, value text and register rectangle are horizontal alignment.
    - register rectangle and value text are vertical alignment.

    --------------------------------------------------
    |         |        Register Rectangle            |
    |         |  ---------------------------------   |
    | Label   |  | Value Text | Value Text | ... |   |
    |  Text   |  ---------------------------------   |
    |         |                                      |
    --------------------------------------------------

    Register rectangle support scale ratio on x-axis, which means the ratio of
    the width in scene to the width of register.

    Members:
        label_text: Label text object.
        value_text_list: List of value text object.
        reg_rect: Register rectangle object.
        ratio: scene width / register width.
        reg_width: register width.
        elem_width: element width.
        elements: number of element.
    """

    require_serialization = False

    def __init__(self,
                 text: str,
                 color: Color,
                 width: int,
                 elements: int = 1,
                 **kwargs):
        """
        Constructor an scalar register.

        Args:
            text: Register name.
            color: Color of register.
            width: Width of register, in Byte
            elements: Number of elements.

        kwargs:
            ratio: scene width / register width
            label_pos: Label position related to the center of elem_width.
            font_size: Font size of label and value text.
        """
        # Scene ratio
        self.ratio = 1.0
        if "ratio" in kwargs:
            self.ratio = kwargs["ratio"]
            del kwargs["ratio"]

        # Font size
        if "font_size" in kwargs:
            font_size = kwargs["font_size"]
            del kwargs["font_size"]
        else:
            font_size = DEFAULT_FONT_SIZE

        # Element value
        if "values" in kwargs:
            if isinstance(kwargs["values"], str):
                value_str_list = [kwargs["values"]]
            else:
                value_str_list = kwargs["values"]
            del kwargs["values"]
        else:
            value_str_list = []

        # element number:
        self.elements = elements

        # Register width
        self.reg_width = width
        self.elem_width = float(width) / elements

        # Register rectangle
        self.reg_rect = Rectangle(color=color,
                                  height=1.0,
                                  width=width * self.ratio,
                                  grid_xstep=self.elem_width,
                                  **kwargs)

        # Label text
        self.label_text = Text(text=text,
                               color=color,
                               font_size=font_size)
        if "label_pos" in kwargs:
            label_pos = np.ndarray(kwargs["label_pos"])
        else:
            label_pos = self.reg_rect.get_left() \
                + self.label_text.get_left() + LEFT * 0.2
        self.label_text.move_to(label_pos)

        # Value text
        self.value_text_list = []
        for index, value in enumerate(value_str_list):
            elem_label_pos = self.reg_rect.get_right() + \
                LEFT * (index + 0.5 ) * self.elem_width * self.ratio
            elem_label = Text(text=value,
                                color=color,
                                font_size=font_size) \
                .move_to(elem_label_pos)
            self.value_text_list.append(elem_label)

        super().__init__(**kwargs)
        self.add(self.reg_rect, self.label_text, *self.value_text_list)

    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    def get_reg_width(self) -> float:
        """
        Return scene width of register.
        """
        return self.reg_width * self.ratio

    def get_max_boundary_width(self) -> float:
        """
        Return maximum scene width (left or right).
        """
        return self.reg_rect.width / 2 + self.label_text.width

    def get_reg_center(self) -> np.ndarray:
        """
        return center position of register rectangle.
        """
        return self.reg_rect.get_center()

    def get_elem_center(self,
                        index: int,
                        elem_width: float = -1.0) -> np.ndarray:
        """
        Return center position of specified item.

        If not specified element width, return one elem as same as definition.
        Otherwise, return one element with specified width.

        Args:
            index: Index of elements.
            elem_width: Width of element in byte.
        """
        if elem_width < 0:
            elem_width = self.elem_width

        return self.reg_rect.get_right() \
            + LEFT * (index + 0.5) * elem_width * self.ratio


    def get_elem(self,
                 color: Color,
                 elem_width: float = -1.0,
                 index: int = 0,
                 **kwargs) -> Rectangle:
        """
        Return a rectangle of specified item. 

        If not specified element width, new rectangle has same width as register.

        If specified element width, new rectangle and original rectangle are
        align right, if index is 0. Otherwise, move rectangle left by index.

        Args:
            color: Color of new rectangle.
            elem_width: Width of data element in Byte.
            index: Index of data element in register.
            kwargs: Arguments to new elements.
        """
        if elem_width < 0:
            elem_width = self.elem_width

        return OneDimRegElem(color=color,
                             width=elem_width * self.ratio,
                             fill_opacity=0.5,
                             **kwargs) \
            .move_to(self.get_elem_center(index=index, elem_width=elem_width))
