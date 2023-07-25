"""
Define APIs for animation in ISA data flow, manage animation flow and object placement.
"""

from typing import List
from colour import Color
import sys
from manim import WHITE
from ..isa_animate import (decl_register,
                           replace_register,
                           concat_vector,
                           read_elem,
                           assign_elem,
                           replace_elem,
                           decl_func_call,
                           function_call)
from ..isa_objects import OneDimReg, OneDimRegElem, TwoDimReg, FunctionCall
from .isa_animate import IsaAnimationMap
from .isa_placement import IsaPlacementMap
from .isa_color_map import IsaColorMap

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

    def _traceback_hash(self, depth = 2) -> int:
        """
        Return hash value according to traceback.
        """
        # frame 0 is _traceback_hash
        # frame 1 is animation API 
        # frame 2 is the caller of animation API
        frame = sys._getframe(depth)
        return hash(str(frame))

    #
    # Animations APIs
    #
    def decl_scalar(self,
                    text: str,
                    width: int,
                    **kwargs) -> OneDimReg:
        """
        Declare scalar variables, return one-dim register.
        """
        color = self.colormap_default_color
        scalar_reg = OneDimReg(
            text=text, color=color, width=width, elements=1, **kwargs)
        self.placement_add_object(scalar_reg)

        self.animation_add_animation(
            animate=decl_register(scalar_reg), src=None, dst=scalar_reg)
        return scalar_reg

    def decl_vector(self,
                    text: str,
                    width: int,
                    elements: int = 1,
                    **kwargs) -> OneDimReg:
        """
        Declare vector variables, return one-dim register.
        """
        color = self.colormap_default_color
        vector_reg = OneDimReg(
            text=text, color=color, width=width, elements=elements, **kwargs)
        self.placement_add_object(vector_reg)

        self.animation_add_animation(
            animate=decl_register(vector_reg), src=None, dst=vector_reg)
        return vector_reg

    def decl_vector_group(self,
                          text_list: List[str],
                          width: int,
                          elements: int = 1,
                          **kwargs) -> TwoDimReg:
        """
        Declare a list of vector variables, return a two-dim register.
        """
        color = self.colormap_default_color
        nreg = len(text_list)
        vector_reg = TwoDimReg(
            text=text_list, color=color, nreg=nreg, width=width, elements=elements, **kwargs)
        self.placement_add_object(vector_reg)

        self.animation_add_animation(
            animate=decl_register(vector_reg), src=None, dst=vector_reg)
        return vector_reg

    def decl_2d_vector(self,
                       text: str,
                       nreg: int,
                       width: int,
                       elements: int = 1,
                       **kwargs) -> TwoDimReg:
        """
        Declare a 2D vector, return a two-dim register.
        """
        color = self.colormap_default_color
        vector_reg = TwoDimReg(
            text=text, color=color, nreg=nreg, width=width, elements=elements, **kwargs)
        self.placement_add_object(vector_reg)

        self.animation_add_animation(
            animate=decl_register(vector_reg), src=None, dst=vector_reg)
        return vector_reg

    def read_elem(self,
                  vector: OneDimReg,
                  size: float = -1.0,
                  reg_idx: int = 0,
                  index: int = 0,
                  **kwargs):
        """
        Read element from register, return one Rectangle.

        Args:
            vector: Register.
            color: Color of new element.
            size: Width of element in byte.
            e: Index of element.
            kargs: Arguments to new element.
        """
        if "color_hash" in kwargs:
            hash_str = kwargs["color_hash"]
            del kwargs["color_hash"]
            color = self.colormap_get_color(hash_str)
        else:
            color = self.colormap_get_color(self._traceback_hash())
        elem = OneDimRegElem(color=color, width=size, **kwargs)

        self.last_dep_map[elem] = vector

        self.animation_add_animation(
            animate=read_elem(vector=vector, elem=elem, reg_idx=reg_idx, index=index),
            src=vector,
            dst=elem,
            dep=[vector])
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

        self.animation_add_animation(
            animate=assign_elem(elem=elem, vector=vector, size=size, reg_idx=reg_idx, index=index),
            src=elem,
            dst=elem,
            dep=[old_dep, vector] if old_dep else [vector])

    def counter_to_predicate(self,
                             png_obj: OneDimReg,
                             text: str,
                             width: int,
                             elements: int = 1,
                             **kwargs):
        """
        Animate of predict-as-counter to mask predicate.
        """
        color = self.colormap_default_color
        mask_pred = OneDimReg(text=text, color=color, width=width, elements=elements, **kwargs)
        self.animation_add_animation(
            animate=replace_register(png_obj, mask_pred, align="left"),
            src=png_obj,
            dst=mask_pred)
        return mask_pred

    def concat_vector(self,
                      vector_list: List[OneDimReg],
                      text: str,
                      **kwargs) -> OneDimReg:
        """
        Animate of vector concat.
        """
        reg_width_list = [item.reg_width for item in vector_list]
        reg_width = sum(reg_width_list)
        elem_width = int(min([item.elem_width for item in vector_list]))
        elements = int(reg_width / elem_width)

        color = self.colormap_default_color
        new_vector = OneDimReg(
            text=text, color=color, width=reg_width, elements=elements, **kwargs)
        self.placement_add_object(new_vector)

        self.animation_add_animation(
            animate=concat_vector(vector_list=vector_list, new_vector=new_vector),
            src=vector_list,
            dst=new_vector)
        return new_vector

    def data_convert(self,
                     elem: OneDimRegElem,
                     size: float,
                     index: int,
                     **kwargs) -> OneDimRegElem:
        """
        Animate of data convert.
        """
        if "color_hash" in kwargs:
            hash_str = kwargs["color_hash"]
            del kwargs["color_hash"]
            color = self.colormap_get_color(hash_str)
        else:
            color = self.colormap_get_color(self._traceback_hash())
        new_elem = OneDimRegElem(color=color, width=size, **kwargs)

        old_dep = None
        if elem in self.last_dep_map:
            old_dep = self.last_dep_map[elem]
        self.last_dep_map[new_elem] = old_dep

        self.animation_add_animation(
            animate=replace_elem(old_elem=elem, new_elem=new_elem, index=index, align="right"),
            src=elem,
            dst=new_elem,
            dep=old_dep)
        return new_elem

    def function_call(self,
                      func: str,
                      args: List[OneDimRegElem],
                      res_size: float,
                      isa_hash: str = None,
                      **kwargs) -> OneDimRegElem:
        """
        Animate of Function call.
        """
        if not isa_hash:
            isa_hash = self._traceback_hash()

        func_kwargs = dict()
        if "args_value" in kwargs:
            func_kwargs["args_value"] = kwargs["args_value"]
            del kwargs["args_value"]

        if self.placement_has_object(isa_hash):
            func_unit = self.placement_get_object(isa_hash)
        else:
            args_width = [item.elem_width for item in args]
            func_color = self.colormap_default_color
            func_unit = FunctionCall(text=func, color=func_color, args_width=args_width,
                                     res_width=res_size)
            self.placement_add_object(func_unit, isa_hash)

            self.animation_add_animation(
                animate=decl_func_call(func_unit), src=None, dst=func_unit)

        if "color_hash" in kwargs:
            hash_str = kwargs["color_hash"]
            del kwargs["color_hash"]
            res_color = self.colormap_get_color(hash_str)
        else:
            res_color = self.colormap_get_color(self._traceback_hash())
        res_elem = OneDimRegElem(color=res_color, width=res_size, **kwargs)

        old_dep = []
        for arg in args:
            if arg in self.last_dep_map:
                old_dep.append(self.last_dep_map[arg])
                del self.last_dep_map[arg]
        self.last_dep_map[res_elem] = func_unit

        self.animation_add_animation(
            animate=function_call(func_object=func_unit, args_list=args, res_item=res_elem),
            src=args,
            dst=res_elem,
            dep=old_dep + [func_unit] if old_dep else [func_unit])
        return res_elem
