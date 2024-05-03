"""
Color map.

The color of objects in ISA scenes can be allocated automatically by color scheme. Each new item 
will be assigned a color in the color scheme. 

The color of objects can be controlled by a hash. The objects with the same hash value share the 
same color.
"""

from typing import List, Dict
from colour import Color
from manim import WHITE, RED, BLUE, GREEN, YELLOW, TEAL, PURPLE, MAROON

class IsaColorMap:
    """
    This class is used to map colors for ISA objects by allocating colors in color scheme.

    Attributes:
        _colormap_color_list: List of color scheme.
        _colormap_color_index: Index points to previous color.
        colormap_default_color: Default color.
        _colormap_hash_dict: Dictionary of objects and their color. Key of the dictionary is the 
            hash value and the value is assigned color.
    """
    def __init__(self, default_color: Color = WHITE, color_scheme: List[Color] = None):
        """
        Construct color.

        Args:
            default_color: Default color.
            color_scheme: Color scheme
        """
        self._colormap_color_list: List[Color] = \
            color_scheme if color_scheme else [RED, BLUE, GREEN, YELLOW, TEAL, PURPLE, MAROON]
        self._colormap_color_index: int = len(self._colormap_color_list) - 1
        self.colormap_default_color: Color = default_color
        self._colormap_hash_dict: Dict[str, Color] = {}

    def colormap_reset(self):
        """
        Reset color map.

        Reset color index and clear dictionary.
        """
        self._colormap_color_index = len(self._colormap_color_list) - 1
        self._colormap_hash_dict = {}

    def colormap_get_color(self, color_hash = None) -> Color:
        """
        Get color for one object. If one hash value is specified and the value is existed in the
        dictionary, return assigned color from dictionary. Otherwise, if hash value is not specified
        or the hash value is new, return next color in the color scheme. 

        Args:
            color_hash: hash for item.
        """
        if color_hash:
            if color_hash in self._colormap_hash_dict:
                # Return assigned color from dictionary.
                return self._colormap_hash_dict[color_hash]
            else:
                # Return next color in color scheme and report object in the dictionary.
                self._colormap_color_index = \
                    (self._colormap_color_index + 1) % len(self._colormap_color_list)
                color = self._colormap_color_list[self._colormap_color_index]
                self._colormap_hash_dict[color_hash] = color
                return color
        else:
            # Return next color in color scheme
            self._colormap_color_index = \
                (self._colormap_color_index + 1) % len(self._colormap_color_list)
            return self._colormap_color_list[self._colormap_color_index]

    def colormap_get_multi_color(self, num: int, color_hash = None) -> List[Color]:
        """
        Get color for multiple object. If one hash value is specified and the value is existed in the
        dictionary, return assigned color from dictionary. Otherwise, if hash value is not specified
        or the hash value is new, return next color in the color scheme. 

        Args:
            num: Count of item.
            color_hash: hash for item.
        """
        if color_hash:
            if color_hash in self._colormap_hash_dict:
                # Return assigned color from dictionary.
                ret_color = self._colormap_hash_dict[color_hash]
                return ret_color if isinstance(ret_color, list) else [ret_color]
            else:
                # Get a list of color
                color_list = []
                for _ in range(0, num):
                    self._colormap_color_index = \
                        (self._colormap_color_index + 1) % len(self._colormap_color_list)
                    color_list.append(self._colormap_color_list[self._colormap_color_index])
                # Return color list and report object in the dictionary.
                self._colormap_hash_dict[color_hash] = color_list
                return color_list
        else:
            # Get a list of color
            color_list = []
            for _ in range(0, num):
                self._colormap_color_index = \
                    (self._colormap_color_index + 1) % len(self._colormap_color_list)
                color_list.append(self._colormap_color_list[self._colormap_color_index])
            # Return color list
            return color_list
