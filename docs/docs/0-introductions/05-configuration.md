
# Configuration

`isa_manim.isa_config` provides configuration options for IsaManim.

## Configuration options for Animation Objects

IsaManim provides the following configuration options:

- `scene_ratio` defines the ratio of scene width and bit. The default value is 1/8 which means the width of 1.0 means 8 bits.
- `mem_addr_width` defines the default address width of memory units. The default value is 64 bits.
- `mem_data_width` defines the default data width of memory units. The default value is 128 bits.
- `mem_range` defines the default memory range of memory units. The default value is one range from 0 to 0x1000.
- `mem_align` defines the default memory alignment of memory units. The default value is 64 bytes.
- `elem_fill_opacity` defines the default fill opacity of elements. The default value is 0.5/
- `elem_value_format` defines one format string to print the value of elements. The default value is `{:d}`.

## Configuration options for Animation Flow

To provide options to the animation flow described in animation scenes, IsaManim applies one environment variable `MANIM_ISA_ARG` to define a list of options.

`MANIM_ISA_ARG` accepts a list of pairs of option names and values. The name and the value of one option must be concatenated by `=`. The value of options can be:

- Hexadecimal number. The value starts with `0x`. The characters can be split by `'_'`.
- Binary number. The value starts with `0b`. The characters can be split by `'_'`.
- Decimal number. 
- Floating number.
- Boolean value. `true` and `t` means true while `false` and `f` means false.
- List value. Several items can be rounded by square brackets or brackets as one list value. Items can be hexadecimal numbers, binary numbers, decimal numbers, floating numbers and boolean values as above. Items in one list are split by `','` and `' '`. 

For example,

```bash
MANIM_ISA_ARG="a=0x400 b=0b1010 c=10 d=0.5 e=true f=[t,f,t,t,t,f]"
```

## Functions to access options

::: isa_manim.isa_config
    :functions:
