"""
Object placement.

isa_manim provides the capacity to auto placement objects in the scene. 

:py:class:`isa_manim.isa_scene.isa_placement.IsaPlacementMap` provides the object placement manager.
The placement manager will provide a location for each object when registering it:

- Scalar registers, vector registers, vector register groups or matrix registers.
- Function units.

Data elements should not be registered to the placement manager because they are moved between the 
above objects.

The placement algorithm abstracts the placement into an array. Each row in the array presents 1.0 
in the vertical direction while each column in the array presents 1.0 in the horizontal direction.
The value of items in the placement array describes the status of each item:

- 0 means the item is free to allocate;
- 1 means the item is a margin between objects or a margin between objects and items.
- 2 means the item is occupied by a register.
- 3 means the item is occupied by a function unit.

Hence, the placement algorithm became one question to find one rectangle space in the placement 
array, which addresses all the following conditions:

- the rectangle is larger enough for the object to place.
- the rectangle is free to allocate (all items are 0).
- items around the rectangle have not been allocated by another object (all items are 0 or 1).
- all items on the same row with the rectangle should be free (0), margin (1) or the same type of
  object to place.

If such a rectangle cannot be found in the current placement array, the placement array is scaled
until such a rectangle can be found.

There are two strategies to search rectangle in the placement array:

- RB means search along the horizontal direction first, then vertical direction. By default, RB is
  used.
- BR means search along the vertical direction first, than horizontal direction.
"""

from math import ceil
import numpy as np
from typing import List, Union, Dict
from manim import Mobject, config, RIGHT, DOWN
from ..isa_objects import (OneDimReg, TwoDimReg, OneDimRegElem, FunctionCall)

class IsaPlacementItem:
    """
    Data structure for animate for auto placement.

    Attributes:
        isa_object: Isa object.
        isa_hash: Hash value of this object.
    """

    def __init__(self,
                 isa_object: Mobject,
                 isa_hash: str = None):
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
            self.isa_hash = hash(self.isa_object)

    def __str__(self) -> str:
        string = f"[Object={str(self.isa_object)}, "
        return string

    def __repr__(self) -> str:
        string = f"[Object={str(self.isa_object)}, "
        return string

    def get_width(self) -> int:
        """
        Return width of item in integer for placement.
        """
        if isinstance(self.isa_object, OneDimReg):
            if self.isa_object.label_text.width < 2:
                return ceil(self.isa_object.reg_rect.width + 2)
            else:
                return ceil(self.isa_object.reg_rect.width + self.isa_object.label_text.width)
        elif isinstance(self.isa_object, TwoDimReg):
            label_text_width = max([item.width for item in self.isa_object.label_text_list])
            reg_rect_width = max([item.width for item in self.isa_object.reg_rect_list])
            if label_text_width < 2:
                return ceil(2 + reg_rect_width)
            else:
                return ceil(label_text_width + reg_rect_width)
        elif isinstance(self.isa_object, OneDimRegElem):
            return ceil(self.isa_object.elem_rect.width)
        elif isinstance(self.isa_object, FunctionCall):
            return ceil(self.isa_object.func_ellipse.width)
        else:
            raise ValueError("Not ISA Object.")

    def get_height(self) -> int:
        """
        Return height of item in integer for placement.
        """
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

    def get_marker(self) -> int:
        """
        Return the marker of object.
        """
        if isinstance(self.isa_object, OneDimReg):
            return 2
        elif isinstance(self.isa_object, TwoDimReg):
            return 2
        elif isinstance(self.isa_object, OneDimRegElem):
            return 2
        elif isinstance(self.isa_object, FunctionCall):
            return 3
        else:
            raise ValueError("Not ISA Object.")

    def set_corner(self, row: int, col: int):
        """
        Set the position of object by the left-up corner position.

        Args:
            row: Vertical ordinate of left-up corner.
            col: Horizontal ordinate of left-up corner.
        """
        if isinstance(self.isa_object, OneDimReg):
            x = col + self.get_width() - self.isa_object.reg_rect.width / 2
            y = row + 0.5
            self.isa_object.shift(RIGHT * x + DOWN * y - self.isa_object.reg_rect.get_center())
        elif isinstance(self.isa_object, TwoDimReg):
            x = col + self.get_width() - self.isa_object.reg_rect_list[0].width / 2
            y = row + 0.5
            self.isa_object.shift(
                RIGHT * x + DOWN * y - self.isa_object.reg_rect_list[0].get_center())
        elif isinstance(self.isa_object, OneDimRegElem):
            x = col + self.get_width() / 2
            y = row + 0.5
            self.isa_object.move_to(RIGHT * x + DOWN * y)
        elif isinstance(self.isa_object, FunctionCall):
            x = col + self.get_width() / 2
            y = row + 2 + 0.5
            self.isa_object.move_to(RIGHT * x + DOWN * y)
        else:
            raise ValueError("Not ISA Object.")

