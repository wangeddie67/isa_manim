"""
Concat two vectors.
"""

from colour import Color
from manim import LEFT, RIGHT
from manim import FadeIn, FadeOut, AnimationGroup, Succession
from ..isa_objects import OneDimReg
from .isa_animate import IsaAnimate

def concat_vector(src1: OneDimReg,
                  src2: OneDimReg,
                  text: str,
                  color: Color,
                  **kargs) -> IsaAnimate:
    """
    Concat two vectors.

    Move v1 to left by half, move v2 to right by half, and up to align with v1.
    Fadeout v1 and v2, while fadein new vector.

    Animation from [v1,v2] to a new vector [vector]
    Animation has two step:
    - move v1 and v2
    - fade out v1/v2 and fade in vector.

    Args:
        v1: Vector 1.
        v2: Vector 2.
        text: Register name after conversion.
        color: Color of new element.
        kargs: Arguments to new element.
    """
    reg_width = src1.reg_width + src2.reg_width
    elem_width = int(min(src1.elem_width, src2.elem_width))
    elements = int(reg_width / elem_width)
    if "ratio" not in kargs:
        kargs["ratio"] = max(src1.ratio, src2.ratio)

    vector = OneDimReg(text=text,
                       color=color,
                       width=reg_width,
                       elements=elements,
                       font_size=40,
                       **kargs)
    vector.shift(src1.get_reg_center() - vector.get_reg_center())

    move_animate = AnimationGroup(
        src1.animate.move_to(src1.get_center() + LEFT * src1.get_reg_width() / 2),
        src2.animate.move_to(src1.get_center() + RIGHT * src2.get_reg_width() / 2))

    fade_animate = AnimationGroup(
        FadeIn(vector), FadeOut(src1), FadeOut(src2))

    return IsaAnimate(animate=Succession(move_animate, fade_animate),
                      src=[src1, src2], dst=vector)
