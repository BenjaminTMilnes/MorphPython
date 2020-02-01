from morphe.core import *


propertySynonyms = {
    "font-color": "font-colour",
    "background-color": "background-colour",
    "border-color": "border-colour",
    "border-top-color": "border-top-colour",
    "border-right-color": "border-right-colour",
    "border-bottom-color": "border-bottom-colour",
    "border-left-color": "border-left-colour",
}

allowedProperties = [
    ["font-name", "str"],
    ["font-height", "MLength"],
    ["font-weight",  "MFontWeight"],
    ["font-colour", "MColour"], ]

apd = {}

for p in allowedProperties:
    apd[p[0]] = p


class MorpheValidationError(Exception):
    def __init__(self, message):
        super(MorpheValidationError, self).__init__(message)


def validateDocument(document):

    for sr in document.styleRules:
        for p in sr.properties:

            name = p.name

            if name in propertySynonyms:
                name = propertySynonyms[name]

            if name not in apd:
                raise MorpheValidationError("'{0}' is not a valid Morphe property name.".format(p.name))

            ap = apd[name]

            if ap[1] == "MLength":
                if not isinstance(p.value, MLength):
                    raise MorpheValidationError("'{0}' must be a length.".format(p.name))