class IsaPlacementMap:
    """
    This class is used to analyse the order of animations.

    Attributes:
        _placement_object_dict: Dictionary of objects, key is one hash value and the value is
            item of IsaPlacementItem.
        _placement_map: Array of the placement.
        _placement_width: Width of the placement.
        _placement_height: Height of the placement.
        _placement_hv_ratio: height/width ratio of the placement.
        _placement_strategy: Strategy to find rectangle.
    """

    def __init__(self, strategy = "RB"):
        """
        Initialize placement map.

        Args:
            strategy: Strategy to search rectangle, option: RB or BR.
        """
        self._placement_object_dict: Dict[str, IsaPlacementItem] = dict()
        self._placement_map: List[List[str]] = []
        self._placement_width: int = 0
        self._placement_height: int = 0

        self.placement_resize(new_width=config.frame_width, new_height=config.frame_height)

        self._placement_hv_ratio: float = config.frame_height / config.frame_width
        self._placement_strategy: str = strategy # "BR", "RB"

    def placement_width(self) -> int:
        """
        Return width of the placement, only occupied column or margins are count.
        """
        max_col = 0
        for col in range(0, self._placement_width):
            for row in range(0, self._placement_height):
                if self._placement_map[row][col] > 0:
                    max_col = col
                    break
        return max_col + 1

    def placement_height(self) -> int:
        """
        Return height of the placement, only occupied rows or margins are count.
        """
        max_row = 0
        for row in range(0, self._placement_height):
            for col in range(0, self._placement_width):
                if self._placement_map[row][col] > 0:
                    max_row = row
                    break
        return max_row + 1

    def placement_origin(self) -> np.array:
        """
        Return center position of placement.
        """
        return RIGHT * self.placement_width() / 2 + DOWN * self.placement_height() / 2

    def placement_scale(self,
                        camera_width: float,
                        camera_height: float) -> float:
        """
        Return scale factor of the placement to fit into specified camera.

        Args:
            camera_width: Width of camera.
            camera_height: Width of camera.
        """
        return max((self.placement_height() + 1) / camera_height,
                   (self.placement_width() + 1) / camera_width)

    def placement_resize(self,
                         new_width: int,
                         new_height: int):
        """
        Resize placement map while keeping items in the old placement map.

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
                        self._placement_map[row] + [0 for _ in range(old_width, new_width)]
                new_placement_map.append(new_placement_row)
            else:
                new_placement_map.append([0 for _ in range(0, new_width)])

        self._placement_width = new_width
        self._placement_height = new_height
        self._placement_map = new_placement_map

    def _placement_check_rect(self,
                              corner_row: int,
                              corner_col: int,
                              rect_width: int,
                              rect_height: int,
                              marker: int = None) -> bool:
        """
        Check whether there is a space rectangle in placement map.
        Placement map should not only contains the rectangle, but also a boundary around it.

        Args:
            corner_row: Left-up corner position of rectangle.
            corner_col: Left-up corner position of rectangle.
            rect_width: Width of rectangle.
            rect_height: Height of rectangle.
            marker: Marker of object.
        """
        # Return false if there is not enough space in partition map.
        if self._placement_width - corner_col + 1 < rect_width + 2:
            return False
        elif self._placement_height - corner_row + 1 < rect_height + 2:
            return False

        # If the space has allocated point, return False
        for row in range(corner_row - 1, corner_row + rect_height + 1):
            for col in range(corner_col - 1, corner_col + rect_width + 1):
                if self._placement_map[row][col] > 1:
                    return False

        # If the row is not empty, the exist item should be the same mark as new one.
        if marker:
            for row in range(corner_row - 1, corner_row + rect_height + 1):
                for col in range(0, corner_col - 1):
                    if self._placement_map[row][col] > 1 \
                            and self._placement_map[row][col] != marker:
                        return False

        return True

    def _placement_mark_rect(self,
                             marker: int,
                             corner_row: int,
                             corner_col: int,
                             rect_width: int,
                             rect_height: int):
        """
        Mark one rectangle in placement map with provided marker. Meanwhile, mark the elements
        around the rectangle with 1.

        Args:
            marker: Marker.
            corner_row: Left-up corner position of rectangle.
            corner_col: Left-up corner position of rectangle.
            rect_width: Width of rectangle.
            rect_height: Height of rectangle.
        """
        for row in range(corner_row - 1, corner_row + rect_height + 1):
            for col in range(corner_col - 1, corner_col + rect_width + 1):
                # Skip if outside placement map.
                if not 0 <= row < self._placement_height:
                    continue
                if not 0 <= col < self._placement_width:
                    continue

                # Elements around rectangle
                if row == corner_row - 1 or row == corner_row + rect_height \
                        or col == corner_col - 1 or col == corner_col + rect_width:
                    self._placement_map[row][col] = 1
                else:
                    self._placement_map[row][col] = marker

    def place_item_into_map(self, placement_item: IsaPlacementItem) -> bool:
        """
        Place object into placement map.

        Args:
            placement_item: Item to place.
        """
        rect_width = placement_item.get_width()
        rect_height = placement_item.get_height()
        marker = placement_item.get_marker()

        # BR strategy, first try to place item under exist item.
        if self._placement_strategy == "RB":
            for row in range(1, self._placement_height - rect_height + 1):
                for col in range(1, self._placement_width - rect_width + 1):
                    if self._placement_map[row][col] != 0:
                        continue
                    if self._placement_check_rect(row, col, rect_width, rect_height, marker):
                        placement_item.set_corner(row, col)
                        self._placement_mark_rect(marker, row, col, rect_width, rect_height)
                        return True

        # BR strategy, first try to place item beside exist item.
        elif self._placement_strategy == "BR":
            for col in range(1, self._placement_width - rect_width + 1):
                for row in range(1, self._placement_height - rect_height + 1):
                    if self._placement_map[row][col] != 0:
                        continue
                    if self._placement_check_rect(row, col, rect_width, rect_height, marker):
                        placement_item.set_corner(row, col)
                        self._placement_mark_rect(marker, row, col, rect_width, rect_height)
                        return True

        return False

    def placement_has_object(self, place_hash: str) -> bool:
        """
        Check whether the object is existed.
        """
        return place_hash in self._placement_object_dict

    def placement_get_object(self, place_hash: str) -> Mobject:
        """
        Return ISA object.

        Args:
            place_hash: Hash value of ISA object.
        """
        return self._placement_object_dict[place_hash].isa_object

    def placement_add_object(self,
                             object: Mobject,
                             place_hash: str = None):
        """
        Add object into dictionary and place it into placement map.

        Args:
            object: Object to place.
            place_hash: Hash value of ISA object.
        """
        if not isinstance(object, Mobject):
            raise ValueError("Argument must be Mobject.")

        #
        isa_object_item = IsaPlacementItem(object, place_hash)
        self._placement_object_dict[isa_object_item.isa_hash] = isa_object_item

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
                self.placement_resize(new_width, new_height)

    def placement_reset(self):
        """
        Reset placement map.
        """
        self._placement_object_dict = dict()
        self._placement_map = []
        self._placement_width = 0
        self._placement_height = 0

        self.placement_resize(new_width=config.frame_width,
                                  new_height=config.frame_height)

    def placement_dump(self) -> str:
        """
        Return a string of placement map for debug.
        """
        map_str = ""
        for row in self._placement_map:
            for item in row:
                if item == 0:   # Not occupied
                    map_str += " "
                elif item == 1: # Margin
                    map_str += "*"
                else:           # Occupied
                    map_str += "O"
            map_str += "\n"
        return map_str
