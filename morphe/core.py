

class MProperty(object):
    """
    Represents a Morphe style property. Style properties have two attributes: a 
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
    Represents a number in a Morphe document. This class just acts as a 
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


class MLengthUnit(object):
    """
    Represents a Morphe length unit. Morphe length units are a subset of 
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
    Represents a Morphe length. A length consists of a magnitude and a length 
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
        A Morphe number representing the magnitude of this length
    unit : MLengthUnit
        A Morphe length unit representing the unit of this length
    """

    def __init__(self, number="", unit=""):

        self.number = MNumber(number)
        self.unit = MLengthUnit(unit)

    def __str__(self):
        return "{0}{1}".format(self.number, self.unit)


class MLengthSet(object):
    """
    Represents a Morphe length set. A length set is a list of n lengths, where 
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


class MColour(object):
    """
    A base class for all Morphe colour objects.
    """
    pass


class MRGBAColour(MColour):
    """
    Represents an RGBA colour.
    """

    def __init__(self, r=0, g=0, b=0, a=0):
        super(MRGBAColour, self).__init__()

        self.r = r
        self.g = g
        self.b = b
        self.a = a


class MRGBColour(MRGBAColour):
    """
    Represents an RGB colour.
    """

    def __init__(self, r=0, g=0, b=0):
        super(MRGBColour, self).__init__(r, g, b)


class MHSLAColour(MColour):
    """
    Represents a HSLA colour.
    """

    def __init__(self, h=0, s=0, l=0, a=0):
        super(MHSLAColour, self).__init__()

        self.h = h
        self.s = s
        self.l = l
        self.a = a


class MHSLColour(MHSLAColour):
    """
    Represents a HSL colour.
    """

    def __init__(self, h=0, s=0, l=0):
        super(MHSLColour, self).__init__(h, s, l)


class MCMYKColour(MColour):
    """
    Represents a CMYK colour.
    """

    def __init__(self, c=0, m=0, y=0, k=0):
        super(MCMYKColour, self).__init__()

        self.c = c
        self.m = m
        self.y = y
        self.k = k


class MElementNameSelector(object):
    """
    Represents a Morphe element name selector.

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
    Represents a Morphe class name selector.

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
    Represents a Morphe id selector.

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


class MStyleRule(object):
    """
    Represents a Morphe style rule. A style rule consists of a list of 
    selectors and a list of style properties.

    When applied to a Graphe document, the elements of the document will be 
    filtered based on the selectors of the style rule, and the style properties 
    will be applied to each matching element.

    Attributes
    ----------
    selectors : list
        A list of Morphe selectors
    properties : list<MProperty>
        A list of Morphe style properties
    """

    def __init__(self):

        self.selectors = []
        self.properties = []


class MDocument(object):
    """
    Represents a Morphe document. A Morphe document contains a list of style 
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
    Handles converting Morphe objects into their text representation.
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


def exportMorpheDocument(document):
    """
    A helper function that takes a Morphe document and returns its text 
    representation.
    """
    exporter = MExporter()

    return exporter.exportDocument(document)


def exportMorpheProperties(properties, inline=True):
    """
    A helper function that takes a list of Morphe properties and returns their
    text representation.
    """
    exporter = MExporter()

    return exporter.exportProperties(properties, inline)


