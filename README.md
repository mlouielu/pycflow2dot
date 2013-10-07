# pycflow2dot

## Summary
Draw call graphs for C source codes using `dot` and `cflow`.
Typeset PDF with a page per source file and clickable cross-file function references.

`pycflow2dot -i hello_simple.c -f png` produces:

![](http://www.cds.caltech.edu/~ifilippi/temp/releases/python/pycflow2dot/hello_simple.png)

from [`hello_simple.c`](https://github.com/johnyf/pycflow2dot/blob/master/examples/simple/hello_simple.c).

## Description
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

## Dependencies
- Python 2.7.\* or 3.\*
- [GNU cflow](http://en.wikipedia.org/wiki/GNU_cflow) (e.g. `port install cflow` with [MacPorts](http://www.macports.org/))
- [dot](http://www.graphviz.org/)
- [networkx](http://networkx.github.io/) (e.g. `port install py-networkx` with MacPorts)
- [pydot](https://pypi.python.org/pypi/pydot) (optional)
- [cpp](http://en.wikipedia.org/wiki/C_preprocessor) (optional)

## License
PyCflow2dot is licensed under the GNU GPL v3.
