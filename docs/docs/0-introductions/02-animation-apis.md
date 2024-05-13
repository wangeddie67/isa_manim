
# Animation APIs

The following APIs can be called within `SingleIsaScene` and `MultiIsaScene`.

Please reference [Animation for ISA Behaviors](../1-references/20-animation/index.md) for the details about animation.

Please reference [Data flow](../1-references/30-scene/35-data_flow.md) for additional information about `isa_data_flow`.

## APIs for Registers and Elements

### decl_register

::: isa_manim.isa_scene.isa_data_flow.IsaDataFlow.decl_register

`decl_register` has three overloading methods for different shapes of registers:

``` python
# Scalar register.
@overload
def decl_register(self, text: str, width: int,
                  value: Any = None, font_size: int = DEFAULT_FONT_SIZE, value_format: str = None, align_with = None) -> RegUnit: ...

# Vector register
@overload
def decl_register(self, text: str, width: int, elements: int,
                  value: List[Any] = None, font_size: int = DEFAULT_FONT_SIZE, value_format: str = None, align_with = None) -> RegUnit: ...

# Matrix register or a list of regsiters.
@overload
def decl_register(self, text: str, width: int, elements: int, nreg: int,
                  value: List[List[Any]] = None, font_size: int = DEFAULT_FONT_SIZE, value_format: str = None, align_with = None) -> RegUnit: ...
```

### read_elem

::: isa_manim.isa_scene.isa_data_flow.IsaDataFlow.read_elem

`read_elem` has three overloading methods for different shapes of registers.

``` python
# Scalar register.
@overload
def read_elem(self,
              vector: RegUnit, offset: int = 0, width: int = -1,
              value = None, color_hash = None, fill_opacity: float = None, font_size: int = DEFAULT_FONT_SIZE, value_format: str = None) -> ElemUnit: ...

# Vector register
@overload
def read_elem(self,
              vector: RegUnit, index: int, offset: int = 0, width: int = -1,
              value = None, color_hash = None, fill_opacity: float = None, font_size: int = DEFAULT_FONT_SIZE, value_format: str = None) -> ElemUnit: ...

# Matrix register or a list of regsiters.
@overload
def read_elem(self,
              vector: RegUnit, index: int, reg_idx: int, offset: int = 0, width: int = -1,
              value = None, color_hash = None, fill_opacity: float = None, font_size: int = DEFAULT_FONT_SIZE, value_format: str = None) -> ElemUnit: ...
```

### move_elem

::: isa_manim.isa_scene.isa_data_flow.IsaDataFlow.move_elem

> If there are further animations on this element unit, must replace variables of this element unit with return value.

`move_elem` has three overloading methods for different shapes of registers.

``` python
# Scalar register.
@overload
def move_elem(self, elem: ElemUnit, vector: RegUnit, offset: int = 0, width: int = 0): ...

# Vector register
@overload
def move_elem(self, elem: ElemUnit, vector: RegUnit, index: int, offset: int = 0, width: int = 0): ...

# Matrix register or a list of regsiters.
@overload
def move_elem(self, elem: ElemUnit, vector: RegUnit, index: int, reg_idx: int, offset: int = 0, width: int = 0): ...
```

### data_extend

::: isa_manim.isa_scene.isa_data_flow.IsaDataFlow.data_extend

> The `width` can be lower than the width of original element, as a narrow convert.

> If there are further animations on this element unit, must replace variables of this element unit with return value.

## APIs for Function Units

### decl_function

::: isa_manim.isa_scene.isa_data_flow.IsaDataFlow.decl_function

Function units are identified by hash values because some function units may share the same name. For example, one instruction applies multiple adders (`name` is "Adder"). If the option `name` is not provided, the generated function unit applies `isa_hash` as the name.

`args_width` and `args_name` should have the same number of elements. `res_width` and `res_name` also should have the same number of elements. If there is only one return value, `res_width` and `res_name` can be single elements. For example:

``` python
# Adder without carry bit.
self.decl_function("adder", [16, 16], 16, args_name=["a", "b"], res_name="sum")

# Adder with carry bit
self.decl_function("adder", [16, 16, 1], [1, 16], args_name=["a", "b", "cin"], res_name=["cout", "sum"])
```

> If one instruction apply multiple heterogenous function units, apply `decl_function` to generate each function unit and apply option `align_with` to guide the layout of function units.

> If one instruction apply multiple homogenous function unit, apply `decl_func_group` as below.

### decl_func_group

::: isa_manim.isa_scene.isa_data_flow.IsaDataFlow.decl_func_group

Generated function units share the `args_width`, `res_width`, `args_name`, `res_name`, `font_size`, `value_format` and `func_callee`. `args_width` and `args_name` should have the same number of elements. `res_width` and `res_name` also should have the same number of elements. If there is only one return value, `res_width` and `res_name` can be single elements. 

`num_unit` specifies the number of units. If one single integer is provided, the integer presents the number of units. If a list of integers is provided, the list presents the hierarchy of units. For example, `[2, 4]` means 2 groups of units and each group has 4 units.

