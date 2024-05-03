"""
Predefined Animations.
"""

from typing import List, Union, Tuple
from manim import (Mobject,
                   AnimationGroup, Succession, FadeIn, FadeOut, Animation, Transform, Create,
                   FadeTransformPieces, Indicate, Wait,
                   Rectangle, Triangle,
                   LEFT, RIGHT)
from ..isa_objects import (RegElemUnit,
                           RegUnit,
                           FunctionUnit,
                           MemoryUnit)

#
# Animation with Registers.
#
def decl_register(*register: List[Union[RegUnit]]) -> Animation:
    """
    Animation for declare register. Fadein object of register.

    Args:
        register: object of register.
    """
    return FadeIn(*register)

def replace_register(old_vector: RegUnit,
                     new_vector: RegUnit,
                     align: str = "center") -> Animation:
    """
    Animation for replacing register with another register. The new vector can be left/right/center-
    aligned with the old vector.
    Fade out the old vector and fade in the new vector.

    Args:
        old_vector: object of the old vector.
        new_vector: object of the new vector.
        align: Strategy to align old and new vector, option: center/left/right.
    """

    if align.lower() == "center":
        new_pos = old_vector.reg_rect.get_center()
    elif align.lower() == "right":
        new_pos = old_vector.reg_rect.get_right() + LEFT * new_vector.reg_rect.width / 2
    elif align.lower() == "left":
        new_pos = old_vector.reg_rect.get_left() + RIGHT * new_vector.reg_rect.width / 2
    else:
        raise ValueError("align can only be center/left/right.")

    new_vector.shift(new_pos - new_vector.reg_rect.get_center())

    return Succession(Transform(old_vector, new_vector),
                      AnimationGroup(FadeIn(new_vector), FadeOut(old_vector)))

#
# Animation with Elements.
#
def read_elem(vector: RegUnit,
              elem: RegElemUnit,
              reg_idx: int = 0,
              index: int = 0,
              offset: int = 0) -> Animation:
    """
    Animation for reading element from register. Fade in element at the specified location related
    to the register.

    Args:
        vector: object of the register.
        elem: object of the element.
        reg_idx: register index. Used only for two-dimension register.
        index: element index.
        offset: Offset of lower bit.
    """

    if isinstance(vector, RegUnit):
        elem.move_to(vector.get_elem_center(
            index, reg_idx, offset=offset, elem_width=elem.elem_width))
    else:
        error_str = f"vector is not right type. {str(vector)}"
        raise ValueError(error_str)

    return FadeIn(elem)

def assign_elem(old_elem: RegElemUnit,
                new_elem: RegElemUnit,
                vector: RegUnit,
                reg_idx: int = 0,
                index: int = 0,
                offset: int = 0) -> Animation:
    """
    Animation for assign element to register. Move element to the specified location related to
    the register.

    If the new size is not specified, keep the size of element. Otherwise, scale element to the new 
    specified size.

    Args:
        elem: Element object.
        vector: Register.
        size: Width of destination element in bit.
        reg_idx: register index.
        index: Index of element.
        offset: Offset of lower bit.
    """
    if isinstance(vector, RegUnit):
        dest_pos = vector.get_elem_center(
            index, reg_idx, offset=offset, elem_width=new_elem.elem_width)
    else:
        error_str = f"vector is not right type. {str(vector)}"
        raise ValueError(error_str)

    new_elem.move_to(dest_pos)
    return Transform(old_elem, new_elem)

def replace_elem(old_elem: RegElemUnit,
                 new_elem: RegElemUnit,
                 index: int = 0,
                 align: str = "right") -> Animation:
    """
    Replace element in vector. Fade in new element while fade out old element.

    Args:
        old_elem: Object of the old element.
        new_elem: Object of the new element.
        index: Index of new element related to source elements.
        align: Strategy to align the old and new elements, option: center/left/right.
    """
    if align.lower() == "center":
        new_pos = old_elem.elem_rect.get_center()
    elif align.lower() == "right":
        new_pos = old_elem.elem_rect.get_right() \
            + LEFT * (new_elem.elem_rect.width * index + new_elem.elem_rect.width / 2)
    elif align.lower() == "left":
        new_pos = old_elem.elem_rect.get_left() \
            + RIGHT * (new_elem.elem_rect.width * index + new_elem.elem_rect.width / 2)
    else:
        raise ValueError("align can only be center/left/right.")

    new_elem.move_to(new_pos)
    return FadeTransformPieces(old_elem, new_elem)

