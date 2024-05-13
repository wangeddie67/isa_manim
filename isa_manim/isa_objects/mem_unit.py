"""
Memory Unit.
"""

from colour import Color
from math import ceil
import numpy as np
from typing import List, Tuple
from manim import (VGroup, Text, Rectangle, DashedVMobject, RoundedRectangle, Triangle,
                   CubicBezier,
                   LEFT, RIGHT, UP, DOWN, DEGREES)
from ..isa_config import get_scene_ratio, get_config

class MemoryUnit(VGroup):
    """
    Object for memory unit.

    Attributes:
        mem_rect: Round rectangle of memory unit.
        name_text: Name of memory unit.
        addr_rect: Rectangle of address operand.
        data_rect: Rectangle of data operand.
        mem_map_list: List of rectangles of memory map ranges.
        mem_map_text: List of text of memory map ranges. Each item in the list is a pair of loweset
            and highest address.
        mem_mark_list: List of memory marks.
        mem_map_left_brace: Left brace of memory map.
        mem_map_right_brace: Right brace of memory map. 
        mem_color: Color of memory unit.
        mem_addr_width: Bit width of address operand.
        mem_data_width: Bit width of data operand.
        mem_addr_align: Align requirement of address.
        mem_font_size: Font size of name text.
        mem_value_format: Format string for data values. Inherented by element units.
        mem_range: List of memory range.
        mem_map_width: Width of memory map rectangle.
    """

    require_serialization = True

    def __init__(self,
                 color: Color,
                 addr_width: int,
                 data_width: int,
                 addr_align: int,
                 mem_range: List[Tuple[int,int]],
                 font_size: int,
                 value_format: str,
                 para_enable: bool,
                 status_width: int,
                 mem_map_width: int):
        """
        Constructor an function call.

        Args:
            color: Color of memory unit.
            addr_width: Width of address, in bit
            data_width: Width of data, in bit
            addr_align: Alignment of memory range address.
            mem_range: List of memory range, each item is a pair of lowest address and highest
                address.
            font_size: Font size of memory name.
            value_format: Format string for result values. Inherented by element units.
            para_enable: Whether the animation related to this memory unit can perform parallel or
                not.
            mem_map_width: Hint for width of memory map width.
        """
        self.require_serialization = not para_enable

        # Public attributes
        self.mem_color: Color = color
        self.mem_addr_width: int = addr_width
        self.mem_data_width: int = data_width
        self.mem_addr_align: int = addr_align
        self.mem_font_size: int = font_size
        self.mem_value_format: int = value_format
        self.mem_status_width: int = status_width
        # check alignment of memory map
        self.mem_range: List[Tuple[int, int]] = []
        for laddr, raddr in mem_range:
            laddr = (laddr // addr_align) * addr_align
            if raddr % addr_align > 0:
                raddr = ((raddr // addr_align) + 1) * addr_align
            self.mem_range.append([laddr, raddr])
        # 6 is width of mem_rect (4) + width of splitter (1 * 2).
        if data_width < addr_width:
            self.mem_map_width: int = max((addr_width + addr_width) * get_scene_ratio() + 6,
                                          mem_map_width)
        else:
            self.mem_map_width: int = max((addr_width + data_width) * get_scene_ratio() + 6,
                                          mem_map_width)

        # memory rectangle
        self.mem_rect: RoundedRectangle = RoundedRectangle(color=color, height=3.0, width=4)

        # Label text
        self.name_text: Text = Text("Mem", color=color, font_size=font_size)
        if status_width > 0:
            self.name_text.move_to(self.mem_rect.get_center() + UP * 0.75)
        else:
            self.name_text.move_to(self.mem_rect.get_center())

        # status rectangle
        if status_width > 0:
            self.status_rect: Rectangle = DashedVMobject(
                Rectangle(color=color, height=1.0, width=status_width * get_scene_ratio()))
            self.status_rect.move_to(self.mem_rect.get_center() + DOWN * 0.5)
        else:
            self.status_rect = None

        # Address rectangle
        self.addr_rect: Rectangle = DashedVMobject(
            Rectangle(color=color, height=1.0, width=addr_width * get_scene_ratio()))
        self.addr_rect.shift(LEFT * (1 + self.mem_rect.width / 2 + self.addr_rect.width / 2))
        self.addr_label_text = Text(text="Addr", color=color, font_size=font_size) \
            .move_to(self.addr_rect.get_center() + UP)

        # Data rectangle
        self.data_rect: Rectangle = DashedVMobject(
            Rectangle(color=color, height=1.0, width=data_width * get_scene_ratio()))
        self.data_rect.shift(RIGHT * (1 + self.mem_rect.width / 2 + self.data_rect.width / 2))
        self.data_label_text = Text(text="Data", color=color, font_size=font_size) \
            .move_to(self.data_rect.get_center() + UP)

        # Memory map
        self.mem_map_list: List[Rectangle] = []
        self.mem_map_text: List[Tuple[Text, Text]] = []
        self.mem_mark_list : List[Rectangle] = []
        mem_map_idx = 0
        for laddr, raddr in self.mem_range:
            mem_map_rect = Rectangle(color=color, height=1.0, width=self.mem_map_width)
            mem_map_rect.shift(self.addr_rect.get_left() - mem_map_rect.get_left())
            mem_map_rect.shift(DOWN * (3 + 2 * mem_map_idx))

            left_text = Text(hex(raddr), font_size=font_size * 0.75)
            right_text = Text(hex(laddr), font_size=font_size * 0.75)
            left_text.move_to(mem_map_rect.get_left() + DOWN * 1)
            right_text.move_to(mem_map_rect.get_right() + DOWN * 1)

            self.mem_map_list.append(mem_map_rect)
            self.mem_map_text.extend([left_text, right_text])
            mem_map_idx += 1

        # Brace
        self.mem_map_left_brace: CubicBezier = CubicBezier(
            self.mem_map_list[0].get_left() + UP * 0.7,
            self.mem_map_list[0].get_left() + UP * 1.25,
            self.mem_rect.get_left() + DOWN * 2.25,
            self.mem_rect.get_left() + DOWN * 1.5)
        self.mem_map_right_brace: CubicBezier = CubicBezier(
            self.mem_map_list[0].get_right() + UP * 0.7,
            self.mem_map_list[0].get_right() + UP * 1.25,
            self.mem_rect.get_right() + DOWN * 2.25,
            self.mem_rect.get_right() + DOWN * 1.5)

        super().__init__()
        self.add(self.mem_rect, self.name_text,
                 self.addr_rect, self.addr_label_text, self.data_rect, self.data_label_text,
                 *self.mem_map_list, *self.mem_map_text,
                 self.mem_map_left_brace, self.mem_map_right_brace)
        if self.status_rect:
            self.add(self.status_rect)

    # Override function
    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    # Get locations.
    def get_addr_pos(self, width: int) -> np.ndarray:
        """
        Return center position of address port.

        Args:
            width: Bit width of address.
        """
        return self.addr_rect.get_right() + LEFT * width * get_scene_ratio() / 2

    def get_data_pos(self, width: int) -> np.ndarray:
        """
        Return center position of data port.

        Args:
            width: Bit width of data.
        """
        return self.data_rect.get_right() + LEFT * width * get_scene_ratio() / 2

    def get_status_pos(self, width: int) -> np.ndarray:
        """
        Return center position of status port.

        Args:
            width: Bit width of status.
        """
        return self.status_rect.get_right() + LEFT * width * get_scene_ratio() / 2

    def has_status_port(self) -> bool:
        """
        Return whether the memory unit has status port.

        Returns:
            Return true if the memory unit has status port
        """
        return self.status_rect != None

    def _index_of_mem_range(self, addr: int) -> int:
        """
        Check whether given address is covered in memory map ranges, and return the index of matched
        memory map range.
        
        Args:
            addr: Address to check.

        Returns:
            If the specified address is covered in one memory map range, return the index of matched
            memory map range. Otherwise, return -1.
        """
        idx = 0
        for laddr, raddr in self.mem_range:
            if laddr <= addr < raddr:
                return idx
            else:
                idx = idx + 1

        return -1

    def is_mem_range_cover(self, addr: int) -> bool:
        """
        Check whether given address is covered in memory map ranges.
        
        Args:
            addr: Address to check.

        Returns:
            If the specified address is covered in memory map ranges, return True.
                Otherwise, return False.
        """
        return self._index_of_mem_range(addr) >= 0

    def get_addr_mark(self, addr: int, color: Color) -> Triangle:
        """
        Create an triangle to point the specified address in memory map rectangle.
        
        Args:
            addr: The specified address.
            color: Color of address mark.

        Returns:
            Triangle object of address mark.
        """
        # Calculate scale factor of memory map rectangle
        mem_range_idx = self._index_of_mem_range(addr)
        mem_range_rect = self.mem_map_list[mem_range_idx]
        scale_factor = mem_range_rect.width / \
            (self.mem_range[mem_range_idx][1] - self.mem_range[mem_range_idx][0])

        # Calculate address position.
        addr_offset = addr - self.mem_range[mem_range_idx][0] + 0.5
        addr_pos = mem_range_rect.get_right() - (addr_offset * scale_factor) * RIGHT + UP * 0.6

        # Create address mark and move to position.
        addr_mark = Triangle(color=color).scale(0.2).rotate(60 * DEGREES).move_to(addr_pos)

        return addr_mark

    def get_rd_mem_mark(self, laddr: int, raddr: int, color: Color) -> Rectangle:
        """
        Create one rectangle to cover the memory range specified by `[laddr, raddr)` in memory map
        rectangle.

        The height of the memory mark is 0.34 (1/3 of the height of memory map rectangle). 
        
        Args:
            laddr: Minimum address of memory range.
            raddr: Maximum address of memory range.
            color: Color of address mark.

        Returns:
            Rectangle object of memory mark.
        """
        # Calculate scale factor of memory map rectangle
        mem_range_idx = self._index_of_mem_range(laddr)
        mem_range_rect = self.mem_map_list[mem_range_idx]
        scale_factor = mem_range_rect.width / \
            (self.mem_range[mem_range_idx][1] - self.mem_range[mem_range_idx][0])

        # Calculate mark position.
        laddr_offset = laddr - self.mem_range[mem_range_idx][0]
        addr_range = min(raddr, self.mem_range[mem_range_idx][1]) - laddr
        mem_mark_pos = mem_range_rect.get_right() \
            - ((laddr_offset + addr_range / 2) * scale_factor) * RIGHT + 0.33 * UP

        # Create memory mark and move to position.
        mem_mark = Rectangle(color=color,
                             height=0.34,
                             width=addr_range * scale_factor,
                             fill_opacity=0.25).move_to(mem_mark_pos)

        return mem_mark

    def get_wt_mem_mark(self, laddr: int, raddr: int, color: Color) -> Rectangle:
        """
        Create one rectangle to cover the memory range specified by `[laddr, raddr)` in memory map
        rectangle.

        The height of the memory mark is 0.66 (2/3 of the height of memory map rectangle). 
        
        Args:
            laddr: Minimum address of memory range.
            raddr: Maximum address of memory range.
            color: Color of address mark.

        Returns:
            Rectangle object of memory mark.
        """
        # Calculate scale factor of memory map rectangle
        mem_range_idx = self._index_of_mem_range(laddr)
        mem_range_rect = self.mem_map_list[mem_range_idx]
        scale_factor = mem_range_rect.width / \
            (self.mem_range[mem_range_idx][1] - self.mem_range[mem_range_idx][0])

        # Calculate mark position.
        laddr_offset = laddr - self.mem_range[mem_range_idx][0]
        addr_range = min(raddr, self.mem_range[mem_range_idx][1]) - laddr
        mem_mark_pos = mem_range_rect.get_right() \
            - ((laddr_offset + addr_range / 2) * scale_factor) * RIGHT + 0.17 * DOWN

        # Create memory mark and move to position.
        mem_mark = Rectangle(color=color,
                             height=0.66,
                             width=addr_range * scale_factor,
                             fill_opacity=get_config("elem_fill_opacity")).move_to(mem_mark_pos)

        return mem_mark

    def get_mem_mark_list(self) -> List[Rectangle]:
        """
        Return the list of memory marks.

        Returns:
            The list of memory marks.
        """
        return self.mem_mark_list

    def append_mem_mark_list(self, mark: Rectangle):
        """
        Append one mark to memory mark list.
        
        Args:
            mark: Memory mark to append.
        """
        self.mem_mark_list.append(mark)

    # Untility functions for object placement.
    def get_placement_width(self) -> int:
        """
        Return the width of this object for placement. The width is ceil to an integer.

        Returns:
            The width of this object.
        """
        return ceil(self.mem_map_width + 2)

    def get_placement_height(self) -> int:
        """
        Return the height of this object for placement. The height is ceil to an integer.

        Returns:
            The height of this object.
        """
        return 4 + 2 * len(self.mem_map_list)

    def get_placement_mark(self) -> int:
        """
        Return the marker of this object for placement, which is 4.

        Returns:
            Marker of this object.
        """
        return 4

    def set_placement_corner(self, row: int, col: int):
        """
        Set the position of object by the left-up corner position. Move object to the specified
        position.

        Args:
            row: Vertical ordinate of left-up corner.
            col: Horizontal ordinate of left-up corner.
        """
        x = col + 1 + self.addr_rect.width + 1 + self.mem_rect.width / 2
        y = row + 1.5
        self.shift(RIGHT * x + DOWN * y - self.mem_rect.get_center())

    # Utility functions for debugging.
    def __str__(self) -> str:
        string = f"Memory_{self.mem_addr_width}b_{self.mem_data_width}b"
        return string

    def __repr__(self) -> str:
        string = f"Memory_{self.mem_addr_width}b_{self.mem_data_width}b"
        return string
