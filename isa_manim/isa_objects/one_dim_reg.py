"""
Object for one dimension register

One-dimension register provides an absolute graphic object for registers, including:

* General purpose registers.
* SIMD&FP/SVE registers for ARM
* Predicate registers for ARM.
* MMX/XMM/YMM/ZMM register for Intel.

Graphic object is a VGroup containing one Text objects and one Rectangle object.

* Label text object presents the register name.
* Height of register rectangle object must be 1.0 while width of register rectangle object presents 
  the width of register, 1.0 means 8 bit.

Graphic object structure:

* Label text and register rectangle are horizontal alignment.
"""

import numpy as np
from manim import (VGroup, Rectangle, Text,
                   LEFT,
                   DEFAULT_FONT_SIZE)
from colour import Color
from ..isa_config import get_scene_ratio

class OneDimReg(VGroup):
    """
    Object for one-dimension register.

    Attributes:
        label_text: Label text object.
        reg_rect: Register rectangle object.
        reg_width: register width in bit.
        elem_width: element width in bit.
        elements: number of elements.
        value: Value of this register, which should be an integer or UInt defined by isa_sim_utils.
    """

    require_serialization = False
    """
    Animation related with this object does not need to be serialized.
    """

    def __init__(self,
                 text: str,
                 color: Color,
                 width: int,
                 elements: int = 1,
                 value = None,
                 font_size = DEFAULT_FONT_SIZE,
                 label_pos = None):
        """
        Constructor an scalar register.

        Args:
            text: Register name.
            color: Color of register.
            width: Width of register, in bits
            elements: Number of elements.
            value: Value of this register, which should be an integer or UInt defined by
                isa_sim_utils.
            font_size: Font size of label. By default, the font size is defined by configuration.
            label_pos: position of label text. By default, the position of label text is defined as
                close to the left boundary of register rectangle.
        """
        # Element value
        self.value = value

        # element number:
        self.elements = elements

        # Register width
        self.reg_width = width
        self.elem_width = width // elements

        # Register rectangle
        if elements > 1:
            self.reg_rect = Rectangle(color=color,
                                    height=1.0,
                                    width=width * get_scene_ratio(),
                                    grid_xstep=self.elem_width * get_scene_ratio())
        else:
            self.reg_rect = Rectangle(color=color,
                                    height=1.0,
                                    width=width * get_scene_ratio())

        # Label text
        self.label_text = Text(text=text,
                               color=color,
                               font_size=font_size)
        if label_pos is not None:
            label_pos = np.ndarray(label_pos)
        else:
            label_pos = self.reg_rect.get_left() + self.label_text.get_left() + LEFT * 0.2
        self.label_text.move_to(label_pos)

        super().__init__()
        self.add(self.reg_rect, self.label_text)

    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    def get_elem_center(self,
                        index: int,
                        elem_width: float = -1.0) -> np.ndarray:
        """
        Return center position of specified item.

        If not specified element width, return one elem as same as definition.
        Otherwise, return one element with specified width.

        Args:
            index: Index of elements.
            elem_width: Width of element in bits.
        """
        if elem_width < 0:
            elem_width = self.elem_width

        return self.reg_rect.get_right() \
            + LEFT * (index + 0.5) * elem_width * get_scene_ratio()