#
# Animation with functions.
#
def decl_func_call(*func_unit: List[FunctionUnit]) -> Animation:
    """
    Animation for declare one object of function.

    Args:
        func_unit: Object of function.
    """
    return FadeIn(*func_unit)

def read_func_imm(elem: RegElemUnit) -> Tuple[Mobject, Animation]:
    """
    Animation for set one argument as immediate. Fade in element at the specified location related
    to the function unit..

    Args:
        elem: object of the element.
    """
    return (elem, FadeIn(elem))

def function_call(func_unit: FunctionUnit,
                  args_list: List[RegElemUnit],
                  res_list: List[RegElemUnit],
                  func_args_index: List[int],
                  res_index: List[int]) -> Animation:
    """
    Animation for calling one function.

    Args:
        func_unit: Object of function object.
        args_list: List of object of arguments.
        res_item: List of result item.
    """
    for i, item in enumerate(res_list):
        item.move_to(func_unit.get_dst_pos(i, item.elem_width, res_index[i]))

    move_animate_list = []
    args_list_ : List[RegElemUnit] = []
    for i, arg in enumerate(args_list):
        if isinstance(arg, tuple):
            arg[0].move_to(func_unit.get_args_pos(i, arg[0].elem_width, func_args_index[i]))
            args_list_.append(arg[0])
            move_animate_list.append(arg[1])
        else:
            args_list_.append(arg)
            move_animate_list.append(
                arg.animate.move_to(func_unit.get_args_pos(i, arg.elem_width, func_args_index[i])))
    move_animate = \
        AnimationGroup(*move_animate_list)

    fade_animate = \
        AnimationGroup(
            *[FadeIn(res,
                     shift=func_unit.get_dst_pos(i, res.elem_width, res_index[i]) - \
                          func_unit.func_ellipse.get_center())
              for i, res in enumerate(res_list)],
            *[FadeOut(arg,
                      shift=func_unit.func_ellipse.get_center() - \
                          func_unit.get_args_pos(i, arg.elem_width, func_args_index[i]))
               for i, arg in enumerate(args_list_)]
        )
    return Succession(move_animate, Wait(0.5), fade_animate)

#
# Animation with memory.
#
def decl_memory_unit(mem_unit: MemoryUnit) -> Animation:
    """
    Animation for declare one object of memory.

    Args:
        mem_unit: Object of memory.
    """
    return FadeIn(mem_unit)

def read_memory_without_addr(mem_unit: MemoryUnit,
                             addr_item: RegElemUnit,
                             data_item: RegElemUnit) -> Animation:
    """
    Animation for calling one function.

    Args:
        mem_unit: Object of memory unit.
        addr_item: address item.
        data_item: data item.
    """
    data_item.move_to(mem_unit.get_data_pos(data_item.elem_width))

    move_animate = \
        AnimationGroup(addr_item.animate.move_to(mem_unit.get_addr_pos(addr_item.elem_width)))
    fade_animate = \
        AnimationGroup(
            FadeIn(data_item, shift=mem_unit.get_data_pos() - mem_unit.mem_rect.get_center()),
            FadeOut(addr_item, shift=mem_unit.mem_rect.get_center() - mem_unit.get_addr_pos()))

    return Succession(move_animate, fade_animate)

