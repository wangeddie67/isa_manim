
# Objects for ISA Animation

isa_manim provides several graphic objects that appear in ISA frequently. These objects can be used 
in animate as MObject provided by Manim.

- :py:class:`isa_manim.isa_objects.one_dim_reg` presents one register in just one dimension. This
  object can be used for both general-purpose registers and vector registers.
- :py:class:`isa_manim.isa_objects.two_dim_reg` presents one register with two dimensions. This 
  object can be used for matrix registers in DSA.
- :py:class:`isa_manim.isa_objects.one_dim_reg_elem` presents one element in registers. This object
  can be used to present data read from/write to one register. For example, one element in
  one vector register.
- :py:class:`isa_manim.isa_objects.func_unit` presents one function call in ISA flow. This 
  object provides the name of the function, as well as input arguments and output results.
- :py:class:`isa_manim.isa_objects.mem_unit` presents the memory access in ISA flow.
- :py:class:`isa_manim.isa_objects.mem_map` presents the range of memory access. This object 
  colors the accessed memory addresses.

Each object is a series of MObject (Text, Rectangle, Eclipse or Arrow) packed into one VGroup.

## Register with one dimension

:py:class:`isa_manim.isa_objects.one_dim_reg` presents one register in just one dimension, which
can be used for both general-purpose registers and vector registers. 128-bit register with one 
dimension is as below:

.. image:: _static/TestOneDimReg_ManimCE_v0.17.3.png
  :width: 800

As shown in the above figure, such an object contains two MObject:
- `reg_rect` presents the register, whose width presents the bit width of the register. By default,
  1.0 in the scene means 8 bits in the register.
- `label_text` presents the name of the register, whose right boundary is close to the left boundary 
  of `reg_rect`.

**Note**: By default, the origin point is located in the center position of `reg_rect`, which is
different from the center position of this object. It is suggested to use function `shift` rather 
than function `move_to` to change the location of the register.

The object for registers with one dimension can be assigned a register value, but the object does
not show the value in the graphic object.

The format of 

## Register with two dimension

:py:class:`isa_manim.isa_objects.two_dim_reg` presents one register with two dimensions, which can
be used for matrix registers in DSA as well as a group of vector registers. Four 128-bit registers
are as below:

.. image:: _static/TestTwoDimReg_ManimCE_v0.17.3.png
  :width: 800

As shown in the above figure, such an object contains several MObject:
- `reg_rect_list` presents registers, whose width presents the bit width of the register. By
  default, the height of each register or each row of the matrix register is 1.0.
- `label_text_list` presents the name of registers, whose right boundary is close to the left 
  boundary of `reg_rect_list`.

Each item in `label_text_list` is horizontally aligned with the corresponding item in 
`reg_rect_list`. When presenting a two-dimension register, there is only one item in 
`label_text_list` which is aligned with the first item in `reg_rect_list`.

**Note**: By default, the origin point is located in the center position of the first register in
`reg_rect`, which is different from the center position of this object. It is suggested to use 
function `shift` rather than function `move_to` to change the location of the register.

## Element in register

:py:class:`isa_manim.isa_objects.one_dim_reg_elem` presents one element in registers. This object
can be used to present data read from/write to one register. For example, one element in one vector 
register.

.. image:: _static/TestOneDimRegElem_ManimCE_v0.17.3.png
  :width: 800

As shown in the above figure, such an object contains two MObject:
- `elem_rect` presents the element, whose width presents the bit width of the register. By default,
  the height of the element is 1.0.
- `value_text` presents the value of the element.

`value_text` is centrally aligned with `elem_rect`. Moreover, the width of `value_text` should not
be greater than the width of `elem_rect`.  If `value_text` has too many characters, `value_text`
is scaled to fit the width of `elem_rect`.

By default, the origin point is the same as the center position of this object.

## Function call

:py:class:`isa_manim.isa_objects.func_unit` presents one function call in ISA flow. This object
can be used to present one function unit (like floating-point multiply), one operator (like +/-),
or one predefined function.

This object provides the name of the function, as well as input arguments and output results.

.. image:: _static/TestFunctionCall_ManimCE_v0.17.3.png
  :width: 800

As shown in the above figure, such an object contains several MObject:
- `args_rect` presents the arguments, whose width presents the bit width of each argument. 
- `args_text` presents the name of each argument, which is centrally aligned with the corresponding
  arguments.
- `func_ellipse` presents the function, whose width should cover all arguments and whose height is
  1.0 by default.
- `label_text` presents the name of the function, which is centrally aligned with `func_ellipse`.
- `res_rect` presents the return value, whose width presents the bit width of the result.

The height of `args_rect`, `func_ellipse` and `res_rect` is 1.0. Hence, the total height of such an
object is 5.0. 

**Note**: By default, the origin point is located in the center position of the first register in
`func_ellipse`, which is different from the center position of this object. It is suggested to use 
function `shift` rather than function `move_to` to change the location of the register.

## Memory unit

:py:class:`isa_manim.isa_object.mem_unit` presents memory access in ISA flow.

.. image:: _static/TestMemoryUnit_ManimCE_v0.17.3.png
  :width: 800

As shown in the above figure, such an object contains several MObjects:
- `mem_rect` presents the memory unit, whose size is fixed as 4.0 x 3.0.
- `addr_rect` presents the address of memory access, whose width presents the width of the 
  address.
- `data_rect` presents the data of memory access, whose width presents the width of the data bus.
- `mem_map_rect` presents the position of a memory map.

The height of the entire memory unit is 6.0 because one memory map object costs 2.0 in height.

**Note**: By default, the origin point is located in the center position of the first register in
`mem_rect`, which is different from the center position of this object. It is suggested to use 
function `shift` rather than function `move_to` to change the location of the register.

## Memory map

:py:class:`isa_manim.isa_object.mem_map` presents accessed memory addresses by coloring the accessed
memory access in a horizontal block.

.. image:: _static/TestMemoryMap_ManimCE_v0.17.3.png
  :width: 800

As shown in the above figure, one rectangle presents one certain range from the entire memory. The 
left address is inclusive while the right address is exclusive. The accessed addresses are colored 
in the rectangle. The upper half presents the read addresses while the bottom half presents the
written addresses. 

**Note**: By default, the origin point is located in the center position of the first register in
`mem_map_rect`, which is different from the center position of this object. It is suggested to use 
function `shift` rather than function `move_to` to change the location of the register.

The memory map should use with the memory unit. The memory map is placed at the position marked by
`MemoryUnit.mem_map_rect`.
