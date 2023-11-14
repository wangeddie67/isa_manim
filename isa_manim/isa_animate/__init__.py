"""
Pre-defined Animation for ISA behaviors

By defining common animations, users do not need to choose animation each time.
"""

from .predefine_animate import (decl_register,
                                replace_register,
                                concat_vector,
                                read_elem,
                                assign_elem,
                                replace_elem,
                                decl_func_call,
                                function_call,
                                decl_memory_unit,
                                write_memory_without_addr,
                                read_memory_without_addr,
                                write_memory,
                                read_memory)
