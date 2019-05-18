#!/usr/bin/env python3

# Kevin Matthew Henderson - May 18, 2019

from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import networkx as nx
import os
import subprocess
import click

@click.command()
@click.argument('directory', nargs=1)
@click.argument("output", nargs=1)
@click.option("--width", "-w",  default=1920, help="Graph width")
@click.option("--height", "-h",  default=1080, help="Graph height")
@click.option("--image",  default=None, help="Image file for graph to overlay ontop of")
@click.option("--background-colour", "-b",   default="#33333300", help="Background colour in form '#RRGGBBAA'")
@click.option("--label-size", "-f",  default=12, help="Font size for labels")
@click.option("--label-colour",  default="#AAAAAAFF", help="Font colour in form '#RRGGBBAA'")
@click.option("--label-depth",  default=2, help="Max depth to draw labels")
@click.option("--file-label-size", "-f",  default=8, help="Font size for file labels")
@click.option("--file-label-colour",  default="#AAAAAAFF", help="Font colour in form '#RRGGBBAA'")
@click.option("--edge-width", default=0.5, help="Edge line width")
@click.option("--edge-colour", default="#555555FF", help="Edge colour in form '#RRGGBBAA'")
@click.option("--node-size", default=0, help="Node dot size, set to zero to disable")
@click.option("--file-node-size", default=0, help="Node dot size, set to zero to disable")
@click.option("--node-colour", default="#555555FF", help="Node colour in form '#RRGGBBAA'")
@click.option("--file-node-colour", default="#555555FF", help="Node colour in form '#RRGGBBAA'")
@click.option("--show-files", default=False, is_flag=True, help="Shows files")
@click.option("--show-file-labels", default=False, is_flag=True, help="Shows file labels")
@click.option("--layout", "-l",  default="dot", help="Layout style: ‘dot’, ‘twopi’, ‘fdp’, ‘sfdp’, ‘circo’")
@click.option("--set-wallpaper", default=False, is_flag=True, help="Sets output image as wallpaper using feh")
@click.option("--verbose", "-v",  default=False, is_flag=True, help="Display more output than necessary")
def main(
directory, output, 
width, height, 
label_size, label_colour, label_depth, 
background_colour, image,  
edge_colour, edge_width,  
node_colour, node_size, 
show_files, file_node_colour, file_node_size, file_label_colour, file_label_size, show_file_labels, 
layout,  set_wallpaper, 
verbose):
    """ 
    PFSG - Python Filesystem Grapher
    
    Uses matplotlib and networkx to create graph of given directory structure and exports to png image for use as desktop wallpaper
    
    """
    G = nx.Graph() # create graph
    base_depth = len(directory.split("/"))  -1
    G.add_node(directory,  file='False',  depth=0,  label=directory)
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for f in filenames:
            G.add_node(os.path.join(dirpath, f),  file='True',  depth=(len(dirpath.split("/"))-base_depth),  label=f)
            G.add_edge(dirpath ,  os.path.join(dirpath, f))
        for d in dirnames:
            G.add_node(os.path.join(dirpath, d),  file='False', depth=(len(dirpath.split("/"))-base_depth),  label=d)
            G.add_edge(dirpath ,  os.path.join(dirpath, d))
          
    file_nodes = []
    dir_nodes = []
    file_labels = {}
    dir_labels = {}
    files=nx.get_node_attributes(G,'file')
    labels=nx.get_node_attributes(G,'label')
    depth=nx.get_node_attributes(G,'depth')
    for node, file in files.items():
        if file=='True':
            file_nodes.append(node)
            if depth[node] < label_depth: file_labels[node] = labels[node]
        else:
            dir_nodes.append(node)
            if depth[node] < label_depth: dir_labels[node] = labels[node]
    
    pos = graphviz_layout(G, prog=layout, root=1) # use layout
    fig = plt.figure(figsize=(width/100.0, height/100.0)) # set figure size
    
    nx.draw_networkx_nodes(G, pos, nodelist=dir_nodes, node_size=node_size, node_color=node_colour)
    nx.draw_networkx_nodes(G, pos, nodelist=file_nodes, node_size=file_node_size, node_color=file_node_colour)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colour, width=edge_width)#,  style='dotted',  connectionstyle='arc3,rad=0.2')
    if show_file_labels: nx.draw_networkx_labels(G, pos, labels=file_labels ,  font_color=file_label_colour, font_size=file_label_size,  alpha=1)
    nx.draw_networkx_labels(G, pos, labels=dir_labels ,  font_color=label_colour, font_size=label_size,  alpha=1)
    plt.axis('off')
    #plt.axis('equal')
    
    if image: fig.set_facecolor('#00000000') # for transparency
    else: fig.set_facecolor(background_colour)
    
    plt.savefig(output, facecolor=fig.get_facecolor() )
    plt.close()
    
    # depends on imagemagick
    if image: out = subprocess.call(['composite',  '-blend',  '70',  output, image,  output])
    # depends on feh
    if set_wallpaper: out = subprocess.call(['feh',  '--bg-scale',  output])

if __name__ == '__main__':
    main()
