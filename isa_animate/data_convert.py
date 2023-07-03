"""
Convert data format.
"""

from colour import Color
from manim import FadeIn, FadeOut, AnimationGroup
from ..isa_objects import OneDimRegElem
from .isa_animate import IsaAnimate


def data_convert(elem: OneDimRegElem,
                 color: Color,
                 size: float,
                 index: int,
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

    new_elem = OneDimRegElem(color, size, fill_opacity=0.5, **kwargs) \
        .move_to(elem.get_sub_elem_center(index=index, elem_width=size))

    animate=AnimationGroup(FadeIn(new_elem), FadeOut(elem))

    return IsaAnimate(animate=animate, src=elem, dst=new_elem)
