"""
Object for memory map

Such object provides an absolute graphic object for memory map, marking the range of data access.

Graphic object is a VGroup containing several Rectangle objects and several Text objects.
"""

from typing import List, Tuple
from typing_extensions import Self
from math import ceil
from manim import (VGroup, Text, Rectangle, Triangle,
                   RIGHT, UP, DOWN, DEGREES,
                   DEFAULT_FONT_SIZE)
from colour import Color

class MemoryMap(VGroup):
    """
    Object for memory map.

    Attributes:
        mem_map_rect: rectangle of memory map.
        mem_map_color: color of memory map.
        rd_rect_color: color of read range.
        wr_rect_color: color of write range.
        align: align requirement of address range of memory map.
        left_addr: Low address of memory map, inclusive.
        right_addr: High address of memory map, exclusive.
        rd_range: read access range, list of pair of left/right address.
        wr_range: write access range, list of pair of left/right address.
        left_text: Text of left address.
        right_text: Text of right address.
        write_rect: Rectangle of write accessed range.
        read_rect: rectangle of read accessed range.
    """

    require_serialization = False

    def __init__(self,
                 color: Color,
                 rd_color: Color,
                 wr_color: Color,
                 width: float,
                 align: int = 16,
                 left_addr: int = 0,
                 right_addr: int = 0,
                 rd_range: List[Tuple[int]] = None,
                 wr_range: List[Tuple[int]] = None,
                 font_size = DEFAULT_FONT_SIZE):
        """
        Constructor a memory map.

        Args:
            color: Color of function call.
            rd_color: Color of read address range.
            wr_color: Color of write address range.
            width: Scene width of memory map (not byte).
            align: Align requirement of memory map.
            left_addr: Left address of memory map.
            right_addr: Right address of memory map.
            rd_range: Memory range accessed by read.
            wr_range: Memory range accessed by write.
            font_size: Font size of value text.
        """
        self.mem_map_rect = Rectangle(color=color, height=1.0, width=width)

        self.mem_map_color = color
        self.rd_rect_color = rd_color
        self.wr_rect_color = wr_color

        self.align = align

        self.rd_range = [] if rd_range is None else rd_range
        self.wr_range = [] if wr_range is None else wr_range

        self.left_addr, self.right_addr = self._adjust_range(
            align, left_addr, right_addr, self.rd_range + self.wr_range)

        self.left_text = Text(hex(self.left_addr), font_size=font_size)
        self.right_text = Text(hex(self.right_addr), font_size=font_size)
        self.left_text.move_to(self.mem_map_rect.get_left() + DOWN * 1)
        self.right_text.move_to(self.mem_map_rect.get_right() + DOWN * 1)

        self.write_rect: List[Rectangle] = []
        self.read_rect: List[Rectangle] = []

        if self.right_addr != self.left_addr:
            scale_factor = width / (self.right_addr - self.left_addr)
        else:
            scale_factor = 1

        for rd_left_addr, rd_right_addr in self.rd_range:
            block_width = (rd_right_addr - rd_left_addr) * scale_factor
            center_addr = ceil((rd_left_addr + rd_right_addr) / 2)
            block_offset = (center_addr - self.left_addr) * scale_factor
            self.read_rect.append(
                Rectangle(color=rd_color, height=0.34, width=block_width, fill_opacity=0.25)
                    .move_to(self.mem_map_rect.get_left() + RIGHT * block_offset + UP * 0.33))

        for wr_left_addr, wr_right_addr in self.wr_range:
            block_width = (wr_right_addr - wr_left_addr) * scale_factor
            center_addr = ceil((wr_left_addr + wr_right_addr) / 2)
            block_offset = (center_addr - self.left_addr) * scale_factor
            self.write_rect.append(
                Rectangle(color=wr_color, height=0.66, width=block_width, fill_opacity=0.50)
                    .move_to(self.mem_map_rect.get_left() + RIGHT * block_offset + DOWN * 0.17))

        super().__init__()
        self.add(self.mem_map_rect, self.left_text, self.right_text,
                 *self.write_rect, *self.read_rect)

    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    def _adjust_range(self,
                      align: int,
                      left_addr,
                      right_addr,
                      ranges: List[Tuple[int]]) -> Tuple[int, int]:
        """
        Adjust range of memory map. Memory map should cover all accessed ranges, meanwhile, it
        should align as requirement.

        Args:
            align: Alignment requirement of memory range.
            left_addr: Left address of memory map.
            right_addr: Right address of memory map.
            ranges: Accessed range.
        """
        if len(ranges) > 0:
            min_value = min(x[0] for x in ranges)
            range_left_addr = (min_value // align) * align
            left_addr_ = range_left_addr if left_addr == right_addr else \
                min(left_addr, range_left_addr)
        else:
            left_addr_ = left_addr

        if len(ranges) > 0:
            max_value = max(x[1] for x in ranges)
            range_right_addr = ceil(max_value / align) * align
            right_addr_ = range_right_addr if left_addr == right_addr else \
                max(right_addr, range_right_addr)
        else:
            right_addr_ = right_addr

        return (left_addr_, right_addr_)

    def _add_range(self, old_range: List[Tuple[int]], laddr:int, raddr: int) -> List[Tuple[int]]:
        """
        Add range to existed range. Merge contiguous range to one.

        Args:
            old_range: List of access range.
            laddr: Left address of new access.
            raddr: Right address of new access.
        """
        full_range = old_range + [(laddr, raddr)]
        sorted_range = sorted(full_range, key=lambda x: x[0])
        new_range = []
        for range_elem in sorted_range:
            if len(new_range) == 0:
                new_range.append(range_elem)
                continue

            if new_range[-1][0] <= range_elem[0] <= new_range[-1][1]:
                new_range[-1] = (min(new_range[-1][0], range_elem[0]),
                                 max(new_range[-1][1], range_elem[1]))
            else:
                new_range.append(range_elem)

        return new_range

    def add_range(self, laddr: int, raddr: int) -> Self:
        """
        Add one memory range accessed.

        Args:
            laddr: Left address of new access.
            raddr: Right address of new access.

        Return:
            one new memory map.
        """
        left_addr, right_addr = self._adjust_range(align=self.align,
                                                   left_addr=laddr,
                                                   right_addr=raddr,
                                                   ranges=self.rd_range + self.wr_range)

        return MemoryMap(color=self.mem_map_color,
                         rd_color=self.rd_rect_color,
                         wr_color=self.wr_rect_color,
                         width=self.mem_map_rect.width,
                         align=self.align,
                         left_addr=left_addr,
                         right_addr=right_addr,
                         rd_range=self.rd_range,
                         wr_range=self.wr_range)


    def add_rd_range(self, laddr: int, raddr: int) -> Self:
        """
        Add one memory range accessed.

        Args:
            laddr: Left address of new access.
            raddr: Right address of new access.

        Return:
            one new memory map.
        """
        new_rd_range = self._add_range(self.rd_range, laddr, raddr)

        return MemoryMap(color=self.mem_map_color,
                         rd_color=self.rd_rect_color,
                         wr_color=self.wr_rect_color,
                         width=self.mem_map_rect.width,
                         align=self.align,
                         left_addr=self.left_addr,
                         right_addr=self.right_addr,
                         rd_range=new_rd_range,
                         wr_range=self.wr_range)

    def add_wr_range(self, laddr: int, raddr: int) -> Self:
        """
        Add one memory range accessed.

        Args:
            laddr: Left address of new access.
            raddr: Right address of new access.

        Return:
            one new memory map.
        """
        new_wr_range = self._add_range(self.wr_range, laddr, raddr)

        return MemoryMap(color=self.color,
                         rd_color=self.rd_rect_color,
                         wr_color=self.wr_rect_color,
                         width=self.mem_map_rect.width,
                         align=self.align,
                         left_addr=self.left_addr,
                         right_addr=self.right_addr,
                         rd_range=self.rd_range,
                         wr_range=new_wr_range)

    def get_addr_triangle(self, addr: int, color: Color) -> Triangle:
        """
        Get an triangle point to correct position in memory map.
        
        Args:
            addr: Address.
            color: Color of address trangle.
        """
        if self.right_addr != self.left_addr:
            scale_factor = self.mem_map_rect.width / (self.right_addr - self.left_addr)
        else:
            scale_factor = 1

        block_offset = (addr + 0.5 - self.left_addr) * scale_factor
        return Triangle(color=color, fill_opacity=0.5).scale(0.2) \
            .move_to(self.mem_map_rect.get_left() + RIGHT * block_offset + UP * 0.7) \
            .rotate(60*DEGREES)
