#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Works with Python2 and Python3

import gedcom
import networkx as nx
import os

def gedcom2gephi(gedcomFilename='gedcom.ged', gephiFilename=None):
    getName = lambda n: n.name[0]+' '+n.name[1]
    getId = lambda n: n.id[1:-1]
    getFamilyName = lambda n: n.name[1]

    g = gedcom.parse(gedcomFilename)
    dg = nx.DiGraph()
    for p in g.individuals:
        if p.id not in dg:
            dg.add_node(getId(p), {'label':getName(p), 'name':getName(p), 'familyName':getFamilyName(p)})
    for p in g.individuals:
        if p.father:
            dg.add_edge(getId(p.father), getId(p))
        if p.mother:
            dg.add_edge(getId(p.mother), getId(p))
    if gephiFilename is None:
        gephiFilename = os.path.splitext(gedcomFilename)[0] + '.gexf'
    nx.write_gexf(dg, gephiFilename)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description = 'This script converts a gedcom file to a gexf file')
    pa = parser.add_argument
    pa('-g','--gedcom', type = str, default = 'my_gedcom_file.ged',
       help = 'Gedcom filename')
    pa('-o','--outputGexf', type = str, default = None,
       help='Optional output name. If not provided, a filename will be generated from the gedcom filename')
    args = parser.parse_args()
    gedcom2gephi(gedcomFilename=args.gedcom, gephiFilename=args.outputGexf)
