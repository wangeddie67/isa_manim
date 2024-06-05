"""
ISA configuration structure.
"""


from math import ceil
from random import randint, choice, uniform
import os
import re
import shlex
from typing import List, Dict, Tuple, Any
from typing import overload

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

def def_cfg(name: str,
            cfg_type,
            default: Any,
            options: List[Any] = None,
            condition = None,
            cfg_range: Tuple[Any, Any] = None) -> Dict:
    """
    Define configuration structure.

    Args:
        name (str): Name of config option.
        cfg_type (type): Type of config option.
        default (Any): Default value of config option. Options: int, str, float, "fix_cfg",
                        "reg_index".
        options (List[Any], optional): Option values of config option. Defaults to None.
        condition (optional): Condition of config option. Defaults to None.
        cfg_range ([Any, Any], optional): Value range of config option. Defaults to None.

    Returns:
        Dict: Configuration structure.
    """
    cfg_dict = {"name": name, "type": cfg_type, "default": default}

    if cfg_type == "fix_type":
        return cfg_dict

    if options:
        cfg_dict["options"] = options
    if condition:
        cfg_dict["condition"] = condition
    if cfg_range:
        cfg_dict["range"] = cfg_range
    return cfg_dict

def def_fix_cfg(name: str, default: Any) -> Dict:
    """
    Define configuration structure with fixed value. This option cannot be changed by commandline.

    Args:
        name (str): Name of config option.
        default (Any): Value of config option.

    Returns:
        Dict: Configuration structure.
    """
    return {"name": name, "type": "fix_cfg", "default": default}

@overload
def def_esize_cfg() -> Dict: ...

@overload
def def_esize_cfg(options: List[int]) -> Dict: ...

@overload
def def_esize_cfg(name: str) -> Dict: ...

@overload
def def_esize_cfg(name: str, options: List[int]) -> Dict: ...

def def_esize_cfg(*args, **kwargs) -> Dict:
    """
    Pre-defined configuration structure for "esize", default is 32.
    Used by Fpsimd/SME/SVE instructions.

    Args:
        options (List[int], optional): Option values of config option. Defaults to [32].
        name (str, optional): Name of config option.. Defaults to "esize".

    Returns:
        Dict: Configuration structure of "esize".
    """
    # Handle args and kwargs.
    options = [32]
    name = "esize"
    for arg in args:
        if isinstance(arg, str):
            name = arg
        if isinstance(arg, list) and len(arg) >= 1:
            options = arg
    for key, arg in kwargs.items():
        if key == "name":
            name = arg
        if key == "options":
            options = arg

    if len(options) == 1:
        return {"name": name, "type": "fix_cfg", "default": options[0]}
    else:
        default = 32 if 32 in options else options[-1]
        return {"name": name, "type": int, "options": options, "default": default}

@overload
def def_esize64_cfg() -> Dict: ...

@overload
def def_esize64_cfg(options: List[int]) -> Dict: ...

@overload
def def_esize64_cfg(name: str) -> Dict: ...

@overload
def def_esize64_cfg(name: str, options: List[int]) -> Dict: ...

def def_esize64_cfg(*args, **kwargs) -> Dict:
    """
    Pre-defined configuration structure for "esize", default is 64.
    Used by aarch64 instructions.

    Args:
        options (List[int], optional): Option values of config option. Defaults to [64].
        name (str, optional): Name of config option.. Defaults to "esize".

    Returns:
        Dict: Configuration structure of "esize".
    """
    # Handle args and kwargs.
    options = [64]
    name = "esize"
    for arg in args:
        if isinstance(arg, str):
            name = arg
        if isinstance(arg, list) and len(arg) >= 1:
            options = arg
    for key, arg in kwargs.items():
        if key == "name":
            name = arg
        if key == "options":
            options = arg

    if len(options) == 1:
        return {"name": name, "type": "fix_cfg", "default": options[0]}
    else:
        default = 64 if 64 in options else options[-1]
        return {"name": name, "type": int, "options": options, "default": default}

