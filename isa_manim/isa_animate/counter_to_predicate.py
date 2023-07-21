"""
Convert predicate as counter to marked predicate.
"""

from colour import Color
from manim import FadeIn, FadeOut, AnimationGroup
from ..isa_objects import OneDimReg
from .isa_animate import IsaAnimate


def counter_to_predicate(png_obj: OneDimReg,
                         text: str,
                         color: Color,
                         width: int,
                         elements: int = 1,
                         **kargs):
    """
    Convert predicate as counter to marked predicate.

    Animation from [png_obj] to a new vector [predicate]
    Animation:
    - fade out png_obj and fade in predicate.

    Args:
        png_obj: Predicate as counter.
        text: Register name after conversion.
        color: Color of new element.
        width: Width of register, in Byte.
        elements: Number of elements.
        kargs: Arguments to new element.
    """

    predicate = OneDimReg(text=text,
                          color=color,
                          width=width,
                          elements=elements,
                          font_size=40,
                          **kargs)
    predicate.shift(png_obj.get_reg_center() - predicate.get_reg_center())

    animate=AnimationGroup(FadeIn(predicate), FadeOut(png_obj))

    return IsaAnimate(animate=animate, src=png_obj, dst=predicate)
