# Animation Flow

Several data structures are implemented for the animation flow algorithm:

- `isa_manim.isa_scene.isa_animate.IsaAnimateItem` provides the data structure of one single animation, including `IsaAnimateItem` of dependency objects.
- `isa_manim.isa_scene.isa_animate._IsaAnimateSection` provides the data structure of one animation section.
- `isa_manim.isa_scene.isa_animate._IsaAnimateStep` provides the data structure of one animation step.

`isa_manim.isa_scene.isa_animate.IsaAnimationFlow` provides the animation flow algorithm. When registering one animation, `add_animation` is called to generate the `IsaAnimationItem` and recognize the dependency with registered animations. At the end of one section, `switch_section` is called to generate the `_IsaAnimateSection`.

> When sequentially calling `switch_section` more than once, the final efforts look like the intersection of two `switch_section`.

When rendering the animation, `analysis_animation_flow` is called to analyze the animation flow and generate `_IsaAnimateStep`. As the result of the animation flow algorithm, Animation steps are stored in `animation_step_list`.

## IsaAnimateItem

::: isa_manim.isa_scene.isa_animate.IsaAnimateItem

## _IsaAnimateSection

::: isa_manim.isa_scene.isa_animate._IsaAnimateSection

## _IsaAnimateStep

::: isa_manim.isa_scene.isa_animate._IsaAnimateStep

## IsaAnimationFlow

::: isa_manim.isa_scene.isa_animate.IsaAnimationFlow
