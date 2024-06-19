# Animations for Registers and Elements

`isa_manim.isa_animate.register_animate.decl_register` declares registers by fading in all provided register objects.

`isa_manim.isa_animate.register_animate.replace_register` replaces one existing register with a new register by transform. 

An example for `decl_register` and `replace_register` is as below:

![](../../image/TestRegAnimation.gif)

Source code: [*test_reg_animation.py*](https://github.com/wangeddie67/isa_manim/blob/main/tests/isa_animate/test_reg_animation.py)

`isa_manim.isa_animate.register_animate.read_elem` reads one data element from one register by fading the provided element in the specified position.

`isa_manim.isa_animate.register_animate.assign_elem` assigns one data element to one register by moving the data element to the specified location related to the provided register.

> It is not required that the target element must share the same shape and color as the origin element.

An example for `read_elem` and `assign_elem` is as below:

![](../../image/TestElemAnimation.gif)

Source code: [*test_elem_animation.py*](https://github.com/wangeddie67/isa_manim/blob/main/tests/isa_animate/test_elem_animation.py)

> See `isa_manim.isa_objects.reg_unit.RegUnit.get_elem_pos` and `isa_manim.isa_objects.elem_unit.ElemUnit.get_elem_pos` for detail about how to index one element within one register unit or one element unit.

`isa_manim.isa_animate.register_animate.replace_elem` replaces the existing data element with a new data element by transform.

> The above functions generate a sequence of animations, but they do not register animation to Manim unless `play()` is applied on the result values

## register_animate

::: isa_manim.isa_animate.register_animate
    :members:
