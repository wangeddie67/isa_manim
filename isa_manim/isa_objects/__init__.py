"""
Objects for ISA animation

isa_manim provides several objects that appear in ISA frequently. These objects can be used in 
animate as MObject provided by Manim.

Each object is a series of MObject (Text, Rectangle, Eclipse or Arrow) packed into one VGroup.
"""

from .reg_elem_unit import RegElemUnit
from .reg_unit import RegUnit
from .func_unit import FunctionUnit
from .mem_unit import MemoryUnit
