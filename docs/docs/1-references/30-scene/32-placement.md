# Objects Placement

`isa_manim.isa_scene.isa_placement.IsaPlacementMap` provides the data structures and function interfaces for object placement. The major duty of `IsaPlacementMap` includes:

- `_placement_object_dict` provides one dictionary of objects in the scene. The key of the dictionary can be an integer or string. The value of the dictionary is an entity of `isa_manim.isa_scene.isa_placement.IsaPlacementItem`. The data structure provides the position information of one object.
- `_placement_map` presents the placement map as a 2-D array of an integer. Each element in the array presents the status of one single square of the grid.

`IsaPlacementMap` provides several groups of APIs to operate the dictionary and the map. At first, `has_object` and `get_object` are used to operate the placement dictionary. `has_object` checks whether one specified hash exists in the dictionary and `get_object` returns the object associated with the specified hash.

Then, `place_object` adds one single object to the placement map and `place_object_group` adds a group of objects to the placement map. Both of these two functions call `place_placement_item` to find an appropriate space to place objects.

The following functions return the status of the placement map:

- `get_placement_width` and `get_placement_height` returns the width and height of the actual occupied map. Only occupied columns/rows or margins are counted.
- `get_placement_origin` returns the central position of the placement map.
- `get_camera_scale` returns the scale factor of the placement to fit into a specified camera. The value provided by this camera is used to show all objects in the scene by scaling the camera.
- `dump_placement` returns a string to present the placement for debugging.

The following functions operate on the placement map. `reset_placement` removes all placed objects and resizes the placement map to the initialization size. `resize_placement` resizes the placement map to a specified size while keeping all placed objects.

## Flow charts

The flow charts to add one single object in the placement map:

``` mermaid
flowchart LR

subgraph place_object
A1[Get align row if necessary]
A2[Create a placement item]
A3[Add item to the placement dictionary]
A4[End]

A1-->A2-->A3==>B1

subgraph place_placement_item
B1[Try to place item into the placement map]
B2{Placement success}
B3[Mark the item in the placement map]
B4[Resize the placement with a fix h/w ratio]
end

B1-->B2
B2--"Yes"-->B3==>A4
B2--"No"-->B4-->B1

end
```

The flow graph to add one group of objects in the placement map:

``` mermaid
flowchart LR

subgraph place_object_group
A1[Create placement items]
A2[Convert the object group to a object matrix]
A3[Create place holder for the entire group]
A4[Add each item in the group to the dictionary and map]
A5[End]

A1==>C1
A2-->A3==>B1
A4-->A5

subgraph place_placement_item
B1[Try to place item into the placement map]
B2{Placement success}
B3[Mark the item in the placement map]
B4[Resize the placement with a fix h/w ratio]
end

B1-->B2
B2--"Yes"-->B3==>A4
B2--"No"-->B4-->B1

subgraph Get suitable shape of objects
C1{h/w ratio is fix?}
C2[Take fixed h/w ratio as the shape of the object group]
C3[Count the width and the height of all objects in one row including marigins]
C4{if the h/w ratio is larger than the ratio of scene}
C5[Double the elements in the shape]
C6[Take this h/w ratio as the shape of the object group]

C1--"Yes"-->C2==>A2
C1--"No"-->C3-->C4
C4--"Yes"-->C5-->C3
C4--"No"-->C6==>A2
end

end
```

## IsaPlacementItem

::: isa_manim.isa_scene.isa_placement.IsaPlacementItem

## IsaPlacementMap

::: isa_manim.isa_scene.isa_placement.IsaPlacementMap