def write_memory_without_addr(mem_unit: MemoryUnit,
                              addr_item: RegElemUnit,
                              data_item: RegElemUnit) -> Animation:
    """
    Animation for calling one function.

    Args:
        mem_unit: Object of memory unit.
        addr_item: address item.
        data_item: data item.
        old_mem_map: Old memory map.
        new_mem_map: New memory map.
    """
    move_animate = \
        AnimationGroup(addr_item.animate.move_to(mem_unit.get_addr_pos(addr_item.elem_width)),
                       data_item.animate.move_to(mem_unit.get_data_pos(data_item.elem_width)))
    fade_animate = \
        AnimationGroup(
            FadeOut(data_item, shift=mem_unit.mem_rect.get_center() - mem_unit.get_data_pos()),
            FadeOut(addr_item, shift=mem_unit.mem_rect.get_center() - mem_unit.get_addr_pos()))

    return Succession(move_animate, fade_animate)

def read_memory(mem_unit: MemoryUnit,
                addr_item: RegElemUnit,
                data_item: RegElemUnit,
                addr_mark: Triangle,
                mem_mark: Rectangle,
                addr_match: bool = True) -> Animation:
    """
    Animation for calling one function.

    Args:
        mem_unit: Object of memory unit.
        addr_item: address item.
        data_item: data item.
        old_mem_map: Old memory map.
        new_mem_map: New memory map.
    """
    if mem_unit.require_serialization:
        # Move address to argument position.
        if addr_match:
            move_animate = addr_item.animate.move_to(mem_unit.get_addr_pos(addr_item.elem_width))
        else:
            move_animate = Wait()

        # Address mark.
        if addr_match:
            addr_animate = Transform(addr_item, addr_mark)
        else:
            addr_animate = FadeIn(addr_mark, shift=addr_mark.get_center() - addr_item.get_center())

        # Data item.
        data_item.move_to(mem_unit.get_data_pos(data_item.elem_width))
        data_animate = AnimationGroup(
            Create(mem_mark),
            FadeIn(data_item,
                   shift=mem_unit.get_data_pos(data_item.elem_width) - mem_mark.get_center()))

        return Succession(move_animate, addr_animate, data_animate)
    else:
        # Move address to argument position.
        if addr_match:
            move_animate = Indicate(addr_item, color=addr_item.elem_color)
        else:
            move_animate = Wait()

        # Address mark.
        if addr_match:
            addr_animate = Transform(addr_item, addr_mark)
        else:
            addr_animate = FadeIn(addr_mark, shift=addr_mark.get_center() - addr_item.get_center())

        # Data item.
        data_animate = Create(mem_mark)

        return Succession(move_animate, addr_animate, data_animate)

def write_memory(mem_unit: MemoryUnit,
                 addr_item: RegElemUnit,
                 data_item: RegElemUnit,
                 addr_mark: Triangle,
                 mem_mark: Rectangle,
                 addr_match: bool = True) -> Animation:
    """
    Animation for calling one function.

    Args:
        mem_unit: Object of memory unit.
        addr_item: address item.
        data_item: data item.
        old_mem_map: Old memory map.
        new_mem_map: New memory map.
    """
    if mem_unit.require_serialization:
        # Move address and data to argument position.
        if addr_match:
            move_animate = AnimationGroup(
                addr_item.animate.move_to(mem_unit.get_addr_pos(addr_item.elem_width)),
                data_item.animate.move_to(mem_unit.get_data_pos(data_item.elem_width)))
        else:
            move_animate = Wait()

        # Address mark.
        if addr_match:
            addr_animate = Transform(addr_item, addr_mark)
        else:
            addr_animate = FadeIn(addr_mark, shift=addr_mark.get_center() - addr_item.get_center())

        # Data mark.
        data_animate = AnimationGroup(
            Create(mem_mark),
            FadeOut(data_item,
                    shift=mem_mark.get_center() - mem_unit.get_data_pos(data_item.elem_width)))

        return Succession(move_animate, addr_animate, data_animate)
    else:
        # Move address to argument position.
        if addr_match:
            move_animate = Indicate(addr_item, color=addr_item.elem_color)
        else:
            move_animate = Wait()

        # Address mark.
        if addr_match:
            addr_animate = Transform(addr_item, addr_mark)
        else:
            addr_animate = FadeIn(addr_mark, shift=addr_mark.get_center() - addr_item.get_center())

        # Data mark.
        data_animate = Transform(data_item, mem_mark)

        return Succession(move_animate, addr_animate, data_animate)
