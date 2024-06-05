"""
Library to generate ISA behavior by Manim.
"""

from manim import *

# Objects for ISA flow.
from .isa_objects import (RegUnit,
                          ElemUnit,
                          FunctionUnit,
                          MemoryUnit)

# Animation for ISA flow.
from .isa_animate import (decl_register,
                          replace_register,
                          read_elem,
                          assign_elem,
                          replace_elem,
                          decl_func_unit,
                          read_func_imm,
                          function_call,
                          decl_memory_unit,
                          read_memory_without_addr,
                          write_memory_without_addr,
                          read_memory,
                          write_memory)

# Scene for ISA flow
from .isa_scene import (IsaAnimateItem,
                        IsaAnimationFlow,
                        IsaPlacementItem,
                        IsaPlacementMap,
                        IsaColorMap)

from .isa_scene import SingleIsaScene, MultiIsaScene

from .isa_config import get_config, set_config

from .isa_utils import calculate_mem_range