def def_vl_cfg(name: str = "vl") -> Dict:
    """
    Pre-defined configuration structure for "vl" (vector length of SVE/SME), default is 256.
    Used by SME/SVE instructions.

    Args:
        name (str, optional): Name of config option.. Defaults to "vl".

    Returns:
        Dict: Configuration structure of "vl".
    """
    return {"name": name, "type": "vl_cfg", "condition": "vl >= 128", "default": 256}

def def_datasize_cfg(name: str = "datasize") -> Dict:
    """
    Pre-defined configuration structure for "datasize" (vector length of fpsimd), default is 128.
    Used by Fpsimd instructions.

    Args:
        name (str, optional): Name of config option.. Defaults to "datasize".

    Returns:
        Dict: Configuration structure of "datasize".
    """
    return {"name": name, "type": int, "options": [64, 128], "default": 128}

def def_nreg_cfg(name="nreg",   # pylint: disable=dangerous-default-value
                 options=[2, 4],
                 default=2) -> Dict:
    """
    Pre-defined configuration structure for "nreg" (Register number), default is 2.
    Used by SME/SVE instructions.

    Args:
        name (str, optional): Name of config option.. Defaults to "datasize".

    Returns:
        Dict: Configuration structure of "datasize".
    """
    if len(options) == 1:
        return {"name": name, "type": "fix_cfg", "default": options[0]}
    else:
        return {"name": name, "type": int, "options": options, "default": default}

def def_reg_cfg(name: str) -> Dict:
    """
    Define configuration structure of register name.

    Args:
        name (str): Register name.

    Returns:
        Dict: Configuration structure of register name.
    """
    cfg_dict = {"name": name, "type": "reg_index", "default": name[1:]}

    if name[0] in ["p", "P"]:               # Predicate registers.
        cfg_dict["options"] = list(range(0, 8)) + [name[1:]]
    elif name[0] in ["z", "Z", "v", "V"]:   # Fpsimd/SVE/SME registers.
        cfg_dict["options"] = list(range(0, 16)) + [name[1:]]
    elif name[0] in ["r", "R"]:             # General-purpose registers.
        cfg_dict["options"] = list(range(0, 32)) + [name[1:]]
    elif name[0] in ["w", "W"]:             # ZA registers.
        cfg_dict["default"] = name

    return cfg_dict

def def_reg_cfgs(*name_list: List[str]) -> List[Dict]:
    """
    Define configuration structures of register names.

    Args:
        name_list (str): Register names.

    Returns:
        List[Dict]: List of configuration structure.
    """
    return [def_reg_cfg(name) for name in name_list]

def get_cfgs(cfgs_list: List[Dict]):
    namespace = {}

    for cfg_item in cfgs_list:

        key = cfg_item["name"]
        default = cfg_item["default"] if "default" in cfg_item else None

        if default is "random_choice":
            if "options" in cfg_item:
                default = choice(cfg_item["options"])
            elif "range" in cfg_item:
                min_val, max_val = cfg_item["range"]
                if isinstance(min_val, int) and isinstance(max_val, int):
                    default = randint(min_val, max_val)
                else:
                    default = uniform(min_val, max_val)
            else:
                raise ValueError(
                    f"Do not know how to find default value for configuration {key}.")

        if cfg_item["type"] == "fix_cfg":
            namespace[key] = default
            continue

        val = get_config(key=key, default=default)
        namespace[key] = val

        if "options" in cfg_item:
            option_list = cfg_item["options"]
            if namespace[key] not in option_list:
                raise ValueError(
                    f"Wrong value for configuration {key}, expect options {option_list}.")

        if "checker" in cfg_item:
            checker_expr = cfg_item["checker"]
            if not eval(checker_expr, namespace[key]):
                raise ValueError(
                    f"Wrong value for configuration {key}, expect condition \"{checker_expr}\".")

    return namespace

def get_predmask_cfg(key: str, elements: int, default: Any = [1]) -> Any:
    """
    Get value of predict.
    """
    if default is None:
        default = []
    pred_val = get_config(key, default)

    if pred_val is None or len(pred_val) == 0:
        pred_val = [randint(0, 1) for _ in range(0, elements)]
    elif len(pred_val) < elements:
        pred_val = pred_val * ceil(elements / len(pred_val))

    return pred_val

