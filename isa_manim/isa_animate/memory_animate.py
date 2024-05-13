"""
Animation with Memory Unit.
"""

from typing import Union
from manim import (AnimationGroup, Succession, FadeIn, FadeOut, Animation, Transform, Create,
                   Indicate, Wait,
                   Rectangle, Triangle)
from ..isa_objects import (ElemUnit, MemoryUnit)

def decl_memory_unit(mem_unit: MemoryUnit) -> Animation:
    """
    Declare one memory unit.

    Args:
        mem_unit: Object of memory.

    Returns:
        Animation to declare memory unit.
    """
    return FadeIn(mem_unit)

def read_memory_without_addr(mem_unit: MemoryUnit,
                             addr_item: ElemUnit,
                             data_item: ElemUnit,
                             status_item: Union[ElemUnit, None]) -> Animation:
    """
    Read data from one memory unit.

    Because the address element does not provide an address, or the provided address does not match
    the range of memory maps, address marks and memory marks cannot be generated and displayed.

    Step of this animation is as below:

    - Move the address element to the address port.
    - Fadeout the address element and fadein the data element.
    - Fadein the status element if `status_item` is provided and the `mem_unit` has `status_rect`.

    Args:
        mem_unit: Object of memory unit.
        addr_item: Address element.
        data_item: Data element.
        status_item: Status element.

    Returns:
        Animation to read data from memory unit.
    """
    # Move the address element to the address port
    move_animate = \
        addr_item.animate.move_to(mem_unit.get_addr_pos(addr_item.elem_width))

    # Fadeout address element and fadein data element.
    data_item.move_to(mem_unit.get_data_pos(data_item.elem_width))
    fade_animate = AnimationGroup(
        FadeIn(data_item,
               shift=mem_unit.get_data_pos(data_item.elem_width) - mem_unit.mem_rect.get_center()),
        FadeOut(addr_item,
                shift=mem_unit.mem_rect.get_center() - mem_unit.get_addr_pos(addr_item.elem_width)))

    # Fadein status element.
    if mem_unit.mem_status_width > 0 and status_item is not None:
        status_item.move_to(mem_unit.get_status_pos(status_item.elem_width))
        status_animate = FadeIn(status_item)

    # Return animation sequence.
    if mem_unit.mem_status_width > 0 and status_item is not None:
        return Succession(move_animate, fade_animate, status_animate)
    else:
        return Succession(move_animate, fade_animate)

def write_memory_without_addr(mem_unit: MemoryUnit,
                              addr_item: ElemUnit,
                              data_item: ElemUnit,
                              status_item: Union[ElemUnit, None]) -> Animation:
    """
    Write data to one memory unit.

    Because the address element does not provide an address, or the provided address does not match
    the range of memory maps, address marks and memory marks cannot be generated and displayed.

    Step of this animation is as below:

    - Move the address element to the address port, and move the data element to the data port.
    - Fadeout the address element and data element.
    - Fadein the status element if `status_item` is provided and the `mem_unit` has `status_rect`.

    Args:
        mem_unit: Object of memory unit.
        addr_item: Address element.
        data_item: Data element.
        status_item: Status element.

    Returns:
        Animation to write data to memory unit.
    """
    # Move the address element to the address port, and move the data element to the data port
    move_animate = AnimationGroup( \
        addr_item.animate.move_to(mem_unit.get_addr_pos(addr_item.elem_width)),
        data_item.animate.move_to(mem_unit.get_data_pos(data_item.elem_width)))

    # Fadeout address element and data element.
    fade_animate = AnimationGroup(
        FadeOut(data_item,
                shift=mem_unit.mem_rect.get_center() - mem_unit.get_data_pos(data_item.elem_width)),
        FadeOut(addr_item,
                shift=mem_unit.mem_rect.get_center() - mem_unit.get_addr_pos(addr_item.elem_width)))

    # Fadein status element.
    if mem_unit.mem_status_width > 0 and status_item is not None:
        status_item.move_to(mem_unit.get_status_pos(status_item.elem_width))
        status_animate = FadeIn(status_item)

    # Return animation sequence.
    if mem_unit.mem_status_width > 0 and status_item is not None:
        return Succession(move_animate, fade_animate, status_animate)
    else:
        return Succession(move_animate, fade_animate)

