
# Configuration

`isa_manim.isa_config` provides configuration options for ISAManim.

## Configuration options for Animation Objects

ISAManim provides the following configuration options:

- `scene_ratio` defines the ratio of scene width and bit. The default value is 1/8, which means a width of 1.0, which means 8 bits.
- `mem_addr_width` defines the default address width of memory units. The default value is 64 bits.
- `mem_data_width` defines the default data width of memory units. The default value is 128 bits.
- `mem_range` defines the default memory range of memory units specified by the lowest and highest memory address. The default value is [0,0x1000].
- `mem_align` defines the default memory alignment of memory units. The default value is 64 bytes.
- `elem_fill_opacity` defines the default fill opacity of elements. The default value is 0.5.
- `elem_value_format` defines one format string to print the value of elements. The default value is `{:d}`.

### APIs to set the value of options

#### get_scene_ratio

::: isa_manim.isa_config.get_scene_ratio

#### get_config

::: isa_manim.isa_config.get_config

### APIs to get the value of options

### set_config

::: isa_manim.isa_config.set_config

## Configuration options for Animation Flow

To provide options for the ISA behaviors described in animation scenes, ISAManim applies one environment variable (`MANIM_ISA_ARG`) to define a list of options.

`MANIM_ISA_ARG` accepts a list of pairs of option names and values. The name and the value of one option must be concatenated by `=`. The value of options can be:

- Hexadecimal number. The value starts with `0x`. The characters can be split by a single underscore (`_`).
- Binary number. The value starts with `0b`. The characters can be split by a single underscore (`_`).
- Decimal number. 
- Floating number.
- Boolean value. A string of `true` or `t` means true, while a string of `false` or `f` means false.
- List value. Several items can be rounded by square brackets or brackets as one list value. Items can be hexadecimal numbers, binary numbers, decimal numbers, floating numbers, and boolean values as above. Items in one list are split by commas (`,`) and spaces (` `). 

For example,

```bash
MANIM_ISA_ARG="a=0x400 b=0b1010 c=10 d=0.5 e=true f=[t,f,t,t,t,f]"
```

`SingleIsaScene` and `MultiIsaScene` have integrated the functionality to register options and parse `MANIM_ISA_ARG`. Options should be registered in the global member `cfgs_list` of animation classes as a list.

```python
class Animation(SingleIsaScene):

    cfgs_list = [def_cfg("vl", 256, options=[128, 256, 512]),
                 def_cfg("nreg", 2, options=[2, 4]),
                 def_cfg("index")]
```

The above example registers three options: `vl`, `nreg`, and `index`. `def_cfg` returns an entity of `isa_manim.isa_config.OptionDef` that holds attributes of one option.

Meanwhile, `construct_isa_flow` should provide the arguments for all the options.

```python
class Animation(SingleIsaScene):

    def construct_isa_flow(self, vl, nreg, index):
        ...
```

Moreover, options can also be inherited by the function `inherit_cfgs`. The function `inherit_cfgs` receives positional arguments and keyword arguments. Positional arguments add new options or override existing options. Keyword arguments add options or override existing options with one fixed value.

```python
class Animation2(Animation):

    cfgs_list = Animation.inherit_cfgs(def_cfg("size", 32, options=[8, 16, 32, 64]), vl=256, nreg=2)

    def construct_isa_flow(self, esize, vl, nreg, index):
        ...
```

In the above example, `Animation2` inherits options from `Animation`. `Animation2` has four options: `size`, `vl`, `nreg`, and `index`. The latter three options are inherited from `Animation`. Moreover, `vl` and `nreg` are assigned a fixed value, which is no longer configurable.

`isa_manim.isa_config.OptionDef` maintains the attributes of options. Four kinds of options have been defined.

- `FIX_CFG` means the option is not configurable. One fixed value is assigned to this option.
- `CONFIG_CFG` means the option is configurable. The specified default value is applied if the option is not provided in `MANIM_ISA_ARG`.
- `RANDOM_CFG` means the option is configurable. The random value is applied if the option is not provided in `MANIM_ISA_ARG`. The random value is selected among a list (`options`) or a value range (`opt_range`).
- `VALUE_CFG` does not need to appear in the argument list of `construct_isa_flow`. Users can get the value of options within `construct_isa_flow`.

Animation scenes call `get_cfgs` to parse the value of `MANIM_ISA_ARG` according to the options registered in `cfgs_list`. `get_cfgs` checks whether the option value is legal. There are three ways to define the legal condition of one option:

- The option of `options` specifies one list of the option values.
- The option of `opt_range` specifies one range of integer/floating-point values within which the option value should be.
- The option of `condition` specifies one callable function that should return true if the option value is legal.

### APIs to register options

#### OptionDef

::: isa_manim.isa_config.OptionDef

#### def_cfg

::: isa_manim.isa_config.def_cfg

#### def_random_cfg

::: isa_manim.isa_config.def_random_cfg

#### def_fix_cfg

::: isa_manim.isa_config.def_fix_cfg

#### def_value_cfg

::: isa_manim.isa_config.def_value_cfg

#### inherit_cfgs

::: isa_manim.isa_config.inherit_cfgs

### APIs to get the value of options

#### get_config

`get_config` returns the value of options. It applies to options for both animation objects and animation flow.

::: isa_manim.isa_config.get_config

#### get_cfgs

`get_cfgs` returns a dictionary of options and their values. 

::: isa_manim.isa_config.get_cfgs

> Users do not need to call this function.
