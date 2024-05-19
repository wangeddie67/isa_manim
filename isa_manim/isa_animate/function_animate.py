"""
Animation with Function unit.
"""

from typing import List
from manim import (AnimationGroup, Succession, FadeIn, FadeOut, Animation, Wait)
from ..isa_objects import (ElemUnit, FunctionUnit)

def decl_func_unit(*func_unit: List[FunctionUnit]) -> Animation:
    """
    Declare one function unit.

    Args:
        func_unit: Object of function.

    Returns:
        Animation to declare function unit.
    """
    return FadeIn(*func_unit)

def read_func_imm(elem: ElemUnit) -> Animation:
    """
    Animation for declare one immediate operand. Fade in element at the specified location related
    to the function unit.

    Args:
        elem: Object of the immediate element.

    Returns:
        Animation to declare immediate operand.
    """
    return FadeIn(elem)

def function_call(func_unit: FunctionUnit,
                  args_list: List[ElemUnit],
                  res_list: List[ElemUnit],
                  args_offset: List[int],
                  res_offset: List[int]) -> Animation:
    """
    Animation for calling one function.
    
    This animation has the following steps:

    - Move elements of source operands to the position of arguments.
    - Wait 0.5 second.
    - Fadeout the source operands and fadein the destination operands.

    Args:
        func_unit: Object of function object.
        args_list: List of argument elements.
        res_list: List of result elements.
        args_offset: Offset of LSB of each argument.
        res_offset: Offset of LSB of each result.

    Returns:
        Animation to calling one function.
    """
    # Move argument element to source operand.
    move_animate_list = []
    args_list_ : List[ElemUnit] = []
    for i, (arg, offset) in enumerate(zip(args_list, args_offset)):
        if isinstance(arg, tuple):  # immediate operand
            arg_animate: FadeIn = arg[1]
            arg: ElemUnit = arg[0]
            arg.move_to(func_unit.get_arg_pos(i, offset, arg.elem_width))
            args_list_.append(arg)
            move_animate_list.append(arg_animate)
        else:
            args_list_.append(arg)
            move_animate_list.append(
                arg.animate.move_to(func_unit.get_arg_pos(i, offset, arg.elem_width)))
    move_animate = AnimationGroup(*move_animate_list)

    # Fadeout source operands and fadein destination operands
    src_animates = [FadeOut(arg, shift=func_unit.func_rect.get_center() \
                                    - func_unit.get_arg_pos(i, offset, arg.elem_width))
                    for i, (arg, offset) in enumerate(zip(args_list_, args_offset))]
    for i, (item, offset) in enumerate(zip(res_list, res_offset)):
        item.move_to(func_unit.get_res_pos(i, offset, item.elem_width))
    dst_animates = [FadeIn(res, shift=func_unit.get_res_pos(i, offset, res.elem_width) \
                                   - func_unit.func_rect.get_center())
                    for i, (res, offset) in enumerate(zip(res_list, res_offset))]
    fade_animate = AnimationGroup(*src_animates, *dst_animates)

    # Return animation sequence.
    return Succession(move_animate, Wait(0.5), fade_animate)
