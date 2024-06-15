"""
Element Unit.
"""

from colour import Color
from math import ceil
import numpy as np
from typing import Any
from manim import (VGroup, Rectangle, Text, LEFT, RIGHT, DOWN)
from ..isa_config import get_scene_ratio

class ElemUnit(VGroup):
    """
    Object for register element.

    Attributes:
        elem_rect: Rectangle of element unit.
        value_text: Text of element value.
        elem_color: Color of element rectangle and value text.
        elem_width: Bit width of element.
        elem_value: Value of this element.
        elem_fill_opacity: Fill opacity of this element.
        elem_font_size: Font size of value text.
        elem_value_format: Format to print data value.
        elem_high_bits: Specify a number of Most significant bits.
        elem_high_zero: True means the higher part of the register is forced to zero.
    """

    require_serialization = False
    """
    Animation related with this object does not need to be serialized.
    """

    def __init__(self,
                 color: Color,
                 width: int,
                 value: Any,
                 fill_opacity: float,
                 font_size: int,
                 value_format: str,
                 high_bits: int,
                 high_zero: bool):
        """
        Constructor an element.

        Args:
            color: Color of this element.
            width: Width of this element, in bit.
            value: Value of this element, which should be Any type rather than array.
            fill_opacity: Fill opacity of this element.
            font_size: Font size of value text.
            value_format: Format to print data value.
            high_bits: Specify a number of Most significant bits.
            high_zero: True means the higher part of the register is forced to zero.
        """
        # Public attributes
        self.elem_color: Color = color
        self.elem_width: int = width
        self.elem_value: Any = value
        self.elem_fill_opacity: float = fill_opacity
        self.elem_font_size: int = font_size
        self.elem_value_format: str = value_format
        self.elem_high_bits: int = high_bits
        self.elem_high_zero: bool = high_zero

        # If some MSB bits are specified to be zero, two rectangle is used to describe one element.
        # One covers the LSB bits, while the other covers the zero MSB bits.
        if high_bits > 0 and high_zero:
            # Register rectangle
            self.elem_rect: Rectangle = Rectangle(color=color,
                                                  height=1.0,
                                                  width=width * get_scene_ratio())
            fill_elem_rect = Rectangle(color=color,
                                       height=1.0,
                                       width=(width - high_bits) * get_scene_ratio(),
                                       fill_opacity=fill_opacity)
            fill_elem_rect.move_to(self.elem_rect.get_right() + \
                                   LEFT * ((width - high_bits) * 0.5) * get_scene_ratio())

            # Value text
            self.value_text: Text = Text(self._value2str(), color=color, font_size=font_size)
            self.value_text.move_to(fill_elem_rect.get_center())

            fill_value_text = Text(text="0",
                                   color=color,
                                   font_size=font_size)
            fill_value_text.move_to(self.elem_rect.get_left() + \
                                    RIGHT * high_bits * 0.5 * get_scene_ratio())
            # Scale text
            if self.value_text.width > fill_elem_rect.width:
                value_text_scale = fill_elem_rect.width / self.value_text.width
                self.value_text.scale(value_text_scale)
            if fill_value_text.width > (self.elem_rect.width - fill_elem_rect.width):
                value_text_scale = \
                    (self.elem_rect.width - fill_elem_rect.width) / fill_value_text.width
                self.value_text.scale(value_text_scale)

            super().__init__()
            self.add(fill_elem_rect, self.value_text, self.elem_rect, fill_value_text)
        # Otherwise, one single rectangle is used to present the element.
        else:
            # Register rectangle
            self.elem_rect: Rectangle = Rectangle(color=color,
                                                  height=1.0,
                                                  width=width * get_scene_ratio(),
                                                  fill_opacity=fill_opacity)

            # Value text
            self.value_text: Text = Text(self._value2str(), color=color, font_size=font_size)
            # Scale text
            if self.value_text.width > self.elem_rect.width:
                value_text_scale = self.elem_rect.width / self.value_text.width
                self.value_text.scale(value_text_scale)

            super().__init__()
            self.add(self.elem_rect, self.value_text)

    def _value2str(self) -> str:
        """
        Convert value to string.
        """
        if self.elem_value is None:
            return ""
        elif isinstance(self.elem_value, (int, float)):
            return self.elem_value_format.format(self.elem_value)
        else:
            return str(self.elem_value)

    # Override function
    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    # Get locations.
    def get_elem_pos(self,
                     offset: int,
                     elem_width: int) -> np.ndarray:
        """
        Return the center position of another element that is right-aligned with current element.
        `offset` specifies the offset of the lowest bit.

        Args:
            offset: Offset of lower bits.
            elem_width: Width of element in bits.

        Returns:
            Position of the specified element.
        """
        # Return center position
        return self.elem_rect.get_right() \
            + LEFT * offset * get_scene_ratio() + LEFT * 0.5 * elem_width * get_scene_ratio()

    # Utility functions for object placement.
    def get_placement_width(self) -> int:
        """
        Return the width of this object for placement. The width is ceil to an integer.

        Returns:
            The width of this object.
        """
        return ceil(self.elem_rect.width)

    def get_placement_height(self) -> int:
        """
        Return the height of this object for placement. The height is ceil to an integer.

        Returns:
            The height of this object.
        """
        return 1

    def get_placement_mark(self) -> int:
        """
        Return the marker of this object, which is 2.

        Returns:
            Marker of this object.
        """
        return 2

    def set_placement_corner(self, row: int, col: int):
        """
        Set the position of object by the left-up corner position. Move object to the specified
        position.

        Args:
            row: Vertical ordinate of left-up corner.
            col: Horizontal ordinate of left-up corner.
        """
        x = col + self.get_width() / 2
        y = row + 0.5
        self.move_to(RIGHT * x + DOWN * y)

    # Utility functions for debugging.
    def __str__(self) -> str:
        if self.elem_value:
            string = f"Element_{self.elem_width}b({self._value2str()})"
        else:
            string = f"Element_{self.elem_width}b"
        return string

    def __repr__(self) -> str:
        if self.elem_value:
            string = f"Element_{self.elem_width}b({self._value2str()})"
        else:
            string = f"Element_{self.elem_width}b"
        return string
