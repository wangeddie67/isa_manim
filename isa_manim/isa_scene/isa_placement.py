"""
Object placement.
"""

import numpy as np
from typing import List, Dict, Tuple, Union
from manim import Mobject, config, RIGHT, DOWN

class IsaPlacementItem:
    """
    Data structure of one object for auto placement.

    Attributes:
        isa_object: Isa object, RegUnit, ElemUnit, FunctionUnit and MemoryUnit.
        isa_hash: Hash value of this object.
        row: Vertical ordinate of left-up corner.
        col: Horizontal ordinate of left-up corner.
    """

    def __init__(self, isa_object: Mobject, isa_hash: Union[int, str]):
        """
        Construct one data structure for animate.

        Args:
            isa_object: Isa object.
            isa_hash: Hash value of this object.
        """
        self.isa_object: Mobject = isa_object
        self.isa_hash: Union[int, str] = isa_hash
        self.row: int = 0
        self.col: int = 0

    def __str__(self) -> str:
        string = f"[Object={str(self.isa_object)}, row={self.row}, col={self.col}]"
        return string

    def __repr__(self) -> str:
        string = f"[Object={str(self.isa_object)}, row={self.row}, col={self.col}]"
        return string

    def get_width(self) -> int:
        """
        Return the width of this object for placement. The width is ceil to an integer.

        Returns:
            The width of this object.
        """
        return self.isa_object.get_placement_width()

    def get_height(self) -> int:
        """
        Return the height of this object for placement. The height is ceil to an integer.

        Returns:
            The height of this object.
        """
        return self.isa_object.get_placement_height()

    def get_marker(self) -> int:
        """
        Return the marker of this object for placement.

        Returns:
            Marker of this object.
        """
        return self.isa_object.get_placement_mark()

    def set_corner(self, row: int, col: int):
        """
        Set the position of object by the left-up corner position. Move object to the specified
        position.

        Args:
            row: Vertical ordinate of left-up corner.
            col: Horizontal ordinate of left-up corner.
        """
        self.row = row
        self.col = col
        self.isa_object.set_placement_corner(row, col)

class _IsaPlaceHolderObject:
    """
    Data structure for auto placement.
    """

    def __init__(self,
                 width: int,
                 height: int):
        """
        Construct one data structure for animate.
        """
        self.width = width
        self.height = height

    def __str__(self) -> str:
        string = "PlaceHolder"
        return string

    def __repr__(self) -> str:
        string = "PlaceHolder"
        return string

    # Utility functions for object placement.
    def get_placement_width(self) -> int:
        """
        Return the width of this object for placement. The width is ceil to an integer.

        Returns:
            The width of this object.
        """
        return self.width

    def get_placement_height(self) -> int:
        """
        Return the height of this object for placement. The height is ceil to an integer.

        Returns:
            The height of this object.
        """
        return self.height

    def get_placement_mark(self) -> int:
        """
        Return the marker of this object, which is 0.

        Returns:
            Marker of this object.
        """
        return 0

    def set_placement_corner(self, row: int, col: int):
        """
        Set the position of object by the left-up corner position. Move object to the specified
        position.

        Args:
            row: Vertical ordinate of left-up corner.
            col: Horizontal ordinate of left-up corner.
        """
        pass

