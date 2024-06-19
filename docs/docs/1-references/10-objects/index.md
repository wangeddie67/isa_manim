
# Objects for ISA Animation

**isa_manim** provides several graphic objects that frequently appear in ISA. These objects can be used in animate as objects provided by Manim.

- [`isa_manim.isa_objects.reg_unit.RegUnit`](11-register-unit.md) presents registers in ISA. This object can be used for general-purpose registers, vector registers, and matrix registers.
- [`isa_manim.isa_objects.func_unit.FunctionUnit`](12-function-unit.md) presents function units in ISA. This object provides the name of the function unit, as well as input arguments and output results.
- [`isa_manim.isa_objects.mem_unit.MemoryUnit`](13-memory-unit.md) presents the memory unit in ISA. This object also presents a range of memory access.
- [`isa_manim.isa_objects.elem_unit.ElemUnit`](14-element-unit.md) presents data elements in ISA. This object can be used to present data read from/written to registers and memory.

Each object is comprised of a series of MObject (Text, Rectangle, and Eclipse) packed into one VGroup. The definition of objects provides the constructor function to create one object. Objects also provide functions to return some positions in the object to control animations — for example, the position of a specified element in one vector register.

Register units and element units can also maintain values. Values can be any type: integer, floating-point, and string. Element units show values if one value is assigned. However, register units do not show any value. The global configuration option `elem_value_format` and the option `value_format` in the constructor function control the output format of values.

Function units can also maintain one pointer to a Python function. If element units as source operands provide valid values, one function unit calls the Python function and returns a valid value to element units as destination operands.

> It is not suggested to directly create and operate the above objects in user's codes. Instead, please use APIs provided in ISA scenes.
