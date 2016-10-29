#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This script reads a gedcom file and changes the case
# of family names: it uppers case the first letter of the family name.
# The result is exported in a new file.
#
# This script does not require any additional library to work.

def upperCaseFirstLetterName(gedcomFilename, outputFilename = None):
    """
    gedcomFilename : str of the gedcom file to import
    outputFilename : str of the output gedcom to generate. If None, 
                     the function appends '_WithUpperCase.ged'
                     to the gedcomFilename
    One uses regular expression to match all expressions between two slash    
    """
    import os
    import re
    def repl_func(m):
        """process regular expression match groups for word upper-casing problem"""
        name = m.group(2)
        upperCaseName = ' '.join([n[0].upper()+n[1:].lower() for n in name.split()])
        return m.group(1) + '/' + upperCaseName + '/' + m.group(3)
    gg = re.compile('(.*)\/(.*)\/(.*)', flags=re.UNICODE)
    lines = [c.strip() for c in open(gedcomFilename, 'r', encoding='utf-8').readlines()]
    newLines = [gg.sub(repl_func, line) for line in lines]
    if outputFilename is None:
        outputFilename = os.path.splitext(gedcomFilename)[0] + '_WithUpperCase.ged'
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
