"""
ISA configuration structure.
"""


from random import randint, choice, uniform
import os
import re
import shlex
from typing import List, Dict, Any

def _convert_value(value_str: str) -> Any:
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
    
    Args:
        key: Name of the option.
        value: Value of the option.
    """
    global isa_config   # pylint: disable=global-variable-not-assigned,invalid-name
    isa_config[key] = value

def get_config(key: str, default: Any = None) -> Any:
    """
    Get configuration.

    Args:
        key: Name of the option.
        default: Default value of the option.

    Returns:
        Value of the option. If the option is not defined, return default value.
    """
    global isa_config   # pylint: disable=global-variable-not-assigned,invalid-name
    if key in isa_config:
        return isa_config[key]
    elif default is not None:
        return default
    else:
        err_msg = f"Cannot get value of {key}"
        raise ValueError(err_msg)

#
# Option Configurations.
#

class OptionDef:
    """
    Structure to define configuration options.
    """

    FIX_CFG = 0
    CONFIG_CFG = 1
    RANDOM_CFG = 2
    VALUE_CFG = 3

    def __init__(self, name: str, opt_type: int, default: Any, **kwargs):
        """
        Create structure for configuration options.

        Args:
            name: Name of config option.
            opt_type: Option type. Options: FIX_CFG, CONFIG_CFG, RANDOM_CFG.
            default: Default value of config option.
            options: Option values of config option. Defaults to None.
            condition: Condition of config option. Defaults to None.
            opt_range: Value range of config option. Defaults to None.
            transform: Function to transfer configured value. Defaults to None.
        """
        self.name = name
        self.opt_type = opt_type
        self.default = default
        self.options = None
        self.condition = None
        self.opt_range = None
        self.transform = None

        if "options" in kwargs:
            self.options = kwargs["options"]
        if "condition" in kwargs:
            self.condition = kwargs["condition"]
        if "opt_range" in kwargs:
            self.opt_range = kwargs["opt_range"]
        if "transform" in kwargs:
            self.transform = kwargs["transform"]

def def_cfg(name: str, default: Any, **kwargs) -> OptionDef:
    """
    Define one option with default value. Option can be configurable by command line.

    Args:
        name: Name of config option.
        default: Default value of config option.
        options: Option values of config option. Defaults to None.
        condition: Condition of config option. Defaults to None.
        opt_range: Value range of config option. Defaults to None.
        transform: Function to transfer configured value. Defaults to None.

    Returns:
        Structure for configuration option.
    """
    return OptionDef(name, OptionDef.CONFIG_CFG, default, **kwargs)

def def_random_cfg(name: str, **kwargs) -> OptionDef:
    """
    Define one option with random value. Default value is choosen from a list or a range.

    Args:
        name: Name of config option.
        options: Option values of config option. Defaults to None.
        opt_range: Value range of config option. Defaults to None.

    Returns:
        Structure for configuration option.
    """
    return OptionDef(name, OptionDef.RANDOM_CFG, None, **kwargs)

def def_fix_cfg(name: str, default: Any) -> OptionDef:
    """
    Define one option with fixed value. This option cannot be changed by commandline.

    Args:
        name: Name of config option.
        default: Value of config option.

    Returns:
        Structure for configuration option.
    """
    return OptionDef(name, OptionDef.FIX_CFG, default)

def def_value_cfg(name: str) -> OptionDef:
    """
    Define one value option. This option does not parse by `get_cfgs`.

    Args:
        name: Name of config option.

    Returns:
        Structure for configuration option.
    """
    return OptionDef(name, OptionDef.VALUE_CFG, None)

def get_cfgs(cfgs_list: List[OptionDef]) -> Dict:
    """
    Get value of options and return in a dictionary.

    Args:
        cfgs_list: List of option structures.

    Returns:
        A dictionary providing the value of options.
    """
    namespace = {}

    for cfg_item in cfgs_list:
        # Skip value configuration
        if cfg_item.opt_type == OptionDef.VALUE_CFG:
            continue

        # Option name
        key = cfg_item.name

        # Default value of option
        if cfg_item.opt_type == OptionDef.RANDOM_CFG:
            if cfg_item.options is not None:
                value = choice(cfg_item.options)
            elif cfg_item.opt_range is not None:
                min_val, max_val = cfg_item.opt_range
                if isinstance(min_val, int) and isinstance(max_val, int):
                    value = randint(min_val, max_val)
                else:
                    value = uniform(min_val, max_val)
            else:
                raise ValueError(
                    f"Do not know how to find default value for configuration {key}.")
        else:
            value = cfg_item.default

        # Get value from command line.
        if cfg_item.opt_type != OptionDef.FIX_CFG:
            value = get_config(key=key, default=value)

        # Check whether value is correct
        if cfg_item.options is not None:
            if value not in cfg_item.options:
                raise ValueError(
                    f"Wrong value for configuration {key}, expect options {cfg_item.options}.")

        if cfg_item.condition is not None:
            if not cfg_item.condition(value):
                raise ValueError(f"Wrong value for configuration {key}, "
                                 f"expect condition \"{cfg_item.condition}\".")

        namespace[key] = value

    return namespace

def inherit_cfgs(old_list: List[OptionDef],
                 *cfg_items: OptionDef,
                 **fix_cfg_items) -> List[OptionDef]:
    """
    Append configuration item.

    Args:
        old_list: Old list of configuration options.
        cfg_item: List of configurable options.
        fix_cfg_item: List of fixed options.

    Returns:
        New list of options.
    """
    cfgs_list: List[OptionDef] = old_list.copy()

    # Configurable options.
    for item in cfg_items:
        # Remove old item.
        for old_item in cfgs_list:
            if old_item.name == item.name:
                cfgs_list.remove(old_item)
                break
        # Add new item
        cfgs_list.append(item)

    # Fixed options.
    for key, value in fix_cfg_items.items():
        # Remove old item.
        for old_item in cfgs_list:
            if old_item.name == key:
                cfgs_list.remove(old_item)
                break
        # Add new item
        item = def_fix_cfg(key, value)
        cfgs_list.append(item)

    return cfgs_list
