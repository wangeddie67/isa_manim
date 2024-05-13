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

class TestIsaPlacementMap2(MovingCameraScene):
    """
    Test object placement.
    """
    def construct(self):
        animation_map = IsaPlacementMap()

        func16_unit_list = [FunctionUnit("*(a,b)", WHITE, [16, 16], [32], ["a", "b"], [""],
                                DEFAULT_FONT_SIZE, get_config("elem_value_format"), None)
                            for _ in range(0, 8)]
        func16_hash_list = [f"func16{i}" for i in range(0, 8)]

        func32_unit_list = [FunctionUnit("+(a,b)", WHITE, [32, 32], [32], ["a", "b"], [""],
                                DEFAULT_FONT_SIZE, get_config("elem_value_format"), None)
                            for _ in range(0, 8)]
        func32_hash_list = [f"func32{i}" for i in range(0, 8)]

        animation_map.place_object_group(func16_unit_list, func16_hash_list, force_hw_ratio=8)
        animation_map.place_object_group(func32_unit_list, func32_hash_list)

        mem_unit = MemoryUnit(WHITE, 64, 64, 64, [[0, 0x100]],
                              DEFAULT_FONT_SIZE, get_config("elem_value_format"), False, 0,
                              animation_map.get_placement_width() - 2)

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

        self.add(*dots, *func16_unit_list, *func32_unit_list, mem_unit, grids)
