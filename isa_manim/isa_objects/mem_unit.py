"""
Object for memory unit.

Such object provides an absolute graphic object for memory unit.

Graphic object is a VGroup containing one Round rectangle objects, several rectangle objects, two
Cubic Bezier lines and several Text objects.
"""

from math import ceil
import numpy as np
from typing import List, Tuple
from manim import (VGroup, Text, Rectangle, DashedVMobject, RoundedRectangle, Triangle,
                   CubicBezier,
                   LEFT, RIGHT, UP, DOWN, DEGREES,
                   DEFAULT_FONT_SIZE)
from colour import Color
from ..isa_config import get_scene_ratio

class MemoryUnit(VGroup):
    """
    Object for memory unit.

    Attributes:
        addr_width: width of address, in bit.
        data_width: Width of data, in bit.
        mem_rect: Round rectangle of memory unit.
        label_text: Text of memory.
        addr_rect: rectangle of address argument.
        data_rect: rectangle of data argument.
        mem_map_rect: rectangle of memory map. Provides the position of memory map.
        mem_map_left_brace: left brace of memory map.
        mem_map_right_brace: right brace of memory map. 
    """

    require_serialization = True

    def __init__(self,
                 color: Color,
                 addr_width: int,
                 data_width: int,
                 addr_align: int,
                 mem_range: List[Tuple[int]],
                 font_size: int = DEFAULT_FONT_SIZE,
                 para_enable: bool = False,
                 mem_map_width: int = 0):
        """
        Constructor an function call.

        Args:
            color: Color of memory unit.
            addr_width: Width of address, in bit
            data_width: Width of data, in bit
            addr_align: Alignment of memory range address, default is 64.
            mem_range: Memory range
            font_size: Font size of value text.
        """
        self.require_serialization = not para_enable

        self.mem_font_size = font_size

        # memory rectangle
        self.mem_rect: RoundedRectangle = RoundedRectangle(color=color, height=3.0, width=4)

        # Label text
        self.label_text: Text = Text(text="Mem",
                                     color=color,
                                     font_size=font_size) \
                .move_to(self.mem_rect.get_center())

        # Address rectangle
        self.addr_rect: Rectangle = DashedVMobject(
            Rectangle(color=color, height=1.0, width=addr_width * get_scene_ratio()))
        self.addr_rect.shift(
            LEFT * (1 + self.mem_rect.width / 2 + self.addr_rect.width / 2))
        self.addr_label_text = Text(text="Addr", color=color, font_size=font_size) \
            .move_to(self.addr_rect.get_center() + UP)

        # Data rectangle
        self.data_rect: Rectangle = DashedVMobject(
            Rectangle(color=color, height=1.0, width=data_width * get_scene_ratio()))
        self.data_rect.shift(
            RIGHT * (1 + self.mem_rect.width / 2 + self.data_rect.width / 2))
        self.data_label_text = Text(text="Data", color=color, font_size=font_size) \
            .move_to(self.data_rect.get_center() + UP)

        # Memory map
        mem_map_width = max(self.addr_rect.width + self.data_rect.width + self.mem_rect.width + 2,
                            mem_map_width)
        self.mem_addr_align: int = addr_align

        self.mem_range: List[Tuple[int, int]] = []
        self.mem_map_list: List[Rectangle] = []
        self.mem_map_text: List[Tuple[Text, Text]] = []
        self.mem_mark_list : List[Rectangle] = []
        mem_map_idx = 0
        for laddr, raddr in mem_range:
            laddr = (laddr // addr_align) * addr_align
            raddr = ((raddr // addr_align) + 1) * addr_align if raddr % addr_align > 0 else \
                    (raddr // addr_align) * addr_align

            mem_map_rect = Rectangle(color=color, height=1.0, width=mem_map_width)
            mem_map_rect.shift(self.addr_rect.get_left() - mem_map_rect.get_left())
            mem_map_rect.shift(DOWN * (3 + 2 * mem_map_idx))

            left_text = Text(hex(raddr), font_size=font_size * 0.75)
            right_text = Text(hex(laddr), font_size=font_size * 0.75)
            left_text.move_to(mem_map_rect.get_left() + DOWN * 1)
            right_text.move_to(mem_map_rect.get_right() + DOWN * 1)

            self.mem_map_list.append(mem_map_rect)
            self.mem_map_text.extend([left_text, right_text])
            self.mem_range.append([laddr, raddr])
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
        self.add(self.mem_rect, self.label_text,
                 self.addr_rect, self.addr_label_text, self.data_rect, self.data_label_text,
                 *self.mem_map_list, *self.mem_map_text,
                 self.mem_map_left_brace, self.mem_map_right_brace)

    # Property functions
    @property
    def mem_color(self) -> Color:
        return self.mem_rect.color

    @property
    def mem_addr_width(self) -> int:
        return int(self.addr_rect.width / get_scene_ratio())

    @property
    def mem_data_width(self) -> int:
        return int(self.data_rect.width / get_scene_ratio())

    @property
    def mem_map_width(self) -> float:
        return self.addr_rect.width + self.data_rect.width + self.mem_rect.width + 2

    # Override function
    def align_points_with_larger(self, larger_mobject):
        raise NotImplementedError("Please override in a child class.")

    # Get locations.
    def get_addr_pos(self, width: int = None) -> np.ndarray:
        """
        Return center position of access address.

        Args:
            width: Width of address in bit.
        """
        if width:
            return self.addr_rect.get_right() + LEFT * width * get_scene_ratio() / 2
        else:
            return self.addr_rect.get_center()

    def get_data_pos(self, width: int = None) -> np.ndarray:
        """
        Return center position of write data.

        Args:
            width: Width of write data in bit.
        """
        if width:
            return self.data_rect.get_right() + LEFT * width * get_scene_ratio() / 2
        else:
            return self.data_rect.get_center()

    def _index_of_mem_range(self, addr: int) -> int:
        """
        Check whether given address is covered in memory range.
        
        Args:
            addr: given address.
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
        Check whether given address is covered in memory range.
        
        Args:
            addr: given address.
        """
        return True if self._index_of_mem_range(addr) >= 0 else False

    def get_addr_mark(self,
                      addr: int,
                      color: Color) -> Triangle:
        """
        Get a mark of address.
        
        Args:
            addr: given address.
            color: Color of address mark.
        """
        mem_range_idx = self._index_of_mem_range(addr)
        mem_range_rect = self.mem_map_list[mem_range_idx]
        scale_factor = mem_range_rect.width / \
            (self.mem_range[mem_range_idx][1] - self.mem_range[mem_range_idx][0])

        addr_offset = addr - self.mem_range[mem_range_idx][0] + 0.5
        addr_mark = Triangle(color=color).scale(0.2).rotate(60 * DEGREES).move_to(
            mem_range_rect.get_right() - (addr_offset * scale_factor) * RIGHT + UP * 0.6)

        return addr_mark

    def get_rd_mem_mark(self,
                        laddr: int,
                        raddr: int,
                        color: Color) -> Rectangle:
        """
        Get a mark of accessed memory range.
        
        Args:
            addr: given address.
            color: Color of address mark.
        """
        mem_range_idx = self._index_of_mem_range(laddr)
        mem_range_rect = self.mem_map_list[mem_range_idx]
        scale_factor = mem_range_rect.width / \
            (self.mem_range[mem_range_idx][1] - self.mem_range[mem_range_idx][0])

        laddr_offset = laddr - self.mem_range[mem_range_idx][0]
        addr_range = min(raddr, self.mem_range[mem_range_idx][1]) - laddr
        mem_mark = Rectangle(color=color,
                             height=0.34,
                             width=addr_range * scale_factor,
                             fill_opacity=0.25).move_to(
            mem_range_rect.get_right() - ((laddr_offset + addr_range / 2) * scale_factor) * RIGHT
            + UP * 0.33)

        return mem_mark

    def get_wt_mem_mark(self,
                        laddr: int,
                        raddr: int,
                        color: Color) -> Rectangle:
        """
        Get a mark of accessed memory range.
        
        Args:
            addr: given address.
            color: Color of address mark.
        """
        mem_range_idx = self._index_of_mem_range(laddr)
        mem_range_rect = self.mem_map_list[mem_range_idx]
        scale_factor = mem_range_rect.width / \
            (self.mem_range[mem_range_idx][1] - self.mem_range[mem_range_idx][0])

        laddr_offset = laddr - self.mem_range[mem_range_idx][0]
        addr_range = min(raddr, self.mem_range[mem_range_idx][1]) - laddr
        mem_mark = Rectangle(color=color,
                             height=0.66,
                             width=addr_range * scale_factor,
                             fill_opacity=0.5).move_to(
            mem_range_rect.get_right() - ((laddr_offset + addr_range / 2) * scale_factor) * RIGHT
            + DOWN * 0.17)

        return mem_mark

    def get_mem_mark_list(self) -> List[Rectangle]:
        """
        Return memory mark list.
        """
        return self.mem_mark_list

    def append_mem_mark_list(self, mark: Rectangle):
        """
        Append one mark to memory mark list.
        """
        self.mem_mark_list.append(mark)
