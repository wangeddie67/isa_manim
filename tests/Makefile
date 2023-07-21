# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SOURCEDIR     = source
BUILDDIR      = build

all: demo

test_one_dim_reg:
	manim -ql --format=png isa_objects/test_one_dim_reg.py

test_two_dim_reg:
	manim -ql --format=png isa_objects/test_two_dim_reg.py

test_one_dim_reg_elem:
	manim -ql --format=png isa_objects/test_one_dim_reg_elem.py

test_function_call:
	manim -ql --format=png isa_objects/test_function_call.py

demo: test_one_dim_reg test_two_dim_reg test_one_dim_reg_elem test_function_call

clean:
	@rm -rf $(BUILDDIR) $(SOURCEDIR)/_autosummary