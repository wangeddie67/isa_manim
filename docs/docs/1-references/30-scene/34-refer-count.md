# Element Reference Counter

## Reuse elements from the same index of the same register

When reading one element from one register, the accessed element is recorded. If the element is accessed again, the recorded element is used, rather than creating a new element.

The recorded element is identified by all the following attributes:

- The source register.
- The element index to access the register.
- The register index to access the register.
- The bit offset of LSB.
- The width of the accessed element.

The recorded element is returned, only when all the above attributes match.

`isa_manim.isa_scene.isa_elem_refcount.IsaElemRefCount.set_elem_source` records one element and the source attributes of this element. `isa_manim.isa_scene.isa_elem_refcount.IsaElemRefCount.get_elem_by_source` returns the record element by the source attributes. If no matched recorded element, `get_elem_by_source` returns `None`.

## Duplicate elements with multiple consumers

The animation to create one element is referenced as the producer. The animation that references one element as a source is referenced as the consumer. In most situations, one element has only one producer and multiple consumers. 

- `isa_manim.isa_scene.isa_elem_refcount.IsaElemRefCount.set_elem_producer` registers one element when the element is generated. The initial value of the reference counter is 0. `set_elem_producer` is applied where the element unit is created.
- `isa_manim.isa_scene.isa_elem_refcount.IsaElemRefCount.set_elem_cusumer` registers the last consumer animation and increases the reference counter by 1. The `set_elem_cusumer` is applied where the element unit is used as the source.
- If the reference counter is 0, `isa_manim.isa_scene.isa_elem_refcount.IsaElemRefCount.get_duplicate_item` returns the original element. If the reference counter is higher than 1, `get_duplicate_item` returns a copy of the element unit. Meanwhile, the copy i

For example, one element `A` from vector `Zm` operates with all elements in `Zn` in one vector instruction. The 0-th element of `Zn` operates with the original element `A`. Other elements of `Zn` operate with a copy of `A`. The copied elements will be added to the scene **before** the last consumer animation.

``` mermaid
flowchart TB

A1((Read one element<br/>from the register))

subgraph Copy element
A2[Element unit A]
A31[Element unit A']
A32[Element unit A'']
A33[Element unit A''']
end

A1-->A2
A2--copy-->A31--copy-->A32--copy-->A33

subgraph Add element to scene
A41[Add A']
A42[Add A'']
A43[Add A''']
A44((*))
end

A2-->A41
A31-->A42
A32-->A43
A33-->A44

subgraph Operate animation
A41-->operate0
A42-->operate1
A43-->operate2
A44-->operate3
end

operate0-->End[More animations]
operate1-->End
operate2-->End
operate3-->End
```

### General flow within animation API

The general flow within an animation API is as below:

``` mermaid
flowchart TB

A1[Call <code>get_duplicate_item</code> for source elements]
A2[Create destination elements]
A3[Play animations<br> Animations operate on duplicated element]
A4[Call <code>set_elem_cusumer</code> for source elements]
A5[Call <code>set_elem_producer</code> for destination elements]

A1-->A2-->A3-->A4-->A5
```

## _IsaElemSourceItem

::: isa_manim.isa_scene.isa_elem_refcount._IsaElemSourceItem

## _IsaElemRefCountItem

::: isa_manim.isa_scene.isa_elem_refcount._IsaElemRefCountItem

## IsaElemRefCount

::: isa_manim.isa_scene.isa_elem_refcount.IsaElemRefCount
