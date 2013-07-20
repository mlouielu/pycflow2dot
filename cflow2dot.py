#!/opt/local/bin/python3
# -*- coding: utf-8 -*-

# note:
#   python3 macports path

#TODO import transys and export TS
#TODO use argparse instead
#TODO deal with multiple src fnames in one svg

#TODO link for latex, just put the hyperref code, no need for cross-file hurdle,
#     they can be produced separately and merged when latex gets compiled
#TODO produce latex automatically, by creating sources and calling xelatex

#TODO list to exclude symbols
#TODO detect symbols defined in: local, global includes

import os
import sys
import subprocess
import locale
import re
import networkx as nx # make this an optional dependency
# pydot will also be an optional depepndency

def dprint(s):
    """Debug mode printing."""
    # debug print
    #TODO make this a package
    #print(s)

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

def call_cflow(c_fname, cflow, numbered_nesting):
    if numbered_nesting:
        cflow_cmd = [cflow, '-l', c_fname]
    else:
        cflow_cmd = [cflow, c_fname]
    
    dprint('cflow command:\n\t' +str(cflow_cmd) )
    
    cflow_data = subprocess.check_output(cflow_cmd)
    cflow_data = bytes2str(cflow_data)
    #dprint('cflow returned:\n\n' +cflow_data)
    
    return cflow_data

def cflow2dot_old(data, offset = 0, filename = ''):
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

def cflow2dot_nx(cflow_str, fname, for_latex):
    if for_latex:
        fname = re.sub(r'_', r'\\\\_', fname)
    
    colors = ['#eecc80', '#ccee80', '#80ccee', '#eecc80', '#80eecc']
    shapes = ['box', 'ellipse', 'octagon', 'hexagon', 'diamond']
    
    dot_str = 'digraph G {\n'
    dot_str += 'node [peripheries=2 style="filled,rounded" '+ \
           'fontname="Vera Sans Mono" color="#eecc80"];\n'
    dot_str += 'rankdir=LR;\n'
    dot_str += 'label="' +fname +'"\n'
    dot_str += 'main [shape=box];\n'
    
    lines = cflow_str.replace('\r', '').split('\n')
    
    ts = nx.DiGraph()
    stack = dict()
    for line in lines:
        dprint(line)
        
        # empty line ?
        if line == '':
            continue
        
        # trim
        s = re.sub(r'\(.*$', '', line)
        s = re.sub(r'^\{\s*', '', s)
        s = re.sub(r'\}\s*', r'\t', s)
        
        # where are we ?
        (nest_level, func_name) = re.split(r'\t', s)
        nest_level = int(nest_level)
        cur_node = func_name
        
        dprint('Found function:\n\t' +func_name
              +',\n at depth:\n\t' +str(nest_level) )
        
        stack[nest_level] = cur_node
        
        # fix underscores ?
        if for_latex:
            cur_label = re.sub(r'_', r'\\\\_', cur_node)
        else:
            cur_label = cur_node
        
        # already seen ?
        if cur_node not in ts:
            ts.add_node(cur_node)
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

def usage():
    doc = 'cflow2dot.py file1 file2 ..... --output[-o] outputfilename\n'
    doc += 'output file format is svg\n'
    doc += '--version (-v) show version\n'
    doc += '--help (-h) show this document.'
    print(doc)

def get_input_file():
    input_filename = ''
    argv = sys.argv
    for i in range(1, len(argv)):
        if argv[i] == '-o' or argv[i] == '--output':
            break
        else:
            input_filename += (argv[i] + ' ')
    return input_filename

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

def main():
    """Rnn cflow, parse output, produce dot and compile it into pdf | svg."""
    
    (cflow, dot) = check_cflow_dot_availability()
    img_format = 'svg'
    numbered_nesting = True
    for_latex = False
    
    # assume svg will be imported to LaTeX via Inkscape
    if img_format == 'svg':
        for_latex = True
    
    # C fname ?
    if len(sys.argv) == 2:
        c_fname = sys.argv[1]
    else:
        c_fname = get_input_file()
    
    cflow_data = call_cflow(c_fname, cflow, numbered_nesting)
    (dotdata, ts) = cflow2dot_nx(cflow_data, c_fname, for_latex)
    
    dot_path = write_dot_file(dotdata, c_fname)
    dot2svg(c_fname, dot_path, img_format)

if __name__ == "__main__":
    main()
