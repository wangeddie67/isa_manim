"""
ISA configuration structure.
"""

isa_config = {
    "scene_ratio": (1/8),   # scene width / bit. Default 1.0 means 8 bit.
}
"""
Configuration structure to pass arguments of ISA. For example, element size and vector length.
"""

def get_scene_ratio() -> float:
    """
    Return scene ratio. 
    scene width / bit. Default: 1.0 means 8 bits.
    """
    global isa_config   # pylint: disable=global-variable-not-assigned,invalid-name
    return isa_config["scene_ratio"]