def get_predcnt_cfg(key: str, elements: int, default: Any = None) -> Any:
    """
    Get value of predict.
    """
    if default is None:
        default = elements
    cnt_val = get_config(key, default)
    cnt_val = max(-elements, min(cnt_val, elements))

    if cnt_val >= 0:
        pred_val = [True] * cnt_val + [False] * (elements - cnt_val)
    else:
        pred_val = [False] * (-cnt_val) + [True] * (elements - (-cnt_val))

    return pred_val

@overload
def get_addr_cfg(key: str,
                 width: int,
                 align: int,
                 elements: int,
                 val_range: Tuple[int, int] = None) -> Any: ...

@overload
def get_addr_cfg(key: str,
                 width: int,
                 align: int,
                 val_range: Tuple[int, int] = None) -> Any: ...

def get_addr_cfg(key: str,
                 width: int,
                 align: int,
                 repeat: int = 1,
                 val_range: Tuple[int, int] = None) -> Any:
    """
    Get value of address.
    """
    if val_range is None:
        default_list = [randint(0, 1 << width) // align * align for _ in range(0, repeat)]
    else:
        min_val, max_val = val_range
        if isinstance(min_val, int) and isinstance(max_val, int):
            default_list = [randint(min_val, max_val) // align * align for _ in range(0, repeat)]
        else:
            default_list = [uniform(min_val, max_val) for _ in range(0, repeat)]

    default = default_list if repeat > 1 else default_list[0]
    addr_val = get_config(key, default)
    return addr_val

@overload
def get_value_cfg(key: str, default: Any): ...

@overload
def get_value_cfg(key: str, range: Tuple[Any, Any], align: int = 1): ...

@overload
def get_value_cfg(key: str, elements: int, reps: int, range: Tuple[Any, Any], align: int = 1): ...

@overload
def get_value_cfg(key: str, elements: int, reps: int, width: int, align: int = 1): ...

@overload
def get_value_cfg(key: str, options: List[Any]): ...

@overload
def get_value_cfg(key: str, elements: int, reps: int, options: List[Any]): ...

def get_value_cfg(*args, **kwargs) -> Any:
    """
    Get random value of item.
    """
    key = args[0]
    elements = kwargs["elements"] if "elements" in kwargs else args[1] if len(args) > 1 else 1
    repeat = kwargs["reps"] if "reps" in kwargs else args[2] if len(args) > 2 else elements
    align = kwargs["align"] if "align" in kwargs else 1

    # Get default value.
    default = 0 if elements == 1 else []
    if "default" in kwargs:
        default = [kwargs["default"]]
    elif "range" in kwargs:
        min_val, max_val = kwargs["range"]
        if isinstance(min_val, int) and isinstance(max_val, int):
            default = [randint(min_val, max_val) // align * align for _ in range(0, repeat)]
        else:
            default = [uniform(min_val, max_val) for _ in range(0, repeat)]
    elif "options" in kwargs:
        default = [choice(kwargs["options"]) for _ in range(0, repeat)]

    if elements == 1:
        if isinstance(default, list):
            default = default[0]
        var_val = get_config(key, default)
        return var_val
    else:
        var_val = get_config(key, default)
        if len(var_val) == 0:
            var_val = [default] * elements
        elif len(var_val) < elements:
            var_val = var_val * ceil(elements / len(var_val))

        return var_val

def append_cfg(parent, *cfg_items: List[Dict], **fix_cfg_items) -> List[Dict]:
    """
    Append configuration item.

    Args:
        parent: Parent scene.
        cfg_item: List of configurable options.
        fix_cfg_item: List of fixed options.

    Returns:
        List of options.
    """
    cfgs_list: List[Dict] = parent.cfgs_list.copy()

    # Configurable options.
    for item in cfg_items:
        # Remove old item.
        for old_item in cfgs_list:
            if old_item["name"] == item["name"]:
                cfgs_list.remove(old_item)
                break
        # Add new item
        cfgs_list.append(item)

    # Fixed options.
    for key, value in fix_cfg_items.items():
        # Remove old item.
        for old_item in cfgs_list:
            if old_item["name"] == key:
                cfgs_list.remove(old_item)
                break
        # Add new item
        item = def_fix_cfg(key, value)
        cfgs_list.append(item)

    return cfgs_list
