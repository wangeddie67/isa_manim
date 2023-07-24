
# Scenes for ISA Behaviors

isa_manim provides scenes for ISA animation, which provide the following functionalities:

- APIs to describe ISA animation.
- ISA objection placement.
- Animation flow analysis.
- Color scheme.

## Object Placement

ISA objects are placed into the placement according to the specified algorithm. By default, the area
of the placement is defined by `config.frame_height` and `config.frame_width`. As the increasing of
items, the range of placement is scaled, but the ratio of height and width is kept.

For placement with the height of `H` and the width of `W`, the left-up corner of the placement 
is the origin point of the frame:

- The left point of the placement is `(0, H/2)`.
- The right point of the placement is `(W, H/2)`.
- The up point of the placement is `(W/2, 0)`
- The down point of the placement is `(W/2, H)`

The placement algorithm must address the following limitations:

- There is a margin of 1.0 between each object in all directions.
- There is a margin of 1.0 between each object and the boundary of the placement.
- The ratio of height and width of the placement is kept as the h/v ratio of the frame.
- In one row, only the same kind of object can be allocated.
  - For example, function units can be placed vertically aligned, but registers must be placed in
    a different row.

:py:class:`isa_manim.isa_scene.isa_placement.IsaPlacementMap` provides the object placement 
manager. The placement manager will provide a location for each object when registering it:

- Scalar registers, vector registers, vector register groups or matrix registers.
- Function units.

Data elements should not be registered to the placement manager because they are moved between the 
above objects.

The placement algorithm abstracts the placement into an array. Each row in the array presents 1.0 
in the vertical direction while each column in the array presents 1.0 in the horizontal direction.
The value of items in the placement array describes the status of each item:

- 0 means the item is free to allocate;
- 1 means the item is a margin between objects or a margin between objects and items.
- 2 means the item is occupied by a register.
- 3 means the item is occupied by a function unit.

Hence, the placement algorithm became one question to find one rectangle space in the placement 
array, which addresses all the following conditions:

- the rectangle is larger enough for the object to place.
- the rectangle is free to allocate (all items are 0).
- items around the rectangle have not been allocated by another object (all items are 0 or 1).
- all items on the same row with the rectangle should be free (0), margin (1) or the same type of
  object to place.

If such a rectangle cannot be found in the current placement array, the placement array is scaled
until such a rectangle can be found.

.. image:: _static/TestIsaPlacementMap_ManimCE_v0.17.3.png
  :width: 800

## Animation Flow Analysis



## Color Scheme

The color of objects in ISA scenes can be allocated automatically by color scheme. Each new item 
will be assigned a color in the color scheme. 

:py:class:`isa_manim.isa_scene.isa_color_map.IsaColorMap` provides the functionality to manage
object color. The default color and the color scheme can all be changed by the constructor function.

The color of objects can be controlled by a hash. The objects with the same hash value share the 
same color.

## ISA Scenes Manager

## ISA Scenes

One scene for ISA animation should inherit from both the ISA scene manager as well as the scene 
provided by Manim. The frontier provides the functionality of object placement, animation flow 
analysis and color scheme. The latter provides the functionality of the Manim animation.

ISA scenes should overwrite the behavior of the function `construct`. It is suggested to provide 
another function `construct_isa_flow` to users to describe the behavior of ISA. In function 
`construct`, call function `play` or `wait` according to the result of the animation flow analysis.

ISA scene should pay attention on adjust the location of the camera so that objects can be seen. 
Because the object placement places objects at the right-bottom side of the origin, objects cannot
be moved to the center of the frame by only changing the height and width of the frame.

### ISA Scene for Single Instruction

:py:class:`isa_manim.isa_scene.single_isa_scene.SingleIsaScene` is used to describe one single 
instruction. Hence, it only provides one title, by function `draw_title`.

The height of the frame is 9 while the width of the frame is 16.

:py:class:`isa_manim.isa_scene.single_isa_scene.SingleIsaScene` applies `ZoomedScene`. 
The camera frame of the zoomed scene covers the area of the object placement while the display 
frame of the zoomed scene covers the area below the title (from 3.0 to the bottom, from the left to 
the right).

The behavior of ISA is described in the function `construct_isa_flow`. Instead of `switch_section`, 
apply `end_section` at the end of a sequence of contiguous animations because it would adjust the 
position of objects.

### ISA Scene for Multiple Instructions

:py:class:`isa_manim.isa_scene.multi_isa_scene.MultiIsaScene` performs the same behavior as the ISA
scene for single instruction, except it provides one subtitle below the title by function
`draw_subtitle`. Hence, the display frame of the zoomed scene covers the area below the subtitle (from 2.0 to the bottom, from the left to the right).

Moreover, the function `start_section` is provided to reset the object placement, which should be 
placed before each instruction. As below:

```python
def construct_isa_flow(self):
    self.start_section("instruction 1")
    # Instruction behaviors.
    self.end_section()

    self.start_section("instruction 2")
    # Instruction behaviors.
    self.end_section()
```
