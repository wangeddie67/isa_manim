
# Register file

isa_arm_utils provide data structure of architectural registers defined by specified ISA. These 
registers maintain operands of instructions. 

Because one register can present variables with different sizes or precision, each register is 
presented as a bit string (:py:class:`isa_sim_utils.data_types.integer.UInt`). Each register can be 
read/written by functions, which specified the position of bits to operate.

By default, each register is at X state before any write operation. Register file structure provide 
several strategies to initialize register file, which varies among different ISA. See specified data
structure for initialization strategy.

## Predefined Register Files

### AArch64 ISA

:py:class:`isa_sim_utils.reg_file.arm_regfile.ArmRegFile` defines the following architecture 
registers for AArch64 ISA:

- 31 64-bit general purpose registers, which are named R0-R30.
  - R31 is used as ZERO registers, which cannot be written.
  - General-purpose registers can be read as 8/16/32/64 bit signed/unsigned integers.
- 32 vector registers with configurable size (VL).
  - By SIMD&FP instructions, the lower 64/128 bit of these registers can be read as HP/SP/DP 
    floating-point numbers. In SIMD&FP instructions, these registers are named V0-V31.
  - By SVE instructions, these registers can be read as SIMD vectors. In SVE instructions, these
    registers are named Z0-Z31.
  - SIMD&FP registers and SVE registers share the same physical registers.
- 16 predicate registers with configurable size (VL / 8).
  - Predicate registers can be read as SIMD vectors. The size of each element in predicate registers 
    is equal to 1/8 of the size of each element in vector registers.
- ZA registers (coming soon).
- ZT0 registers (coming soon).

The constructor function provides option `vl` to specify the length of vector registers, which
should be as same as the proposed implementation.

:py:class:`isa_sim_utils.reg_file.arm_regfile.ArmRegFile` provides several methods to initialize 
registers.

- Predicate registers:
  - The strategy is defined by option `predicate_strategy` in the constructor function.
  - `ALL_TRUE`: All bits are one, which means all elements are active.
  - `ALL_FALSE`: All bits are zero, which means all elements are inactive.
  - `RANDOM`: Value of registers is determined by random numbers so that some elements are
    active while other elements are inactive.

By default, all registers keep at X state except predicate registers are initialized as ALL-TRUE.

## How to Add Register File

To do.

