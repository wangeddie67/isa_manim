"""
Assign element to register.
"""

from ..isa_objects import OneDimReg, OneDimRegElem
from .isa_animate import IsaAnimate
from ..isa_config import get_scene_ratio

def assign_elem(elem: OneDimRegElem,
                vector: OneDimReg,
                size: float = -1.0,
                index: int = 0) -> IsaAnimate:
    """
    Assign element to register, return animation.

    If the new size is not specified, scale element to the same width as elements
    in destination register. Otherwise, scale element to the new specified size.

    Args:
        elem: Element object.
        vector: Register.
        size: Width of destination element in byte.
        e: Index of element.
    """
    if size < 0:
        size = vector.elem_width

    dest_pos = vector.get_elem_center(index=index, elem_width=size)

    # Calculate scaling factor
    old_width = elem.get_elem_width()
    new_width = size * get_scene_ratio()
    scale = new_width / old_width

    if scale != 1.0:
        animate = elem.animate.move_to(dest_pos).stretch(scale, 0)
    else:
        animate = elem.animate.move_to(dest_pos)

    return IsaAnimate(animate=animate, src=elem, dst=elem, dep=[vector])
