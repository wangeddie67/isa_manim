"""
Objects for ISA animation

isa_manim provides several objects that appear in ISA frequently. These objects can be used in 
animate as MObject provided by Manim.

Each object is a series of MObject (Text, Rectangle, Eclipse or Arrow) packed into one VGroup.
"""

from .one_dim_reg_elem import OneDimRegElem
from .one_dim_reg import OneDimReg
from .two_dim_reg import TwoDimReg
from .function_call import FunctionCall
