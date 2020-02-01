from morphe.core import *


allowedProperties = [
    ["font-height", "MLength"],
    ["font-colour", "MColour"]]

apd = {}

for p in allowedProperties:
    apd[p[0]] = p


class MorpheValidationError(Exception):
    def __init__(self, message):
        super(MorpheValidationError, self).__init__(message)


def validateDocument(document):

    for sr in document.styleRules:
        for p in sr.properties:

            if p.name not in apd:
                raise MorpheValidationError("'{0}' is not a valid Morphe property name.".format(p.name))

            ap = apd[p.name]

            if ap[1] == "MLength":
                if not isinstance(p.value, MLength):
                    raise MorpheValidationError("'{0}' must be a length.".format(p.name))
