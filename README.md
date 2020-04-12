# MorphePython

Morphe, from *Morphē*, a Greek word meaning 'form', 'shape', 'beauty', 'outward appearance'.

---

Morphe is a language used for describing the appearance of printable documents written in the mark-up language Graphe. Morphe is based heavily on CSS, and many of the names of style properties are the same.

This repository contains a Python implementation of Morphe.

## An example Morphe style sheet

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

Get a Morphe document from a string:

```python

from morphe.core import *

document = importMorpheDocument(morpheString)

```

Convert a Morphe document to a string:

```python

from morphe.core import *

morpheString = exportMorpheDocument(document)

```

## Running the Unit Tests

```bash

py -m unittest discover

```