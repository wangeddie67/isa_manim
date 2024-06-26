# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SOURCEDIR     = source
BUILDDIR      = build

all: demo

# Test object.
test_one_dim_reg:
	manim -ql --format=png isa_objects/test_one_dim_reg.py

test_two_dim_reg:
	manim -ql --format=png isa_objects/test_two_dim_reg.py

test_elem_unit:
	manim -ql --format=png isa_objects/test_elem_unit.py

test_elem_unit_zero:
	manim -ql --format=png isa_objects/test_elem_unit_zero.py

test_func_unit:
	manim -ql --format=png isa_objects/test_func_unit.py

test_mem_unit:
	manim -ql --format=png isa_objects/test_mem_unit.py

test_mem_unit_status:
	manim -ql --format=png isa_objects/test_mem_unit_status.py

test_objects: test_one_dim_reg test_two_dim_reg test_elem_unit test_elem_unit_zero test_func_unit \
	test_mem_unit

# Test animation.
test_reg_animation:
	manim -ql --format=gif isa_animate/test_reg_animation.py

test_elem_animation:
	manim -ql --format=gif isa_animate/test_elem_animation.py

test_func_animation:
	manim -ql --format=gif isa_animate/test_func_animation.py

test_memmap_animation:
	manim -ql --format=gif isa_animate/test_memmap_animation.py

test_memory_animation:
	manim -ql --format=gif isa_animate/test_memory_animation.py

test_memory_animation_without_addr:
	manim -ql --format=gif isa_animate/test_memory_animation_without_addr.py

test_memory_animation_parallel:
	manim -ql --format=gif isa_animate/test_memory_animation_parallel.py

test_animations: test_reg_animation test_elem_animation test_func_animation test_memory_animation

# Test scene.
test_isa_placement_map:
	manim -ql --format=png isa_scene/test_isa_placement_map.py
	manim -ql --format=png isa_scene/test_isa_placement_map_2.py

test_single_isa_scene:
	manim -ql --format=gif isa_scene/test_single_isa_scene.py

test_single_isa_scene_mem:
	manim -ql --format=gif isa_scene/test_single_isa_scene_mem.py

test_multi_isa_scene:
	manim -ql --format=gif isa_scene/test_multi_isa_scene.py

test_scene: test_isa_placement_map test_single_isa_scene test_multi_isa_scene \
	test_single_isa_scene_mem

demo: test_objects test_animations test_scene

clean:
	@rm -rf $(BUILDDIR) $(SOURCEDIR)/_autosummary