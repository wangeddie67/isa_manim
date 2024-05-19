"""
Define APIs for animation in ISA data flow, manage animation flow and object placement.
"""

import itertools
from typing import Any, List, Tuple, Union, Callable
from typing import overload
from colour import Color
import sys
from manim import (WHITE, DEFAULT_FONT_SIZE, Animation)
from ..isa_animate import (decl_register,
                           read_elem,
                           assign_elem,
                           replace_elem,
                           decl_func_unit,
                           read_func_imm,
                           function_call,
                           decl_memory_unit,
                           read_memory_without_addr,
                           write_memory_without_addr,
                           read_memory,
                           write_memory)
from ..isa_objects import ElemUnit, RegUnit, FunctionUnit, MemoryUnit
from .isa_animate import IsaAnimationFlow
from .isa_elem_refcount import IsaElemRefCount
from .isa_placement import IsaPlacementMap
from .isa_color_map import IsaColorMap
from ..isa_config import get_config

class IsaDataFlow(IsaAnimationFlow, IsaElemRefCount, IsaPlacementMap, IsaColorMap):
    """
    Data flow of ISA, used to define API for ISA animation.
    """
    def __init__(self,
                 strategy: str ="RB",
                 default_color: Color = WHITE,
                 color_scheme: List[Color] = None):
        """
        Construct animation and placement manager.

        Args:
            strategy: Placement strategy, options: RB or BR.
            default_color: Default color of item, used for register and functions.
        """
        IsaAnimationFlow.__init__(self)
        IsaElemRefCount.__init__(self)
        IsaPlacementMap.__init__(self, strategy=strategy)
        IsaColorMap.__init__(self, default_color=default_color, color_scheme=color_scheme)

    def _traceback_hash(self, depth: int = 2) -> int:
        """
        Return hash value according to traceback.
        """
        # frame 0 is _traceback_hash
        # frame 1 is animation API
        # frame 2 is the caller of animation API
        frame = sys._getframe(depth)    # pylint: disable=protected-access
        return hash(str(frame))

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
                      align_with: Union[RegUnit, FunctionUnit, MemoryUnit] = None) -> RegUnit: ...

    @overload
    def decl_register(self,
                      text: str,
                      width: int,
                      elements: int,
                      value: List[Any] = None,
                      font_size: int = DEFAULT_FONT_SIZE,
                      value_format: str = None,
                      align_with: Union[RegUnit, FunctionUnit, MemoryUnit] = None) -> RegUnit: ...

    @overload
    def decl_register(self,
                      text: str,
                      width: int,
                      value: Any = None,
                      font_size: int = DEFAULT_FONT_SIZE,
                      value_format: str = None,
                      align_with: Union[RegUnit, FunctionUnit, MemoryUnit] = None) -> RegUnit: ...

    def decl_register(self,
                      text: str,
                      width: int,
                      elements: int = 1,
                      nreg: int = 1,
                      value: List[List[Any]] = None,
                      font_size: int = DEFAULT_FONT_SIZE,
                      value_format: str = None,
                      align_with: Union[RegUnit, FunctionUnit, MemoryUnit] = None) -> RegUnit:
        """
        Declare one register with a specified name (`text`) and bit width (`width`) and add it to
        the scene.
        
        Args:
            text: Name of this register.
            width: Width of this register width, in bit.
            elements: Elements count in this register, or horizontal size of this register.
            nreg: Number of registers, or vertical size of this register.
            value: Value of this register, single element or 1-D/2-D array.
                If not specified, assign None.
            font_size: Font size of register name.
                If not specified, take the value of `DEFAULT_FONT_SIZE`.
            value_format: Format to print data value.
                If not specified, take the value from global configuration `elem_value_format`.
            align_with: Align with specified element when placement.
                If not specified, placement follows automatic strategy.

        Returns:
            Generated register unit.
        """
        # Handle default value of arguments.
        if not isinstance(text, list):
            text = [text]
        if value_format is None:
            value_format = get_config("elem_value_format")

        # Create register unit.
        color = self.colormap_default_color
        reg_unit = RegUnit(text, color, width, elements, nreg, value, font_size, value_format)

        # Placement register unit.
        self.place_object(reg_unit, hash(reg_unit), align_with=align_with)
        # Create animation
        self.add_animation(decl_register(reg_unit), None, reg_unit)

        # Return register unit.
        return reg_unit

    @overload
    def read_elem(self,
                  vector: RegUnit,
                  index: int,
                  reg_idx: int,
                  offset: int = 0,
                  width: int = -1,
                  color_hash = None,
                  value = None,
                  fill_opacity: float = None,
                  font_size: int = DEFAULT_FONT_SIZE,
                  value_format: str = None) -> ElemUnit: ...

    @overload
    def read_elem(self,
                  vector: RegUnit,
                  index: int,
                  offset: int = 0,
                  width: int = -1,
                  value = None,
                  color_hash = None,
                  fill_opacity: float = None,
                  font_size: int = DEFAULT_FONT_SIZE,
                  value_format: str = None) -> ElemUnit: ...

    @overload
    def read_elem(self,
                  vector: RegUnit,
                  offset: int = 0,
                  width: int = -1,
                  value = None,
                  color_hash = None,
                  fill_opacity: float = None,
                  font_size: int = DEFAULT_FONT_SIZE,
                  value_format: str = None) -> ElemUnit: ...

    def read_elem(self,
                  vector: RegUnit,
                  index: int = 0,
                  reg_idx: int = 0,
                  offset: int = 0,
                  width: int = 0,
                  color_hash: Union[int, str] = None,
                  value: Any = None,
                  fill_opacity: float = None,
                  font_size: int = DEFAULT_FONT_SIZE,
                  value_format: str = None) -> ElemUnit:
        """
        Read one element from the specified position (`reg_idx` and `index`) of the specified
        register `vector` and return one element unit.

        Args:
            vector: Register.
            index: Element index.
            reg_idx: Regsiter index.
            offset: Offset of LSB.
            width: Width of element in bit.
            color_hash: Hash to get color from color scheme.
            value: Value of this register, single element or 1-D/2-D array.
                If not specified, assign None.
            fill_opacity: Fill opacity.
                If not specified, take the value from global configuration `elem_fill_opacity`.
            font_size: Font size of element value.
                If not specified, take the value of `DEFAULT_FONT_SIZE`.
            value_format: Format to print data value.
                If not specified, take the value from global configuration `elem_value_format`.

        Returns:
            Generated element unit.
        """
        # If there is one element from the same position, return existing element.
        if width == 0:
            width = vector.elem_width
        elem = self.get_elem_by_source(vector, width, reg_idx, index, offset)
        if elem is not None:
            return elem

        # Handle default value of arguments.
        if fill_opacity is None:
            fill_opacity = get_config("elem_fill_opacity")
        if value_format is None:
            value_format = vector.reg_value_format
        if width == 0:
            width = vector.elem_width
        if value is None:
            value = vector.get_elem_value(index, reg_idx)
        if color_hash is None:
            color_hash = self._traceback_hash()

        # Create new element.
        color = self.colormap_get_color(color_hash)
        elem = ElemUnit(color, width, value, fill_opacity, font_size, value_format, 0, False)

        # Create animation.
        self.add_animation(
            read_elem(vector, elem, index, reg_idx, offset), vector, elem, dep=[vector])

        # Update element reference counter.
        self.set_elem_source(elem, vector, reg_idx, index, offset)
        self.set_elem_producer(elem, vector)

        # Return new element
        return elem

    @overload
    def move_elem(self,
                  elem: ElemUnit,
                  vector: RegUnit,
                  index: int,
                  reg_idx: int,
                  offset: int = 0,
                  width: int = 0) -> ElemUnit: ...

    @overload
    def move_elem(self,
                  elem: ElemUnit,
                  vector: RegUnit,
                  index: int,
                  offset: int = 0,
                  width: int = 0) -> ElemUnit: ...

    @overload
    def move_elem(self,
                  elem: ElemUnit,
                  vector: RegUnit,
                  offset: int = 0,
                  width: int = 0) -> ElemUnit: ...

    def move_elem(self,
                  elem: ElemUnit,
                  vector: RegUnit,
                  index: int = 0,
                  reg_idx: int = 0,
                  offset: int = 0,
                  width: int = 0) -> ElemUnit:
        """
        Aassign one element `elem` to the specified position (`reg_idx` and `index`) of the
        specified register `vector`. 

        Args:
            elem: Element object.
            vector: Register unit.
            index: Element index.
            reg_idx: Regsiter index.
            offset: Offset of LSB.
            width: Width of element in bit.

        Returns:
            Element unit after move.
        """
        # Handle default value of arguments.
        if width == 0:
            width = elem.elem_width

        # Create new element.
        color = elem.elem_color
        value = elem.elem_value
        fill_opacity = elem.elem_fill_opacity
        font_size = elem.elem_font_size
        value_format = elem.elem_value_format
        high_bits = elem.elem_high_bits
        high_zero = elem.elem_high_zero
        new_elem = ElemUnit(
            color, width, value, fill_opacity, font_size, value_format, high_bits, high_zero)

        # Create animation. Replace dup_elem with new_elem.
        dup_elem = self.get_duplicate_item(elem)
        old_dep = self.get_last_deps(elem)
        animation_item = self.add_animation(
            assign_elem(dup_elem, new_elem, vector, index, reg_idx, offset),
            [elem, dup_elem], new_elem,
            dep=[old_dep, vector] if old_dep else [vector],
            remove_after=[dup_elem],
            add_after=[new_elem])

        # Update element reference counter.
        self.set_elem_cusumer(elem, animation_item, vector)
        self.set_elem_producer(new_elem, vector)

        # Functionality of operation: move element to vector.
        if elem.elem_value is not None:
            vector.set_elem_value(elem.elem_value, index, reg_idx)

        # Return new element.
        return new_elem

    def data_extend(self,
                    elem: ElemUnit,
                    width: float,
                    zero_extend: bool = False,
                    value: Any = None) -> ElemUnit:
        """
        Signaled extend or zero-extend element `elem` to bitwidth `width. Return the new element
        after extension.

        Args:
            elem: Origin element unit.
            width: Target width for extend.
            zero_extend: True means zero extension. The extend part will be assign with zero.
            value: New value of the element unit.
                If not specified, inherent value from the origin element.

        Returns:
            Element unit after extension.
        """
        # Handle default value of arguments.
        if value is not None:
            value = elem.elem_value
        if width > elem.elem_width:
            if zero_extend:
                high_bits = width - elem.elem_width
            else:
                high_bits = width - elem.elem_width + 1
        else:
            high_bits = 0

        # Create new element.
        color = elem.elem_color
        value = elem.elem_value
        fill_opacity = elem.elem_fill_opacity
        font_size = elem.elem_font_size
        value_format = elem.elem_value_format
        new_elem = ElemUnit(
            color, width, value, fill_opacity, font_size, value_format, high_bits, zero_extend)

        # Create animation. Replace dup_elem with new_elem.
        dup_elem = self.get_duplicate_item(elem)
        old_dep = self.get_last_deps(elem)
        animation_item = self.add_animation(
            replace_elem(dup_elem, new_elem, 0), [elem, dup_elem], new_elem,
            dep=old_dep, remove_after=[dup_elem], add_after=[new_elem])

        # Update element reference counter.
        self.set_elem_cusumer(elem, animation_item, old_dep)
        self.set_elem_producer(new_elem, old_dep)

        # Return new element.
        return new_elem

    #
    # Function behavior
    #
    def decl_function(self,
                      isa_hash: str,
                      args_width: List[float],
                      res_width: Union[int, List[int]],
                      name: str = None,
                      args_name: List[str] = None,
                      res_name: Union[str, List[str]] = None,
                      font_size: int = DEFAULT_FONT_SIZE,
                      value_format: str = None,
                      align_with: Union[RegUnit, FunctionUnit, MemoryUnit] = None,
                      func_callee: Callable = None) -> FunctionUnit:
        """
        Declare one function unit with a specified hash (`isa_hash`), arguments (`arg_width`), and
        return values (`res_width`) and add it to the scene.

        Args:
            isa_hash: Hash value of this function unit, used by `function_call`.
            args_width: A list of bit-width of arguments.
            res_width: Bit-width of return values. If there is only one return value, one single
                interger is required.
            name: Function name. If not specified, take `isa_hash` as function name.
            args_name: A list of name of arguments. The number of elements should be same as
                `args_width`.
            res_name: Name of return value. The number of elements should be same as `res_name`.
            font_size: Font size of register name.
                If not specified, take the value of `DEFAULT_FONT_SIZE`.
            value_format: Format to print data value.
                If not specified, take the value from global configuration `elem_value_format`.
            align_with: Align with specified element when placement.
                If not specified, placement follows automatic strategy.
            func_callee: Pointer to a function to perform the functionality. 

        Returns:
            Generated function unit.
        """
        # If there is existing function unit with the same hash, return existing unit.
        if self.has_object(isa_hash):
            func_unit = self.get_object(isa_hash)
            return func_unit

        # Handle default value of arguments.
        if not name:
            name = isa_hash
        if value_format is None:
            value_format = get_config("elem_value_format")
        if not isinstance(res_width, list):
            res_width = [res_width]
        if args_name is None:
            args_name = [""] * len(args_width)
        elif not isinstance(args_name, list):
            args_name = [args_name] * len(res_width)
        if res_name is None:
            res_name = [""] * len(res_width)
        elif not isinstance(res_name, list):
            res_name = [res_name] * len(res_width)

        # Create function unit.
        color = self.colormap_default_color
        func_unit = FunctionUnit(name, color, args_width, res_width, args_name, res_name,
                                 font_size, value_format, func_callee)

        # Placement function unit.
        self.place_object(func_unit, isa_hash, align_with=align_with)
        # Create animation
        self.add_animation(decl_func_unit(func_unit), None, func_unit)

        # Return function unit.
        return func_unit

    def decl_func_group(self,
                        num_unit: Union[int, List[int]],
                        isa_hash: Union[str, List[str]],
                        args_width: List[float],
                        res_width: Union[int, List[int]],
                        func_name: Union[str, List[str]] = None,
                        args_name: List[str] = None,
                        res_name: Union[str, List[str]] = None,
                        font_size: int = DEFAULT_FONT_SIZE,
                        value_format: str = None,
                        force_hw_ratio: bool = False,
                        func_callee: Callable = None) -> List[FunctionUnit]:
        """
        Declare a group of function units with a sequential of specified hash (`isa_hash`),
        arguments (`arg_width`), and return values (`res_width`) and add them to the scene as a
        group.

        Args:
            num_unit: The number of units. More than one hierachy level is accepted.
            isa_hash: Hash value of this function unit, used by `function_call`.
                Both a single hash and a sequence of hash are accepted.
            args_width: A list of bit-width of arguments.
            res_width: Bit-width of return values. If there is only one return value, one single
                interger is required.
            func_name: Function name. If not specified, take `isa_hash` as function name.
            args_name: A list of name of arguments. The number of elements should be same as
                `args_width`.
            res_name: Name of return value. The number of elements should be same as `res_name`.
            font_size: Font size of register name.
                If not specified, take the value of `DEFAULT_FONT_SIZE`.
            value_format: Format to print data value.
                If not specified, take the value from global configuration `elem_value_format`.
            force_hw_ratio: If `force_hw_ratio` is true, the number of units in one row is forced
                by the last item in `num_unit`.
                If `force_hw_ratio` is false, the shape of function groups is auto-adjusted
                according to the scene h/w ratio.
            func_callee: Pointer to a function to perform the functionality.

        Returns:
            A list of generated function unit.
        """
        def _generate_name_with_index(name: Union[str, List[str]], num_id: List[int]):
            if not isinstance(name, list):
                return name + "_".join([str(sub_id) for sub_id in num_id])
            else:
                for sub_id in num_id:
                    name = name[sub_id]
                return name

        # Handle default value of arguments.
        if not func_name:
            func_name = isa_hash
        if not isinstance(res_width, list):
            res_width = [res_width]
        if value_format is None:
            value_format = get_config("elem_value_format")
        if isinstance(num_unit, int):
            num_unit = [num_unit]
        if args_name is None:
            args_name = [""] * len(args_width)
        elif not isinstance(args_name, list):
            args_name = [args_name] * len(res_width)
        if res_name is None:
            res_name = [""] * len(res_width)
        elif not isinstance(res_name, list):
            res_name = [res_name] * len(res_width)

        # Loop across all function units.
        func_unit_list = []
        func_unit_hash = []
        num_id_list = itertools.product(*[list(range(0, numi)) for numi in num_unit])
        for num_id in num_id_list:
            # Create function unit.
            if func_name:
                name = func_name
                if isinstance(name, list):
                    name = _generate_name_with_index(name, num_id)
            else:
                name = _generate_name_with_index(isa_hash, num_id)
            color = self.colormap_default_color
            func_unit = FunctionUnit(name, color, args_width, res_width, args_name, res_name,
                                     font_size, value_format, func_callee)
            func_unit_list.append(func_unit)
            # Create hash value.
            func_unit_hash.append(_generate_name_with_index(isa_hash, num_id))

        # Placement function units.
        self.place_object_group(func_unit_list, func_unit_hash,
                                force_hw_ratio=num_unit[-1] if force_hw_ratio else None)
        # Create animation
        self.add_animation(decl_func_unit(*func_unit_list), None, func_unit_list)

        # Return a list of function units.
        return func_unit_list

    def function_call(self,
                      isa_hash: str,
                      args: List[ElemUnit],
                      args_offset: List[int] = None,
                      color_hash: Union[int, str] = None,
                      res_width: Union[int, List[int]] = None,
                      res_offset: Union[int, List[int]] = None,
                      res_value: Union[Any, List[Any]] = None,
                      res_fill_opacity: float = None,
                      res_font_size: int = DEFAULT_FONT_SIZE,
                      res_value_format: str = None) -> Union[ElemUnit, List[ElemUnit]]:
        """
        Function call.

        Args:
            isa_hash: Hash value of the specified function unit.
            args: Element units as arguments.
            args_offset: LSB offset for the argument elements.
                If not specified, 0 for each argument elements.
            color_hash: Specified hash to get color from scheme.
            res_width: Bit-width of return values. If there is only one return value, one single
                interger is required.
            res_offset: LSB offset for the result element units.
                If not specified, 0 for each result element units.
            res_value: Value of the result element units.
                If not specified, assign None or calculate by inline function.
            res_fill_opacity: Fill opacity.
                If not specified, take the value from global configuration `elem_fill_opacity`.
            res_font_size: Font size of result element unit.
                If not specified, take the value of `DEFAULT_FONT_SIZE`.
            res_value_format: Format to print result value.
                If not specified, take the value from global configuration `elem_value_format`.

        Returns:
            Result element units. If only one result value, only one element unit returns.
        """
        func_unit: FunctionUnit = self.get_object(isa_hash)

        # Handle default value of arguments.
        if args_offset is None:
            args_offset = [0 for _ in args]
        if res_width is None:
            res_width = func_unit.func_res_width_list
        elif not isinstance(res_width, list):
            res_width = [res_width]
        if res_offset is None:
            res_offset = [0 for _ in range(0, func_unit.func_res_count)]
        elif not isinstance(res_offset, list):
            res_offset = [res_offset]
        if color_hash is None:
            color_hash = self._traceback_hash()
        if res_fill_opacity is None:
            res_fill_opacity = get_config("elem_fill_opacity")
        if res_value_format is None:
            res_value_format = func_unit.func_value_format

        # Special handle for immediate operand.
        args_elem: List[ElemUnit] = []
        args_elem_exist: List[ElemUnit] = []
        dup_args_elem: List[ElemUnit] = []
        dup_args_elem_exist: List[ElemUnit] = []
        for elem in args:
            # Immediate operand:
            if isinstance(elem, tuple):
                args_elem.append(elem[0])
                # Special case for immediate, read_func_imm is aligned with the animation to move
                # animation.
                dup_args_elem.append(elem)
            else:
                args_elem.append(elem)
                args_elem_exist.append(elem)
                dup_elem = self.get_duplicate_item(elem)
                dup_args_elem.append(dup_elem)
                dup_args_elem_exist.append(dup_elem)

        # Functionality of operation: function callee
        args_elem_value: List = [arg.elem_value for arg in args_elem]
        if (res_value is None) and (func_unit.func_callee is not None) \
                and (None not in args_elem_value):
            res_value = func_unit.func_callee(*args_elem_value)
        if res_value is None:
            res_value = [None] * func_unit.func_res_count
        elif not isinstance(res_value, list):
            res_value = [res_value] * len(res_width)

        # Create result elements
        res_color_list = self.colormap_get_color(color_hash, len(res_width))
        if not isinstance(res_color_list, list):
            res_color_list = [res_color_list]
        res_elem_list = [
            ElemUnit(
                color, width, value, res_fill_opacity, res_font_size, res_value_format, 0, False)
            for width, value, color in zip(res_width, res_value, res_color_list)]

        # Create animation.
        old_dep = self.get_last_deps(*args_elem_exist)
        if old_dep is not None and not isinstance(old_dep, list):
            old_dep = [old_dep]
        animation_item = self.add_animation(
            function_call(func_unit, dup_args_elem, res_elem_list, args_offset, res_offset),
            args_elem_exist + dup_args_elem_exist, res_elem_list,
            dep=(old_dep + [func_unit]) if old_dep else [func_unit])

        # Update elements reference counter.
        for arg in args_elem_exist:
            self.set_elem_cusumer(arg, animation_item, None)
        for res in res_elem_list:
            self.set_elem_producer(res, func_unit)

        # Return single result element or a list of result elements
        if len(res_elem_list) == 1:
            return res_elem_list[0]
        else:
            return res_elem_list

    def read_func_imm(self,
                      width: float,
                      color_hash: Union[int, str] = None,
                      value: Any = None,
                      fill_opacity: float = None,
                      font_size: int = DEFAULT_FONT_SIZE,
                      value_format: str = None) -> Tuple[ElemUnit, Animation]:
        """
        Generate immediate operand for function calling.
        
        Args:
            width: Bit width.
            color_hash: Specified hash to get color from scheme.
            value: Value of the immediate element units.
                If not specified, assign None or calculate by inline function.
            fill_opacity: Fill opacity.
                If not specified, take the value from global configuration `elem_fill_opacity`.
            font_size: Font size of result element unit.
                If not specified, take the value of `DEFAULT_FONT_SIZE`.
            value_format: Format to print result value.
                If not specified, take the value from global configuration `elem_value_format`. 
           
        Returns:
            A tuple of element unit and fade-in animation.
        """
        # Handle default value of arguments.
        if fill_opacity is None:
            fill_opacity = get_config("elem_fill_opacity")
        if value_format is None:
            value_format = get_config("elem_value_format")
        if color_hash is None:
            color_hash = self._traceback_hash()

        # Create element unit.
        color = self.colormap_get_color(color_hash)
        res_elem = ElemUnit(color, width, value, fill_opacity, font_size, value_format, 0, False)

        # Retuen a tuple of element unit and animation.
        return (res_elem, read_func_imm(res_elem))

    #
    # Memory
    #
    def decl_memory(self,
                    addr_width: int,
                    data_width: int,
                    mem_range: List[Tuple[int,int]],
                    isa_hash: str = None,
                    addr_align: int = None,
                    status_width: int = 0,
                    font_size: int = DEFAULT_FONT_SIZE,
                    value_format: str = None,
                    para_enable: bool = False) -> MemoryUnit:
        """
        Declare one memory unit with a specified address width (`addr_width`), data width
        (`data_width`), and memory range (`mem_range`) and add it to the scene.

        Args:
            addr_width: Bit-width of the address port.
            data_width: Bit-width of the data port.
            mem_range: Range of memory map. Each tuple in `mem_range` presents the range of one
                memory map. The first element in tuple is the lowest address and the second element
                is the highest address.
            isa_hash: Hash value of this memory unit. Used to declare more than one memory unit.
            addr_align: Align requirement of memory range.
                If not specified, take the value from global configuration `mem_align`.
            status_width: Bit width of the status port.
                If not specified, the memory unit does not have status port.
            font_size: Font size of register name.
                If not specified, take the value of `DEFAULT_FONT_SIZE`.
            value_format: Format to print data value.
                If not specified, take the value from global configuration `elem_value_format`.
            para_enable: True means memory unit allow parallel animations. False means animations
                with this memory unit must be serialized.

        Returns:
            Generated memory unit.
        """
        # If there is existing memory unit with the same hash, return existing unit.
        if not isa_hash:
            isa_hash = "Memory"
        if self.has_object(isa_hash):
            mem_unit = self.get_object(isa_hash)
            return mem_unit

        # Handle default value of arguments.
        if isa_hash is None:
            isa_hash = "Memory"
        if addr_align is None:
            addr_align = get_config("mem_align")
        if value_format is None:
            value_format = get_config("elem_value_format")

        # Create memory unit.
        mem_color = self.colormap_default_color
        mem_unit = MemoryUnit(mem_color, addr_width, data_width, addr_align, mem_range,
                              font_size, value_format, para_enable, status_width,
                              self.get_placement_width() - 2)

        # Placement memory unit.
        self.place_object(mem_unit, isa_hash)
        # Create animation
        self.add_animation(decl_memory_unit(mem_unit), None, mem_unit)

        # Return memory unit.
        return mem_unit

    def read_memory(self,
                    addr: ElemUnit,
                    width: int,
                    offset: int = 0,
                    color_hash: Union[int, str] = None,
                    res_value: Any = None,
                    res_fill_opacity: float = None,
                    res_font_size: int = DEFAULT_FONT_SIZE,
                    res_value_format: str = None,
                    has_status_output: bool = False,
                    status_width: int = None,
                    status_value: Any = None,
                    status_fill_opacity: float = None,
                    status_font_size: int = DEFAULT_FONT_SIZE,
                    status_value_format: str = None,
                    mem_isa_hash: str = None) -> Union[Tuple[ElemUnit, ElemUnit], ElemUnit]:
        """
        Read data from the specified address.

        Args:
            addr: Address element unit.
            width: Bit width of read data.
            offset: LSB offset of read data.
            color_hash: Hash value to get color from color scheme.
            res_value: Value of data element.
            res_fill_opacity: Fill opacity.
                If not specified, take the value from global configuration `elem_fill_opacity`.
            res_font_size: Font size of result element unit.
                If not specified, take the value of `DEFAULT_FONT_SIZE`.
            res_value_format: Format to print result value.
                If not specified, take the value from global configuration `elem_value_format`. 
            has_status_output: True means output of the status port is required.
                If the memory unit does not have a status port, `has_status_output` is ignored.
            status_width: Bit width of output status.
                If not specified, the width of the generated status element unit is as same as the
                status port.
            status_value: Value of status element.
            status_fill_opacity: Fill opacity.
                If not specified, take the value from global configuration `elem_fill_opacity`.
            status_font_size: Font size of result element unit.
                If not specified, take the value of `DEFAULT_FONT_SIZE`.
            status_value_format: Format to print result value.
                If not specified, take the value from global configuration `elem_value_format`. 
            mem_isa_hash: Hash to idenify memory unit.
                If not specified, operate on the memory unit with the hash of "Memory".

        Returns:
            If having status output, return a tuple of the data and status element units.
                Otherwise, return the data element unit.
        """
        if mem_isa_hash is None:
            mem_isa_hash = "Memory"
        mem_unit: MemoryUnit = self.get_object(mem_isa_hash)

        # Handle default value of arguments.
        if res_fill_opacity is None:
            res_fill_opacity = get_config("elem_fill_opacity")
        if res_value_format is None:
            res_value_format = mem_unit.mem_value_format
        if color_hash is None:
            color_hash = self._traceback_hash()
        if status_width is None:
            status_width = mem_unit.mem_status_width
        if status_fill_opacity is None:
            status_fill_opacity = get_config("elem_fill_opacity")
        if status_value_format is None:
            status_value_format = get_config("elem_value_format")

        addr_value = None
        if addr.elem_value is not None:
            addr_value = int(addr.elem_value) + offset
            if not mem_unit.is_mem_range_cover(addr_value):
                addr_value = None
        addr_match = addr_value is not None and offset == 0

        has_status_output = mem_unit.has_status_port() and has_status_output

        if has_status_output:
            color, status_color = self.colormap_get_color(color_hash, 2)
        else:
            color = self.colormap_get_color(color_hash)

        # Create data element
        data = ElemUnit(
            color, width, res_value, res_fill_opacity, res_font_size, res_value_format, 0, False)

        # Create address mark and memory mark
        if addr_value is not None:
            addr_mark = mem_unit.get_addr_mark(addr_value, addr.elem_color)
            mem_mark = mem_unit.get_rd_mem_mark(addr_value, addr_value + width // 8, color)
            mem_unit.append_mem_mark_list(mem_mark)

        # Create status element
        if has_status_output:
            status = ElemUnit(status_color, status_width, status_value, status_fill_opacity,
                              status_font_size, status_value_format, 0, False)
        else:
            status = None

        # Create animation.
        if addr_match:
            dup_addr = self.get_duplicate_item(addr)
        else:
            dup_addr = addr
        old_dep = self.get_last_deps(addr)
        if addr_value is not None:
            animation_item = self.add_animation(
                read_memory(mem_unit, dup_addr, data, status, addr_mark, mem_mark, addr_match),
                [addr, dup_addr],
                [data, mem_mark, status] if has_status_output else [data, mem_mark],
                dep=[old_dep, mem_unit] if old_dep else [mem_unit],
                remove_after=[dup_addr] if addr_match else [addr_mark])

        else:
            animation_item = self.add_animation(
                read_memory_without_addr(mem_unit, dup_addr, data, status),
                [addr, dup_addr],
                [data, status] if has_status_output else [data],
                dep=[old_dep, mem_unit] if old_dep else [mem_unit],
                remove_after=[dup_addr])

        # Update element reference counter.
        self.set_elem_cusumer(addr, animation_item, None)
        self.set_elem_producer(data, mem_unit)
        if has_status_output:
            self.set_elem_producer(status, mem_unit)

        # Return data element and status element.
        if has_status_output:
            return data, status
        else:
            return data

    def write_memory(self,
                     addr: ElemUnit,
                     data: ElemUnit,
                     offset: int = 0,
                     color_hash: Union[int, str] = None,
                     has_status_output: bool = False,
                     status_width: int = None,
                     status_value: Any = None,
                     status_fill_opacity: float = None,
                     status_font_size: int = DEFAULT_FONT_SIZE,
                     status_value_format: str = None,
                     mem_isa_hash: str = None) -> Union[ElemUnit, None]:
        """
        Write data to the specified address.

        Args:
            addr: Address element unit.
            data: Data element unit.
            offset: LSB offset of read data.
            color_hash: Hash value to get color from color scheme.
            has_status_output: True means output of the status port is required.
                If the memory unit does not have a status port, `has_status_output` is ignored.
            status_width: Bit width of output status.
                If not specified, the width of the generated status element unit is as same as the
                status port.
            status_value: Value of status element.
            status_fill_opacity: Fill opacity.
                If not specified, take the value from global configuration `elem_fill_opacity`.
            status_font_size: Font size of result element unit.
                If not specified, take the value of `DEFAULT_FONT_SIZE`.
            status_value_format: Format to print result value.
                If not specified, take the value from global configuration `elem_value_format`. 
            mem_isa_hash: Hash to idenify memory unit.
                If not specified, operate on the memory unit with the hash of "Memory".

        Returns:
            If having status output, return status element unit. Otherwise, return None.
        """
        if not mem_isa_hash:
            mem_isa_hash = "Memory"
        mem_unit: MemoryUnit = self.get_object(mem_isa_hash)

        # Handle default value of arguments.
        if color_hash is None:
            color_hash = self._traceback_hash()
        if status_width is None:
            status_width = mem_unit.mem_status_width
        if status_fill_opacity is None:
            status_fill_opacity = get_config("elem_fill_opacity")
        if status_value_format is None:
            status_value_format = get_config("elem_value_format")

        addr_value = None
        if addr.elem_value is not None:
            addr_value = int(addr.elem_value) + offset
            if not mem_unit.is_mem_range_cover(addr_value):
                addr_value = None
        addr_match = addr_value is not None and offset == 0

        has_status_output = mem_unit.has_status_port() and has_status_output

        # Create address mark and memory mark
        if addr_value is not None:
            addr_mark = mem_unit.get_addr_mark(addr_value, addr.elem_color)
            mem_mark = mem_unit.get_wt_mem_mark(
                addr_value, addr_value + data.elem_width // 8, data.elem_color)
            mem_unit.append_mem_mark_list(mem_mark)

        # Create status element
        status_color = self.colormap_get_color(color_hash)
        if has_status_output:
            status = ElemUnit(status_color, status_width, status_value, status_fill_opacity,
                              status_font_size, status_value_format, 0, False)
        else:
            status = None

        # Create animation.
        if addr_match:
            dup_addr = self.get_duplicate_item(addr)
        else:
            dup_addr = addr
        dup_data = self.get_duplicate_item(data)
        old_dep = self.get_last_deps(addr, data)
        if addr_value is not None:
            animation_item = self.add_animation(
                write_memory(mem_unit, dup_addr, dup_data, status, addr_mark, mem_mark, addr_match),
                [addr, data, dup_addr, dup_data],
                [mem_mark, status] if has_status_output else [mem_mark],
                dep=old_dep + [mem_unit] if old_dep else [mem_unit],
                remove_after=[dup_addr, dup_data] if addr_match else [addr_mark, dup_data],
                add_after=[mem_mark])
        else:
            animation_item = self.add_animation(
                write_memory_without_addr(mem_unit, dup_addr, status, dup_data),
                [addr, data, dup_addr, dup_data],
                [status] if has_status_output else [],
                dep=old_dep + [mem_unit] if old_dep else [mem_unit],
                remove_after=[dup_addr])

        # Update element reference counter.
        self.set_elem_cusumer(addr, animation_item, None)
        self.set_elem_cusumer(data, animation_item, None)
        if has_status_output:
            self.set_elem_producer(status, mem_unit)

        if has_status_output:
            return status
        else:
            return None
