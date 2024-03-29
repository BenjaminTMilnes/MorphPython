import math
from morph.colour import *


class MProperty(object):
    """
    Represents a Morph style property. Style properties have two attributes: a 
    name, which must be a string, and a value, which can be anything, but which 
    is set to a string by default.

    Parameters
    ----------
    name : str
        The name of this style property
    value
        The value of this style property

    Attributes
    ----------
    name : str
        The name of this style property
    value
        The value of this style property
    """

    def __init__(self, name="", value=""):

        self.name = name
        self.value = value

    def __str__(self):
        return "{0}: {1};".format(self.name.strip(), str(self.value).strip())


class MNumber(object):
    """
    Represents a number in a Morph document. This class just acts as a 
    container for a number written as a string.

    Parameters
    ----------
    value : str
        The string representation of the number

    Attributes
    ----------
    value : str
        The string representation of the number
    """

    def __init__(self, value=""):

        self.value = value

    def __str__(self):
        return self.value.strip()


class MPercentage(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "{0}%".format(self.value * 100)


class MLengthUnit(object):
    """
    Represents a Morph length unit. Morph length units are a subset of 
    physical length units that are useful for things on the scale of printed 
    documents.

    The allowed values are:

    "mm" - millimetres
    "cm" - centimetres
    "dm" - decimetres
    "m" - metres
    "in" - inches
    "pt" - points

    Parameters
    ----------
    value : str
        The string representation of the length unit

    Attributes
    ----------
    value : str
        The string representation of the length unit
    """

    def __init__(self, value=""):

        self.value = value

    def __str__(self):
        return self.value.strip()


class MLength(object):
    """
    Represents a Morph length. A length consists of a magnitude and a length 
    unit.

    Parameters
    ----------
    number : str
        The string representation of the magnitude of this length
    unit : str
        The string representation of the unit of this length

    Attributes
    ----------
    number : MNumber
        A Morph number representing the magnitude of this length
    unit : MLengthUnit
        A Morph length unit representing the unit of this length
    """

    def __init__(self, number="", unit=""):

        self.number = MNumber(number)
        self.unit = MLengthUnit(unit)

    def __str__(self):
        return "{0}{1}".format(self.number, self.unit)


class MLengthSet(object):
    """
    Represents a Morph length set. A length set is a list of n lengths, where 
    n >= 1.

    Attributes
    ----------
    lengths : list<MLength>
        The list of lengths in this set
    """

    def __init__(self):

        self.lengths = []

    def __str__(self):
        return " ".join([str(l) for l in self.lengths])


class MElementNameSelector(object):
    """
    Represents a Morph element name selector.

    Parameters
    ----------
    elementName : str
        The element name to select

    Attributes
    ----------
    elementName : str
        The element name to select
    """

    def __init__(self, elementName=""):

        self.elementName = elementName

    def __str__(self):
        return self.elementName


class MClassSelector(object):
    """
    Represents a Morph class name selector.

    Parameters
    ----------
    className : str
        The class name to select

    Attributes
    ----------
    className : str
        The class name to select
    """

    def __init__(self, className=""):

        self.className = className

    def __str__(self):
        return ".{0}".format(self.className)


class MIdSelector(object):
    """
    Represents a Morph id selector.

    Parameters
    ----------
    _id : str
        The id to select

    Attributes
    ----------
    id : str
        The id to select
    """

    def __init__(self, _id=""):

        self.id = _id

    def __str__(self):
        return "#{0}".format(self.id)


class MSubelementSelector(object):
    """
    Represents a Morph subelement selector.

    Parameters
    ----------

    Attributes
    ----------
    """

    def __init__(self):
        pass

    def __str__(self):
        return " "


class MStyleRule(object):
    """
    Represents a Morph style rule. A style rule consists of a list of 
    selectors and a list of style properties.

    When applied to a Graph document, the elements of the document will be 
    filtered based on the selectors of the style rule, and the style properties 
    will be applied to each matching element.

    Attributes
    ----------
    selectors : list
        A list of Morph selectors
    properties : list<MProperty>
        A list of Morph style properties
    """

    def __init__(self):

        self.selectors = []
        self.properties = []


class MDocument(object):
    """
    Represents a Morph document. A Morph document contains a list of style 
    rules.

    Attributes
    ----------
    styleRules : list<MStyleRule>
        A list of style rules within the document
    """

    def __init__(self):

        self.styleRules = []


class MExporter(object):
    """
    Handles converting Morph objects into their text representation.
    """

    def exportDocument(self, document):
        return "".join([self.exportStyleRule(sr) for sr in document.styleRules])

    def exportStyleRule(self, styleRule):
        ss = "".join(["{0}".format(s) for s in styleRule.selectors])
        pp = self.exportProperties(styleRule.properties)
        t = ss + " {\n" + pp + "}\n\n"
        return t

    def exportProperties(self, properties, inline=False):
        if inline == True:
            return " ".join(["{0}".format(p) for p in properties])
        else:
            return "".join(["\t{0}\n".format(p) for p in properties])


def exportMorphDocument(document):
    """
    A helper function that takes a Morph document and returns its text 
    representation.
    """
    exporter = MExporter()

    return exporter.exportDocument(document)


def exportMorphProperties(properties, inline=True):
    """
    A helper function that takes a list of Morph properties and returns their
    text representation.
    """
    exporter = MExporter()

    return exporter.exportProperties(properties, inline)


class MMarker(object):
    """
    A marker class used in parsing the Morph syntax.

    Attributes
    ----------
    position : int
        The position of the marker in the input string.
    """

    def __init__(self):

        self.position = 0

    @property
    def p(self):
        return self.position

    @p.setter
    def p(self, value):
        self.position = value

    def copy(self):
        m = MMarker()

        m.p = self.p

        return m


def cut(text, startIndex, length=1):
    """
    A simple function that makes cutting strings a bit nicer.
    """
    a = startIndex
    b = startIndex + length
    return text[a:b]


class MorphSyntaxError(Exception):
    """
    Nice to have a more specific error type for when the Morph syntax is wrong.

    Parameters
    ----------
    message : str
        A message describing what and where the syntax error is
    """

    def __init__(self, message):
        super(MorpheSyntaxError, self).__init__(message)


def isAlphanumeric(c):
    n = ord(c)

    return (n >= 48 and n < 58) or (n >= 65 and n < 91) or (n >= 97 and n < 123)


def isDigit(c):
    n = ord(c)

    return (n >= 48 and n < 58)


def isHexadecimalDigit(c):
    n = ord(c)

    return (n >= 48 and n < 58) or (n >= 65 and n < 71) or (n >= 97 and n < 103)


class MImporter(object):
    _lengthUnits = ["mm", "cm", "dm", "m", "pt", "in", "pc"]

    def importDocument(self, inputText):
        marker = MMarker()

        styleRules = []

        while True:
            sr = self._getStyleRules(inputText, marker)

            if sr != None:
                styleRules += sr
            else:
                break

        d = MDocument()

        d.styleRules = styleRules

        return d

    def _getStyleRules(self, inputText, marker):
        """
        Gets a style rule at the current position and returns it.
        """
        m = marker.copy()

        # First there should be some sets of selectors.
        selectorSets = self._getSelectorSets(inputText, m)
        # Then get a set of properties.
        properties = self._getProperties(inputText, m)

        # If either the selectors or the properties are none, then there isn't
        # a complete style rule at the current position, so return nothing.
        if selectorSets == [] or properties == None:
            return None

        srs = []

        for selectorSet in selectorSets:
            sr = MStyleRule()

            sr.selectors = selectorSet
            sr.properties = properties

            srs.append(sr)

        marker.p = m.p

        return srs

    def _getSelectorSets(self, inputText, marker):
        """
        Gets the sets of selectors at the current position and returns them.
        """
        m = marker.copy()

        self._getWhiteSpace(inputText, m)

        selectorSets = []
        selectors = []

        addSubelementSelector = False

        # Keep iterating until there aren't any more selectors.
        while True:

            s = self._getIdSelector(inputText, m)

            if s != None:
                if addSubelementSelector:
                    selectors.append(MSubelementSelector())
                    addSubelementSelector = False

                selectors.append(s)
                continue

            s = self._getClassSelector(inputText, m)

            if s != None:
                if addSubelementSelector:
                    selectors.append(MSubelementSelector())
                    addSubelementSelector = False

                selectors.append(s)
                continue

            s = self._getElementNameSelector(inputText, m)

            if s != None:
                if addSubelementSelector:
                    selectors.append(MSubelementSelector())
                    addSubelementSelector = False

                selectors.append(s)
                continue

            if cut(inputText, m.p) == " ":
                addSubelementSelector = True
                m.p += 1
                continue

            if cut(inputText, m.p) == ",":
                selectorSets.append(selectors)
                selectors = []
                m.p += 1

                self._getWhiteSpace(inputText, m)
                
                continue

            break

        if len(selectors) > 0:
            selectorSets.append(selectors)

        marker.p = m.p

        return selectorSets

    def _getIdSelector(self, inputText, marker):
        """
        Gets an id selector at the current position and returns it.
        """
        m = marker.copy()
        start = m.p

        c = cut(inputText, m.p)

        # Id selectors must start with a hash.
        if c != "#":
            return None

        m.p += 1

        # Iterate over the characters in the input text.
        for c in inputText[start + 1:]:
            if isAlphanumeric(c) or c in "-_":
                # If the current character is an allowed id character
                # move the marker along by 1.
                m.p += 1
            else:
                # Otherwise stop iterating.
                break

        end = m.p

        if end - start < 2:
            return None

        t = inputText[start + 1:end]

        marker.p = m.p

        s = MIdSelector(t)

        return s

    def _getClassSelector(self, inputText, marker):
        """
        Gets a class selector at the current position and returns it.
        """
        m = marker.copy()
        start = m.p

        c = cut(inputText, m.p)

        # Class selectors must start with a dot.
        if c != ".":
            return None

        m.p += 1

        # Iterate over the characters in the input text.
        for c in inputText[start + 1:]:
            if isAlphanumeric(c) or c in "-_":
                # If the current character is an allowed class name character
                # move the marker along by 1.
                m.p += 1
            else:
                # Otherwise stop iterating.
                break

        end = m.p

        if end - start < 2:
            return None

        t = inputText[start + 1:end]

        marker.p = m.p

        s = MClassSelector(t)

        return s

    def _getElementNameSelector(self, inputText, marker):
        """
        Gets an element name selector at the current position and returns it.
        """
        m = marker.copy()
        start = m.p

        # Iterate over the characters in the input text.
        for c in inputText[start:]:
            if isAlphanumeric(c) or c in "-_":
                # If the current character is an allowed element name character
                # move the marker along by 1.
                m.p += 1
            else:
                # Otherwise stop iterating.
                break

        end = m.p

        if end == start:
            return None

        t = inputText[start:end]

        marker.p = m.p

        s = MElementNameSelector(t)

        return s

    def _getProperties(self, inputText, marker):
        """
        Gets a set of properties at the current position and returns it.
        """
        m = marker.copy()

        self._getWhiteSpace(inputText, m)

        c = cut(inputText, m.p)

        # A list of properties should start with a recurve bracket.
        if c != "{":
            return None

        m.p += 1

        properties = []

        # Keep trying to find properties at the current position until there
        # aren't any more.
        while True:
            p = self._getProperty(inputText, m)

            if p != None:
                properties.append(p)
            else:
                break

        self._getWhiteSpace(inputText, m)

        c = cut(inputText, m.p)

        # Then there should be a closing recurve bracket at the end.
        if c != "}":
            return None

        m.p += 1

        marker.p = m.p

        return properties

    def _getInlineProperties(self, inputText, marker):
        m = marker.copy()

        self._getWhiteSpace(inputText, m)

        properties = []

        # Keep trying to find properties at the current position until there
        # aren't any more.
        while True:
            p = self._getProperty(inputText, m)

            if p != None:
                properties.append(p)
            else:
                break

        self._getWhiteSpace(inputText, m)

        marker.p = m.p

        return properties

    def _getProperty(self, inputText, marker):
        """
        Gets a property at the current position and returns it.
        """
        m = marker.copy()

        self._getWhiteSpace(inputText, m)

        # First look for a property name.
        name = self._getPropertyName(inputText, m)

        # If there isn't a property name, return nothing.
        if name == None:
            return None

        self._getWhiteSpace(inputText, m)

        c = cut(inputText, m.p)

        # The property name must be followed by a colon.
        if c != ":":
            return None

        m.p += 1

        # Then look for a property value.
        value = self._getPropertyValue(inputText, m)

        # If there isn't a property value, return nothing.
        if value == None:
            return None

        c = cut(inputText, m.p)

        # The property value must be followed by a semi-colon.
        if c != ";":
            return None

        m.p += 1

        marker.p = m.p

        p = MProperty(name.strip(), value)

        return p

    def _getPropertyName(self, inputText, marker):
        """
        Gets a property name at the current position and returns it.
        """
        m = marker
        start = m.p

        # Iterate over the characters in the input text.
        for c in inputText[start:]:
            if isAlphanumeric(c) or c == "-":
                # If the character is an allowed property name character,
                # move the marker along by 1.
                m.p += 1
            else:
                # Otherwise stop iterating.
                break

        end = m.p

        if end == start:
            return None

        t = inputText[start:end]

        return t

    def _getPropertyValue(self, inputText, marker):
        """
        Gets a property value at the current position and returns it.
        """
        # First check if there's a length set at the current position.
        # If there is one, return it.
        lengthSet = self._getLengthSet(inputText, marker)

        if lengthSet != None:
            return lengthSet

        # Now check if there's an rgba colour at the current position.
        # If there is one, return it.
        colour = self._getRGBAColour(inputText, marker)

        if colour != None:
            return colour

        # Now check if there's a hsla colour at the current position.
        # If there is one, return it.
        colour = self._getHSLAColour(inputText, marker)

        if colour != None:
            return colour

        # Otherwise just get the property value as a string.

        m = marker
        start = m.p

        # Iterate over the characters in the input text
        for c in inputText[start:]:
            # Unless it's a character that denotes the end of a property value
            # move the marker along by 1.
            if c not in ";}{":
                m.p += 1
            else:
                break

        end = m.p

        if end == start:
            return None

        t = inputText[start:end]
        t = t.strip()

        if t in namedColours:
            return namedColours[t]

        return t

    def _getHSLAColour(self, inputText, marker):
        m = marker.copy()

        c = cut(inputText, m.p, 4)

        if c == "hsla":
            m.p += 4

            ns = self._getNumberSet(inputText, m)

            if ns == None:
                return None

            if len(ns) != 4:
                raise MorpheSyntaxError("A HSLA colour must have four values.")

            h = ns[0]
            s = ns[1]
            l = ns[2]
            a = ns[3]

            return MHSLAColour(h, s, l, a)

        c = cut(inputText, m.p, 3)

        if c == "hsl":
            m.p += 3

            ns = self._getNumberSet(inputText, m)

            if ns == None:
                return None

            if len(ns) != 3:
                raise MorpheSyntaxError("A HSL colour must have three values.")

            h = ns[0]
            s = ns[1]
            l = ns[2]

            return MHSLColour(h, s, l)

        return None

    def _getRGBAColour(self, inputText, marker):
        m = marker.copy()

        hn = self._getHexadecimalNumber(inputText, m)

        if hn != None:

            if len(hn) != 6 and len(hn) != 8:
                raise MorpheSyntaxError("'#{0}' is not a valid hexadecimal colour code.".format(hn))

            r = int(hn[0:2], 16)
            g = int(hn[2:4], 16)
            b = int(hn[4:6], 16)

            if len(hn) == 8:
                a = int(hn[6:8], 16)

                colour = MRGBAColour(r, g, b, a)

                return colour
            else:
                colour = MRGBColour(r, g, b)

                return colour

        c = cut(inputText, m.p, 4)

        if c == "rgba":
            m.p += 4

            s = self._getNumberSet(inputText, m)

            if s == None:
                return None

            if len(s) != 4:
                raise MorpheSyntaxError("An RGBA colour must have four values.")

            r = s[0]
            g = s[1]
            b = s[2]
            a = s[3]

            self._validateRGBAColourValue(r)
            self._validateRGBAColourValue(g)
            self._validateRGBAColourValue(b)
            self._validateRGBAColourValue(a)

            return MRGBAColour(r, g, b, a)

        c = cut(inputText, m.p, 3)

        if c == "rgb":
            m.p += 3

            s = self._getNumberSet(inputText, m)

            if s == None:
                return None

            if len(s) != 3:
                raise MorpheSyntaxError("An RGB colour must have three values.")

            r = s[0]
            g = s[1]
            b = s[2]

            self._validateRGBAColourValue(r)
            self._validateRGBAColourValue(g)
            self._validateRGBAColourValue(b)

            return MRGBColour(r, g, b)

        return None

    def _validateRGBAColourValue(self, value):

        if isinstance(value, MNumber):
            v = int(value.value)

            if v < 0 or v > 255:
                raise MorpheSyntaxError("RGBA colour values must be between 0 and 255.")
        elif isinstance(value, MPercentage):
            v = value.value * 100

            if v < 0 or v > 100:
                raise MorpheSyntaxError("RGBA colour values must be between 0%% and 100%%.")

    def _getHexadecimalNumber(self, inputText, marker):
        m = marker.copy()
        start = m.p

        c = cut(inputText, m.p)

        if c != "#":
            return None

        m.p += 1

        for c in inputText[m.p:]:
            if isHexadecimalDigit(c):
                m.p += 1
            else:
                break

        end = m.p

        if end - start < 2:
            return None

        t = inputText[start + 1:end]

        marker.p = m.p

        return t

    def _getNumberSet(self, inputText, marker):
        m = marker.copy()

        c = cut(inputText, m.p)

        if c != "(":
            return None

        m.p += 1

        numbers = []

        while True:

            self._getWhiteSpace(inputText, m)

            p = self._getPercentage(inputText, m)

            if p != None:
                numbers.append(p)
            else:
                n = self._getNumber(inputText, m)

                if n != None:
                    numbers.append(n)

            self._getWhiteSpace(inputText, m)

            c = cut(inputText, m.p)

            if c == ",":
                m.p += 1
                continue
            elif c == ")":
                m.p += 1
                break
            else:
                raise MorpheSyntaxError("Expected a comma or a closing bracket.")

        return numbers

    def _getPercentage(self, inputText, marker):
        m = marker.copy()

        number = self._getNumber(inputText, m)

        if number == None:
            return None

        c = cut(inputText, m.p)

        if c != "%":
            return None

        m.p += 1

        marker.p = m.p

        p = MPercentage(float(number.value) / 100)

        return p

    def _getLengthSet(self, inputText, marker):
        """
        Gets a length set at the current position and returns it.
        """
        m = marker.copy()

        # A list to store the lengths that are found
        lengths = []

        # Keep iterating as long as another length expression is found.
        while True:
            self._getWhiteSpace(inputText, m)
            # See if there is a length at the current position.
            # If there is, this function moves the marker along.
            length = self._getLength(inputText, m)

            if length != None:
                # If there is a length, then add it to the list.
                lengths.append(length)
            else:
                # If not, then the current length set has ended, so stop
                # iterating.
                break

        if not lengths:
            # If no lengths were found, return nothing.
            return None

        marker.p = m.p

        # Otherwise, return a length set.
        lengthSet = MLengthSet()

        lengthSet.lengths = lengths

        return lengthSet

    def _getLength(self, inputText, marker):
        """
        Gets a length at the current position and returns it.
        """
        m = marker.copy()

        # First, see if there's a number at the current position.
        number = self._getNumber(inputText, m)

        if number == None:
            # A length expression must start with a number, so if there isn't
            # one, return nothing.
            return None

        # There may be optional white space here - if there is, skip over it.
        self._getWhiteSpace(inputText, m)

        # Now see if there's a length unit at the current position.
        unit = self._getLengthUnit(inputText, m)

        if unit == None:
            # A length expression must have a length unit, so if there isn't
            # one, return nothing.
            return None

        marker.p = m.p

        # If both a number and a length unit have been found, then that's a
        # length expression, so make a new length, set the number and unit
        # and return it.
        length = MLength()

        length.number = number
        length.unit = unit

        return length

    def _getNumber(self, inputText, marker):
        """
        Gets a number at the current position and returns it.
        """
        m = marker
        start = m.p
        # q is the number of decimal points that have been seen.
        # Only one decimal point is allowed in a number.
        q = 0

        # Iterate over the characters in the input text.
        for c in inputText[start:]:
            if isDigit(c):
                # If the current character is a digit, then it is part of a
                # number, so move the marker along by 1.
                m.p += 1
            elif c == ".":
                # If the current character is a decimal point, then move the
                # marker along by 1, and increase the decimal point counter by 1.
                q += 1
                m.p += 1
            else:
                # If the current character is anything else, then it is not part
                # of the current number, so stop iterating.
                break

        end = m.p

        if end == start:
            # If no digits were found, return nothing.
            return None

        t = inputText[start:end]

        if t == "." or q > 1:
            # If all that was found was a single decimal point, or if there
            # was more than one decimal point, then the number is not a valid
            # number, so raise a Morphe syntax error.
            raise MorpheSyntaxError("'{0}' is not a valid number.".format(t))

        # Otherwise return the number.
        number = MNumber(t)

        return number

    def _getLengthUnit(self, inputText, marker):
        """
        Gets a length unit at the current position and returns it.
        """
        m = marker
        l = len(inputText)

        # Iterate over the allowed length units
        for lu in self._lengthUnits:
            lul = len(lu)

            if m.p <= l - lul:
                c = cut(inputText, m.p, lul)

                if c == lu:
                    # If any of the length unit symbols is at the current
                    # position, then return it.
                    lengthUnit = MLengthUnit(c)
                    m.p += lul

                    return lengthUnit

        # Otherwise return nothing.
        return None

    def _getWhiteSpace(self, inputText, marker):
        """
        Gets white space at the current position and returns it.
        """
        m = marker
        start = m.p

        # Iterate over the characters in the input text
        for c in inputText[start:]:
            if c in " \t\n":
                # If the current character is a white space character, move
                # the marker along and keep iterating.
                m.p += 1
            else:
                # If the current character is not a white space character, then
                # the current section of white space has ended, so stop
                # iterating.
                break

        end = m.p

        if end == start:
            # If no white space was found, return nothing.
            return None

        t = inputText[start:end]

        # Otherwise, return a string containing the white space.
        return t


def importMorphDocument(document):
    """
    A helper function that takes a Morph document as a string and returns a 
    Morph document object.
    """
    importer = MImporter()

    return importer.importDocument(document)


def importMorphDocumentFromFile(filePath):
    """
    A helper function that imports a Morph document from a file.
    """
    with open(filePath, "r") as fo:
        data = fo.read()

        return importMorphDocument(data)


def importMorphProperties(properties):
    """
    A helper function that gets a list of style properties from a string. 
    Useful for importing inline style properties.
    """
    importer = MImporter()

    return importer._getInlineProperties(properties, MMarker())
