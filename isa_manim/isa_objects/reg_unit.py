"""
Register Unit.
"""

from colour import Color
from math import ceil
import numpy as np
from typing import Any, List, Tuple, Union
from manim import (VGroup, Rectangle, Text, LEFT, RIGHT, DOWN, UP)
from ..isa_config import get_scene_ratio

class RegUnit(VGroup):
    """
    Object for one register.

    Attributes:
        name_text_list: List of label text objects.
        reg_rect: List of register rectangle objects.
        reg_name_list: List of register names.
        reg_color: Color of register rectangle and labels.
        reg_font_size: Font size of register labels.
        reg_value_format: Format string for output values. Inherented by element units.
        reg_value: Register value. Inherented by element units.
        reg_width: Bit width of register.
        reg_count: Number of registers, or row count of matrix registers.
        elem_count: Number of elements.
        elem_width: Bit width of elements.
    """

    require_serialization = False
    """
    Animation related with this object does not need to be serialized.
    """

    def __init__(self,
                 name_list: List[str],
                 color: Color,
                 width: int,
                 elements: int,
                 nreg: int,
                 value: Union[Any, List[Any], List[List[Any]], None],
                 font_size: int,
                 value_format: str
                 ):
        """
        Constructor a register.

        - When construct a scalar register, `elements` is 1 and `nreg` is 1.
        - When construct a vector register, `elements` is the number of elements, and `nreg` is 1.
        - When construct a matrix register or a list of registers, `elements` is the number of
          elements and `nreg` is the number of registers or the row count of matrix registers.

        Args:
            name_list: Register names which could be a string or a list of string.
            color: Color of register and label.
            width: Width of register, in bits.
            elements: Number of elements in one register.
            nreg: Number of registers, used to create matrix registers or a list of registers.
            value: Value of this element. None is provided if not necessary.
            font_size: Font size of label.
            value_format: Format string for output values. Inherented by element units.
        """
        # Public attributes
        self.reg_name_list: List[str] = name_list
        self.reg_color: Color = color
        self.reg_font_size: int = font_size
        self.reg_value_format: str = value_format
        self.reg_value: Union[Any, List[Any], List[List[Any]], None] = value
        self.reg_width: int = width
        self.reg_count: int = nreg
        self.elem_count: int = elements
        self.elem_width: int = width // elements

        # Register rectangle
        self.reg_rect: Rectangle = Rectangle(color=color,
                                             height=nreg,
                                             width=width * get_scene_ratio(),
                                             grid_xstep=self.elem_width * get_scene_ratio(),
                                             grid_ystep=1.0,
                                             ).shift(DOWN * nreg / 2.0 + UP * 0.5)

        # Name label texts
        reg_rect_corner = self.reg_rect.get_corner(UP + LEFT)
        self.name_text_list: List[Text] = []
        for i in range(0, len(name_list)):
            name_text = Text(name_list[i], color=color, font_size=font_size)
            label_pos = reg_rect_corner + name_text.get_left() + 0.2 * LEFT + (i + 0.5) * DOWN
            name_text.move_to(label_pos)
            self.name_text_list.append(name_text)

        super().__init__()
        self.add(self.reg_rect, *self.name_text_list)

    # Override function
    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    # Regular index
    def _regular_index(self, index: int, reg_idx: int) -> Tuple[int, int]:
        """
        Regular element index and register index.

        If `index` or `reg_idx` beyond the scope of the register, this function returns the index
        pointint to one valid element as below:

        - The actual index to access element is `index % elem_count`
        - The actual row index to access element is `(reg_idx + index // elem_count) % reg_count`. 

        Args:
            index: Index of elements.
            reg_idx: Index of register.

        Returns:
            Tuple[int, int]: element index and register index after regulation.
        """
        actual_index = index % self.elem_count
        actual_reg_index = (reg_idx + index // self.elem_count) % self.reg_count
        return actual_index, actual_reg_index

    # Get locations.
    def get_elem_pos(self,
                     index: int,
                     reg_idx: int,
                     offset: int,
                     elem_width: int) -> np.ndarray:
        """
        Return the center position of one specified element.

        The element is specified by `index` and `reg_idx`. In general, `index` and `reg_idx` should
        within the scope of the register. If `index` or `reg_idx` beyond the scope of the register,
        this function returns one element specified as below:

        - The actual index to access element is `index % elem_count`
        - The actual row index to access element is `(reg_idx + index // elem_count) % reg_count`. 

        The width to index elements is determined by the construtor function. However, it is not
        possible to operate on only a part of the element. For example, one 128 bit vector has
        eight 16-bit elements.

        - The 4-th element [79:64] is accessed if `index` is 4, `offset` is 0 and
          `elem_width` is 16.
        - Lower half of the 4-th element [71:64] is accessed if `index` is 4, `offset` is 0 and
          `elem_width` is 8.
        - Higher half of the 4-th element [79:72] is accessed if `index` is 4, `offset` is 8 and
          `elem_width` is 8.

        Args:
            index: Index of elements.
            reg_idx: Index of register.
            offset: Offset of lower bits.
            elem_width: Width of element in bits.

        Returns:
            Position of the specified element.
        """
        # Regular index
        index, reg_idx = self._regular_index(index, reg_idx)

        # Return center position
        return self.reg_rect.get_corner(UP + RIGHT) + (reg_idx + 0.5) * DOWN \
            + LEFT * index * self.elem_width * get_scene_ratio() + \
            + LEFT * offset * get_scene_ratio() + LEFT * 0.5 * elem_width * get_scene_ratio()

    # Get element value
    def get_elem_value(self,
                       index: int,
                       reg_idx: int) -> Union[Any, List[Any], List[List[Any]], None]:
        """
        Return the value of one specified element. Return None if the value of this register is not
        specified in the constructor function.

        - Return `self.elem_value` for scalar registers.
        - Return `self.elem_value[index]` for vector registers.
        - Return `self.elem_value[reg_idx][index]` for a list of registers or matrix registers.

        The element is specified by `index` and `reg_idx`. In general, `index` and `reg_idx` should
        within the scope of the register. If `index` or `reg_idx` beyond the scope of the register,
        this function returns one element specified as below:

        - The actual index to access element is `index % elem_count`
        - The actual row index to access element is `(reg_idx + index // elem_count) % reg_count`. 

        Args:
            index: Index of elements.
            reg_idx: Index of register.

        Returns:
            Value of the specified element.
        """
        # If the value is not specified, return None.
        if self.reg_value is None:
            return None

        # Regular index.
        index, reg_idx = self._regular_index(index, reg_idx)

        if isinstance(self.reg_value, list):
            # For matrix registers, return value[reg_idx][index]
            if isinstance(self.reg_value[0], list):
                return self.reg_value[reg_idx][index]
            # For vector registers, return value[index]
            else:
                return self.reg_value[index]
        # For scalar registers, return value.
        else:
            return self.reg_value

    # Get element value
    def set_elem_value(self,
                       value: Any,
                       index: int,
                       reg_idx: int):
        """
        Modify the value of one specified element.

        - Modify `self.elem_value` for scalar registers.
        - Modify `self.elem_value[index]` for vector registers.
        - Modify `self.elem_value[reg_idx][index]` for a list of registers or matrix registers.

        The element is specified by `index` and `reg_idx`. In general, `index` and `reg_idx` should
        within the scope of the register. If `index` or `reg_idx` beyond the scope of the register,
        this function returns one element specified as below:

        - The actual index to access element is `index % elem_count`
        - The actual row index to access element is `(reg_idx + index // elem_count) % reg_count`. 

        If the value of this register is not specified in the constructor function
        (`self.elem_value` is None), and this register is one vector register, matrix register, or a
        group of registers, one 1-D/2-D array of values is created with None elements.

        Args:
            index: Index of elements.
            reg_idx: Index of register.
            value: Value of this element.
        """
        # Create array of value for vector/matrix register.
        if self.reg_value is None:
            # Create 1-D array for a vector register.
            if self.reg_count == 1:
                if self.elem_count > 1:
                    self.reg_value = [None for _ in range(0, self.elem_count)]
            # Create 2-D array for a matrix register or a list of registers.
            else:
                self.reg_value = \
                    [[None for _ in range(0, self.elem_count)] for _ in range(0, self.reg_count)]

        # Regular index.
        index, reg_idx = self._regular_index(index, reg_idx)

        if isinstance(self.reg_value, list):
            # For matrix registers, set value[reg_idx][index]
            if isinstance(self.reg_value[0], list):
                self.reg_value[reg_idx][index] = value
            # For vector registers, set value[index]
            else:
                self.reg_value[index] = value
        # For scalar registers, set value.
        else:
            self.reg_value = value

    # Untility functions for object placement.
    def get_placement_width(self) -> int:
        """
        Return the width of this object for placement. The width is ceil to an integer.

        Returns:
            The width of this object.
        """
        label_text_width = max(item.width for item in self.name_text_list)
        # If element is not aligned by the Y-axis (X=0), the width provided by Mobject is not
        # correct.
        reg_rect_width = self.reg_width * get_scene_ratio()
        if label_text_width < 2:
            return ceil(2 + reg_rect_width)
        else:
            return ceil(label_text_width + reg_rect_width)

    def get_placement_height(self) -> int:
        """
        Return the height of this object for placement. The height is ceil to an integer.

        Returns:
            The height of this object.
        """
        return int(self.reg_count)

    def get_placement_mark(self) -> int:
        """
        Return the marker of this object for placement, which is 2.

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
        x = col + self.get_placement_width() - self.reg_width * get_scene_ratio()
        y = row
        self.shift(RIGHT * x + DOWN * y - self.reg_rect.get_corner(UP + LEFT))

    # Utility functions for debugging.
    def __str__(self) -> str:
        string = f"{self.reg_name_list}({self.reg_width}b,{self.elem_count},{self.reg_count})"
        return string

    def __repr__(self) -> str:
        string = f"{self.reg_name_list}({self.reg_width}b,{self.elem_count},{self.reg_count})"
        return string
