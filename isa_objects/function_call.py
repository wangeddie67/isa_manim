"""
One dimension register object.
"""

from typing import List
import numpy as np
from manim import VGroup, Ellipse, Text, Rectangle, DashedVMobject
from manim import LEFT, RIGHT, UP, DOWN
from manim import DEFAULT_FONT_SIZE
from colour import Color
from ..isa_config import get_scene_ratio

class FunctionCall(VGroup):
    """
    Function call.

    Graphic object is a VGroup containing one Text objects and one Ellipse
    object.
    - Label text object presents the function name.
    - Height of register ellipse object must be 1.0 while width of register
    ellipse object presents the width of operands.

    Graphic object structure:
    - Label text and register ellipse are central alignment.

       --------------------
      /  Function Ellipse  \
     /    --------------    \
    |     | Label Text |     |
     \    --------------    /
      \                    /
       --------------------

    Members:
        label_text: Label text object.
        value_text_list: List of value text object.
        reg_rect: Register rectangle object.
        reg_width: register width.
        elem_width: element width.
        elements: number of element.
    """

    require_serialization = True

    def __init__(self,
                 text: str,
                 color: Color,
                 args_width: List[float],
                 res_width: float,
                 **kwargs):
        """
        Constructor an function call.

        Args:
            text: Register name.
            color: Color of register.
            width: Width of register, in Byte
            elements: Number of elements.

        kwargs:
            label_pos: Label position related to the center of elem_width.
            font_size: Font size of label and value text.
        """
        # Font size
        if "font_size" in kwargs:
            font_size = kwargs["font_size"]
            del kwargs["font_size"]
        else:
            font_size = DEFAULT_FONT_SIZE

        # Argument Text
        if "args_value" in kwargs:
            args_value = kwargs["args_value"]
            del kwargs["args_value"]
        else:
            args_value = ["" for _ in range(0, args_width)]

        args_scene_width = [width * get_scene_ratio() for width in args_width]

        # function width
        self.func_width = sum(args_scene_width) + len(args_scene_width) - 1
        self.func_height = 4
        self.args_pos = [LEFT * (self.func_width / 2)
                            + RIGHT * (sum(args_scene_width[0:i]) + i + args_scene_width[i] / 2)
                            + UP * 1.5
                         for i in range(0, len(args_scene_width))]
        self.dst_pos = DOWN * 1.5

        # function ellipse
        self.func_ellipse = Ellipse(color=color,
                                    height=1.0,
                                    width=self.func_width,
                                    **kwargs)

        # Label text
        self.label_text = Text(text=text,
                               color=color,
                               font_size=font_size)

        # Scale
        if self.label_text.width > self.func_ellipse.width:
            value_text_scale = self.func_ellipse.width / self.label_text.width
            self.label_text.scale(value_text_scale)

        # Arguments Rectangle
        self.args_rect = []
        self.args_text = []
        for arg_pos, arg_width, arg_value in zip(self.args_pos, args_width, args_value):
            arg_rect = DashedVMobject(Rectangle(color=color,
                                                height=1.0,
                                                width=arg_width * get_scene_ratio() )) \
                    .move_to(arg_pos + UP * 0.5)
            arg_text = Text(text=arg_value, color=color, font_size=font_size) \
                    .move_to(arg_pos + UP * 0.5)
            # Scale
            if arg_text.width > arg_rect.width:
                arg_text_scale = arg_rect.width / arg_text.width
                arg_text.scale(arg_text_scale)

            self.args_rect.append(arg_rect)
            self.args_text.append(arg_text)

        # Result Rectangle
        self.args_rect.append(
            DashedVMobject(Rectangle(color=color,
                                     height=1.0,
                                     width=res_width * get_scene_ratio())) \
                .move_to(self.dst_pos + DOWN * 0.5)
        )

        super().__init__(**kwargs)
        self.add(self.func_ellipse, self.label_text, *self.args_rect, *self.args_text)

    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    def get_func_width(self) -> float:
        """
        Return scene width of register.
        """
        return self.func_width * get_scene_ratio()

    def get_max_boundary_width(self) -> float:
        """
        Return maximum scene width (left or right).
        """
        return self.func_ellipse.width / 2

    def get_func_center(self) -> np.ndarray:
        """
        return center position of register rectangle.
        """
        return self.func_ellipse.get_center()

    def get_args_pos(self,
                     index: int,
                     arg_height: float = 1.0) -> np.ndarray:
        """
        Return center position of specified argument item.

        Args:
            index: Index of elements.
            arg_height: Height of source arguments.
        """
        return self.get_func_center() \
            + self.args_pos[index] + UP * arg_height / 2

    def get_dst_pos(self,
                    dst_height: float = 1.0) -> np.ndarray:
        """
        Return center position of destination item.

        Args:
            dst_height: Height of destination argument.
        """
        return self.get_func_center() \
            + self.dst_pos + DOWN * dst_height / 2
