#!/opt/local/bin/python3
# -*- coding: utf-8 -*-

"""
Copyright 2010 developer of https://code.google.com/p/cflow2dot/ (name yet unknown)
Copyright 2013 Dabaichi Valbendan
Copyright 2013 Ioannis Filippidis

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# note:
#   python3 macports path

#TODO import transys and export TS
#TODO deal with multiple src fnames in one svg

#TODO link for latex, just put the hyperref code, no need for cross-file hurdle,
#     they can be produced separately and merged when latex gets compiled
#TODO produce latex automatically, by creating sources and calling xelatex

#TODO list to exclude symbols
#TODO detect symbols defined in: local, global includes

import os
import sys
import argparse
import subprocess
import locale
import re
import networkx as nx # make this an optional dependency
# pydot will also be an optional depepndency

def dprint(s):
    """Debug mode printing."""
    # debug print
    #TODO make this a package
    print(s)

def bytes2str(b):
    encoding = locale.getdefaultlocale()[1]
    return b.decode(encoding)

def get_max_space(lines):
    space = 0
    for i in range(0, len(lines)):
        if lines[i].startswith(space * 4 * ' '):
            i = 0
            space += 1
    return space

def get_name(line):
    name = ''
    for i in range(0, len(line)):
        if line[i] == ' ':
            pass
        elif line[i] == '(':
            break
        else:
            name += line[i]
    return name

def call_cflow(c_fname, cflow, numbered_nesting=True):
    if numbered_nesting:
        cflow_cmd = [cflow, '-l', c_fname]
    else:
        cflow_cmd = [cflow, c_fname]
    
    dprint('cflow command:\n\t' +str(cflow_cmd) )
    
    cflow_data = subprocess.check_output(cflow_cmd)
    cflow_data = bytes2str(cflow_data)
    dprint('cflow returned:\n\n' +cflow_data)
    
    return cflow_data

def cflow2dot_old(data, offset=False, filename = ''):
    color = ['#eecc80', '#ccee80', '#80ccee', '#eecc80', '#80eecc']
    shape = ['box', 'ellipse', 'octagon', 'hexagon', 'diamond']
    
    dot = 'digraph G {\n'
    dot += 'node [peripheries=2 style="filled,rounded" '+ \
           'fontname="Vera Sans Mono" color="#eecc80"];\n'
    dot += 'rankdir=LR;\n'
    dot += 'label="' +filename +'"\n'
    dot += 'main [shape=box];\n'
    
    lines = data.replace('\r', '').split('\n')
    
    max_space = get_max_space(lines)
    nodes = set()
    edges = set()
    for i in range(0, max_space):
        for j in range(0, len(lines)):
            if lines[j].startswith((i + 1) *4 *' ') \
            and not lines[j].startswith((i +2) *4 *' '):
                cur_node = get_name(lines[j] )
                
                # node already seen ?
                if cur_node not in nodes:
                    nodes.add(cur_node)
                    print('New Node: ' +cur_node)
                
                # predecessor \exists ?
                try:
                    pred_node
                except NameError:
                    raise Exception('No predecessor node defined yet! Buggy...')
                
                # edge already seen ?
                cur_edge = (pred_node, cur_node)
                if cur_edge not in edges:
                    edges.add(cur_edge)
                else:
                    continue
                
                dot += (('node [color="%s" shape=%s];edge [color="%s"];\n') % (
                        color[i % 5], shape[i % 5], color[i % 5] ) )
                dot += (pred_node + '->' + cur_node +'\n')
            elif lines[j].startswith(i *4 *' '):
                pred_node = get_name(lines[j] )
            else:
                raise Exception('bug ?')
    dot += '}\n'
    
    #dprint('dot dump str:\n\n' +dot)
    return dot

def dot_format_node(cur_node, cur_label, cur_color, cur_shape):
    dot_str = cur_node +'[label="' +cur_label +'" ' \
            +'color="' +cur_color +'" shape=' +cur_shape +'];\n'
    return dot_str

def cflow2dot_nx(cflow_str, c_fname, for_latex=False, multi_page=False):
    # load C source for extra checks
    #if multi_page:
    #    f = open(c_fname, 'r')
    #    src = f.read()
    #    f.close()
    
    if for_latex:
        c_fname = re.sub(r'_', r'\\\\_', c_fname)
    
    colors = ['#eecc80', '#ccee80', '#80ccee', '#eecc80', '#80eecc']
    shapes = ['box', 'ellipse', 'octagon', 'hexagon', 'diamond']
    
    dot_str = 'digraph G {\n'
    dot_str += 'node [peripheries=2 style="filled,rounded" '+ \
           'fontname="Vera Sans Mono" color="#eecc80"];\n'
    dot_str += 'rankdir=LR;\n'
    dot_str += 'label="' +c_fname +'"\n'
    dot_str += 'main [shape=box];\n'
    
    lines = cflow_str.replace('\r', '').split('\n')
    
    ts = nx.DiGraph()
    stack = dict()
    for line in lines:
        dprint(line)
        
        # empty line ?
        if line == '':
            continue
        
        # defined in this file ?
        # apparently, this check is not needed: check this better
        
        # get source line #
        src_line_no = re.findall(':.*>', line)
        if src_line_no != []:
            def_in_cfname = True
            src_line_no = int(src_line_no[0][1:-1] )
        else:
            def_in_cfname = False
            src_line_no = -1
        
        # trim
        s = re.sub(r'\(.*$', '', line)
        s = re.sub(r'^\{\s*', '', s)
        s = re.sub(r'\}\s*', r'\t', s)
        
        # where are we ?
        (nest_level, func_name) = re.split(r'\t', s)
        nest_level = int(nest_level)
        cur_node = func_name
        
        dprint('Found function:\n\t' +func_name
              +',\n at depth:\n\t' +str(nest_level)
              +',\n at src line:\n\t' +str(src_line_no) )
        
        stack[nest_level] = cur_node
        
        # not already seen ?
        if cur_node not in ts:
            ts.add_node(cur_node, scr_line=src_line_no)
            dprint('New Node: ' +cur_node)
        
        # root node ?
        if nest_level == 0:
            # dump node, no pred->curnode edge
            cur_color = colors[0]
            cur_shape = 'box'
        
            # node
            dot_str += dot_format_node(cur_node, cur_label, cur_color, cur_shape)
        else:
            # > 0 depth
            pred_node = stack[nest_level -1]
            
            # new edge ?
            if ts.has_edge(pred_node, cur_node):
                # avoid duplicate edges
                # note DiGraph is so def
                continue
            else:
                ts.add_edge(pred_node, cur_node)
                dprint('Found edge:\n\t' +pred_node +'--->' +cur_node)
            
            cur_color = colors[(nest_level -1) % 5]
            cur_shape = shapes[nest_level % 5]
            
            # node
            dot_str += dot_format_node(cur_node, cur_label, cur_color, cur_shape)
            
            # edge
            dot_str += 'edge [color="' +cur_color +'"];\n'
            dot_str += pred_node +'->' +cur_node +'\n'
        
    dot_str += '}\n'
    
    dprint('dot dump str:\n\n' +dot_str)
    return (dot_str, ts)

def label_graphs():
    
    for graph in call_graphs:
        other_graphs = call_graphs.remove(graph)

def label_single_graph():
    """Annotate edges of single src file call graph."""
    
    
    
def label_node():
    sl = '\\\\'
    
    # fix underscores ?
    if for_latex:
        cur_label = re.sub(r'_', r'\\\\_', cur_node)
    else:
        cur_label = cur_node
    dprint('Label:\n\t: ' +cur_label)
    
    # src line of def here ?
    if def_in_cfname:
        if for_latex:
            cur_label = cur_label +2*sl +str(src_line_no)
        else:
            cur_label = cur_label +'\n' +str(src_line_no)
    
    # multi-page pdf ?
    if for_multi_src:
        if def_in_cfname:
            # label
            cur_label = sl +'descitem{' +cur_node +'}' +cur_label
        else:
            # link
            cur_label = sl +'descref[' +cur_label +']{' +cur_node +'}'
        
        dprint('Node text:\n\t: ' +cur_label)

def get_output_file(in_fname):
    argv = sys.argv
    if argv[len(argv) - 2] == '-o' or argv[len(argv) - 2] == '--output':
        output_file = os.path.join(os.getcwd(), argv[len(argv) - 1])
    else:
        output_file = os.path.join(os.getcwd(), in_fname)
    return output_file

def check_cflow_dot_availability():
    required = ['cflow', 'dot']
    
    dep_paths = []
    for dependency in required:
        path = subprocess.check_output(['which', dependency] )
        path = bytes2str(path)
        
        if path.find(dependency) < 0:
            raise Exception(dependency +' not found in $PATH.')
        else:
            path = path.replace('\n', '')
            print('found ' +dependency +' at: ' +path)
            dep_paths += [path]
    
    return dep_paths

def write_dot_file(dotdata, c_fname):
    dot_fname = get_output_file(c_fname)
    try:
        dot_path = os.path.join(dot_fname, dot_fname +'.dot')
        with open(dot_path, 'w') as fp:
            fp.write(dotdata)
            print('Dumped dot file.')
    except:
        raise Exception('Failed to save dot.')
    
    return dot_path

def dot2svg(c_fname, dot_path, img_format):
    img_fname = c_fname +'.' +img_format
    
    dot_cmd = ['dot', '-T'+img_format, '-o', img_fname, dot_path]
    dprint(dot_cmd)
    
    print('This may take some time... ...')
    subprocess.check_call(dot_cmd)
    print('Dot produced ' +img_format +' successfully.')

def dump_latex_preamble():
    """Return string for LaTeX preamble.
    
    Used if you want to compile the SVGs stand-alone.
    
    If SVGs are included as part of LaTeX document, then copy required
    packages from this example to your own preamble.
    """
    
    latex = r"""
    \documentclass[12pt, final]{article}
    
    usepackage{mybasepreamble}
    % fix this !!! to become a minimal example

    \usepackage[paperwidth=25.5in, paperheight=28.5in]{geometry}
    
    \newcounter{desccount}
    \newcommand{\descitem}[1]{%
        	\refstepcounter{desccount}\label{#1}
    }
    \newcommand{\descref}[2][\undefined]{%
    	\ifx#1\undefined%
        \hyperref[#2]{#2}%
    	\else%
    	    \hyperref[#2]{#1}%
    	\fi%
    }%
    """
    return latex

def usage():
    doc = 'cflow2dot.py file1 file2 ..... --output[-o] outputfilename\n'
    doc += 'output file format is svg\n'
    doc += '--version (-v) show version\n'
    doc += '--help (-h) show this document.'
    print(doc)

def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('input_filenames', nargs='+',
                        help='Filename(s) of C source code files to be parsed.')
    parser.add_argument('-o', '--output-filename', default='cflow',
                        help='name of dot, svg, pdf etc file produced')
    parser.add_argument('-f', '--output-format', default='svg',
                        choices=['dot', 'svg', 'pdf', 'png'],
                        help='output file format')
    parser.add_argument('-l', '--latex-svg', default=False, action='store_true',
                        help = 'produce SVG for import to LaTeX via Inkscape')
    parser.add_argument('-m', '--multi-page', default=False, action='store_true',
                        help = 'produce hyperref links between function calls '
                              +'and their definitions. Used for multi-page '
                              +'PDF output, where each page is a different '
                              +'source file.')
    args = parser.parse_args()
    
    return args

def main():
    """Rnn cflow, parse output, produce dot and compile it into pdf | svg."""
    
    (cflow, dot) = check_cflow_dot_availability()
    
    args = parse_args()
    
    c_fnames = args.input_filenames
    img_format = args.output_format
    for_latex = args.latex_svg
    multi_page = args.multi_page
    img_fname = args.output_filename
    
    dprint('C src files:\n\t' +str(c_fnames) +", (extension '.c' omitted)\n"
           +'img fname:\n\t' +str(img_fname) +'.' +img_format +'\n'
           +'LaTeX export from Inkscape:\n\t' +str(for_latex) +'\n'
           +'Multi-page PDF:\n\t' +str(multi_page) )
    
    cflow_strs = []
    for c_fname in c_fnames:
        cflow_strs += call_cflow(c_fname, cflow, numbered_nesting=True)
    
    return
    (dotdata, ts) = cflow2dot_nx(cflow_str, c_fnames,
                                 for_latex=for_latex, multi_page=multi_page)
    
    dot_path = write_dot_file(dotdata, img_fname)
    dot2svg(img_fname, dot_path, img_format)

if __name__ == "__main__":
    main()
