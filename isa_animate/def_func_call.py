"""
Call function.
"""

from typing import List
from colour import Color
from manim import FadeIn
from ..isa_objects import FunctionCall
from .isa_animate import IsaAnimate


def def_func_call(func: str,
                  color: Color,
                  args_width: List[float],
                  res_width: float,
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

    func_object = FunctionCall(
        text=func, color=color, args_width=args_width, res_width=res_width, **kwargs)

    animate = FadeIn(func_object)

    return IsaAnimate(animate=animate, src=[], dst=func_object)