"""
Object for register element

Register element provides an absolute graphic object for register elements.

Graphic object is a VGroup containing one Text objects and one Rectangle object.

* Value text object presents the register value of each element.
* Height of element rectangle object must be 1.0 while width of register rectangle object presents 
  the width of element, 1.0 means 8 bit.

Graphic object structure:

* Value text and Element rectangle are central alignment.
"""

import numpy as np
from manim import (VGroup, Rectangle, Text,
                   LEFT,
                   DEFAULT_FONT_SIZE)
from colour import Color
from ..isa_config import get_scene_ratio

class OneDimRegElem(VGroup):
    """
    Object for register element.

    Attributes:
        value_text: Value text object.
        elem_rect: Register rectangle object.
        elem_width: element width.
        value: Value of this element, which should be an integer or UInt defined by isa_sim_utils.
    """

    require_serialization = False

    def __init__(self,
                 color: Color,
                 width: int,
                 value = None,
                 fill_opacity = 0.5,
                 font_size = DEFAULT_FONT_SIZE):
        """
        Constructor an element.

        Args:
            color: Color of register.
            width: Width of register, in bit.
            value: Value of this register, which should be an integer or UInt defined by
                isa_sim_utils.
            font_size: Font size of value text.
        """
        # Element value
        self.value = value

        # Register width
        self.elem_width = width

        # Register rectangle
        self.elem_rect = Rectangle(color=color,
                                  height=1.0,
                                  width=width * get_scene_ratio(),
                                  fill_opacity=fill_opacity)

        # Value text
        self.value_text = Text(text="" if self.value is None else str(self.value),
                               color=color,
                               font_size=font_size)

        # Scale
        if self.value_text.width > self.elem_rect.width:
            value_text_scale = self.elem_rect.width / self.value_text.width
            self.value_text.scale(value_text_scale)

        super().__init__()
        self.add(self.elem_rect, self.value_text)

    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    def get_sub_elem_center(self,
                            index: int,
                            elem_width: float = -1.0) -> np.ndarray:
        """
        Return center position of specified sub-item.

        If not specified element width, return one elem as same as definition.
        Otherwise, return one element with specified width.

        Args:
            index: Index of elements.
            elem_width: Width of element in byte.
        """
        if elem_width < 0:
            elem_width = self.elem_width

        return self.elem_rect.get_right() \
            + LEFT * (index + 0.5) * elem_width * get_scene_ratio()
