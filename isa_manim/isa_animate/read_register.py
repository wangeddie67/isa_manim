"""
Read register from register files.
"""

from typing import List
from colour import Color
from manim import FadeIn
from ..isa_objects import OneDimReg
from .isa_animate import IsaAnimate

def read_scalar_reg(text: str,
                    color: Color,
                    width: int,
                    **kargs):
    """
    Read scalar register.

    Args:
        text_list:
        color:
        width:
    """
    scalar = OneDimReg(text=text, color=color, width=width, elements=1,
                       font_size=40, **kargs)

    return IsaAnimate(animate=FadeIn(scalar), src=None, dst=scalar)

def read_vector_reg(text: str,
                    color: Color,
                    width: int,
                    elements: int = 1,
                    **kargs):
    """
    Read vector register.

    Args:
        text_list:
        color:
        width:
        elements:
    """
    vector = OneDimReg(text=text, color=color, width=width, elements=elements,
                       font_size=40, **kargs)

    return IsaAnimate(animate=FadeIn(vector), src=None, dst=vector)

def read_vector_group(text_list: List[str],
                      color: Color,
                      width: int,
                      elements: int = 1,
                      **kargs):
    """
    Read vector register group.

    Args:
        text_list:
        color:
        width:
        elements:
    """
    vector_list = []
    for text in text_list:
        vector_list.append(OneDimReg(
            text=text, color=color, width=width, elements=elements,
            font_size=40, **kargs))

    return IsaAnimate(animate=FadeIn(*vector_list), src=None, dst=vector_list)
