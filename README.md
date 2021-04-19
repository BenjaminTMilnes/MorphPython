# MorphPython

Morph, from *Morphē*, a Greek word meaning 'form', 'shape', 'beauty', 'outward appearance'.

---

Morph is a language used for describing the appearance of printable documents written in the mark-up language Graphe. Morph is based heavily on CSS, and many of the names of style properties are the same.

This repository contains a Python implementation of Morph.

## An example Morph style sheet

```css

.main {
    page-size: a4;
    font-height: 12pt;
}

h1 {
    font-height: 20pt;
    font-weight: bold;
}

p.red {
    font-colour: red;
}

```

## Basic usage

Get a Morph document from a string:

```python

from morph.core import *

document = importMorphDocument(morphString)

```

Convert a Morph document to a string:

```python

from morph.core import *

morphString = exportMorphDocument(document)

```

## Running the Unit Tests

```bash

py -m unittest discover

```