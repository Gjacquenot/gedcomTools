# gedcomTools

`gedcomTools` contains a set of scripts to manipulate `gedcom`
files.

## gedcom2gexf

`gedcom2gexf` allows to import genealogical data stored
in [Gephi](https://gephi.org),
an open-source network analysis and visualization software.

The `gedcom2gexf` script converts
a [`gedcom`](https://en.wikipedia.org/wiki/GEDCOM) file to
a [`gexf`](https://gephi.org/gexf/format) file.

A `gedcom` file contains genealogical data, that can be created
with many softwares, like [Gramps](https://gramps-project.org).

A `gexf` file contains graph data, that can be imported in `Gephi`.

## gedcomAddLatLon

`gedcomAddLatLon` reads a gedcom file and adds latitude
and longitude to all places without these informations.
The result is written in a new gedcom file.
This script uses [`geopy`](https://github.com/geopy/geopy)
to find the latitude and longitude
of locations.
