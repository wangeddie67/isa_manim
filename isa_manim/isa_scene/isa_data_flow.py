"""
Define APIs for animation in ISA data flow, manage animation flow and object placement.
"""

import itertools
from typing import Any, List, Tuple, Dict, Union
from typing import overload
from colour import Color
import sys
from manim import (WHITE, DEFAULT_FONT_SIZE)
from ..isa_animate import (decl_register,
                           read_elem,
                           assign_elem,
                           replace_elem,
                           decl_func_call,
                           read_func_imm,
                           function_call,
                           decl_memory_unit,
                           read_memory_without_addr,
                           write_memory_without_addr,
                           read_memory,
                           write_memory)
from ..isa_objects import RegElemUnit, RegUnit, FunctionUnit, MemoryUnit
from .isa_animate import IsaAnimationMap, IsaAnimateItem
from .isa_placement import IsaPlacementMap
from .isa_color_map import IsaColorMap
from ..isa_config import get_config

class IsaDataFlow(IsaAnimationMap, IsaPlacementMap, IsaColorMap):
    """
    Data flow of ISA, used to define API for ISA animation.
    """
    def __init__(self,
                 strategy: str ="RB",
                 default_color: Color = WHITE,
                 color_scheme: List[Color] = None,
                 default_font_size: int = 40):
        """
        Construct animation and placement manager.

        Args:
            strategy: Placement strategy, options: RB or BR.
            default_color: Default color of item, used for register and functions.
        """
        IsaAnimationMap.__init__(self)
        IsaPlacementMap.__init__(self, strategy=strategy)
        IsaColorMap.__init__(self, default_color=default_color, color_scheme=color_scheme)

        self.default_font_size = default_font_size

        self.last_dep_map = {}
        self.elem_source_dict: Dict[RegElemUnit, List] = {}
        self.elem_producer_copy: Dict[RegElemUnit, RegElemUnit] = {}
        self.elem_producer_map: Dict[RegElemUnit, IsaAnimateItem] = {}
        self.elem_refer_count: Dict[RegElemUnit, int] = {}
        self.elem_last_consumer: Dict[RegElemUnit, IsaAnimateItem] = {}

    def _traceback_hash(self, depth: int = 2) -> int:
        """
        Return hash value according to traceback.
        """
        # frame 0 is _traceback_hash
        # frame 1 is animation API
        # frame 2 is the caller of animation API
        frame = sys._getframe(depth)    # pylint: disable=protected-access
        return hash(str(frame))

    def _set_item_producer(self,
                           item: RegElemUnit,
                           producer: IsaAnimateItem,
                           copy_item: RegElemUnit = None):
        """
        Set producer of element.
        """
        self.elem_producer_map[item] = producer
        self.elem_producer_copy[item] = item.copy() if copy_item is None else copy_item.copy()
        self.elem_refer_count[item] = 0
        self.elem_last_consumer[item] = None

    def _set_item_cusumer(self,
                          item: RegElemUnit,
                          consumer: IsaAnimateItem):
        """
        Set consumer of element.
        """
        self.elem_last_consumer[item] = consumer

    def _get_duplicate_item(self,
                            item: RegElemUnit) -> RegElemUnit:
        """
        Get a copy of element if the element has been referenced.
        """
        if self.elem_refer_count[item] == 0:
            item_ = item
        else:
            item_ = self.elem_producer_copy[item]
            self.elem_producer_copy[item] = self.elem_producer_copy[item].copy()
        self.elem_refer_count[item] += 1
        self.elem_producer_map[item].add_copy_item(item_)

        if self.elem_last_consumer[item] is not None:
            self.elem_last_consumer[item].add_before.append(item_)

        return item_

    def _set_elem_source_elem(self,
                              elem: RegElemUnit,
                              vector: RegUnit,
                              size: float,
                              reg_idx: int,
                              index: int,
                              offset: int):
        self.elem_source_dict[elem] = [vector, size, reg_idx, index, offset]

    def _get_elem_source_elem(self,
                              vector: RegUnit,
                              size: float = -1.0,
                              reg_idx: int = 0,
                              index: int = 0,
                              offset: int = 0):
        for elem, elem_src in self.elem_source_dict.items():
            elem_src_vector, elem_src_size, elem_src_reg_idx, elem_src_index, elem_src_offset = \
                elem_src
            if elem_src_vector == vector and elem_src_size == size \
                    and elem_src_reg_idx == reg_idx and elem_src_index == index \
                    and elem_src_offset == offset:
                return elem
        return None

    #
    # Animations APIs
    #
    @overload
    def decl_register(self,
                      text: str,
                      width: int,
                      elements: int,
                      nreg: int,
                      value: List[List[Any]] = None,
                      font_size: int = DEFAULT_FONT_SIZE,
                      value_format: str = None,
                      align_with = None) -> RegUnit: ...

    @overload
    def decl_register(self,
                      text: str,
                      width: int,
                      elements: int,
                      value: List[Any] = None,
                      font_size: int = DEFAULT_FONT_SIZE,
                      value_format: str = None,
                      align_with = None) -> RegUnit: ...

    @overload
    def decl_register(self,
                      text: str,
                      width: int,
                      value: Any = None,
                      font_size: int = DEFAULT_FONT_SIZE,
                      value_format: str = None,
                      align_with = None) -> RegUnit: ...

    def decl_register(self,
                      text: str,
                      width: int,
                      elements: int = 1,
                      nreg: int = 1,
                      value: List[List[Any]] = None,
                      font_size: int = DEFAULT_FONT_SIZE,
                      value_format: str = None,
                      align_with = None) -> RegUnit:
        """
        Declare register unit.
        
        Attributes:
            text: Name of this register.
            width: Width of this register width, in bit.
            elements: Elements count in this register, or horizontal size of this register.
                Optional and positinal.
            nreg: Number of registers, or vertical size of this register. Optional and positinal.
            value: Value of this register, single element or 1-D/2-D array. Optional and keyword.
            font_size: Font size of register name. Optional and keyword.
            align_width: Align with specified element when placement.
        """
        # Handle default value of arguments.
        if value_format is None:
            value_format = get_config("elem_value_format")

        # Create register unit.
        color = self.colormap_default_color
        reg_unit = RegUnit(text, color, width, elements, nreg, value, font_size, value_format)

        # Placement
        self.placement_add_object(reg_unit, align_with=align_with)
        # Animation
        self.animation_add_animation(animate=decl_register(reg_unit), src=None, dst=reg_unit)

        # Return register unit.
        return reg_unit

    @overload
    def read_elem(self,
                  vector: RegUnit,
                  index: int,
                  reg_idx: int,
                  offset: int = 0,
                  size: float = -1.0,
                  color_hash = None,
                  value = None,
                  fill_opacity: float = 0.5,
                  font_size: int = DEFAULT_FONT_SIZE,
                  value_format: str = None) -> RegElemUnit: ...

    @overload
    def read_elem(self,
                  vector: RegUnit,
                  index: int,
                  offset: int = 0,
                  size: float = -1.0,
                  value = None,
                  color_hash = None,
                  fill_opacity: float = 0.5,
                  font_size: int = DEFAULT_FONT_SIZE,
                  value_format: str = None) -> RegElemUnit: ...

    @overload
    def read_elem(self,
                  vector: RegUnit,
                  offset: int = 0,
                  size: float = -1.0,
                  value = None,
                  color_hash = None,
                  fill_opacity: float = 0.5,
                  font_size: int = DEFAULT_FONT_SIZE,
                  value_format: str = None) -> RegElemUnit: ...

    def read_elem(self,
                  vector: RegUnit,
                  index: int = 0,
                  reg_idx: int = 0,
                  offset: int = 0,
                  size: float = -1.0,
                  color_hash = None,
                  value = None,
                  fill_opacity: float = 0.5,
                  font_size: int = DEFAULT_FONT_SIZE,
                  value_format: str = None) -> RegElemUnit:
        """
        Read element from register, return one Rectangle.

        Args:
            vector: Register.
            color: Color of new element.
            size: Width of element in byte.
            e: Index of element.
            kargs: Arguments to new element.
        """
        value_format = vector.reg_value_format if value_format is None else value_format
        size = vector.elem_width if size < 0 else size
        value = value if value is not None else vector.get_elem_value(index, reg_idx)

        color = self.colormap_get_color(
            self._traceback_hash() if color_hash is None else color_hash)

        elem = self._get_elem_source_elem(
            vector=vector, size=size, reg_idx=reg_idx, index=index, offset=offset)
        if elem is None:
            elem = RegElemUnit(color, size, value, fill_opacity, font_size, value_format, 0, False)
            self._set_elem_source_elem(
                elem=elem, vector=vector, size=size, reg_idx=reg_idx, index=index, offset=offset)

            self.last_dep_map[elem] = vector

            animation_item = self.animation_add_animation(
                animate=read_elem(vector, elem, reg_idx=reg_idx, index=index, offset=offset),
                src=vector,
                dst=elem,
                dep=[vector])
            self._set_item_producer(elem, animation_item)
        return elem

    @overload
    def move_elem(self,
                  elem: RegElemUnit,
                  vector: RegUnit,
                  index: int,
                  reg_idx: int,
                  offset: int = 0,
                  size: float = -1.0): ...

    @overload
    def move_elem(self,
                  elem: RegElemUnit,
                  vector: RegUnit,
                  index: int,
                  offset: int = 0,
                  size: float = -1.0): ...

    def move_elem(self,
                  elem: RegElemUnit,
                  vector: RegUnit,
                  index: int = 0,
                  reg_idx: int = 0,
                  offset: int = 0,
                  size: float = -1.0):
        """
        Move element to register, add animate to list.

        Args:
            elem: Element object.
            vector: Register.
            size: Width of element in byte.
            e: Index of element.
        """
        if elem.elem_value is not None:
            vector.set_elem_value(elem.elem_value, index, reg_idx)

        old_dep = None
        if elem in self.last_dep_map:
            old_dep = self.last_dep_map[elem]
            del self.last_dep_map[elem]
        self.last_dep_map[elem] = vector

        elem_ = self._get_duplicate_item(elem)
        elem_width = elem.elem_width if size <= 0 else size
        new_elem = RegElemUnit(
            elem.elem_color, elem_width, elem.elem_value,
            elem.elem_fill_opacity, elem.elem_font_size, elem.elem_value_format, 0, False)

        animation_item = self.animation_add_animation(
            animate=assign_elem(elem_, new_elem, vector, reg_idx, index, offset),
            src=[elem, elem_],
            dst=new_elem,
            dep=[old_dep, vector] if old_dep else [vector],
            remove_after=[elem_],
            add_after=[new_elem])
        self._set_item_cusumer(elem, animation_item)
        self._set_item_producer(new_elem, animation_item, copy_item=new_elem)

        self.last_dep_map[new_elem] = vector

        return new_elem

    def data_extend(self,
                    elem: RegElemUnit,
                    size: float,
                    zero_extend: bool = False,
                    value = None) -> RegElemUnit:
        """
        Animate of data convert.
        """
        new_value = value if value is not None else elem.elem_value
        if size > elem.elem_width:
            high_bits = size - elem.elem_width if zero_extend else size - elem.elem_width + 1
        else:
            high_bits = 0
        new_elem = RegElemUnit(elem.elem_color, size, new_value,
                               elem.elem_fill_opacity, elem.elem_font_size, elem.elem_value_format,
                               high_bits, zero_extend)

        old_dep = None
        if elem in self.last_dep_map:
            old_dep = self.last_dep_map[elem]

        elem_ = self._get_duplicate_item(elem)

        animation_item = self.animation_add_animation(
            animate=replace_elem(old_elem=elem_, new_elem=new_elem, align="right"),
            src=[elem, elem_],
            dst=new_elem,
            dep=old_dep,
            remove_after=[elem_],
            add_after=[new_elem])
        self._set_item_cusumer(elem, animation_item)
        self._set_item_producer(new_elem, animation_item, copy_item=new_elem)

        if old_dep:
            self.last_dep_map[new_elem] = old_dep

        return new_elem

    #
    # Function behavior
    #
    def decl_function(self,
                      isa_hash: str,
                      args_width: List[float],
                      res_size: Union[int, List[int]],
                      func_name: str = None,
                      args_name: List[str] = None,
                      font_size: int = DEFAULT_FONT_SIZE,
                      value_format: str = None,
                      align_with = None,
                      func_callee = None) -> FunctionUnit:
        """
        Animation of declare function call.
        
        Used to control placement and animation.
        """
        # Handle default value of arguments.
        if not func_name:
            func_name = isa_hash
        if value_format is None:
            value_format = get_config("elem_value_format")
        if not isinstance(res_size, list):
            res_size = [res_size]

        if self.placement_has_object(isa_hash):
            func_unit = self.placement_get_object(isa_hash)
        else:
            func_color = self.colormap_default_color
            func_unit = FunctionUnit(
                func_name, func_color, args_width, res_size, args_name,
                font_size, value_format, func_callee)
            self.placement_add_object(func_unit, isa_hash, align_with=align_with)

            self.animation_add_animation(
                animate=decl_func_call(func_unit), src=None, dst=func_unit)

        return func_unit

    def decl_func_group(self,
                        num_unit: Union[int, List[int]],
                        isa_hash: Union[str, List[str]],
                        args_width: List[float],
                        res_size: Union[int, List[int]],
                        func_name: Union[str, List[str]] = None,
                        args_name: List[str] = None,
                        font_size: int = DEFAULT_FONT_SIZE,
                        value_format: str = None,
                        force_hw_ratio: bool = False,
                        func_callee = None) -> List[FunctionUnit]:
        """
        Animation of declare a group of function call.
        
        Used to control placement and animation.
        """
        # Handle default value of arguments.
        if not func_name:
            func_name = isa_hash
        if not isinstance(res_size, list):
            res_size = [res_size]
        if value_format is None:
            value_format = get_config("elem_value_format")
        if isinstance(num_unit, int):
            num_unit = [num_unit]

        func_unit_list = []
        func_unit_hash = []
        num_id_list = itertools.product(*[list(range(0, numi)) for numi in num_unit])
        for num_id in num_id_list:
            if func_name:
                func_ = func_name
                if isinstance(func_name, list):
                    for sub_id in num_id:
                        func_ = func_[sub_id]
            else:
                if not isinstance(isa_hash, list):
                    func_ = isa_hash + "_".join([str(sub_id) for sub_id in num_id])
                else:
                    func_ = isa_hash
                    for sub_id in num_id:
                        func_ = func_[sub_id]

            func_color = self.colormap_default_color
            func_unit = FunctionUnit(
                func_, func_color, args_width, res_size, args_name,
                font_size, value_format, func_callee)

            if not isinstance(isa_hash, list):
                func_hash = isa_hash + "_".join([str(sub_id) for sub_id in num_id])
            else:
                func_hash = isa_hash
                for sub_id in num_id:
                    func_hash = func_hash[sub_id]

            func_unit_list.append(func_unit)
            func_unit_hash.append(func_hash)

        self.placement_add_object_group(func_unit_list, func_unit_hash,
                                        force_hw_ratio=num_unit if force_hw_ratio else None)

        self.animation_add_animation(
            animate=decl_func_call(*func_unit_list), src=None, dst=func_unit_list)

        return func_unit_list

    def function_call(self,
                      func_isa_hash: str,
                      args: List[RegElemUnit],
                      func_args_index: List[int] = None,
                      res_width: Union[int, List[int]] = None,
                      res_color_hash = None,
                      res_index: Union[int, List[int]] = None,
                      res_value: Union[Any, List[Any]] = None,
                      res_fill_opacity: float = 0.5,
                      res_font_size: int = DEFAULT_FONT_SIZE,
                      res_value_format: str = None) -> Union[RegElemUnit, List[RegElemUnit]]:
        """
        Animate of Function call.
        """
        if res_width is not None and not isinstance(res_width, list):
            res_width = [res_width]
        if res_index is not None and not isinstance(res_index, list):
            res_index = [res_index]
        if res_value is not None and not isinstance(res_value, list):
            res_value = [res_value]

        args_item: List[RegElemUnit] = []
        args_item_exist: List[RegElemUnit] = []
        for item in args:
            if isinstance(item, tuple):
                args_item.append(item[0])
            else:
                args_item.append(item)
                args_item_exist.append(item)

        if self.placement_has_object(func_isa_hash):
            func_unit: FunctionUnit = self.placement_get_object(func_isa_hash)
        if res_value_format is None:
            res_value_format = func_unit.func_value_format
        if res_width is None:
            res_width = func_unit.func_res_width
        if res_index is None:
            res_index = [0 for _ in range (0, func_unit.func_res_count)]
        if func_args_index is None:
            func_args_index = [0 for _ in args]

        # Arguments
        old_dep = []
        args_ = []
        args_exist_ = []
        for arg in args:
            if isinstance(arg, tuple):
                args_.append(arg)
            else:
                if arg in self.last_dep_map:
                    old_dep.append(self.last_dep_map[arg])
                    del self.last_dep_map[arg]

                arg_ = self._get_duplicate_item(arg)
                args_.append(arg_)
                args_exist_.append(arg_)

        # Function callee
        args_item_value: List = [arg.elem_value for arg in args_item]
        if (res_value is None) and (func_unit.func_callee is not None) \
                and (None not in args_item_value):
            res_value = func_unit.func_callee(*args_item_value)
        if not isinstance(res_value, list):
            res_value = [res_value] * len(res_width)

        # Result elements
        res_color_list = self.colormap_get_multi_color(
            len(res_width), self._traceback_hash() if res_color_hash is None else res_color_hash)
        res_elem_list = []

        for res_width_, res_value_, res_color in zip(res_width, res_value, res_color_list):
            res_elem = RegElemUnit(
                res_color, res_width_, res_value_,
                res_fill_opacity, res_font_size, res_value_format, 0, False)
            self.last_dep_map[res_elem] = func_unit
            res_elem_list.append(res_elem)

        animation_item = self.animation_add_animation(
            animate=function_call(func_unit=func_unit,
                                  args_list=args_,
                                  res_list=res_elem_list,
                                  func_args_index=func_args_index,
                                  res_index=res_index),
            src=args_item_exist + args_exist_,
            dst=res_elem,
            dep=(old_dep + [func_unit]) if old_dep else [func_unit])
        for arg in args_item_exist:
            self._set_item_cusumer(arg, animation_item)
        for res in res_elem_list:
            self._set_item_producer(res, animation_item)

        return res_elem_list[0] if len(res_elem_list) == 1 else res_elem_list

    def read_func_imm(self,
                      size: float,
                      color_hash = None,
                      value = None,
                      fill_opacity: float = 0.5,
                      font_size: int = DEFAULT_FONT_SIZE,
                      value_format: str = None) -> RegElemUnit:
        """
        Animate of Function call.
        """
        # Handle default value of arguments.
        if value_format is None:
            value_format = get_config("elem_value_format")

        res_color = self.colormap_get_color(
            self._traceback_hash() if color_hash is None else color_hash)
        res_elem = RegElemUnit(
            res_color, size, value, fill_opacity, font_size, value_format, 0, False)

        return read_func_imm(elem=res_elem)

    #
    # Memory
    #
    def decl_memory(self,   # pylint: disable=dangerous-default-value
                    addr_width: int,
                    data_width: int,
                    mem_range: List[Tuple[int]],
                    isa_hash: str = None,
                    addr_align: int = None,
                    font_size = DEFAULT_FONT_SIZE,
                    value_format: str = None,
                    para_enable = False) -> MemoryUnit:
        """
        Animation of declare memory.

        Used to control placement and animation.
        """
        # Handle default value of arguments.
        if addr_align is None:
            addr_align = get_config("mem_align")
        if value_format is None:
            value_format = get_config("elem_value_format")

        if not isa_hash:
            isa_hash = "Memory"

        if self.placement_has_object(isa_hash):
            mem_unit = self.placement_get_object(isa_hash)
        else:
            mem_unit = MemoryUnit(color=WHITE,
                                  addr_width=addr_width,
                                  data_width=data_width,
                                  addr_align=addr_align,
                                  mem_range=mem_range,
                                  font_size=font_size,
                                  value_format=value_format,
                                  para_enable=para_enable,
                                  mem_map_width=self.placement_width() - 2)
            self.placement_add_object(mem_unit, "Memory")

            self.animation_add_animation(
                animate=decl_memory_unit(mem_unit), src=None, dst=mem_unit)

        return mem_unit

    def read_memory(self,   # pylint: disable=dangerous-default-value
                    addr: RegElemUnit,
                    size: int,
                    offset: int = 0,
                    addr_match: bool = False,
                    res_color_hash = None,
                    res_value = None,
                    res_fill_opacity: float = 0.5,
                    res_font_size: int = DEFAULT_FONT_SIZE,
                    res_value_format: str = None,
                    mem_isa_hash: str = None) -> RegElemUnit:
        """
        Animate of read memory.
        """
        if not mem_isa_hash:
            mem_isa_hash = "Memory"
        mem_unit: MemoryUnit = self.placement_get_object(mem_isa_hash)
        res_value_format = mem_unit.mem_value_format if res_value_format is None else \
                           res_value_format

        addr_value = None
        if addr.elem_value is not None:
            addr_value = int(addr.elem_value) + offset
            if not mem_unit.is_mem_range_cover(addr_value):
                addr_value = None
        addr_match = addr_value is not None and offset == 0

        data_color = self.colormap_get_color(
            self._traceback_hash() if res_color_hash is None else res_color_hash)
        data = RegElemUnit(
            data_color, size, res_value, res_fill_opacity, res_font_size, res_value_format,
            0, False)

        old_dep = []
        if addr in self.last_dep_map:
            old_dep.append(self.last_dep_map[addr])
            del self.last_dep_map[addr]

        if addr_match:
            addr_ = self._get_duplicate_item(addr)
        else:
            addr_ = addr

        self.last_dep_map[data] = mem_unit

        if addr_value is not None:
            addr_mark = mem_unit.get_addr_mark(addr=addr_value,
                                               color=addr_.elem_color)
            mem_mark = mem_unit.get_rd_mem_mark(laddr=addr_value,
                                                raddr=addr_value + size // 8,
                                                color=data_color)
            mem_unit.append_mem_mark_list(mem_mark)
            if not mem_unit.require_serialization:
                data = data.stretch_to_fit_width(mem_mark.width) \
                    .stretch_to_fit_height(mem_mark.height) \
                    .move_to(mem_mark.get_center())

            animation_item = self.animation_add_animation(
                animate=read_memory(mem_unit=mem_unit,
                                    addr_item=addr_,
                                    data_item=data,
                                    addr_mark=addr_mark,
                                    mem_mark=mem_mark,
                                    addr_match=addr_match),
                src=[addr, addr_],
                dst=[data, mem_mark],
                dep=old_dep + [mem_unit],
                remove_after=[addr_] if addr_match else [addr_mark])
            self._set_item_cusumer(addr, animation_item)
            self._set_item_producer(data, animation_item)
        else:
            animation_item = self.animation_add_animation(
                animate=read_memory_without_addr(
                    mem_unit=mem_unit, addr_item=addr_, data_item=data),
                src=[addr, addr_],
                dst=[data],
                dep=old_dep + [mem_unit],
                remove_after=[addr_])
            self._set_item_cusumer(addr, animation_item)
            self._set_item_producer(data, animation_item)

        return data

    def write_memory(self,  # pylint: disable=dangerous-default-value
                     addr: RegElemUnit,
                     data: RegElemUnit,
                     offset: int = 0,
                     addr_match: bool = False,
                     mem_isa_hash: str = None) -> None:
        """
        Animate of write memory.
        """
        if not mem_isa_hash:
            mem_isa_hash = "Memory"
        mem_unit: MemoryUnit = self.placement_get_object(mem_isa_hash)

        addr_value = None
        if addr.elem_value is not None:
            addr_value = int(addr.elem_value) + offset
            if not mem_unit.is_mem_range_cover(addr_value):
                addr_value = None
        addr_match = addr_value is not None and offset == 0

        old_dep = []
        if addr in self.last_dep_map:
            old_dep.append(self.last_dep_map[addr])
            del self.last_dep_map[addr]

        if addr_match:
            addr_ = self._get_duplicate_item(addr)
        else:
            addr_ = addr

        if data in self.last_dep_map:
            old_dep.append(self.last_dep_map[data])
            del self.last_dep_map[data]

        data_ = self._get_duplicate_item(data)

        if addr_value is not None:
            addr_mark = mem_unit.get_addr_mark(addr=addr_value,
                                               color=addr_.elem_color)
            mem_mark = mem_unit.get_wt_mem_mark(laddr=addr_value,
                                                raddr=addr_value + data.elem_width // 8,
                                                color=data_.elem_rect.color)
            mem_unit.append_mem_mark_list(mem_mark)

            animation_item = self.animation_add_animation(
                animate=write_memory(mem_unit=mem_unit,
                                     addr_item=addr_,
                                     data_item=data_,
                                     addr_mark=addr_mark,
                                     mem_mark=mem_mark,
                                     addr_match=addr_match),
                src=[addr, data, addr_, data_],
                dst=[mem_mark],
                dep=old_dep + [mem_unit],
                remove_after=[addr_, data_] if addr_match else [addr_mark, data_],
                add_after=[mem_mark])
            self._set_item_cusumer(addr, animation_item)
            self._set_item_cusumer(data, animation_item)
        else:
            animation_item = self.animation_add_animation(
                animate=write_memory_without_addr(
                    mem_unit=mem_unit, addr_item=addr_, data_item=data_),
                src=[addr, data, addr_, data_],
                dst=[],
                dep=old_dep + [mem_unit],
                remove_after=[addr_])
            self._set_item_cusumer(addr, animation_item)
            self._set_item_cusumer(data, animation_item)
