"""
Test animation for function, including declaring and calling function.
"""

import os
import sys
path = sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       config,
                       WHITE, BLUE, GREEN, PURPLE, YELLOW,
                       UP, LEFT, RIGHT,
                       Text,
                       OneDimRegElem, FunctionCall,
                       decl_func_call, function_call)

config.frame_height = 6
config.frame_width = 30

class TestFuncAnimation(Scene):
    """
    Test animation for function, including declaring and calling function.
    """
    def construct(self):
        # Read elements.
        r1_elem = OneDimRegElem(color=GREEN, width=16).move_to(UP * 4 + LEFT * 2)
        r2_elem = OneDimRegElem(color=BLUE, width=16).move_to(UP * 4 + RIGHT * 2)
        self.add(r1_elem, r2_elem)

        # Declare function.
        function_item = FunctionCall(text="+(a, b)",
                                     color=WHITE,
                                     args_width=[16, 16],
                                     res_width=32,
                                     args_value=["a", "b"])
        function_animate = decl_func_call(function_item)
        def_func_call_label = Text("def_func_call", color=YELLOW) \
            .move_to(function_item.func_ellipse.get_right() + RIGHT * 4)

        self.add(def_func_call_label)
        self.play(function_animate)
        self.wait(duration=2)
        self.remove(def_func_call_label)

        # Function call.
        res_elem = OneDimRegElem(color=PURPLE, width=32)
        func_call_animate = function_call(func_object=function_item,
                                          args_list=[r1_elem, r2_elem],
                                          res_item=res_elem)
        func_cal_label = Text("function_call", color=YELLOW) \
            .move_to(function_item.func_ellipse.get_right() + RIGHT * 4)

        # Play Animation.
        self.add(func_cal_label)
        self.play(func_call_animate)
        self.wait(duration=2)
