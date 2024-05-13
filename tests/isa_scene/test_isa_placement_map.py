"""
Test object placement.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (MovingCameraScene, # pylint: disable=wrong-import-position
                       config, get_config, DEFAULT_FONT_SIZE,
                       WHITE,
                       RIGHT, DOWN,
                       RegUnit, FunctionUnit, MemoryUnit, Dot, NumberPlane,
                       IsaPlacementMap)

config.frame_height = 9
config.frame_width = 16

class TestIsaPlacementMap(MovingCameraScene):
    """
    Test object placement.
    """
    def construct(self):
        animation_map = IsaPlacementMap()

        zn = RegUnit(["Zn"], WHITE, 128, 1, 1, None,
                     DEFAULT_FONT_SIZE, get_config("elem_value_format"))
        zm = RegUnit(["Zm"], WHITE, 128, 1, 1, None,
                     DEFAULT_FONT_SIZE, get_config("elem_value_format"))
        za = RegUnit(["Za"], WHITE, 256, 8, 2, None,
                     DEFAULT_FONT_SIZE, get_config("elem_value_format"))

        mul_unit = FunctionUnit("*(a,b)", WHITE, [16, 16], [32], ["a", "b"], [""],
                                DEFAULT_FONT_SIZE, get_config("elem_value_format"), None)
        add_unit = FunctionUnit("+(a,b)", WHITE, [32, 32], [32], ["a", "b"], [""],
                                DEFAULT_FONT_SIZE, get_config("elem_value_format"), None)

        mem_unit = MemoryUnit(WHITE, 64, 64, 64, [[0, 0x100]],
                              DEFAULT_FONT_SIZE, get_config("elem_value_format"), False, 0, 0)

        animation_map.place_object(zn, "zn")
        animation_map.place_object(zm, "zm", align_with=zn)
        animation_map.place_object(za, "za")
        animation_map.place_object(mul_unit, "mul")
        animation_map.place_object(add_unit, "add", align_with=mul_unit)
        animation_map.place_object(mem_unit, "memory")

        print(animation_map.dump_placement())
        self.camera.frame.move_to(animation_map.get_placement_origin())
        self.camera.frame.scale(
            animation_map.get_camera_scale(config.frame_width, config.frame_height))

        dots = [Dot(),
                Dot(animation_map.get_placement_width() * RIGHT),
                Dot(animation_map.get_placement_height() * DOWN),
                Dot(animation_map.get_placement_width() * RIGHT
                    + animation_map.get_placement_height() * DOWN)
                ]

        grids = NumberPlane(x_range=(0, animation_map.get_placement_width(), 1),
                            y_range=(-animation_map.get_placement_height(), 0, 1)) \
                .move_to(animation_map.get_placement_origin())

        self.add(*dots, zn, zm, za, mul_unit, add_unit, mem_unit, grids)
