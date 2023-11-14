"""
Test object placement.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (MovingCameraScene, # pylint: disable=wrong-import-position
                       config,
                       WHITE,
                       RIGHT, DOWN,
                       OneDimReg, TwoDimReg, FunctionUnit, Dot, NumberPlane,
                       IsaPlacementMap)

config.frame_height = 9
config.frame_width = 16

class TestIsaPlacementMap(MovingCameraScene):
    """
    Test object placement.
    """
    def construct(self):
        animation_map = IsaPlacementMap()

        zn = OneDimReg(text="Zn", color=WHITE, width=128)
        zm = OneDimReg(text="Zm", color=WHITE, width=128)
        za = TwoDimReg(text="Za", color=WHITE, nreg=2, width=256)

        mul_unit = FunctionUnit(text="*(a,b)", color=WHITE, args_width=[16, 16], res_width=32)
        add_unit = FunctionUnit(text="+(a,b)", color=WHITE, args_width=[32, 32], res_width=32)

        animation_map.placement_add_object(zn)
        animation_map.placement_add_object(zm)
        animation_map.placement_add_object(za)
        animation_map.placement_add_object(mul_unit)
        animation_map.placement_add_object(add_unit)

        print(animation_map.placement_dump())
        self.camera.frame.move_to(animation_map.placement_origin())
        self.camera.frame.scale(
            animation_map.placement_scale(config.frame_width, config.frame_height))

        dot = [Dot(),
               Dot(animation_map.placement_width() * RIGHT),
               Dot(animation_map.placement_height() * DOWN),
               Dot(animation_map.placement_width() * RIGHT
                   + animation_map.placement_height() * DOWN)
               ]

        grid = NumberPlane(
            x_range=(-animation_map.placement_width(), animation_map.placement_width(), 1),
            y_range=(-animation_map.placement_height(), animation_map.placement_height(), 1))

        self.add(*dot, zn, zm, za, mul_unit, add_unit, grid)
