
"""
Utilize functions.
"""

from typing import List, Tuple

def calculate_mem_range(array: List[int], mbyte: int) -> Tuple[int, int]:
    """
    Calculate memory range of memory access.

    Args:
        array: Array of memory address.
        mbyte: Amount of bytes of memory access.

    Returns:
        Tuple of minimum address and maximum address.
    """
    if not isinstance(array, list):
        array = [array]

    flatten_array = []
    for item in array:
        if isinstance(item, (list, tuple)):
            flatten_array += calculate_mem_range(item, mbyte)
        else:
            flatten_array += [item, item + mbyte]
    return [min(flatten_array), max(flatten_array)]
