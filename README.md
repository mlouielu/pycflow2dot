pycflow2dot
===========

Description
-----------
Draw the call graph of C source code using [cflow](http://en.wikipedia.org/wiki/GNU_cflow) and [dot](http://www.graphviz.org/).
Output to LaTeX, .dot, .PDF, .SVG, .PNG
and from dot to all formats supported from it.
The LaTeX output is obtained by including the SVG via [Inkscape](http://inkscape.org/)'s LaTeX [export](http://mirror.math.ku.edu/tex-archive/info/svg-inkscape/InkscapePDFLaTeX.pdf) functionality.

Multi-file sources are converted to multiple SVG files, one for each source.
These contain links using the LaTeX package [hyperref](http://ctan.org/pkg/hyperref), so that after compilation
one can click on the name of a function call and be taken to its definition,
even if that definition is in another page of the PDF, because the function is defined in
another source file than the one corresponding to the current PDF page.

Note that if a file containing the definition is missing, then the hyperref link
is omitted, so that no dead links result after compiling with LaTeX.
This might be the case of for example the file with the definitions is available,
but is not passed to pycflow2dot, e.g., for the purpose of focusing on a
subset of the sources.

For now the LaTeX result has to be manually compiled, though this
extra step will be automated in the future. Multi-SVG export will still be
available, so that the results can be included in a larger document, e.g., a report.

PyCflow2dot is a Python port of the Perl script cflow2dot.
Tested with Python 3.2 (NetworkX not yet available in 3.3.).

License
-------
PyCflow2dot is licensed under the GNU GPL v3.
