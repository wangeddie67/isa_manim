
# Animation for ISA Behaviors

isa_manim provides several animations that appear in ISA frequently so that users do not need to
choose animations for ISA behaviors.

Animations can be categorized into three types:

- Animation for registers, including declaring, concatenating and replacing registers.
- Animation for elements, including reading, assigning and replacing elements.
- Animation for function, including declaring and calling function.

isa_manim provides one function for each kind of animation. Each function accepts related objects 
and returns Animation.

## Animation for registers

Animations for registers include declaring, concatenating and replacing registers, as below:

.. image:: _static/TestRegAnimation_ManimCE_v0.17.3.gif
  :width: 800

:py:func:`isa_manim.isa_animate.predefine_animate.decl_register` declares registers by fading in
all provided register objects.

:py:func:`isa_manim.isa_animate.predefine_animate.replace_register` replaces the existing register 
object with a new register object by fading out the old one and fading in the new one. The new
object can be left/right/center-aligned with the old object.

:py:func:`isa_manim.isa_animate.predefine_animate.concat_vector` concatenates registers into one
new register. Besides a list of existing registers, one new register should be provided. Existing
registers are moved to the new registers in the order specified by input arguments. The first 
source register is ordered in the lowest bits.

After source registers are ordered in the same location as the new register, the source registers
are fading out while the new register is fading in.

## Animation for elements

Animations for elements include reading, assigning and replacing elements, as below:

.. image:: _static/TestElemAnimation_ManimCE_v0.17.3.gif
  :width: 800

:py:func:`isa_manim.isa_animate.predefine_animate.read_elem` reads one data element from one 
register by fading in the provided element at one specified location related to the provided 
register.

:py:func:`isa_manim.isa_animate.predefine_animate.assign_elem` assigns one data element to one 
register by moving the data element to one specified location related to the provided register.

Both :code:`read_elem` and :code:`assign_elem` apply the location related to one register. If the 
register is one scalar register, the element covers the lower bits; if the register is one vector
register, the element covers one specified index in the register.

If the register is one two-dimension register, the element is specified by both the index among
rows and the index within one row. If the index within one row is beyond the range of elements 
within one register, it overflows to the next register. If there is no next row, the index overflows
to the first row. Therefore, it is possible to index all elements in one two-dimension register by
one single index.

:py:func:`isa_manim.isa_animate.predefine_animate.replace_elem` replaces the existing data element 
object with a new data element object by fading out the old one and fading in the new one. The new
object can be left/right/center-aligned with the old object.

## Animation for functions

Animations for functions include declaring and calling one function, as below:

.. image:: _static/TestFuncAnimation_ManimCE_v0.17.3.gif
  :width: 800

:py:func:`isa_manim.isa_animate.predefine_animate.decl_function` declares one function unit by 
fading in.

:py:func:`isa_manim.isa_animate.predefine_animate.function_call` presents how elements pass through
one function unit in two steps. In the first step, elements are moved to arguments of one function
unit. In the second step, elements are faded out while one result element is faded in at the 
location of the result of one function unit.

## Animation for the memory unit

Animations for memory include declaring one unit and reading/writing memory, as below:

.. image:: _static/TestMemUnitAnimation_ManimCE_v0.17.3.gif
  :width: 800

.. image:: _static/TestMemMapAnimation_ManimCE_v0.17.3.gif
  :width: 800

:py:func:`isa_manim.isa_animate.predefine_animate.decl_memory_unit` declares one memory unit by
fading in.

:py:func:`isa_manim.isa_animate.predefine_animate.read_memory` presents the animation to read data
from memory. The address item is fading out while the data item is fading in. Meanwhile, the memory
map is replaced by fading in/out if the old or new memory map is provided.

:py:func:`isa_manim.isa_animate.predefine_animate.write_memory` presents the animation to write data
to memory. The address item and data item are fading out. Meanwhile, the memory map is replaced by 
fading in/out if the old or new memory map is provided.