class IsaPlacementMap:
    """
    This class manages the position of objects in scene.

    Attributes:
        _placement_object_dict: Dictionary of objects, key is one hash value and the value is
            item of IsaPlacementItem.
        _placement_map: Array of the placement.
        _placement_width: Width of the placement.
        _placement_height: Height of the placement.
        _placement_hv_ratio: height/width ratio of the placement.
        _placement_strategy: Strategy to find rectangle.
    """

    def __init__(self, strategy: str = "RB"):
        """
        Initialize placement map.

        Args:
            strategy: Strategy to search rectangle, option: RB or BR.
        """
        self._placement_object_dict: Dict[str, IsaPlacementItem] = {}
        self._placement_map: List[List[int]] = []
        self._placement_width: int = 0
        self._placement_height: int = 0
        self._placement_hv_ratio: float = None
        self._placement_strategy: str = strategy # "BR", "RB"

        self.resize_placement(new_width=config.frame_width, new_height=config.frame_height)

    # Placement dictionary
    def has_object(self, place_hash: str) -> bool:
        """
        Check whether the object is existed.

        Args:
            place_hash: Hash value of ISA object.

        Returns:
            True means the hash exists in the placement dictionary.
        """
        return place_hash in self._placement_object_dict

    def get_object(self, place_hash: str) -> Mobject:
        """
        Return ISA object of the specified hash.

        Args:
            place_hash: Hash value of ISA object.

        Returns:
            The object for the specified ISA.
        """
        return self._placement_object_dict[place_hash].isa_object

    # Placement map
    def get_placement_width(self) -> int:
        """
        Return the width of the placement, only occupied column or margins are count.

        Returns:
            Return the width of the placement map.
        """
        max_col = 0
        for col in range(0, self._placement_width):
            for row in range(0, self._placement_height):
                if self._placement_map[row][col] > 0:
                    max_col = col
                    break
        return max_col + 1

    def get_placement_height(self) -> int:
        """
        Return the height of the placement, only occupied rows or margins are count.

        Returns:
            Return the width of the placement map.
        """
        max_row = 0
        for row in range(0, self._placement_height):
            for col in range(0, self._placement_width):
                if self._placement_map[row][col] > 0:
                    max_row = row
                    break
        return max_row + 1

    def get_placement_origin(self) -> np.array:
        """
        Return center position of the placement map related to the left-up corner.

        Returns:
            Return the center position of the placement map.
        """
        return RIGHT * self.get_placement_width() / 2 + DOWN * self.get_placement_height() / 2

    def get_camera_scale(self, camera_width: float, camera_height: float) -> float:
        """
        Return scale factor of the placement to fit into specified camera.

        Args:
            camera_width: The width of camera.
            camera_height: The height of camera.

        Returns:
            Scale factor of the camera.
        """
        return max((self.get_placement_height() + 1) / camera_height,
                   (self.get_placement_width() + 1) / camera_width)

    def resize_placement(self,
                         new_width: int,
                         new_height: int):
        """
        Resize placement map while keeping items in the old placement map.

        Args:
            new_width: New width of the placement map.
            new_height: New height of the placement map.
        """
        old_width = self._placement_width
        old_height = self._placement_height

        # Resize placement map
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
        self._placement_hv_ratio = self._placement_height / self._placement_width
        self._placement_map = new_placement_map

    def reset_placement(self, keep_objects: List[Mobject] = None, keep_pos: bool = True):
        """
        Reset placement map.
        
        Args:
            keep_objects: Objects should keep in the scene.
            keep_pos: True means keep the position of keep objects in the new placement.
        """
        # Get a list of keep objects
        keep_place_items: List[IsaPlacementItem] = []
        if keep_objects is not None:
            for keep_object in keep_objects:
                for _, place_item in self._placement_object_dict.items():
                    if place_item.isa_object is keep_object:
                        keep_place_items.append(place_item)

        # Reset placement dictonary and map.
        self._placement_object_dict = {}
        self._placement_map = []
        self._placement_width = 0
        self._placement_height = 0
        self.resize_placement(new_width=config.frame_width, new_height=config.frame_height)

        # Add keep objects back to the placement map.
        for place_item in keep_place_items:
            self._placement_object_dict[place_item.isa_hash] = place_item
            self.place_placement_item(place_item, force=keep_pos)

    def dump_placement(self) -> str:
        """
        Return a string of placement map for debug.

        Returns:
            A string of placement map.
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

    # Find a suitable position for one item.
    def _placement_check_rect(self,
                              corner_row: int,
                              corner_col: int,
                              rect_width: int,
                              rect_height: int,
                              marker: int = None) -> bool:
        """
        Check whether there is a spare rectangle space in the placement map.
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
        if marker is not None:
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

    def _placement_check_space(self,
                               placement_item: IsaPlacementItem,
                               force: bool = False,
                               align_row: int = None) -> Union[Tuple[int, int], None]:
        """
        Check whether there is space to allocate the object into the current placement map.

        Args:
            placement_item: Object item to place in the map.
            force: True means the object item must place at the position specified in
                `placement_item`.
            align_row: The object item must be specified at the specified row.

        Returns:
            If there is space to place the object, return a tuple contains the coordianate of
                object. The first element in the tuple is the vertical coordinate of the left-up
                corner while the second element is the horizontal coordinate. Return None if there
                is no space to place the object.
        """
        rect_width = placement_item.get_width()
        rect_height = placement_item.get_height()
        marker = placement_item.get_marker()

        # Force strategy, only check the position specified by placement_item.
        if force:
            row = placement_item.row
            col = placement_item.col
            if self._placement_check_rect(row, col, rect_width, rect_height, marker):
                self._placement_mark_rect(marker, row, col, rect_width, rect_height)
                return (row, col)
            else:
                return None

        # Align strategy, only check the specified row.
        if align_row is not None:
            for col in range(1, self._placement_width - rect_width + 1):
                if self._placement_map[align_row][col] != 0:
                    continue
                if self._placement_check_rect(align_row, col, rect_width, rect_height, marker):
                    placement_item.set_corner(align_row, col)
                    self._placement_mark_rect(marker, align_row, col, rect_width, rect_height)
                    return (align_row, col)

        # RB strategy, first try to place item under exist item. Row -> Col.
        elif self._placement_strategy == "RB":
            for row in range(1, self._placement_height - rect_height + 1):
                for col in range(1, self._placement_width - rect_width + 1):
                    if self._placement_map[row][col] != 0:
                        continue
                    if self._placement_check_rect(row, col, rect_width, rect_height, marker):
                        placement_item.set_corner(row, col)
                        self._placement_mark_rect(marker, row, col, rect_width, rect_height)
                        return (row, col)

        # BR strategy, first try to place item beside exist item. Col -> Row.
        elif self._placement_strategy == "BR":
            for col in range(1, self._placement_width - rect_width + 1):
                for row in range(1, self._placement_height - rect_height + 1):
                    if self._placement_map[row][col] != 0:
                        continue
                    if self._placement_check_rect(row, col, rect_width, rect_height, marker):
                        return (row, col)

        return None

    # Place placement item.
    def place_placement_item(self,
                             placement_item: IsaPlacementItem,
                             force: bool = False,
                             align_row: int = None):
        """
        Place one item into the placement map.

        This function tries to allocate the item into the placement map. If placement fails, this
        function will resize the placement map and try again. This function continues iteration
        until the object can be allocated into the placement map.

        Args:
            placement_item: Object item to place in the map.
            force: True means the object item must place at the position specified in
                `placement_item`.
            align_row: The object item must be specified at the specified row.
        """
        while True:
            # place item into scene
            place_coord = self._placement_check_space(placement_item, force, align_row)

            # If place fail, resize map.
            if place_coord is None:
                if self._placement_hv_ratio > 1:
                    new_width = int(self._placement_width + 1)
                    new_height = int(new_width * self._placement_hv_ratio)
                else:
                    new_height = int(self._placement_height + 1)
                    new_width = int(new_height / self._placement_hv_ratio)
                self.resize_placement(new_width, new_height)
            # If place success, mark the object in map and quit.
            else:
                rect_width = placement_item.get_width()
                rect_height = placement_item.get_height()
                marker = placement_item.get_marker()
                row, col = place_coord
                placement_item.set_corner(row, col)
                self._placement_mark_rect(marker, row, col, rect_width, rect_height)
                break

    # Place object(s).
    def place_object(self,
                     place_object: Mobject,
                     place_hash: Union[int, str],
                     align_with: Mobject = None):
        """
        Add object into the dictionary and place it into the placement map.

        Args:
            place_object: Object to place.
            place_hash: Hash value of ISA object.
            align_with: The object will be placed at the same row with another object.
        """
        if not isinstance(place_object, Mobject):
            raise ValueError("Argument must be Mobject.")

        #  Get align row.
        align_row = None
        if align_with:
            for place_key, place_item in self._placement_object_dict.items():
                if place_item.isa_object is align_with or place_key == align_with:
                    align_row = place_item.row

        # Create placement item.
        placement_item = IsaPlacementItem(place_object, place_hash)
        # Add placement item to placement dictionary.
        self._placement_object_dict[placement_item.isa_hash] = placement_item
        # Add placement item to placement map.
        self.place_placement_item(placement_item, align_row=align_row)

    def place_object_group(self,
                           place_object_list: List[Mobject],
                           place_hash_list: List[Union[int,str]],
                           force_hw_ratio: Union[int, None] = None):
        """
        Add a group of object into the dictionary and place it into the placement map.

        Args:
            place_object_list: List of object to place.
            place_hash_list: Hash value of ISA object.
            force_hw_ratio: Force the horization/vertical ratio of the groups.
        """
        for place_object in place_object_list:
            if not isinstance(place_object, Mobject):
                raise ValueError("Argument must be Mobject.")

        # Create placement item.
        place_item_list = [IsaPlacementItem(place_object, place_hash)
                           for place_object, place_hash in zip(place_object_list, place_hash_list)]

        # Convert to matrix according to width of placement.
        if force_hw_ratio is None:
            split = 1
            screen_factor = config.frame_width / config.frame_height
            while split < len(place_item_list):
                temp_width = sum(item.get_width() for item in place_item_list[0:split]) + split - 1
                temp_height = place_item_list[0].get_height() * (len(place_item_list) // split) \
                    + (len(place_item_list) // split) - 1
                if temp_width / temp_height > screen_factor:
                    break
                else:
                    split *= 2
        else:
            split = force_hw_ratio

        place_item_matrix: List[List[IsaPlacementItem]] = \
            [place_item_list[left:left + split][::-1] \
                for left in range(0, len(place_item_list), split)]

        matrix_row_width_list = [sum(item.get_width() for item in row) + len(row) - 1 \
            for row in place_item_matrix]
        matrix_width = max(matrix_row_width_list)
        matrix_row_height_list = [max(item.get_height() for item in row) \
            for row in place_item_matrix]
        matrix_height = sum(matrix_row_height_list) + len(place_item_matrix) - 1

        # Allocate location of the entire group without side-effort.
        place_holder_object = _IsaPlaceHolderObject(matrix_width, matrix_height)
        place_holder_item = IsaPlacementItem(place_holder_object, "placeholder")
        self.place_placement_item(place_holder_item)

        # Add each item in the group to the dictionary and map.
        place_row = place_holder_item.row
        for item_row, row_height in zip(place_item_matrix, matrix_row_height_list):
            place_col = place_holder_item.col
            for placement_item in item_row:
                self._placement_object_dict[placement_item.isa_hash] = placement_item
                placement_item.set_corner(place_row, place_col)
                self.place_placement_item(placement_item, force=True)
                place_col += placement_item.get_width() + 1
            place_row += row_height + 1
