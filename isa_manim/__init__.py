"""
Library to generate ISA behavior by Manim.
"""

from manim import *

# Objects for ISA flow.
from .isa_objects import OneDimReg, TwoDimReg, OneDimRegElem, FunctionCall

# Animation for ISA flow.
from .isa_animate import (decl_register,
                          replace_register,
                          concat_vector,
                          read_elem,
                          assign_elem,
                          replace_elem,
                          decl_func_call,
                          function_call)

# Scene for ISA flow
from .isa_scene import (IsaAnimateItem,
                        IsaAnimationMap,
                        IsaPlacementItem,
                        IsaPlacementMap,
                        IsaColorMap)

from .isa_scene import SingleIsaScene, MultiIsaScene
