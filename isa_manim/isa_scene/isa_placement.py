"""
Object placement.
"""

from math import ceil
import numpy as np
from typing import List, Tuple, Union, Dict
from manim import Mobject, config, LEFT, RIGHT, UP, DOWN
from ..isa_objects import *
from time import sleep

class IsaPlacementItem:
    """
    Data structure for animate for auto placement.

    Attributes:
        isa_object: Isa object.
        isa_hash: Hash value of this object.
    """

    def __init__(self,
                 isa_object: Mobject,
                 isa_hash: str = None
        ):
        """
        Construct one data structure for animate.

        Args:
            isa_object: Isa object.
            isa_hash: Hash value of this object.
        """
        self.isa_object = isa_object
        if isa_hash:
            self.isa_hash = isa_hash
        else:
            hash(self.isa_object)

    def __str__(self) -> str:
        string = f"[Object={str(self.isa_object)}, "
        return string

    def __repr__(self) -> str:
        string = f"[Object={str(self.isa_object)}, "
        return string

    def get_width(self) -> int:
        """
        Return width of item when placement.
        """
        if isinstance(self.isa_object, OneDimReg):
            return ceil(self.isa_object.reg_rect.width + self.isa_object.label_text.width)
        elif isinstance(self.isa_object, TwoDimReg):
            label_text_width = max([item.width for item in self.isa_object.label_text_list])
            reg_rect_width = max([item.width for item in self.isa_object.reg_rect_list])
            return ceil(label_text_width + reg_rect_width)
        elif isinstance(self.isa_object, OneDimRegElem):
            return ceil(self.isa_object.elem_rect.width)
        elif isinstance(self.isa_object, FunctionCall):
            return ceil(self.isa_object.func_ellipse.width)
        else:
            raise ValueError("Not ISA Object.")

    def get_height(self) -> int:
        if isinstance(self.isa_object, OneDimReg):
            return 1
        elif isinstance(self.isa_object, TwoDimReg):
            return int(self.isa_object.reg_count)
        elif isinstance(self.isa_object, OneDimRegElem):
            return 1
        elif isinstance(self.isa_object, FunctionCall):
            return 5
        else:
            raise ValueError("Not ISA Object.")

    def set_corner(self, row: int, col: int):
        if isinstance(self.isa_object, OneDimReg):
            x = col + self.get_width() - self.isa_object.reg_rect.width / 2
            y = row
            self.isa_object.shift(RIGHT * x + DOWN * y - self.isa_object.reg_rect.get_center())
        elif isinstance(self.isa_object, TwoDimReg):
            x = col + self.get_width() - self.isa_object.reg_rect_list[0].width / 2
            y = row
            self.isa_object.shift(
                RIGHT * x + DOWN * y - self.isa_object.reg_rect_list[0].get_center())
        elif isinstance(self.isa_object, OneDimRegElem):
            x = col + self.get_width() / 2
            y = row
            self.isa_object.move_to(RIGHT * x + DOWN * y)
        elif isinstance(self.isa_object, FunctionCall):
            x = col + self.get_width() / 2
            y = row + 2
            self.isa_object.move_to(RIGHT * x + DOWN * y)
        else:
            raise ValueError("Not ISA Object.")

