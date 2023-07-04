"""
Call function.
"""

from typing import List
from colour import Color
from manim import FadeIn, FadeOut, AnimationGroup, Succession
from manim import DOWN
from ..isa_objects import OneDimRegElem, FunctionCall
from .isa_animate import IsaAnimate


def function_call(func: FunctionCall,
                  args: List[OneDimRegElem],
                  color: Color,
                  width: float,
                  **kwargs) -> IsaAnimate:
    """
    Convert data to another element.

    Args:
        elem: Source element.
        color: Color of destination register.
        size: Size of new element.
        index: Index of new element related to source elements.
    
    Return:
        - New elements.
        - Animation.
    """

    dst_elem = OneDimRegElem(color=color,
                             width=width,
                             fill_opacity=0.5,
                             font_size=40, **kwargs)
    dst_elem.move_to(func.get_dst_pos())

    move_animate = \
        AnimationGroup(
            *[arg.animate.move_to(func.get_args_pos(i))
               for i, arg in enumerate(args)]
        )
    fade_animate = \
        AnimationGroup(
            FadeIn(dst_elem,
                   shift=func.get_dst_pos() - func.get_func_center()),
            *[FadeOut(arg,
                      shift=func.get_func_center() - func.get_args_pos(i))
               for i, arg in enumerate(args)]
        )

    return IsaAnimate(animate=Succession(move_animate, fade_animate),
                      src=args, dst=dst_elem, dep=func)
