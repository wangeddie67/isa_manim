"""
Color map.
"""

from typing import List, Dict, Union
from colour import Color
from manim import WHITE, RED, BLUE, GREEN, YELLOW, TEAL, PURPLE, MAROON

class IsaColorMap:
    """
    This class is used to map colors for ISA objects by allocating colors in the color scheme.

    Attributes:
        colormap_default_color: Default color, used by registers, function units and memory units.
            Default is WHITE.
        _colormap_color_list: List of color scheme. Default is
            [RED, BLUE, GREEN, YELLOW, TEAL, PURPLE, MAROON].
        _colormap_color_index: Index points to the last picked color.
        _colormap_hash_dict: Dictionary of objects and their color. Key of the dictionary is the 
            hash value and the value is assigned color.
    """
    def __init__(self, default_color: Color = WHITE, color_scheme: List[Color] = None):
        """
        Construct color map.

        Args:
            default_color: Default color.
            color_scheme: Color scheme.
        """
        self._colormap_color_list: List[Color] = \
            color_scheme if color_scheme else [RED, BLUE, GREEN, YELLOW, TEAL, PURPLE, MAROON]
        self._colormap_color_index: int = len(self._colormap_color_list) - 1
        self.colormap_default_color: Color = default_color
        self._colormap_hash_dict: Dict[Union[int, str], Color] = {}

    def colormap_reset(self):
        """
        Reset color map.

        Reset color index and clear hash dictionary.
        """
        self._colormap_color_index = len(self._colormap_color_list) - 1
        self._colormap_hash_dict = {}

    def colormap_get_color(self,
                           color_hash: Union[int, str],
                           num: int = 1) -> Union[Color, List[Color]]:
        """
        Get one color or one list of colors for one given hash value.

        - If the hash value exists in the color map, return the assigned color from dictionary.
        - Otherwise, return the next color or next colors in the color scheme.

        Args:
            color_hash: Hash for item.
            num: Number of color.

        Returns:
            If `num` is 1, return a single color. If `num` is larger than 1, return a list of
            colors.
        """
        # If the hash value exists in the color map, return the assigned color from dictionary.
        if color_hash in self._colormap_hash_dict:
            # Get assigned color from dictionary.
            assign_color = self._colormap_hash_dict[color_hash]
            # Reshape the return color(s)
            if num == 1:
                if isinstance(assign_color, list):
                    return assign_color[0]
                else:
                    return assign_color
            else:
                if isinstance(assign_color, list):
                    if len(assign_color) == num:
                        return assign_color
                    else:
                        return [assign_color[i % len(assign_color)] for i in range(0, num)]
                else:
                    return [assign_color for _ in range(0, num)]
        # Otherwise, return the next color(s) in the color scheme.
        else:
            # Get a list of color
            assign_color = []
            for _ in range(0, num):
                self._colormap_color_index = \
                    (self._colormap_color_index + 1) % len(self._colormap_color_list)
                assign_color.append(self._colormap_color_list[self._colormap_color_index])
            # Reshape the return color(s)
            if num == 1:
                assign_color = assign_color[0]
            # Add hash value and color in the dictionary.
            self._colormap_hash_dict[color_hash] = assign_color
            # Return color list
            return assign_color