def read_memory(mem_unit: MemoryUnit,
                addr_item: ElemUnit,
                data_item: ElemUnit,
                status_item: Union[ElemUnit, None],
                addr_mark: Triangle,
                mem_mark: Rectangle,
                addr_match: bool) -> Animation:
    """
    Read data from one memory unit.

    Step of this animation is as below:

    - Move the address element to the address port only when the memory unit does not allow parallel
        animations and the actual address matches value in `addr_item`.
        - Highlight indicate the address element when the memory unit allows parallel animations
            and the actual address matches value in `addr_item`.
        - Otherwise, wait 1s.
    - Transform the address element to the address mark on the matched memory map.
        - If the actual address to read is not same as the value in `addr_item`, fadein the address
            mark.
    - Create memory mark on the matched memory map.
    - Move memory mark to the data port if the memory unit only allows serialized animations.
    - Fadein the status element if `status_item` is provided and the `mem_unit` has `status_rect`.

    Args:
        mem_unit: Object of memory unit.
        addr_item: Address element.
        data_item: Data element.
        status_item: Status element.
        addr_mark: Address mark.
        mem_mark: Memory mark.
        addr_match: True means the actual address to read is same as the value of `addr_item`.

    Returns:
        Animation to read data from memory unit.
    """
    # Move address to argument position.
    if addr_match:
        if mem_unit.require_serialization:
            move_animate = addr_item.animate.move_to(mem_unit.get_addr_pos(addr_item.elem_width))
        else:
            move_animate = Indicate(addr_item, color=addr_item.elem_color)
    else:
        move_animate = Wait()

    # Address mark.
    if addr_match:
        addr_animate = Transform(addr_item, addr_mark)
    else:
        addr_animate = FadeIn(addr_mark, shift=addr_mark.get_center() - addr_item.get_center())

    # Data item.
    if mem_unit.require_serialization:
        data_item.move_to(mem_unit.get_data_pos(data_item.elem_width))
        data_animate = AnimationGroup(
            Create(mem_mark),
            FadeIn(data_item,
                   shift=mem_unit.get_data_pos(data_item.elem_width) - mem_mark.get_center()))
    else:
        data_item.stretch_to_fit_width(mem_mark.width) \
                 .stretch_to_fit_height(mem_mark.height) \
                 .move_to(mem_mark.get_center())
        data_animate = Create(mem_mark)

    # Fadein status element.
    if mem_unit.mem_status_width > 0 and status_item is not None:
        status_item.move_to(mem_unit.get_status_pos(status_item.elem_width))
        status_animate = FadeIn(status_item)

    # Return animation sequence.
    if mem_unit.mem_status_width > 0 and status_item is not None:
        return Succession(move_animate, addr_animate, data_animate, status_animate)
    else:
        return Succession(move_animate, addr_animate, data_animate)

def write_memory(mem_unit: MemoryUnit,
                 addr_item: ElemUnit,
                 data_item: ElemUnit,
                 status_item: Union[ElemUnit, None],
                 addr_mark: Triangle,
                 mem_mark: Rectangle,
                 addr_match: bool) -> Animation:
    """
    Write data to one memory unit.

    Step of this animation is as below:

    - Move the address element to the address port and move the data element to the data port only
        when the memory unit does not allow parallel animations and the actual address matches value
        in `addr_item`.
        - Highlight indicate the address element when the memory unit allows parallel animations
            and the actual address matches value in `addr_item`.
        - Otherwise, wait 1s.
    - Transform the address element to the address mark on the matched memory map.
        - If the actual address to read is not same as the value in `addr_item`, fadein the address
            mark.
    - Move the data element to the data port to the memory mark if the memory unit only allows
        serialized animations.
        - Otherwise, create memory mark on the matched memory map.
    - Fadein the status element if `status_item` is provided and the `mem_unit` has `status_rect`.

    Args:
        mem_unit: Object of memory unit.
        addr_item: Address element.
        data_item: Data element.
        status_item: Status element.
        addr_mark: Address mark.
        mem_mark: Memory mark.
        addr_match: True means the actual address to write is same as the value of `addr_item`.

    Returns:
        Animation to write data to memory unit.
    """
    # Move address and data to argument position.
    if addr_match:
        if mem_unit.require_serialization:
            move_animate = AnimationGroup(
                addr_item.animate.move_to(mem_unit.get_addr_pos(addr_item.elem_width)),
                data_item.animate.move_to(mem_unit.get_data_pos(data_item.elem_width)))
        else:
            move_animate = Indicate(addr_item, color=addr_item.elem_color)
    else:
        move_animate = Wait()

    # Address mark.
    if addr_match:
        addr_animate = Transform(addr_item, addr_mark)
    else:
        addr_animate = FadeIn(addr_mark, shift=addr_mark.get_center() - addr_item.get_center())

    # Data mark.
    if mem_unit.require_serialization:
        data_animate = AnimationGroup(
            Create(mem_mark),
            FadeOut(data_item,
                    shift=mem_mark.get_center() - mem_unit.get_data_pos(data_item.elem_width)))
    else:
        data_animate = Transform(data_item, mem_mark)

    # Fadein status element.
    if mem_unit.mem_status_width > 0 and status_item is not None:
        status_item.move_to(mem_unit.get_status_pos(status_item.elem_width))
        status_animate = FadeIn(status_item)

    # Return animation sequence.
    if mem_unit.mem_status_width > 0 and status_item is not None:
        return Succession(move_animate, addr_animate, data_animate, status_animate)
    else:
        return Succession(move_animate, addr_animate, data_animate)
