"""
One dimension register element object.
"""

import numpy as np
from manim import VGroup, Rectangle, Text
from manim import LEFT
from manim import DEFAULT_FONT_SIZE
from colour import Color

class OneDimRegElem(VGroup):
    """
    Register element provides an absolute graphic object for register elements.

    Graphic object is a VGroup containing one Text objects and one Rectangle
    object.
    - Value text object presents the register value of each element.
    - Height of element rectangle object must be 1.0 while width of register
    rectangle object presents the width of element, 1.0 means 1 byte.

    Graphic object structure:
    - Value text and Element rectangle are central alignment.

    --------------------
    | Element Rectangle|
    |  --------------  |
    |  | Value Text |  |
    |  --------------  |
    |                  |
    --------------------

    Element rectangle support scale ratio on x-axis, which means the ratio of
    the width in scene to the width of register.

    Members:
        value_text: Value text object.
        reg_rect: Register rectangle object.
        ratio: scene width / register width.
        elem_width: element width.
    """

    def __init__(self,
                 color: Color,
                 width: int,
                 **kwargs):
        """
        Constructor an element.

        Args:
            color: Color of register.
            width: Width of register, in Byte

        kwargs:
            ratio: scene width / register width
            font_size: Font size of label and value text.
            value: element value.
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
        if "value" in kwargs:
            value_str = kwargs["value"]
            del kwargs["value"]
        else:
            value_str = ""

        # Register width
        self.elem_width = width

        # Register rectangle
        self.elem_rect = Rectangle(color=color,
                                  height=1.0,
                                  width=width * self.ratio,
                                  **kwargs)

        # Value text
        self.value_text = Text(text=value_str,
                               color=color,
                               font_size=font_size)

        # Scale
        if self.value_text.width > self.elem_rect.width:
            value_text_scale = self.elem_rect.width / self.value_text.width
            self.value_text.scale(value_text_scale)

        super().__init__(**kwargs)
        self.add(self.elem_rect, self.value_text)

    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    def get_elem_width(self) -> float:
        """
        Return scene width of element.
        """
        return self.elem_width * self.ratio

    def get_elem_center(self) -> np.ndarray:
        """
        return center position of register rectangle.
        """
        return self.elem_rect.get_center()

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
            + LEFT * (index + 0.5) * elem_width * self.ratio
