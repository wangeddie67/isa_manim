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
from manim import (VGroup, Rectangle, Text,
                   LEFT, RIGHT,
                   DEFAULT_FONT_SIZE)
from colour import Color
from ..isa_config import get_scene_ratio, get_config

class RegElemUnit(VGroup):
    """
    Object for register element.

    Public M-Objects:
        elem_rect: Register rectangle object.
        value_text: Value text object.

    Public attributes:
        elem_value: Value of this element, which should be Any type rather than vector.
        elem_fill_opacity: Fill opacity of this element.
        elem_font_size: Font size of value text.
        elem_value_format: Format to print data value.
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
            value: Value of this element, which should be Any type rather than vector.
            fill_opacity: Fill opacity of this element.
            font_size: Font size of value text.
            value_format: Format to print data value.
            high_bits: Specify a number of Most significant bits.
            high_zero: True means the higher part of the register is forced to zero.
        """
        self.elem_value_format: str = value_format
        self.elem_font_size: int = font_size
        self.elem_value: Any = value
        self.elem_width: int = width

        if high_bits > 0 and high_zero:
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

            # Scale text
            if self.value_text.width > self.elem_rect.width:
                value_text_scale = self.elem_rect.width / self.value_text.width
                self.value_text.scale(value_text_scale)

            super().__init__()
            self.add(self.elem_rect, self.value_text)

    # Property functions
    @property
    def elem_color(self) -> Color:
        """
        Return color of this element.
        """
        return self.elem_rect.color

    @property
    def elem_fill_opacity(self) -> float:
        """
        Return fill opacity of this element.
        """
        return self.elem_rect.fill_opacity

    # Override function
    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    def __bool__(self):
        """
        Return whether the value of element is True of False. Used by predicate mask.
        """
        return bool(self.elem_value)