class IsaPlacementMap:
    """
    This class is used to analyse the order of animations.

    Attributes:
        isa_animation_section_list: List of ISA animation section, which contains a set of 
            animations.
        isa_animation_step_list: List of ISA step section, which contains a set of animations
            after analysis animation flow.
        _section_animate_list: List of animations after previous section, which will be packed into
            one section.
        always_on_item_list: List of items that will not be faded out between section.
    """

    def __init__(self, strategy = "BR"):
        self.isa_object_dict: Dict[str, IsaPlacementItem] = dict()
        self._placement_map: List[List[str]] = [[-1]]
        self._placement_width: int = 1
        self._placement_height: int = 1

        self.resize_placement_map(new_width=config.frame_width,
                                  new_height=config.frame_height)

        self._placement_hv_ratio = config.frame_height / config.frame_width
        self._placement_strategy = strategy # "BR", "RB"

    @property
    def width(self) -> int:
        max_col = 0
        for col in range(0, self._placement_width):
            for row in range(0, self._placement_height):
                if self._placement_map[row][col] is not None:
                    max_col = col
                    break
        return max_col
    
    @property
    def height(self) -> int:
        max_row = 0
        for row in range(0, self._placement_height):
            for col in range(0, self._placement_width):
                if self._placement_map[row][col] is not None:
                    max_row = row
                    break
        return max_row

    def camera_origin(self) -> np.array:
        return RIGHT * self.width / 2 + DOWN * self.height / 2

    def camera_scale(self, camera_width, camera_height) -> float:
        return max((self.height + 1) / camera_height, self.width / camera_width)

    def resize_placement_map(self,
                             new_width: int, new_height: int):
        """
        Resize placement map.

        Args:
            new_width: New width of map.
            new_height: New height of map.
        """
        old_width = self._placement_width
        old_height = self._placement_height

        new_placement_map = []
        for row in range(0, new_height):
            if row < old_height:
                if new_width <= old_width:
                    new_placement_row = self._placement_map[row][0:new_width]
                else:
                    new_placement_row = \
                        self._placement_map[row] + [None for _ in range(old_width, new_width)]
                new_placement_map.append(new_placement_row)
            else:
                new_placement_map.append([None for _ in range(0, new_width)])

        for row in range(0, new_height):
            new_placement_map[row][0] = -1
        for col in range(0, new_width):
            new_placement_map[0][col] = -1

        self._placement_width = new_width
        self._placement_height = new_height
        self._placement_map = new_placement_map

    def _check_space_rect(self,
                          corner_row: int,
                          corner_col: int,
                          rect_width: int,
                          rect_height: int) -> bool:
        """
        Check whether there is a space rectangle in placement map.
        Placement map should not only contains the rectangle, but also a boundary around it.

        Args:
            corner_row: Left-up corner position of rectangle.
            corner_col: Left-up corner position of rectangle.
            rect_width: Width of rectangle.
            rect_height: Height of rectangle.
        """
        # Return false if there is not enough space in partition map.
        if self._placement_width - corner_col < rect_width + 1:
            return False
        elif self._placement_height - corner_row < rect_height + 1:
            return False

        # If the space has allocated point, return False
        for row in range(corner_row, corner_row + rect_height + 1):
            for col in range(corner_col, corner_col + rect_width + 1):
                if self._placement_map[row][col] is not None:
                    return False

        return True

    def _mark_space_rect(self,
                         hash_str: str,
                         corner_row: int,
                         corner_col: int,
                         rect_width: int,
                         rect_height: int):
        """
        Mark one rectangle in placement map with provided hash string. Meanwhile, mark the elements
        around the rectangle with -1.

        Args:
            hash_str: Hash string.
            corner_row: Left-up corner position of rectangle.
            corner_col: Left-up corner position of rectangle.
            rect_width: Width of rectangle.
            rect_height: Height of rectangle.
        """
        for row in range(corner_row - 1, corner_row + rect_height + 1):
            for col in range(corner_col - 1, corner_col + rect_width + 1):
                # Skip if outside placement map.
                if not (0 <= row < self._placement_height):
                    continue
                if not (0 <= col < self._placement_width):
                    continue

                # Elements around rectangle
                if row == corner_row - 1 or row == corner_row + rect_height \
                        or col == corner_col - 1 or col == corner_col + rect_width + 1:
                    self._placement_map[row][col] = -1
                else:
                    self._placement_map[row][col] = hash_str

    def place_item_into_map(self, isa_object: IsaPlacementItem) -> bool:
        """
        Place item into placement map.
        """
        rect_width = isa_object.get_width()
        rect_height = isa_object.get_height()

        # BR strategy, first try to place item under exist item.
        if self._placement_strategy == "RB":
            for row in range(0, self._placement_height - rect_height + 1):
                for col in range(0, self._placement_width - rect_width + 1):
                    if self._placement_map[row][col] is not None:
                        continue
                    if self._check_space_rect(row, col, rect_width, rect_height):
                        isa_object.set_corner(row, col)
                        self._mark_space_rect(
                            isa_object.isa_hash, row, col, rect_width, rect_height)
                        return True

        # BR strategy, first try to place item beside exist item.
        elif self._placement_strategy == "BR":
            for col in range(0, self._placement_width - rect_width + 1):
                for row in range(0, self._placement_height - rect_height + 1):
                    if self._placement_map[row][col] is not None:
                        continue
                    if self._check_space_rect(row, col, rect_width, rect_height):
                        isa_object.set_corner(row, col)
                        self._mark_space_rect(
                            isa_object.isa_hash, row, col, rect_width, rect_height)
                        return True

        return False

    def register_object(self,
                        isa_object: Union[Mobject, List[Mobject]],
                        isa_hash: str = None):
        """
        Register objects and place them.

        Args:
            animate: IsaAnimateItem or a list of IsaAnimateItem.
        """
        if isinstance(isa_object, list):
            for item in isa_object:
                if not isinstance(item, Mobject):
                    raise ValueError(
                        "Arguments must be Mobject or a list of Mobject.")
                else:
                    self.register_object(item, hash)
            return

        if not isinstance(isa_object, Mobject):
            raise ValueError(
                "Arguments must be IsaAnimate or a list of Mobject.")

        isa_object_item = IsaPlacementItem(isa_object, isa_hash)
        self.isa_object_dict[isa_object_item.isa_hash] = isa_object_item

        place_success = False
        while not place_success:
            # place item into scene
            place_success = self.place_item_into_map(isa_object_item)

            # If place fail, resize map.
            if not place_success:
                if self._placement_hv_ratio > 1:
                    new_width = int(self._placement_width + 1)
                    new_height = int(new_width * self._placement_hv_ratio)
                else:
                    new_height = int(self._placement_height + 1)
                    new_width = int(new_height / self._placement_hv_ratio)
                self.resize_placement_map(new_width, new_height)