The hash value of each function unit is specified by `isa_hash`. If one single string is provided, `decl_func_group` will generate one individual hash for each element. Take `isa_hash` is "Addr" as an example:

- If `num_unit` is 8, the hash values are `Addr0`, `Addr1`, `Addr2`, ..., `Addr7`.
- If `num_unit` is [8, 8], the hash value are `Addr0_0`, `Addr0_1`, ..., `Addr_1_0`, `Addr_1_1`, ..., `Addr7_7`

If a list is provided to the option `isa_hash`, the list must follow the hierarchy defined by `num_unit`. So that `isa_hash` can be assigned to each function unit.

The option `func_name` specifies names for function units. If `func_name` is not specified, take `isa_hash` as the name. If one single string is provided, all function units share the same function name. Otherwise, `func_name` should follow the hierarchy defined by `num_unit`.

The shape of a function group is auto-adjusted if `force_hw_ratio` is False. See [Objects Placement](../1-references/30-scene/32-placement.md) as an example.


> It is recommand to provide one single element to `num_unit`, `isa_hash` and `func_name`. `decl_func_group` will generate one individual hash for each element.

### function_call

::: isa_manim.isa_scene.isa_data_flow.IsaDataFlow.function_call

To reduce the coding complexity, `function_call` provides the capacity to perform the functionality. If one callable function has been provided to the function unit through option `func_callee` and all the argument element units have assigned value (`elem_value`), `function_call` performs the functionality by calling `func_callee` with value from all `args`. An example is as below:

``` python
mbytes = 4

# Registers
rn_reg = self.decl_register("rn", addrlen, value=0x100)
rm_reg = self.decl_register("rm", addrlen, value=0x100, align_with=rn_reg)

# Function unit
self.decl_function("addrgen", [addrlen, addrlen], addrlen,
                    name="base+offset", args_name=["base", "offset"],
                    func_callee=lambda x, y: x + y)
self.decl_function("scale", [addrlen], addrlen,
                    name=f"offset*{mbytes}", args_name=["offset"],
                    func_callee=lambda x: x * mbytes)

# Behaviors
base = self.read_elem(rn_reg)
# element value of `base` is 0x100
offset = self.read_elem(rm_reg)
# element value of `offset` is 0x100
offset = self.function_call("scale", [offset])
# element value of `offset` is 0x100 * 4 = 0x400
base = self.function_call("addrgen", [base, offset])
# element value of `base` is 0x100 + 0x400 = 0x500
```

In some situations, argument element units and result element units may not cover all bits as the bit-width of arguments and results. For example, some multiply instructions only return the high-half of the product. For such situations, `args_offset` and `res_offset` specify the LSB offset of element units. An example is as below:

``` python
# Registers
rn_reg = self.decl_register("rn", 32)
rm_reg = self.decl_register("rm", 32, align_with=rn_reg)

# Function unit
self.decl_function("multiply", [32, 32], 64)

# Behaviors
rn = self.read_elem(rn_reg)
rm = self.read_elem(rm_reg)
result = self.function_call("multiply", [rn, rm], res_width=32, res_offset=32)
```

### read_func_imm

::: isa_manim.isa_scene.isa_data_flow.IsaDataFlow.read_func_imm

The function of `read_func_imm` does not register animation directly. Instead, the tuple of element unit and fade-in animation is delivered to `funcion_call`, so that the fade-in animation will be integrated into the animation of `function_call`.

During the first step of the animation to call a function, the immediate operands fade in at the position of function arguments while other operands move to the position of function arguments.

> If directly deliver the return value of `read_func_imm` to the argument of `function_call`, it is not necessary to unpack the return value of `read_func_imm`.

> It is recommand that only deliver the return value of `read_func_imm` to the argument of `function_call`.

## APIs for Memory Units

### decl_memory

::: isa_manim.isa_scene.isa_data_flow.IsaDataFlow.decl_memory

In most situations, there is only one memory unit in the animation. The hash of this memory unit is `Memory`. Users can still declare more than one memory unit by the option `isa_hash`.

### read_memory

::: isa_manim.isa_scene.isa_data_flow.IsaDataFlow.read_memory

### write_memory

::: isa_manim.isa_scene.isa_data_flow.IsaDataFlow.write_memory

The option `has_status_output` determines whether `read_memory` and `write_memory` generate status output. If the memory unit does not have a status port, option `has_status_output` is ignored. When the memory unit has a status port:

- If `has_status_output` is False, `read_memory` and `write_memory` do not generate the status output.
  - `read_memory` returns the data element unit. `write_memory` returns None.
- If `has_status_output` is True, `read_memory` and `write_memory` generate the status output.
  - `read_memory` returns the tuple of the data and status element unit. `write_memory` returns the status element unit.

The attributes of the generated data element unit are specified by `res_value`, `res_fill_opacity`, `res_font_size` and `res_value_format`. The attributes of the status element unit are specified by another group of options, i.e. `status_width`, `status_value`, `status_fill_opacity`, `status_font_size` and `status_value_format`.

By default, `read_memory` and `write_memory` operate on the memory unit with the hash of "Memory". Still, users can specify a specified memory unit by the option of `mem_isa_hash`.
