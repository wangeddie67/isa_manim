"""
Object for function call

Such object provides an absolute graphic object for function call, including pre-defined functions 
and operators.

Graphic object is a VGroup containing one Ellipse objects, several rectangle objects with dash line 
and several Text objects.
"""

from typing import List
import numpy as np
from manim import (VGroup, Ellipse, Text, Rectangle, DashedVMobject,
                   LEFT, RIGHT, UP, DOWN,
                   DEFAULT_FONT_SIZE)
from colour import Color
from ..isa_config import get_scene_ratio

class FunctionUnit(VGroup):
    """
    Object for function call.

    Attributes:
        args_width: width of arguments, in bit.
        res_width: Width of return value, in bit.
        func_ellipse: Ellipse of function.
        label_text: Text of function name/brief.
        args_rect_list: rectangle of arguments.
        args_text_list: text of arguments.
        res_rect: rectangle of return value.
    """

    require_serialization = True

    def __init__(self,
                 text: str,
                 color: Color,
                 args_width: List[int],
                 res_width: int,
                 args_value: List[str] = None,
                 font_size: int = DEFAULT_FONT_SIZE,
                 func = None):
        """
        Constructor an function call.

        Args:
            text: Register name.
            color: Color of function call.
            args_width: Width of arguments, in bit
            res_width: Width of return value, in bit
            args_value: Text of each argument.
            font_size: Font size of value text.
        """
        self.func_font_size: int = font_size
        self.func = func

        # Argument Text
        if args_value is None:
            args_value = ["" for _ in args_width]

        args_scene_width = [width * get_scene_ratio() for width in args_width]

        # function width
        func_width = sum(args_scene_width) + len(args_scene_width) - 1
        args_pos = [LEFT * (func_width / 2)
                        + RIGHT * (sum(args_scene_width[0:i]) + i + args_scene_width[i] / 2)
                        + UP * 1.5
                    for i in range(0, len(args_scene_width))]

        # function ellipse
        ellipse_width = max(func_width, res_width * get_scene_ratio())
        self.func_ellipse: Ellipse = Ellipse(color=color,
                                              height=1.0,
                                              width=ellipse_width)

        # Label text
        self.label_text: Text = Text(text=text,
                                     color=color,
                                     font_size=font_size)

        # Scale
        if self.label_text.width > self.func_ellipse.width:
            value_text_scale = self.func_ellipse.width / self.label_text.width
            self.label_text.scale(value_text_scale)

        # Arguments Rectangle
        self.args_rect_list: List[Rectangle] = []
        self.args_text_list: List[Text] = []
        for arg_pos, arg_width, arg_value in zip(args_pos, args_width, args_value):
            arg_rect = DashedVMobject(Rectangle(color=color,
                                                height=1.0,
                                                width=arg_width * get_scene_ratio() )) \
                    .move_to(arg_pos + UP * 0.5)
            arg_text = Text(text=arg_value, color=color, font_size=font_size) \
                    .move_to(arg_pos + UP * 0.5 + DOWN * (0.5 + font_size / 200))
            # Scale
            if arg_text.width > arg_rect.width:
                arg_text_scale = arg_rect.width / arg_text.width
                arg_text.scale(arg_text_scale)

            self.args_rect_list.append(arg_rect)
            self.args_text_list.append(arg_text)

        # Result Rectangle
        self.res_rect: Rectangle = DashedVMobject(Rectangle(color=color,
                                                            height=1.0,
                                                            width=res_width * get_scene_ratio())) \
                .move_to(DOWN * 2.0)

        super().__init__()
        self.add(
            self.func_ellipse, self.label_text,
            *self.args_rect_list, *self.args_text_list, self.res_rect)

    # Property functions
    @property
    def func_text(self) -> str:
        return self.label_text.text

    @property
    def func_color(self) -> Color:
        return self.func_ellipse.color

    @property
    def func_args_width(self) -> List[int]:
        return [arg_rect.width / get_scene_ratio() for arg_rect in self.args_rect_list]

    @property
    def func_res_width(self) -> int:
        return round(self.res_rect.width / get_scene_ratio())

    @property
    def func_args_value(self) -> List[str]:
        return [arg_text.text for arg_text in self.args_text_list]

    # Override function
    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    # Get locations.
    def get_args_pos(self, index: int, elem_width: float, elem_index: int) -> np.ndarray:
        """
        Return position of specified argument item.

        Args:
            index: Index of arguments.
            elem_width: Width of element.
            elem_index: Index of element.
        """
        return self.args_rect_list[index].get_right()  \
            + LEFT * (elem_index + 0.5) * elem_width * get_scene_ratio()

    def get_dst_pos(self, elem_width: float, elem_index: int) -> np.ndarray:
        """
        Return position of destination item.
        
        Args:
            elem_width: Width of element.
            elem_index: Index of element.
        """
        return self.res_rect.get_right()  \
            + LEFT * (elem_index + 0.5) * elem_width * get_scene_ratio()
