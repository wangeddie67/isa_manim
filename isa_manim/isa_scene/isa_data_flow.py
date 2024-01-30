"""
Define APIs for animation in ISA data flow, manage animation flow and object placement.
"""

import itertools
from typing import List, Tuple, Dict, Union
from colour import Color
import sys
from manim import (WHITE, DEFAULT_FONT_SIZE)
from ..isa_animate import (decl_register,
                           replace_register,
                           concat_vector,
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
from ..isa_objects import OneDimReg, OneDimRegElem, TwoDimReg, FunctionUnit, MemoryUnit
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
        self.elem_source_dict: Dict[OneDimRegElem, List] = {}
        self.elem_producer_copy: Dict[OneDimRegElem, OneDimRegElem] = {}
        self.elem_producer_map: Dict[OneDimRegElem, IsaAnimateItem] = {}
        self.elem_refer_count: Dict[OneDimRegElem, int] = {}
        self.elem_last_consumer: Dict[OneDimRegElem, IsaAnimateItem] = {}

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
                           item: OneDimRegElem,
                           producer: IsaAnimateItem,
                           copy_item: OneDimRegElem = None):
        """
        Set producer of element.
        """
        self.elem_producer_map[item] = producer
        self.elem_producer_copy[item] = item.copy() if copy_item is None else copy_item.copy()
        self.elem_refer_count[item] = 0
        self.elem_last_consumer[item] = None

    def _set_item_cusumer(self,
                          item: OneDimRegElem,
                          consumer: IsaAnimateItem):
        """
        Set consumer of element.
        """
        self.elem_last_consumer[item] = consumer

    def _get_duplicate_item(self,
                            item: OneDimRegElem) -> OneDimRegElem:
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
                              elem: OneDimRegElem,
                              vector: OneDimReg,
                              size: float,
                              reg_idx: int,
                              index: int,
                              offset: int):
        self.elem_source_dict[elem] = [vector, size, reg_idx, index, offset]

    def _get_elem_source_elem(self,
                              vector: OneDimReg,
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
    def decl_scalar(self,
                    text: str,
                    width: int,
                    font_size: int = DEFAULT_FONT_SIZE,
                    label_pos = None,
                    align_with = None) -> OneDimReg:
        """
        Declare scalar variables, return one-dim register.
        """
        color = self.colormap_default_color
        scalar_reg = OneDimReg(text=text,
                               color=color,
                               width=width,
                               elements=1,
                               font_size=font_size,
                               label_pos=label_pos)
        self.placement_add_object(scalar_reg, align_with=align_with)

        self.animation_add_animation(animate=decl_register(scalar_reg), src=None, dst=scalar_reg)
        return scalar_reg

    def decl_vector(self,
                    text: str,
                    width: int,
                    elements: int = 1,
                    font_size: int = DEFAULT_FONT_SIZE,
                    label_pos = None,
                    align_with = None) -> OneDimReg:
        """
        Declare vector variables, return one-dim register.
        """
        color = self.colormap_default_color
        vector_reg = OneDimReg(text=text,
                               color=color,
                               width=width,
                               elements=elements,
                               font_size=font_size,
                               label_pos=label_pos)
        self.placement_add_object(vector_reg, align_with=align_with)

        self.animation_add_animation(animate=decl_register(vector_reg), src=None, dst=vector_reg)
        return vector_reg

    def decl_vector_group(self,
                          text_list: List[str],
                          width: int,
                          elements: int = 1,
                          font_size: int = DEFAULT_FONT_SIZE,
                          label_pos = None) -> TwoDimReg:
        """
        Declare a list of vector variables, return a two-dim register.
        """
        color = self.colormap_default_color
        nreg = len(text_list)
        vector_reg = TwoDimReg(text=text_list,
                               color=color,
                               nreg=nreg,
                               width=width,
                               elements=elements,
                               font_size=font_size,
                               label_pos=label_pos)
        self.placement_add_object(vector_reg)

        self.animation_add_animation(animate=decl_register(vector_reg), src=None, dst=vector_reg)
        return vector_reg

    def decl_2d_vector(self,
                       text: str,
                       nreg: int,
                       width: int,
                       elements: int = 1,
                       font_size: int = DEFAULT_FONT_SIZE,
                       label_pos = None) -> TwoDimReg:
        """
        Declare a 2D vector, return a two-dim register.
        """
        color = self.colormap_default_color
        vector_reg = TwoDimReg(text=text,
                               color=color,
                               nreg=nreg,
                               width=width,
                               elements=elements,
                               font_size=font_size,
                               label_pos=label_pos)
        self.placement_add_object(vector_reg)

        self.animation_add_animation(animate=decl_register(vector_reg), src=None, dst=vector_reg)
        return vector_reg

    def read_elem(self,
                  vector: OneDimReg,
                  size: float = -1.0,
                  reg_idx: int = 0,
                  index: int = 0,
                  offset: int = 0,
                  color_hash = None,
                  value = None,
                  fill_opacity: float = 0.5,
                  font_size: int = DEFAULT_FONT_SIZE,
                  value_format: str = get_config("elem_value_format")):
        """
        Read element from register, return one Rectangle.

        Args:
            vector: Register.
            color: Color of new element.
            size: Width of element in byte.
            e: Index of element.
            kargs: Arguments to new element.
        """
        color = self.colormap_get_color(
            self._traceback_hash() if color_hash is None else color_hash)

        elem = self._get_elem_source_elem(
            vector=vector, size=size, reg_idx=reg_idx, index=index, offset=offset)
        if elem is None:
            elem = OneDimRegElem(color=color,
                                 width=size,
                                 value=value,
                                 fill_opacity=fill_opacity,
                                 font_size=font_size,
                                 value_format=value_format)
            self._set_elem_source_elem(
                elem=elem, vector=vector, size=size, reg_idx=reg_idx, index=index, offset=offset)

            self.last_dep_map[elem] = vector

            animation_item = self.animation_add_animation(
                animate=read_elem(
                    vector=vector, elem=elem, reg_idx=reg_idx, index=index, offset=offset),
                src=vector,
                dst=elem,
                dep=[vector])
            self._set_item_producer(elem, animation_item)
        return elem

    def move_elem(self,
                  elem: OneDimRegElem,
                  vector: OneDimReg,
                  size: float = -1.0,
                  reg_idx: int = 0,
                  index: int = 0,
                  offset: int = 0):
        """
        Move element to register, add animate to list.

        Args:
            elem: Element object.
            vector: Register.
            size: Width of element in byte.
            e: Index of element.
        """
        old_dep = None
        if elem in self.last_dep_map:
            old_dep = self.last_dep_map[elem]
            del self.last_dep_map[elem]
        self.last_dep_map[elem] = vector

        elem_ = self._get_duplicate_item(elem)
        new_elem = OneDimRegElem(color=elem.elem_color,
                                 width=elem.elem_width if size <= 0 else size,
                                 value=elem.elem_value,
                                 fill_opacity=elem.elem_fill_opacity,
                                 font_size=elem.elem_font_size,
                                 value_format=elem.elem_value_format)

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

    def counter_to_predicate(self,
                             png_obj: OneDimReg,
                             text: str,
                             width: int,
                             elements: int = 1,
                             font_size: int = DEFAULT_FONT_SIZE,
                             label_pos = None):
        """
        Animate of predict-as-counter to mask predicate.
        """
        color = self.colormap_default_color
        mask_pred = OneDimReg(text=text,
                              color=color,
                              width=width,
                              elements=elements,
                              font_size=font_size,
                              label_pos=label_pos)
        self.animation_add_animation(
            animate=replace_register(png_obj, mask_pred, align="left"),
            src=png_obj,
            dst=mask_pred)
        return mask_pred

    def concat_vector(self,
                      vector_list: List[OneDimReg],
                      text: str,
                      font_size: int = DEFAULT_FONT_SIZE,
                      label_pos = None) -> OneDimReg:
        """
        Animate of vector concat.
        """
        reg_width_list = [item.reg_width for item in vector_list]
        reg_width = sum(reg_width_list)
        elem_width = int(min([item.elem_width for item in vector_list]))
        elements = int(reg_width / elem_width)

        color = self.colormap_default_color
        new_vector = OneDimReg(text=text,
                               color=color,
                               width=reg_width,
                               elements=elements,
                               font_size=font_size,
                               label_pos=label_pos)
        self.placement_add_object(new_vector)

        self.animation_add_animation(
            animate=concat_vector(vector_list=vector_list, new_vector=new_vector),
            src=vector_list,
            dst=new_vector)
        return new_vector

    def data_convert(self,
                     elem: OneDimRegElem,
                     size: float,
                     index: int = 0,
                     color_hash = None,
                     value = None,
                     fill_opacity: float = 0.5,
                     font_size: int = DEFAULT_FONT_SIZE,
                     value_format: str = get_config("elem_value_format")) -> OneDimRegElem:
        """
        Animate of data convert.
        """
        color = self.colormap_get_color(
            self._traceback_hash() if color_hash is None else color_hash)
        new_elem = OneDimRegElem(color=color,
                                 width=size,
                                 value=value,
                                 fill_opacity=fill_opacity,
                                 font_size=font_size,
                                 value_format=value_format)

        old_dep = None
        if elem in self.last_dep_map:
            old_dep = self.last_dep_map[elem]

        elem_ = self._get_duplicate_item(elem)

        animation_item = self.animation_add_animation(
            animate=replace_elem(old_elem=elem_, new_elem=new_elem, index=index, align="right"),
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
                      res_size: float,
                      func: str = None,
                      args_value: List[str] = None,
                      font_size: int = DEFAULT_FONT_SIZE,
                      align_with = None) -> FunctionUnit:
        """
        Animation of declare function call.
        
        Used to control placement and animation.
        """
        if not func:
            func = isa_hash

        if self.placement_has_object(isa_hash):
            func_unit = self.placement_get_object(isa_hash)
        else:
            func_color = self.colormap_default_color
            func_unit = FunctionUnit(text=func,
                                     color=func_color,
                                     args_width=args_width,
                                     res_width=res_size,
                                     args_value=args_value,
                                     font_size=font_size)
            self.placement_add_object(func_unit, isa_hash, align_with=align_with)

            self.animation_add_animation(
                animate=decl_func_call(func_unit), src=None, dst=func_unit)

        return func_unit

    def decl_func_group(self,
                        num_unit: Union[int, List[int]],
                        isa_hash: Union[str, List[str]],
                        args_width: List[float],
                        res_size: float,
                        func: Union[str, List[str]] = None,
                        args_value: List[str] = None,
                        font_size: int = DEFAULT_FONT_SIZE,
                        force_hw_ratio: bool = False) -> List[FunctionUnit]:
        """
        Animation of declare a group of function call.
        
        Used to control placement and animation.
        """
        if not func:
            func = isa_hash

        if isinstance(num_unit, int):
            num_unit = [num_unit]

        func_unit_list = []
        func_unit_hash = []
        num_id_list = itertools.product(*[list(range(0, numi)) for numi in num_unit])
        for num_id in num_id_list:
            if func:
                func_ = func
                if isinstance(func, list):
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
            func_unit = FunctionUnit(text=func_,
                                     color=func_color,
                                     args_width=args_width,
                                     res_width=res_size,
                                     args_value=args_value,
                                     font_size=font_size)

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
                      args: List[OneDimRegElem],
                      res_size: float,
                      func: str = None,
                      func_args_index: List[int] = None,
                      func_args_value: List = None,
                      func_font_size: int = DEFAULT_FONT_SIZE,
                      res_color_hash = None,
                      res_index: int = None,
                      res_value = None,
                      res_fill_opacity: float = 0.5,
                      res_font_size: int = DEFAULT_FONT_SIZE,
                      res_value_format: str = get_config("elem_value_format")) -> OneDimRegElem:
        """
        Animate of Function call.
        """
        args_item: List[OneDimRegElem] = []
        args_item_exist: List[OneDimRegElem] = []
        for item in args:
            if isinstance(item, tuple):
                args_item.append(item[0])
            else:
                args_item.append(item)
                args_item_exist.append(item)

        func_unit = self.decl_function(isa_hash=func_isa_hash,
                                       args_width=[item.elem_width for item in args_item],
                                       res_size=res_size,
                                       func=func,
                                       args_value=func_args_value,
                                       font_size=func_font_size)

        res_color = self.colormap_get_color(
            self._traceback_hash() if res_color_hash is None else res_color_hash)
        res_elem = OneDimRegElem(color=res_color,
                                 width=res_size,
                                 value=res_value,
                                 fill_opacity=res_fill_opacity,
                                 font_size=res_font_size,
                                 value_format=res_value_format)

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

        self.last_dep_map[res_elem] = func_unit

        if func_args_index is None:
            func_args_index = [0 for _ in args]
        if res_index is None:
            res_index = 0

        animation_item = self.animation_add_animation(
            animate=function_call(func_unit=func_unit,
                                  args_list=args_,
                                  res_item=res_elem,
                                  func_args_index=func_args_index,
                                  res_index=res_index),
            src=args_item_exist + args_exist_,
            dst=res_elem,
            dep=(old_dep + [func_unit]) if old_dep else [func_unit])
        for arg in args_item_exist:
            self._set_item_cusumer(arg, animation_item)
        self._set_item_producer(res_elem, animation_item)

        return res_elem

    def read_func_imm(self,
                      size: float,
                      color_hash = None,
                      value = None,
                      fill_opacity: float = 0.5,
                      font_size: int = DEFAULT_FONT_SIZE,
                      value_format: str = get_config("elem_value_format")) -> OneDimRegElem:
        """
        Animate of Function call.
        """
        res_color = self.colormap_get_color(
            self._traceback_hash() if color_hash is None else color_hash)
        res_elem = OneDimRegElem(color=res_color,
                                 width=size,
                                 value=value,
                                 fill_opacity=fill_opacity,
                                 font_size=font_size,
                                 value_format=value_format)

        return read_func_imm(elem=res_elem)

    #
    # Memory
    #
    def decl_memory(self,   # pylint: disable=dangerous-default-value
                    addr_width: int = get_config("mem_addr_width"),
                    data_width: int = get_config("mem_data_width"),
                    addr_align: int = get_config("mem_align"),
                    isa_hash: str = None,
                    mem_range: List[Tuple[int]] = get_config("mem_range"),
                    font_size = DEFAULT_FONT_SIZE,
                    para_enable = False) -> MemoryUnit:
        """
        Animation of declare memory.

        Used to control placement and animation.
        """
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
                                  para_enable=para_enable,
                                  mem_map_width=self.placement_width() - 2)
            self.placement_add_object(mem_unit, "Memory")

            self.animation_add_animation(
                animate=decl_memory_unit(mem_unit), src=None, dst=mem_unit)

        return mem_unit

    def read_memory(self,   # pylint: disable=dangerous-default-value
                    addr: OneDimRegElem,
                    size: int,
                    res_color_hash = None,
                    res_value = None,
                    res_fill_opacity: float = 0.5,
                    res_font_size: int = DEFAULT_FONT_SIZE,
                    res_value_format: str = get_config("elem_value_format"),
                    mem_addr_width: int = get_config("mem_addr_width"),
                    mem_data_width: int = get_config("mem_data_width"),
                    mem_addr_align: int = get_config("mem_align"),
                    mem_isa_hash: str = None,
                    mem_mem_range: List[Tuple[int]] = get_config("mem_range"),
                    mem_font_size: int = DEFAULT_FONT_SIZE) -> OneDimRegElem:
        """
        Animate of read memory.
        """
        mem_unit = self.decl_memory(addr_width=mem_addr_width,
                                    data_width=mem_data_width,
                                    addr_align=mem_addr_align,
                                    isa_hash=mem_isa_hash,
                                    mem_range=mem_mem_range,
                                    font_size=mem_font_size)

        data_color = self.colormap_get_color(
            self._traceback_hash() if res_color_hash is None else res_color_hash)
        data = OneDimRegElem(color=data_color,
                             width=size,
                             value=res_value,
                             fill_opacity=res_fill_opacity,
                             font_size=res_font_size,
                             value_format=res_value_format)

        old_dep = []
        if addr in self.last_dep_map:
            old_dep.append(self.last_dep_map[addr])
            del self.last_dep_map[addr]

        addr_ = self._get_duplicate_item(addr)

        self.last_dep_map[data] = mem_unit

        if addr.elem_value is not None and mem_unit.is_mem_range_cover(int(addr.elem_value)):
            addr_value = int(addr.elem_value)
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
                                    mem_mark=mem_mark),
                src=[addr, addr_],
                dst=[data, mem_mark],
                dep=old_dep + [mem_unit],
                remove_after=[addr_])
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
                     addr: OneDimRegElem,
                     data: OneDimRegElem,
                     mem_addr_width: int = get_config("mem_addr_width"),
                     mem_data_width: int = get_config("mem_data_width"),
                     mem_addr_align: int = get_config("mem_align"),
                     mem_isa_hash: str = None,
                     mem_mem_range: List[Tuple[int]] = get_config("mem_range"),
                     mem_font_size: int = DEFAULT_FONT_SIZE) -> None:
        """
        Animate of write memory.
        """
        mem_unit = self.decl_memory(addr_width=mem_addr_width,
                                    data_width=mem_data_width,
                                    addr_align=mem_addr_align,
                                    isa_hash=mem_isa_hash,
                                    mem_range=mem_mem_range,
                                    font_size=mem_font_size)

        old_dep = []
        if addr in self.last_dep_map:
            old_dep.append(self.last_dep_map[addr])
            del self.last_dep_map[addr]

        addr_ = self._get_duplicate_item(addr)

        if data in self.last_dep_map:
            old_dep.append(self.last_dep_map[data])
            del self.last_dep_map[data]

        data_ = self._get_duplicate_item(data)

        if addr.elem_value is not None and mem_unit.is_mem_range_cover(int(addr.elem_value)):
            addr_value = int(addr.elem_value)
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
                                     mem_mark=mem_mark),
                src=[addr, data, addr_, data_],
                dst=[mem_mark],
                dep=old_dep + [mem_unit],
                remove_after=[addr_, data_],
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
