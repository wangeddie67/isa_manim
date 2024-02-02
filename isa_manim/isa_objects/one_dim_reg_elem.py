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

from typing import Any
import numpy as np
from manim import (VGroup, Rectangle, Text, Line,
                   LEFT, RIGHT, UP,
                   DEFAULT_FONT_SIZE)
from colour import Color
from ..isa_config import get_scene_ratio, get_config

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
                 value: Any = None,
                 fill_opacity: float = 0.5,
                 font_size: int = DEFAULT_FONT_SIZE,
                 value_format: str = get_config("elem_value_format"),
                 high_bits: int = 0,
                 high_zero: bool = False):
        """
        Constructor an element.

        Args:
            color: Color of register.
            width: Width of register, in bit.
            value: Value of this register, which should be an integer or UInt defined by
                isa_sim_utils.
            font_size: Font size of value text.
        """
        self.elem_value_format: str = value_format
        self.elem_font_size: int = font_size
        self.elem_value: Any = value

        if high_bits == 0:
            # Register rectangle
            self.elem_rect = Rectangle(color=color,
                                       height=1.0,
                                       width=width * get_scene_ratio(),
                                       fill_opacity=fill_opacity)

            # Value text
            if value is None:
                value_str = ""
            elif isinstance(value, (int, float)):
                value_str = value_format.format(value)
            else:
                value_str = str(value)
            self.value_text = Text(text=value_str,
                                color=color,
                                font_size=font_size)

            # Scale
            if self.value_text.width > self.elem_rect.width:
                value_text_scale = self.elem_rect.width / self.value_text.width
                self.value_text.scale(value_text_scale)

            super().__init__()
            self.add(self.elem_rect, self.value_text)
        elif high_zero:
            # Register rectangle
            self.elem_rect = Rectangle(color=color,
                                       height=1.0,
                                       width=width * get_scene_ratio())
            fill_elem_rect = Rectangle(color=color,
                                       height=1.0,
                                       width=(width - high_bits) * get_scene_ratio(),
                                       fill_opacity=fill_opacity)
            fill_elem_rect.move_to(self.elem_rect.get_right() + \
                                   LEFT * ((width - high_bits) * 0.5) * get_scene_ratio())

            # Value text
            if value is None:
                value_str = ""
            elif isinstance(value, (int, float)):
                value_str = value_format.format(value)
            else:
                value_str = str(value)
            self.value_text = Text(text=value_str,
                                   color=color,
                                   font_size=font_size)
            self.value_text.move_to(fill_elem_rect.get_center())

            fill_value_text = Text(text="0",
                                   color=color,
                                   font_size=font_size)
            fill_value_text.move_to(self.elem_rect.get_left() + \
                                    RIGHT * high_bits * 0.5 * get_scene_ratio())

            # Scale
            if self.value_text.width > fill_elem_rect.width:
                value_text_scale = fill_elem_rect.width / self.value_text.width
                self.value_text.scale(value_text_scale)
            if fill_value_text.width > (self.elem_rect.width - fill_elem_rect.width):
                value_text_scale = \
                    (self.elem_rect.width - fill_elem_rect.width) / fill_value_text.width
                self.value_text.scale(value_text_scale)

            super().__init__()
            self.add(fill_elem_rect, self.value_text, self.elem_rect, fill_value_text)
        else:
            # Register rectangle
            self.elem_rect = Rectangle(color=color,
                                       height=1.0,
                                       width=width * get_scene_ratio(),
                                       fill_opacity=fill_opacity)

            # Value text
            if value is None:
                value_str = ""
            elif isinstance(value, (int, float)):
                value_str = value_format.format(value)
            else:
                value_str = str(value)
            self.value_text = Text(text=value_str,
                                color=color,
                                font_size=font_size)

            # Scale
            if self.value_text.width > self.elem_rect.width:
                value_text_scale = self.elem_rect.width / self.value_text.width
                self.value_text.scale(value_text_scale)

            # Split line
            Line(self.elem_rect.get_left() + RIGHT * high_bits + UP * 0.5,
                 self.elem_rect.get_left() + RIGHT * high_bits + UP * 0.5,
                 color=color)

            super().__init__()
            self.add(self.elem_rect, self.value_text)

    # Property functions
    @property
    def elem_color(self) -> Color:
        return self.elem_rect.color

    @property
    def elem_width(self) -> int:
        return int(self.elem_rect.width / get_scene_ratio())

    @property
    def elem_fill_opacity(self) -> float:
        return self.elem_rect.fill_opacity

    # Override function
    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    # Get locations.
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
