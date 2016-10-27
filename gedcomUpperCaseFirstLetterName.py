#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script geopy to find the latitude and longitude
# of locations.
#
# Since we can not perform too much requests, this script
# stores the result of the requests in a text file.

def upperCaseFirstLetterName(gedcomFilename, outputFilename = None):
    import os
    import re
    def repl_func(m):
        """process regular expression match groups for word upper-casing problem"""
        name = m.group(2)
        upperCaseName = ' '.join([n[0].upper()+n[1:].lower() for n in name.split()])
        return m.group(1)+'/'+upperCaseName+'/'+m.group(3)
    gg = re.compile('(.*)\/(.*)\/(.*)',flags=re.UNICODE)
    lines = [c.strip() for c in open(gedcomFilename, 'r', encoding='utf-8').readlines()]
    newLines = [gg.sub(repl_func, line) for line in lines]
    if outputFilename is None:
        outputFilename = os.path.splitext(gedcomFilename)[0]+'_WithUpperCase.ged'
    open(outputFilename, 'w').writelines('\n'.join(newLines))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description = 'This script changes the case of family name in a gedcom file')
    parser.add_argument('-g','--gedcom', type = str, default = 'my_gedcom_file.ged',
                       help = 'Gedcom filename')
    parser.add_argument('-o','--outputGedcom', type = str, default = None,
                       help='Optional output name. If not provided, a filename will be generated from the gedcom filename')
    args = parser.parse_args()
    upperCaseFirstLetterName(gedcomFilename = args.gedcom, outputFilename = args.outputGedcom)