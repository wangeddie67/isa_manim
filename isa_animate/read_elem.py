"""
Read element from register
"""

from colour import Color
from manim import FadeIn
from ..isa_objects import OneDimReg
from .isa_animate import IsaAnimate

def read_elem(vector: OneDimReg,
              color: Color,
              size: float = -1.0,
              index: int = 0,
              **kargs) -> IsaAnimate:
    """
    Read element from register, return one Rectangle.

    If the element size is not specified, create element with the same width as
    elements in source register. Otherwise, create element with the new
    specified size.

    Args:
        vector: Register.
        color: Color of new element.
        size: Width of element in byte.
        e: Index of element.
        kargs: Arguments to new element.
    """

    if isinstance(vector, OneDimReg):
        elem = vector.get_elem(color=color, elem_width=size, index=index,
                               **kargs)
        return IsaAnimate(animate=FadeIn(elem),
                          src=vector, dst=elem, dep=[vector])
    else:
        error_str = f"vector is not right type. {str(vector)}"
        raise ValueError(error_str)
