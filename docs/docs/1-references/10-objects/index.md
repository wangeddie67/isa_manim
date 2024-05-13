
# Objects for ISA Animation

**isa_manim** provides several graphic objects that appear in ISA frequently. These objects can be used in animate as objects provided by Manim.

- [`isa_manim.isa_objects.reg_unit.RegUnit`](11-register-unit.md) presents registers in ISA. This object can be used for general-purpose registers, vector registers, and matrix registers.
- [`isa_manim.isa_objects.func_unit.FunctionUnit`](12-function-unit.md) presents function units in ISA. This object provides the name of the function unit, as well as input arguments and output results.
- [`isa_manim.isa_objects.mem_unit.MemoryUnit`](13-memory-unit.md) presents the memory unit in ISA. This object also presents a range of memory access.
- [`isa_manim.isa_objects.elem_unit.ElemUnit`](14-element-unit.md) presents data elements in ISA. This object can be used to present data read from/written to registers and memory.

Each object consists of a series of MObject (Text, Rectangle, Eclipse or Arrow) packed into one VGroup. The definition of objects provides the constructor function to create one object. Objects also provide functions to return some positions in the object to control animations. For example, the position of a specified element in one vector, or the position of one source/destination operand in one function unit.

Register units and element units can also maintain values. Values can be any type: integer, floating-point, and string. If values exist, element units show values while register units do not show any value. The output format of values can be controlled by the global configuration option `elem_value_format` and the option `value_format` in the constructor function. One string following the format string of Python is necessary.

Function units can also maintain one pointer to a Python function. If element units as source operands provide valid values, one function unit can perform functionality and return a valid value.

> It is not suggested to directly create and operate the above objects in user's codes. Instead, please use APIs provided in ISA scenes.
