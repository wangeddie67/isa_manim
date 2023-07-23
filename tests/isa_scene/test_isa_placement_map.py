"""
Test data flow analysis with ISA animations.
"""

import os
import sys
path = sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (MovingCameraScene, # pylint: disable=wrong-import-position
                       config,
                       WHITE,
                       OneDimReg, TwoDimReg, FunctionCall, Dot,
                       IsaPlacementMap)

config.frame_height = 9
config.frame_width = 16

class TestIsaPlacementMap(MovingCameraScene):
    """
    Test object for register element.
    """
    def construct(self):
        animation_map = IsaPlacementMap()

        dot = Dot()

        zn = OneDimReg(text="Zn", color=WHITE, width=128)
        zm = OneDimReg(text="Zm", color=WHITE, width=128)
        za = TwoDimReg(text="Za", color=WHITE, nreg=2, width=256)

        mul_unit = FunctionCall(text="*(a,b)", color=WHITE, args_width=[16, 16], res_width=32)
        add_unit = FunctionCall(text="+(a,b)", color=WHITE, args_width=[32, 32], res_width=32)

        animation_map.register_object([zn, zm, za, mul_unit, add_unit])

        print(animation_map.print_map())
        self.camera.frame.move_to(animation_map.camera_origin())
        self.camera.frame.scale(
            animation_map.camera_scale(config.frame_width, config.frame_height))

        self.add(dot, zn, zm, za, mul_unit, add_unit)
