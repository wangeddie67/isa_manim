"""
Library to generate ISA behavior by Manim.
"""

# Mobjects for ISA flow.
from .isa_objects import OneDimReg, OneDimRegElem

# Animation for ISA flow.
from .isa_animate import IsaAnimate

from .isa_animate import assign_elem
from .isa_animate import concat_vector
from .isa_animate import counter_to_predicate
from .isa_animate import data_convert
from .isa_animate import read_elem
from .isa_animate import read_scalar_reg, read_vector_group, read_vector_reg

# Scene for ISA flow
from .isa_scene import MoveFlowScene
