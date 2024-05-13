"""
Animation with Registers and Elements.
"""

from typing import List, Union
from manim import (FadeIn, Animation, Transform, FadeTransformPieces)
from ..isa_objects import (ElemUnit, RegUnit)

def decl_register(*registers: List[Union[RegUnit]]) -> Animation:
    """
    Declare registers. Fadein a list of register objects.

    Args:
        registers: List of registers.

    Returns:
        Animation to declare registers.
    """
    # Creat Animation.
    return FadeIn(*registers)

def replace_register(old_reg: RegUnit,
                     new_reg: RegUnit,
                     offset: int) -> Animation:
    """
    Replacing exist register with a new register. The new register is right-aligned with the old
    register. `offset` specifies the gap between the LSB of two registers, which can be positive or
    negative.

    Args:
        old_reg: Object of the old vector.
        new_reg: Object of the new vector.
        offset: Offset of lower bits.

    Returns:
        Animation to replace registers.
    """
    # Move new register to the specified position.
    new_pos = old_reg.get_elem_pos(0, 0, offset, new_reg.reg_width)
    new_reg.shift(new_pos - new_reg.reg_rect.get_center())
    # Creat Animation.
    return Transform(old_reg, new_reg)

def read_elem(vector: RegUnit,
              elem: ElemUnit,
              index: int,
              reg_idx: int,
              offset: int) -> Animation:
    """
    Read specified element from one register. Fade in element at the specified position related
    to the register.

    Args:
        vector: Object of the register.
        elem: Object of the element.
        index: Element index.
        reg_idx: Register index. Used only for two-dimension register units.
        offset: Offset of lowest bit.

    Returns:
        Animation to read an element from a register.
    """
    # Move element to the specified position in the register unit.
    elem.move_to(vector.get_elem_pos(index, reg_idx, offset, elem.elem_width))
    # Creat Animation.
    return FadeIn(elem)

def assign_elem(old_elem: ElemUnit,
                new_elem: ElemUnit,
                vector: RegUnit,
                index: int,
                reg_idx: int,
                offset: int) -> Animation:
    """
    Assign one element to the register. Move element to the specified location related to
    the register.
    
    Instead of move animation, this function uses transform animation. `new_elem` can use different
    width, color, and value from the `old_elem`.

    Args:
        old_elem: Element object before animation.
        new_elem: Element object after animation.
        vector: Register object.
        index: Index of element.
        reg_idx: register index.
        offset: Offset of lowest bit.

    Returns:
        Animation to assign an element to a register.
    """
    # Move new element to the specified position in the register unit.
    new_elem.move_to(vector.get_elem_pos(index, reg_idx, offset, new_elem.elem_width))
    # Creat Animation.
    return Transform(old_elem, new_elem)

def replace_elem(old_elem: ElemUnit,
                 new_elem: ElemUnit,
                 offset: int) -> Animation:
    """
    Replace exist element with a new element. The new element is right-aligned with the existed
    element. `offset` specifies the gap between the LSB of two registers, which can be positive or
    negative.

    Args:
        old_elem: Object of the old element.
        new_elem: Object of the new element.
        offset: Offset of lower bits.

    Returns:
        Animation to declare registers.
    """
    # Move new element to the specified position
    new_elem.move_to(old_elem.get_elem_pos(offset, new_elem.elem_width))
    # Creat Animation.
    return FadeTransformPieces(old_elem, new_elem)
