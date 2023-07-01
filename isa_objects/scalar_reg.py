"""
Scalar register.
"""

import numpy as np
from manim import VGroup, Rectangle, Text
from manim import LEFT
from manim import DEFAULT_FONT_SIZE
from colour import Color

class ScalarReg(VGroup):
    """
    Scalar register (General-purpose/Predicated as counter/)
    """

    def __init__(self,
                 text: str,
                 color: Color,
                 elem_width: int,
                 **kwargs):
        """
        Constructor an vector register.

        Args:
            label: Register name.
            elements: Number of elements.
            elem_width: Width of elements, in Byte

        kwargs:
            ratio: scene axis width / (elements * elem_width)
            label_pos: Label position related to the center of elem_width.
        """
        self.ratio = 1.0
        if "ratio" in kwargs:
            self.ratio = kwargs["ratio"]
            del kwargs["ratio"]
        self.elem_width = elem_width

        # Register rectangle
        self.reg_rect = Rectangle(color=color,
                                  height=1.0,
                                  width=elem_width * self.ratio,
                                  grid_xstep=elem_width * self.ratio)
        # Register name.
        self.reg_label = Text(text=text, color=color,
                              font_size=kwargs.get("font_size", DEFAULT_FONT_SIZE))
        if "label_pos" in kwargs:
            self.reg_label.move_to(kwargs["label_pos"])
        else:
            self.reg_label.move_to(
                self.reg_rect.get_left() + self.reg_label.get_left() + LEFT * 0.2)

        self.elem_labels = []
        if "value" in kwargs:
            elem_label = Text(text=kwargs["value"], color=color,
                              font_size=kwargs.get("font_size", DEFAULT_FONT_SIZE)) \
                .move_to(self.reg_rect.get_center())
            self.elem_labels.append(elem_label)
            del kwargs["value"]

        if "font_size" in kwargs:
            del kwargs["font_size"]

        super().__init__(**kwargs)
        self.add(self.reg_rect, self.reg_label, *self.elem_labels)

    def get_reg_width(self) -> float:
        """
        Return width of register.
        """
        return self.elem_width * self.ratio

    def get_left_boundary_width(self) -> float:
        """
        Return width of left boundary.
        """
        return self.elem_width * self.ratio / 2 + self.reg_label.width

    def get_reg_center(self) -> np.ndarray:
        """
        return center of register
        """
        return self.reg_rect.get_center()


    def get_elem(self,
                 color: Color) -> Rectangle:
        """
        Return a rectangle of specified item.
        """
        return Rectangle(color=color,
                         height=1.0,
                         width=self.elem_width * self.ratio,
                         fill_opacity=0.5) \
            .move_to(self.reg_rect.get_center())
