
# Animation Scheduling

As explained in previous pages, the animation scheduling and function interfaces are hidden behind the APIs provided by scenes. However, users still need to understand the animation scheduling algorithm so that users can apply APIs at the appropriate time.

In the original Manim, animations are ordered by the order to apply `play()`. However, when describing instructions with parallel behaviors, not only vector instructions but also some scalar instructions, it will not be convenient to manage the order of animations by hand.

The animation flow algorithm takes the responsibility for ordering the animations according to their dependencies. When all the dependency is released, one animation can play. There are two ways to build up dependencies between animations:

One kind of dependency is referenced as consumer-producer dependency. Animations always consume some objects and generate new objects. If any consumed object of one animation (A) is the produced object of another element (B), it is defined that the first animation (A) depends on the second animation (B). The first animation (A) must play after the second animation (B). Consumer objects include not only the source objects but also background objects. For example, the consumer objects of animation to call a function include both source elements and the function unit.

The other kind of dependency is called serialization dependency. For function and memory units, it is limited to only one animation related to such units that can play once. 

One animation can play only the following conditions are addressed:

- All consumer-producer dependencies of one animation are addressed.
- There is no conflict of serialization dependency.

The animations are organized into two levels.

- Animation steps consist of animations that can play parallelly. For example, the same animation applies to vector elements. Animations within one step do not have dependencies with each other. The animation flow algorithm analyzes the dependencies between animations and collects animations without dependencies into one step.

- Animation sections consist of a sequence of animation steps. The splitter between sections is signed by `end_section()`. The animations after `end_section()` cannot play before `end_section()`. Similarly, the animation before `end_section()` cannot play after `end_section()` either. Hence, there is no dependency between animations within different sections.

The algorithm to schedule animation within one section is shown below:

``` mermaid
flowchart TB

A(Begin)
B[Build dependency graph]
C[While dependency graph<br> is not empty]
D[Select animation items<br> with all depedency addressed]
E[Remove selected animation<br> items from dependency graph]
F[Pack selected animation<br> items into one animation step]
G[Add animation step into<br> animation section]
Z(End)

A-->B-->C-->D-->E-->F-->G-->C
C--"graph is empty"-->Z
```

Moreover, several additional steps are added in the section:

- At the first step of one section, the camera is moved or scaled if necessary.
- At the last step of one section, `wait()` is applied to keep the animation.
- After the last step of one section, items on the scene are removed unless:
  - if the option of `fade_out` is `False`, no item is removed.
  - if the option of `keep_object` is not empty, specified items are kept on the scene.

Please reference [Reference/Scene/Animation Flow](../1-references/30-scene/33-animation-flow.md) for implementation.

## Color Scheme

The color of objects in ISA scenes can be allocated automatically by color scheme. Each new item 
will be assigned a color in the color scheme. 

:py:class:`isa_manim.isa_scene.isa_color_map.IsaColorMap` provides the functionality to manage
object color. The constructor function can change the default color and the color scheme.

A hash controls the color of objects. The objects with the same hash value share the 
same color.

## Advanced schedule features

To generate richer and clearer animations, animation flow scheduling also provides the following features:

- Reuse elements from the same index of the same register. When reading one element from one register, the accessed element is recorded. If the element is accessed again, the recorded element is used rather than creating a new element.
- Duplicate elements with multiple consumers. If one element has multiple consumers, the first consumer references the original element unit, while other consumers reference the copy of this element unit.

Please reference [Reference/Scene/Reference Counter](../1-references/30-scene/34-refer-count.md) for implementation.

## Tips to Control the Animation Flow

In general, it is not necessary to call extra functions to control the animation flow. In some situations, more guidance can help users achieve a better experience.

- `end_section()` can perform as a barrier to split animations into several sections and stop animations to execute parallelly. For example, `end_section()` is appropriate if you want animations about one vector element to play separately as a highlight from other vector elements.
    - `fade_out=False` keeps all objects on the scene.
- The combination of `fade_out` and `keep_objects` can perform fine-grained control to keep some objects over sections. If `fade_out` is True, all objects are removed except those specified by `keep_objects`.
