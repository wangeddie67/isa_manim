"""
Define APIs for animation in ISA data flow, manage animation flow and object placement.
"""

from typing import Dict, List, Union
from manim import Mobject
from ..isa_objects import ElemUnit, RegUnit
from .isa_animate import IsaAnimateItem

class _IsaElemSourceItem:
    """
    Data structure to record the source of one element.
    
    Attributes:
        register: Register where the element comes from.
        index: Element index to access the register.
        reg_idx: Register index to access the register.
        offset: Offset of LSB.
    """
    def __init__(self, register: RegUnit, index: int, reg_idx: int, offset: int):
        """
        Construct the data structure.

        Args:
            register: Register where the element comes from.
            index: Element index to access the register.
            reg_idx: Register index to access the register.
            offset: Offset of LSB.
        """
        self.register: RegUnit = register
        self.index: int = index
        self.reg_idx: int = reg_idx
        self.offset: int = offset

    def is_match(self, register: RegUnit, index: int, reg_idx: int, offset: int) -> bool:
        """
        Check whether the specified arguments match this data structure.

        Args:
            register: Register where the element comes from.
            index: Element index to access the register.
            reg_idx: Register index to access the register.
            offset: Offset of LSB.

        Returns:
            If arguments match, return True.
        """
        return self.register == register and self.index == index \
            and self.reg_idx == reg_idx and self.offset == offset

class _IsaElemRefCountItem:
    """
    Data structure of reference counter.
    
    Attributes:
        refer_count: Reference counter. 0 means there is no reference of this unit.
        last_consumer: Animation to consumer this element unit.
        last_dep: Dependency unit of last animation.
    """
    def __init__(self):
        """
        Constructor data structure of reference counter.

        Reset member variables.
        """
        self.refer_count: int = 0
        self.last_consumer: IsaAnimateItem = None
        self.last_dep: Mobject = None

    def set_producer(self, dep: Mobject):
        """
        Set the producer of element.

        Args:
            dep: Dependency unit.
        """
        self.last_dep = dep

    def set_cusumer(self, consumer: IsaAnimateItem, dep: Mobject):
        """
        Set the consumer of element. Increase the reference counter.

        Args:
            consumer: The animation consumes this animation.
            dep: Dependency unit.
        """
        self.last_consumer = consumer
        self.last_dep = dep
        self.refer_count += 1

    def get_dup_elem(self, elem: ElemUnit) -> ElemUnit:
        """
        Get a copy of element if the element has been referenced.

        If the element has not been referenced, return the element unit itself. Otherwise, return
        a copy of the element.

        Add duplicated element after the last consumer animation.

        Args:
            elem: Element unit.

        Returns:
            Return a copy of the specified element unit.
        """
        if self.refer_count == 0:
            return elem
        else:
            dup_elem = elem.copy()
            # Add duplicate item after last consumer animation.
            if self.last_consumer is not None:
                self.last_consumer.add_before_list.append(dup_elem)

            return dup_elem

class IsaElemRefCount:
    """
    Data structure for element reference counter.
    """
    def __init__(self):
        """
        Construct data structure for element reference counter.

        Attributes:
            elem_source_dict: Dictionary of element source. Key is element unit, and value is
                the source register and the index to access the register.
            elem_refcount_dict: Dictionary of reference counter. Key is element unit, and value
                contains the reference counter and the last consumer and dependency.
        """
        # Element source dictionary
        self.elem_source_dict: Dict[ElemUnit, _IsaElemSourceItem] = {}
        # Element reference counter dictionary
        self.elem_refcount_dict: Dict[ElemUnit, _IsaElemRefCountItem] = {}

    # Element source dictionary
    def set_elem_source(self,
                        elem: ElemUnit, register: RegUnit, reg_idx: int, index: int, offset: int):
        """
        Set the source of one element unit.

        Args:
            elem: Element unit.
            register: The source register.
            reg_idx: Register index to access the register.
            index: Element index to access the reigster.
            offset: LSB offset.
        """
        self.elem_source_dict[elem] = _IsaElemSourceItem(register, index, reg_idx, offset)

    def get_elem_by_source(self,
            register: RegUnit, width: int, reg_idx: int, index: int, offset: int) -> ElemUnit:
        """
        Get one element unit by source.

        Args:
            register: The source register.
            width: Width of element.
            reg_idx: Register index to access the register.
            index: Element index to access the reigster.
            offset: LSB offset.

        Returns:
            Return the element unit specified by the source register and index. Otherwise, return
                None.
        """
        for elem, elem_src in self.elem_source_dict.items():
            if elem_src.is_match(register, index, reg_idx, offset) and elem.elem_width == width:
                return elem
        return None

    # Element reference dictionary
    def set_elem_producer(self, elem: ElemUnit, dep: Mobject):
        """
        Set the producer of one element unit. Called when one animation produces the element unit.

        Args:
            elem: Element unit.
            dep: Last dependency unit, RegUnit, FunctionUnit or MemoryUnit.
        """
        self.elem_refcount_dict[elem] = _IsaElemRefCountItem()
        self.elem_refcount_dict[elem].set_producer(dep)

    def set_elem_cusumer(self, elem: ElemUnit, consumer: IsaAnimateItem, dep: Mobject):
        """
        Set the consumer of one element unit. Called when one animation consumes the element unit.

        Args:
            elem: Element unit.
            consumer: Last consumer animation of this element unit.
            dep: Last dependency unit, RegUnit, FunctionUnit or MemoryUnit.
        """
        self.elem_refcount_dict[elem].set_cusumer(consumer, dep)

    def get_duplicate_item(self, elem: ElemUnit) -> ElemUnit:
        """
        Get a copy of element if the element has been referenced.

        Args:
            elem: Element unit.

        Returns:
            Return a copy of the specified element unit.
        """
        return self.elem_refcount_dict[elem].get_dup_elem(elem)

    # Element dependency dictionary
    def get_last_deps(self, *elem_list: ElemUnit) -> Union[List[Mobject], Mobject, None]:
        """
        Return the depedency units (Registers, Memory and Functions) of specified list.

        - If `elem_list` contains only one element unit, return a single unit.
            - Return None if no dependency unit is found.
        - Otherwise, return a list of units.
            - Return an empty list if no dependency unit is found.

        Returns:
            Return a list of dependency units or a single dependency unit.
        """
        # Get last dependency units of element units
        deps = []
        for elem in elem_list:
            if elem in self.elem_refcount_dict:
                dep = self.elem_refcount_dict[elem].last_dep
                if dep is not None and dep not in deps:
                    deps.append(dep)

        # Return with correct format.
        if len(elem_list) == 1:
            if len(deps) == 1:
                return deps[0]
            else:
                return None
        else:
            return deps
