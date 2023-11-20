"""
Define APIs for animation in ISA data flow, manage animation flow and object placement.
"""

from typing import List, Tuple
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
                 strategy="RB",
                 default_color=WHITE,
                 color_scheme: List[Color]=None,
                 default_font_size=40):
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
        self.elem_producer_copy = {}
        self.elem_producer_map = {}
        self.elem_refer_count = {}

    def _traceback_hash(self, depth = 2) -> int:
        """
        Return hash value according to traceback.
        """
        # frame 0 is _traceback_hash
        # frame 1 is animation API
        # frame 2 is the caller of animation API
        frame = sys._getframe(depth)
        return hash(str(frame))

    def _set_item_producer(self,
                           item: OneDimRegElem,
                           producer: IsaAnimateItem):
        """
        Set producer of element.
        """
        self.elem_producer_map[item] = producer
        self.elem_producer_copy[item] = item.copy()
        self.elem_refer_count[item] = 0

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

        return item_

    #
    # Animations APIs
    #
    def decl_scalar(self,
                    text: str,
                    width: int,
                    value = None,
                    font_size = DEFAULT_FONT_SIZE,
                    label_pos = None) -> OneDimReg:
        """
        Declare scalar variables, return one-dim register.
        """
        color = self.colormap_default_color
        scalar_reg = OneDimReg(text=text,
                               color=color,
                               width=width,
                               elements=1,
                               value=value,
                               font_size=font_size,
                               label_pos=label_pos)
        self.placement_add_object(scalar_reg)

        self.animation_add_animation(animate=decl_register(scalar_reg), src=None, dst=scalar_reg)
        return scalar_reg

    def decl_vector(self,
                    text: str,
                    width: int,
                    elements: int = 1,
                    value = None,
                    font_size = DEFAULT_FONT_SIZE,
                    label_pos = None) -> OneDimReg:
        """
        Declare vector variables, return one-dim register.
        """
        color = self.colormap_default_color
        vector_reg = OneDimReg(text=text,
                               color=color,
                               width=width,
                               elements=elements,
                               value=value,
                               font_size=font_size,
                               label_pos=label_pos)
        self.placement_add_object(vector_reg)

        self.animation_add_animation(animate=decl_register(vector_reg), src=None, dst=vector_reg)
        return vector_reg

    def decl_vector_group(self,
                          text_list: List[str],
                          width: int,
                          elements: int = 1,
                          value_list: list = None,
                          font_size = DEFAULT_FONT_SIZE,
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
                               value=value_list,
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
                       value: list = None,
                       font_size = DEFAULT_FONT_SIZE,
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
                               value=value,
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
                  color_hash = None,
                  value = None,
                  fill_opacity = 0.5,
                  font_size = DEFAULT_FONT_SIZE,
                  value_format = get_config("elem_value_format")):
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
        elem = OneDimRegElem(color=color,
                             width=size,
                             value=value,
                             fill_opacity=fill_opacity,
                             font_size=font_size,
                             value_format=value_format)

        self.last_dep_map[elem] = vector

        animation_item = self.animation_add_animation(
            animate=read_elem(vector=vector, elem=elem, reg_idx=reg_idx, index=index),
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
                  index: int = 0):
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

        self.animation_add_animation(
            animate=assign_elem(elem=elem_, vector=vector, size=size, reg_idx=reg_idx, index=index),
            src=[elem, elem_],
            dst=[elem, elem_],
            dep=[old_dep, vector] if old_dep else [vector])

    def counter_to_predicate(self,
                             png_obj: OneDimReg,
                             text: str,
                             width: int,
                             elements: int = 1,
                             value = None,
                             font_size = DEFAULT_FONT_SIZE,
                             label_pos = None):
        """
        Animate of predict-as-counter to mask predicate.
        """
        color = self.colormap_default_color
        mask_pred = OneDimReg(text=text,
                              color=color,
                              width=width,
                              elements=elements,
                              value=value,
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
                      value = None,
                      font_size = DEFAULT_FONT_SIZE,
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
                               value=value,
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
                     fill_opacity = 0.5,
                     font_size = DEFAULT_FONT_SIZE,
                     value_format = get_config("elem_value_format")) -> OneDimRegElem:
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
        if old_dep:
            self.last_dep_map[new_elem] = old_dep

        elem_ = self._get_duplicate_item(elem)

        animation_item = self.animation_add_animation(
            animate=replace_elem(old_elem=elem_, new_elem=new_elem, index=index, align="right"),
            src=[elem, elem_],
            dst=new_elem,
            dep=old_dep)
        self._set_item_producer(new_elem, animation_item)
        return new_elem

    #
    # Function behavior
    #
    def decl_function(self,
                      func: str,
                      args_width: List[float],
                      res_size: float,
                      isa_hash: str = None,
                      args_value = None,
                      font_size = DEFAULT_FONT_SIZE) -> FunctionUnit:
        """
        Animation of declare function call.
        
        Used to control placement and animation.
        """
        if not isa_hash:
            isa_hash = self._traceback_hash()

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
            self.placement_add_object(func_unit, isa_hash)

            self.animation_add_animation(
                animate=decl_func_call(func_unit), src=None, dst=func_unit)

        return func_unit

    def function_call(self,
                      func: str,
                      args: List[OneDimRegElem],
                      res_size: float,
                      func_isa_hash: str = None,
                      func_args_value = None,
                      func_font_size = DEFAULT_FONT_SIZE,
                      res_color_hash = None,
                      res_value = None,
                      res_fill_opacity = 0.5,
                      res_font_size = DEFAULT_FONT_SIZE,
                      res_value_format = get_config("elem_value_format")) -> OneDimRegElem:
        """
        Animate of Function call.
        """
        func_unit = self.decl_function(func=func,
                                       args_width=[item.elem_width for item in args],
                                       res_size=res_size,
                                       isa_hash=func_isa_hash,
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
        for arg in args:
            if arg in self.last_dep_map:
                old_dep.append(self.last_dep_map[arg])
                del self.last_dep_map[arg]

            arg_ = self._get_duplicate_item(arg)
            args_.append(arg_)

        self.last_dep_map[res_elem] = func_unit

        animation_item = self.animation_add_animation(
            animate=function_call(func_unit=func_unit, args_list=args_, res_item=res_elem),
            src=args + args_,
            dst=res_elem,
            dep=(old_dep + [func_unit]) if old_dep else [func_unit])
        self._set_item_producer(res_elem, animation_item)
        return res_elem

    #
    # Memory
    #
    def decl_memory(self,
                    addr_width: int = get_config("mem_addr_width"),
                    data_width: int = get_config("mem_data_width"),
                    addr_align: int = get_config("mem_align"),
                    isa_hash: str = None,
                    mem_range: List[Tuple[int]] = get_config("mem_range"),
                    font_size = DEFAULT_FONT_SIZE) -> MemoryUnit:
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
                                  font_size=font_size)
            self.placement_add_object(mem_unit, "Memory")

            self.animation_add_animation(
                animate=decl_memory_unit(mem_unit), src=None, dst=mem_unit)

        return mem_unit

    def read_memory(self,
                    addr: OneDimRegElem,
                    size: int,
                    res_color_hash = None,
                    res_value = None,
                    res_fill_opacity = 0.5,
                    res_font_size = DEFAULT_FONT_SIZE,
                    res_value_format = get_config("elem_value_format"),
                    mem_addr_width: int = get_config("mem_addr_width"),
                    mem_data_width: int = get_config("mem_data_width"),
                    mem_addr_align: int = get_config("mem_align"),
                    mem_isa_hash: str = None,
                    mem_mem_range: List[Tuple[int]] = get_config("mem_range"),
                    mem_font_size = DEFAULT_FONT_SIZE) -> OneDimRegElem:
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

        if addr.value is not None and mem_unit.is_mem_range_cover(int(addr.value)):
            addr_value = int(addr.value)
            addr_mark = mem_unit.get_addr_mark(addr=addr_value,
                                               color=addr_.elem_rect.color)
            mem_mark = mem_unit.get_rd_mem_mark(laddr=addr_value,
                                                raddr=addr_value + size // 8,
                                                color=data_color)
            mem_unit.append_mem_mark_list(mem_mark)

            animation_item = self.animation_add_animation(
                animate=read_memory(mem_unit=mem_unit,
                                    addr_item=addr_,
                                    data_item=data,
                                    addr_mark=addr_mark,
                                    mem_mark=mem_mark),
                src=[addr, addr_],
                dst=[data, mem_mark],
                dep=old_dep + [mem_unit])
            self._set_item_producer(data, animation_item)
        else:
            animation_item = self.animation_add_animation(
                animate=read_memory_without_addr(
                    mem_unit=mem_unit, addr_item=addr_, data_item=data),
                src=[addr, addr_],
                dst=[data],
                dep=old_dep + [mem_unit])
            self._set_item_producer(data, animation_item)

        return data

    def write_memory(self,
                     addr: OneDimRegElem,
                     data: OneDimRegElem,
                     mem_addr_width: int = get_config("mem_addr_width"),
                     mem_data_width: int = get_config("mem_data_width"),
                     mem_addr_align: int = get_config("mem_align"),
                     mem_isa_hash: str = None,
                     mem_mem_range: List[Tuple[int]] = get_config("mem_range"),
                     mem_font_size = DEFAULT_FONT_SIZE) -> None:
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

        if addr.value is not None and mem_unit.is_mem_range_cover(int(addr.value)):
            addr_value = int(addr.value)
            addr_mark = mem_unit.get_addr_mark(addr=addr_value,
                                               color=addr_.elem_rect.color)
            mem_mark = mem_unit.get_wt_mem_mark(laddr=addr_value,
                                                raddr=addr_value + data.elem_width // 8,
                                                color=data_.elem_rect.color)
            mem_unit.append_mem_mark_list(mem_mark)

            self.animation_add_animation(
                animate=write_memory(mem_unit=mem_unit,
                                     addr_item=addr_,
                                     data_item=data_,
                                     addr_mark=addr_mark,
                                     mem_mark=mem_mark),
                src=[addr, data, addr_, data_],
                dst=[mem_mark],
                dep=old_dep + [mem_unit])
        else:
            self.animation_add_animation(
                animate=write_memory_without_addr(
                    mem_unit=mem_unit, addr_item=addr_, data_item=data_),
                src=[addr, data, addr_, data_],
                dst=[],
                dep=old_dep + [mem_unit])
