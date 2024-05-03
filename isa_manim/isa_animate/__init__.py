"""
Pre-defined Animation for ISA behaviors

By defining common animations, users do not need to choose animation each time.
"""

from .predefine_animate import (decl_register,
                                replace_register,
                                read_elem,
                                assign_elem,
                                replace_elem,
                                decl_func_call,
                                function_call,
                                read_func_imm,
                                decl_memory_unit,
                                write_memory_without_addr,
                                read_memory_without_addr,
                                write_memory,
                                read_memory)