class MMarker(object):
    """
    A marker class used in parsing the Morphe syntax.

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


class MorpheSyntaxError(Exception):
    """
    Nice to have a more specific error type for when the Morphe syntax is wrong.

    Parameters
    ----------
    message : str
        A message describing what and where the syntax error is
    """

    def __init__(self, message):
        super(MorpheSyntaxError, self).__init__(message)


class MImporter(object):
    _allowedPropertyNameCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"

    _allowedIdCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    _allowedClassNameCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    _allowedElementNameCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"

    _lengthUnits = ["mm", "cm", "dm", "m", "pt", "in", "pc"]

    def importDocument(self, inputText):
        marker = MMarker()

        styleRules = []
        wasNone = False

        while wasNone == False:
            sr = self._getStyleRule(inputText, marker)

            if sr == None:
                break
            else:
                styleRules.append(sr)

        d = MDocument()

        d.styleRules = styleRules

        return d

    def _getStyleRule(self, inputText, marker):
        """
        Gets a style rule at the current position and returns it.
        """
        m = marker.copy()

        # First there should be a set of selectors.
        selectors = self._getSelectors(inputText, m)
        # Then get a set of properties.
        properties = self._getProperties(inputText, m)

        # If either the selectors or the properties are none, then there isn't
        # a complete style rule at the current position, so return nothing.
        if selectors == None or properties == None:
            return None

        sr = MStyleRule()

        sr.selectors = selectors
        sr.properties = properties

        marker.p = m.p

        return sr

    def _getSelectors(self, inputText, marker):
        """
        Gets a set of selectors at the current position and returns it.
        """
        m = marker.copy()

        self._getWhiteSpace(inputText, m)

        selectors = []
        wasNone = False

        # Keep iterating until there aren't any more selectors.
        while wasNone == False:

            s = self._getIdSelector(inputText, m)

            if s != None:
                selectors.append(s)
                continue

            s = self._getClassSelector(inputText, m)

            if s != None:
                selectors.append(s)
                continue

            s = self._getElementNameSelector(inputText, m)

            if s != None:
                selectors.append(s)
                continue

            wasNone = True

        marker.p = m.p

        return selectors

    def _getIdSelector(self, inputText, marker):
        """
        Gets an id selector at the current position and returns it.
        """
        m = marker.copy()
        t = ""

        c = cut(inputText, m.p)

        # Id selectors must start with a hash.
        if c != "#":
            return None

        m.p += 1

        # Iterate over the characters in the input text.
        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in self._allowedIdCharacters:
                # If the current character is an allowed id character
                # add it to the temporary string.
                t += c
                m.p += 1
            else:
                # Otherwise stop iterating.
                break

        if len(t) == 0:
            return None

        marker.p = m.p

        s = MIdSelector(t)

        return s

    def _getClassSelector(self, inputText, marker):
        """
        Gets a class selector at the current position and returns it.
        """
        m = marker.copy()
        t = ""

        c = cut(inputText, m.p)

        # Class selectors must start with a dot.
        if c != ".":
            return None

        m.p += 1

        # Iterate over the characters in the input text.
        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in self._allowedClassNameCharacters:
                # If the current character is an allowed class name character
                # add it to the temporary string.
                t += c
                m.p += 1
            else:
                # Otherwise stop iterating.
                break

        if len(t) == 0:
            return None

        marker.p = m.p

        s = MClassSelector(t)

        return s

    def _getElementNameSelector(self, inputText, marker):
        """
        Gets an element name selector at the current position and returns it.
        """
        m = marker.copy()
        t = ""

        # Iterate over the characters in the input text.
        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in self._allowedElementNameCharacters:
                # If the current character is an allowed element name character
                # add it to the temporary string.
                t += c
                m.p += 1
            else:
                # Otherwise stop iterating.
                break

        if len(t) == 0:
            return None

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
        wasNone = False

        # Keep trying to find properties at the current position until there
        # aren't any more.
        while wasNone == False:
            p = self._getProperty(inputText, m)

            if p == None:
                wasNone = True
            else:
                properties.append(p)

        self._getWhiteSpace(inputText, m)

        c = cut(inputText, m.p)

        # Then there should be a closing recurve bracket at the end.
        if c != "}":
            return None

        m.p += 1

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
        t = ""

        # Iterate over the characters in the input text.
        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in self._allowedPropertyNameCharacters:
                # If the character is an allowed property name character,
                # add it to the temporary string.
                t += c
                m.p += 1
            else:
                # Otherwise stop iterating.
                break

        if len(t) == 0:
            return None

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

        # Otherwise just get the property value as a string.

        m = marker
        t = ""

        # Iterate over the characters in the input text
        while m.p < len(inputText):
            c = cut(inputText, m.p)

            # Unless it's a character that denotes the end of a property value
            # add it to the temporary string.
            if c not in ";}{":
                t += c
                m.p += 1
            else:
                break

        if len(t) == 0:
            return None

        return t.strip()

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

        if len(lengths) == 0:
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
        t = ""
        # q is the number of decimal points that have been seen.
        # Only one decimal point is allowed in a number.
        q = 0

        # Iterate over the characters in the input text.
        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in "0123456789":
                # If the current character is a digit, then it is part of a
                # number, so add it to a temporary string, and move the marker
                # along by 1.
                t += c
                m.p += 1
            elif c == ".":
                # If the current character is a decimal point, then add it to
                # the temporary string, move the marker along by 1, and
                # increase the decimal point counter by 1.
                t += c
                q += 1
                m.p += 1
            else:
                # If the current character is anything else, then it is not part
                # of the current number, so stop iterating.
                break

        if len(t) == 0:
            # If no digits were found, return nothing.
            return None

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

        # Iterate over the allowed length units
        for lu in self._lengthUnits:
            if m.p <= len(inputText) - len(lu):
                c = cut(inputText, m.p, len(lu))

                if c == lu:
                    # If any of the length unit symbols is at the current
                    # position, then return it.
                    lengthUnit = MLengthUnit(c)
                    m.p += len(c)

                    return lengthUnit

        # Otherwise return nothing.
        return None

    def _getWhiteSpace(self, inputText, marker):
        """
        Gets white space at the current position and returns it.
        """
        m = marker
        l = len(inputText)
        start = m.p

        # Iterate over the characters in the input text
        while m.p < l:
            c = cut(inputText, m.p)

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


def importMorpheDocument(document):
    """
    A helper function that takes a Morphe document as a string and returns a 
    Morphe document object.
    """
    importer = MImporter()

    return importer.importDocument(document)


def importMorpheDocumentFromFile(filePath):
    """
    A helper function that imports a Morphe document from a file.
    """
    with open(filePath, "r") as fo:
        data = fo.read()

        return importMorpheDocument(data)


def importMorpheProperties(properties):
    """
    A helper function that gets a list of style properties from a string. 
    Useful for importing inline style properties.
    """
    importer = MImporter()

    return importer._getProperties(properties, MMarker())
