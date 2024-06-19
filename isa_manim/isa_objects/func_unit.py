"""
Function Unit.
"""

from colour import Color
from math import ceil
import numpy as np
from typing import List, Callable
from manim import (VGroup, Text, Rectangle, DashedVMobject, RoundedRectangle, LEFT, RIGHT, UP, DOWN)
from ..isa_config import get_scene_ratio

class FunctionUnit(VGroup):
    """
    Object for one function unit.

    Attributes:
        func_rect: Round rectangle of function unit.
        name_text: Text of name of function unit locating at the center of `func_rect`.
        args_rect_list: List of rectangle of source operands.
        args_text_list: List of text of name of source operands.
        res_rect_list: List of rectangle of destination operands.
        res_text_list: List of text of name of destination operands.
        func_name: Function name.
        func_color: Color of function rectangle, operand rectangles and operand name label.
        func_font_size: Font size of function rectangle.
        func_value_format: Format string for result values. Inherented by element units.
        func_callee: Pointer to function that perform the functionality of this unit.
        func_args_width_list: List of bit width of source operands.
        func_args_name_list: List of name of source operands.
        func_res_width_list: List of bit width of destination operands.
        func_res_name_list: List of name of destination operands.
        func_args_count: Number of source operands
        func_res_count: Number of destination operands.
    """

    require_serialization = True
    """
    Animation related with this object must be serialized.
    """

    def __init__(self,
                 name: str,
                 color: Color,
                 args_width_list: List[int],
                 res_width_list: List[int],
                 args_name_list: List[str],
                 res_name_list: List[str],
                 font_size: int,
                 value_format: str,
                 func_callee: Callable):
        """
        Constructor a function call.

        Args:
            name: Function name.
            color: Color of function rectangle, operand rectangles and operand name label.
            args_width_list: List of bit width of source operands.
            res_width_list: List of bit width of destination operands.
            args_name_list: List of name of source operands.
            res_name_list: List of name of destination operands.
            font_size: Font size of function rectangle.
            value_format: Format string for result values.
            func_callee: Pointer to function that perform the functionality of this unit.
        """
        # Public attributes
        self.func_name: str = name
        self.func_color: Color = color
        self.func_font_size: int = font_size
        self.func_value_format: str = value_format
        self.func_callee: Callable = func_callee
        self.func_args_width_list: List[int] = args_width_list
        self.func_args_name_list: List[str] = args_name_list
        self.func_res_width_list: List[int] = res_width_list
        self.func_res_name_list: List[str] = res_name_list
        self.func_args_count: int = len(args_width_list)
        self.func_res_count: int = len(res_width_list)

        # Arguments width
        args_scene_width = [width * get_scene_ratio() for width in args_width_list]
        all_args_width = sum(args_scene_width) + len(args_scene_width) - 1
        args_pos_list = [LEFT * (all_args_width / 2)
                            + RIGHT * (sum(args_scene_width[0:i]) + i + args_scene_width[i] / 2)
                            + UP * 2.0
                        for i in range(0, len(args_scene_width))]

        # Result width
        res_scene_width = [width * get_scene_ratio() for width in res_width_list]
        all_func_width = sum(res_scene_width) + len(res_scene_width) - 1
        res_pos_list = [LEFT * (all_func_width / 2)
                            + RIGHT * (sum(res_scene_width[0:i]) + i + res_scene_width[i] / 2)
                            + DOWN * 2.0
                        for i in range(0, len(res_scene_width))]

        # function rectangle
        ellipse_width = ceil(max(all_args_width, all_func_width))
        self.func_rect: RoundedRectangle = RoundedRectangle(corner_radius=0.25,
                                                            color=color,
                                                            height=1.0,
                                                            width=ellipse_width)

        # Label text
        self.name_text: Text = Text(name, color=color, font_size=font_size)
        # Scale
        if self.name_text.width > self.func_rect.width:
            value_text_scale = self.func_rect.width / self.name_text.width
            self.name_text.scale(value_text_scale)

        # Arguments Rectangle
        self.args_rect_list: List[Rectangle] = []
        self.args_text_list: List[Text] = []
        for arg_pos, arg_width, arg_name in zip(args_pos_list, args_width_list, args_name_list):
            arg_rect = DashedVMobject(Rectangle(color=color,
                                                height=1.0,
                                                width=arg_width * get_scene_ratio() )) \
                    .move_to(arg_pos)
            arg_text = Text(arg_name, color=color, font_size=font_size * 0.75) \
                    .move_to(arg_pos + DOWN * (0.5 + font_size / 200))

            self.args_rect_list.append(arg_rect)
            self.args_text_list.append(arg_text)

        # Result Rectangle
        self.res_rect_list: List[Rectangle] = []
        self.res_text_list: List[Text] = []
        for res_pos, res_width, res_name in zip(res_pos_list, res_width_list, res_name_list):
            res_rect = DashedVMobject(Rectangle(color=color,
                                                height=1.0,
                                                width=res_width * get_scene_ratio())) \
                    .move_to(res_pos)
            res_text = Text(res_name, color=color, font_size=font_size * 0.75) \
                    .move_to(res_pos + UP * (0.5 + font_size / 200))

            self.res_rect_list.append(res_rect)
            self.res_text_list.append(res_text)

        super().__init__()
        self.add(
            self.func_rect, self.name_text,
            *self.args_rect_list, *self.args_text_list, *self.res_rect_list, *self.res_text_list)

    # Override function
    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    # Get locations.
    def get_arg_pos(self, index: int, offset: int, elem_width: int) -> np.ndarray:
        """
        Return the center position of one specified source operand.

        `elem_width` specifies the bit width of generated element unit, which equals the bit width
        of operand in most case. It is possible that generated element unit only cover a part of the
        specified operands. 

        Args:
            index: Index of source operand.
            offset: Offset of lower bits.
            elem_width: Width of element in bits.

        Returns:
            Position of the specified source operand.
        """
        return self.args_rect_list[index].get_right()  \
            + LEFT * offset * get_scene_ratio() + LEFT * 0.5 * elem_width * get_scene_ratio()

    def get_res_pos(self, index: int, offset: int, elem_width: int) -> np.ndarray:
        """
        Return the center position of one specified destination operand.

        `elem_width` specifies the bit width of generated element unit, which equals the bit width
        of operand in most case. It is possible that generated element unit only cover a part of the
        specified operands. For example, 16-bit multiple operation generate 32-bit result.

        - The whole destination operand is accessed if `index` is 0, `offset` is 0 and
          `elem_width` is 16.
        - Lower half of the product is accessed if `index` is 0, `offset` is 0 and
          `elem_width` is 16.
        - Higher half of the product is accessed if `index` is 0, `offset` is 16 and
          `elem_width` is 16.

        Args:
            index: Index of destination operand.
            offset: Offset of lower bits.
            elem_width: Width of element in bits.


        Returns:
            Position of the specified destination operand.
        """
        return self.res_rect_list[index].get_right()  \
            + LEFT * offset * get_scene_ratio() + LEFT * 0.5 * elem_width * get_scene_ratio()

    # Untility functions for object placement.
    def get_placement_width(self) -> int:
        """
        Return the width of this object for placement. The width is ceil to an integer.

        Returns:
            The width of this object.
        """
        return ceil(self.func_rect.width)

    def get_placement_height(self) -> int:
        """
        Return the height of this object for placement. The height is ceil to an integer.

        Returns:
            The height of this object.
        """
        return 5

    def get_placement_mark(self) -> int:
        """
        Return the marker of this object for placement, which is 3.

        Returns:
            Marker of this object.
        """
        return 3

    def set_placement_corner(self, row: int, col: int):
        """
        Set the position of object by the left-up corner position. Move object to the specified
        position.

        Args:
            row: Vertical ordinate of left-up corner.
            col: Horizontal ordinate of left-up corner.
        """
        x = col + self.func_rect.width / 2
        y = row + 2.5
        self.move_to(RIGHT * x + DOWN * y)

    # Utility functions for debugging.
    def __str__(self) -> str:
        """
        Return a string for debugging.

        Returns:
            A string for debugging.
        """
        string = f"{self.func_name}(" \
            + ",".join([f"{width}b" for width in self.func_args_width_list]) + ")->(" \
            + ",".join([f"{width}b" for width in self.func_res_width_list]) + ")"
        return string

    def __repr__(self) -> str:
        """
        Return a string for debugging.

        Returns:
            A string for debugging.
        """
        string = f"{self.func_name}(" \
            + ",".join([f"{width}b" for width in self.func_args_width_list]) + ")->(" \
            + ",".join([f"{width}b" for width in self.func_res_width_list]) + ")"
        return string
