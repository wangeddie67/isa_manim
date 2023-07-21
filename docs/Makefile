# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SOURCEDIR     = source
BUILDDIR      = build

doc:
	@sphinx-build -b html $(SOURCEDIR) $(BUILDDIR)

.PHONY: html Makefile clean

clean:
	@rm -rf $(BUILDDIR) $(SOURCEDIR)/_autosummary