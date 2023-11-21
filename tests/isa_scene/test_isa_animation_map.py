"""
Test animation flow analysis.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from isa_manim import (Scene, # pylint: disable=wrong-import-position
                       config,
                       WHITE, RED, GREEN, BLUE, YELLOW, PURPLE,
                       LEFT, RIGHT, UP, DOWN,
                       read_elem, function_call, assign_elem,
                       OneDimReg, OneDimRegElem, FunctionUnit,
                       IsaAnimationMap)

config.frame_height = 10
config.frame_width = 24

class TestIsaAnimationMap(Scene):
    """
    Test animation flow analysis.
    """
    def construct(self):
        animation_map = IsaAnimationMap()

        zn = OneDimReg(text="Zn", color=WHITE, width=128).shift(UP * 5)
        zm = OneDimReg(text="Zm", color=WHITE, width=128).shift(UP * 3)
        zda = OneDimReg(text="Zda", color=WHITE, width=128).shift(UP * 1)

        mul_unit = FunctionUnit(text="*(a,b)", color=WHITE, args_width=[16, 16], res_width=32) \
            .shift(LEFT * 6 + DOWN * 3)
        add_unit = FunctionUnit(text="+(a,b)", color=WHITE, args_width=[32, 32], res_width=32) \
            .shift(RIGHT * 4 + DOWN * 3)

        self.add(zn, zm, zda, mul_unit, add_unit)

        for i in range(0, 4):
            sum_ = OneDimRegElem(color=RED, width=32)
            animation_map.animation_add_animation(
                animate=read_elem(vector=zda, elem=sum_, index=i),
                src=[], dst=[sum_], dep=[zda])

            for j in range(0, 2):
                opa = OneDimRegElem(color=GREEN, width=16)
                animation_map.animation_add_animation(
                    animate=read_elem(vector=zn, elem=opa, index=i * 2 + j),
                    src=[], dst=[opa], dep=[zn])
                opb = OneDimRegElem(color=BLUE, width=16)
                animation_map.animation_add_animation(
                    animate=read_elem(vector=zm, elem=opb, index=i * 2 + j),
                    src=[], dst=[opb], dep=[zm])
                prod = OneDimRegElem(color=YELLOW, width=32)
                animation_map.animation_add_animation(
                    animate=function_call(mul_unit, args_list=[opa, opb], res_item=prod),
                    src=[opa, opb], dst=[prod], dep=[mul_unit])
                sum__ = OneDimRegElem(color=PURPLE, width=32)
                animation_map.animation_add_animation(
                    animate=function_call(add_unit, args_list=[prod, sum_], res_item=sum__),
                    src=[prod, sum_], dst=[sum__], dep=[add_unit])
                sum_ = sum__

            new_sum_ = OneDimRegElem(color=sum_.elem_color, width=sum_.elem_width)
            animation_map.animation_add_animation(
                animate=assign_elem(old_elem=sum_, new_elem=new_sum_, vector=zda, index=i),
                src=[sum_], dst=[sum_], dep=[zda])

            if i == 0:
                animation_map.switch_section(wait=1)

        animation_map.switch_section(wait=2)

        animation_map.analysis_animation_flow()

        for animation_step in animation_map.isa_animation_step_list:
            self.play(*animation_step.animate_list)
            if animation_step.wait > 0:
                self.wait(animation_step.wait)
