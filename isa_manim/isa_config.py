"""
ISA configuration structure.
"""

import os
import re
import shlex
from typing import Union, List, Any

def _convert_value(value_str: str) -> Union[str, int, float, bool,
                                            List[str], List[int], List[float], List[bool]]:
    """
    Convert string to a value.
    """

    def is_int(string: str):
        try:
            int(string)
            return True
        except ValueError:
            return False

    def is_float(string: str):
        try:
            int(string)
            return True
        except ValueError:
            return False

    value_strip = value_str.strip()
    # Hexadecimal number
    if value_strip.startswith("0x"):
        value = int(value_strip.replace("_", ""), 16)
        return value
    # Binary number
    if value_strip.startswith("0b"):
        value = int(value_strip.replace("_", ""), 2)
        return value
    # Boolean
    if value_strip.lower() in ["true", "t"]:
        return True
    if value_strip.lower() in ["false", "f"]:
        return False
    if is_int(value_strip):
        return int(value_strip)
    if is_float(value_strip):
        return int(value_strip)
    # List with bracket
    if (value_strip.startswith("[") and value_strip.endswith("]")) \
            or (value_strip.startswith("{") and value_strip.endswith("}")):
        # Split value item.
        value_inner_str = value_strip[1:-1].strip()
        value_inner_list = re.split(r"[, ]", value_inner_str)

        # Convert each item.
        value_list = []
        for value_item_str in value_inner_list:
            value_item = _convert_value(value_item_str)
            if value_item != "":
                value_list.append(value_item)

        return value_list

    # Keep origin
    return value_str


isa_config = {
    "scene_ratio": (1/8),   # scene width / bit. Default 1.0 means 8 bit.
    "mem_addr_width": 64,
    "mem_data_width": 128,
    "mem_range": [[0, 0x1000]], # 1KB page
    "mem_align": 64,    # Memory address aligment 64B
    "elem_fill_opacity": 0.5,
    "elem_value_format": "{:d}"
}
"""
Configuration structure to pass arguments of ISA. For example, element size and vector length.
"""

# Get arguments fron environment.
if "MANIM_ISA_ARGS" in os.environ:
    isa_args_str = os.environ["MANIM_ISA_ARGS"]
    isa_args_list = shlex.split(isa_args_str)

    for isa_arg in isa_args_list:
        isa_arg_list = isa_arg.split("=")
        if len(isa_arg_list) != 2:
            raise ValueError("Wrong argument " + isa_arg + ".")

        arg_key, arg_value = isa_arg_list
        isa_config[arg_key] = _convert_value(arg_value)

        log_msg = f"ISA Config: {arg_key} = {isa_config[arg_key]}"
        print(log_msg)

def get_scene_ratio() -> float:
    """
    Return scene ratio, as scene width / bit. Default: 1.0 means 8 bits.
    """
    global isa_config   # pylint: disable=global-variable-not-assigned,invalid-name
    return isa_config["scene_ratio"]

def set_config(key: str, value: Any):
    """
    Set configuration.
    """
    global isa_config   # pylint: disable=global-variable-not-assigned,invalid-name
    isa_config[key] = value

def get_config(key: str, default: Any = None) -> Any:
    """
    Get configuration.
    """
    global isa_config   # pylint: disable=global-variable-not-assigned,invalid-name
    if key in isa_config:
        return isa_config[key]
    elif default is not None:
        return default
    else:
        err_msg = f"Cannot get value of {key}"
        raise ValueError(err_msg)

