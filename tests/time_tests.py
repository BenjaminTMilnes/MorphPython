
from morphe.core import *

import timeit

n = 10000

i = MImporter()

t = timeit.timeit(lambda: i._getNumber("1.23456789", MMarker()), number=n)

print(t/n)

t = timeit.timeit(lambda: importMorpheDocumentFromFile("examples/example1.morphe"), number=n)

print(t/n)

example1 = """

p {
    font-size: 12pt;
    font-colour   :   black   ;
    margin   :12pt 16pt   ;
}

.red { font-colour: red; }

#infobox {
    border: 1px solid blue;
}

"""

t = timeit.timeit(lambda: importMorpheDocument(example1), number=n)

print(t/n)
