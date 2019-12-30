

class MProperty(object):
    def __init__(self, name="", value=""):

        self.name = name
        self.value = value


class MNumber(object):
    def __init__(self, value=""):

        self.value = value

    def __str__(self):
        return self.value

class MLengthUnit(object):
    def __init__(self, value=""):

        self.value = value

    def __str__(self):
        return self.value


class MLength(object):
    def __init__(self, number="", unit=""):

        self.number = MNumber(number)
        self.unit = MLengthUnit(unit)

    def __str__(self):
        return str(self.number) + str(self.unit)


class MLengthSet(object):
    def __init__(self):

        self.lengths = []

    def __str__(self):
        return " ".join([str(l) for l in self.lengths])


class MElementNameSelector(object):
    def __init__(self, elementName=""):

        self.elementName = elementName


class MClassSelector(object):
    def __init__(self, className=""):

        self.className = className


class MIdSelector (object):
    def __init__(self, i=""):

        self.id = i


class MStyleRule(object):
    def __init__(self):

        self.selectors = []
        self.properties = []


class MDocument(object):
    def __init__(self):

        self.styleRules = []


class MExporter (object):

    def exportDocument(self, document):
        return "".join([self.exportStyleRule(sr) for sr in document.styleRules])

    def exportStyleRule(self, styleRule):
        ss = "".join([self.exportSelector(s) for s in styleRule.selectors])
        pp = self.exportProperties(styleRule.properties)
        t = ss + " {\n" + pp + "}\n\n"
        return t

    def exportSelector(self, selector):
        if isinstance(selector, MElementNameSelector):
            return selector.elementName
        if isinstance(selector, MClassSelector):
            return "." + selector.className
        if isinstance(selector, MIdSelector):
            return "#" + selector.id

    def exportProperties(self, properties, inline=False):
        if inline == True:
            return " ".join([self.exportProperty(p) for p in properties])
        else:
            return "".join(["\t" + self.exportProperty(p) + "\n" for p in properties])

    def exportProperty(self, p):
        return p.name.strip() + ": " + self.exportPropertyValue(p.value) + ";"

    def exportPropertyValue(self, value):
        if isinstance(value, MLength):
            return value.number.value + value.unit.value
        if isinstance(value, MLengthSet):
            return " ".join([l.number.value + l.unit.value for l in value.lengths])

        return str(value).strip()


def exportMorpheDocument(document):
    exporter = MExporter()

    return exporter.exportDocument(document)


def exportMorpheProperties(properties, inline=True):
    exporter = MExporter()

    return exporter.exportProperties(properties, inline)


class MMarker (object):
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
    a = startIndex
    b = startIndex + length
    return text[a:b]


class MImporter (object):
    def __init__(self):

        self.lengthUnits = ["mm", "cm", "dm", "m", "pt", "in", "pc"]

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
        m = marker.copy()

        selectors = self._getSelectors(inputText, m)
        properties = self._getProperties(inputText, m)

        if selectors == None or properties == None:
            return None

        sr = MStyleRule()

        sr.selectors = selectors
        sr.properties = properties

        marker.p = m.p

        return sr

    def _getSelectors(self, inputText, marker):
        m = marker.copy()

        self._getWhiteSpace(inputText, m)

        selectors = []
        wasNone = False

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
        m = marker.copy()
        t = ""

        c = cut(inputText, m.p)

        if c != "#":
            return None

        m.p += 1

        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_":
                t += c
                m.p += 1
            else:
                break

        if len(t) == 0:
            return None

        marker.p = m.p

        s = MIdSelector(t)

        return s

    def _getClassSelector(self, inputText, marker):
        m = marker.copy()
        t = ""

        c = cut(inputText, m.p)

        if c != ".":
            return None

        m.p += 1

        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_":
                t += c
                m.p += 1
            else:
                break

        if len(t) == 0:
            return None

        marker.p = m.p

        s = MClassSelector(t)

        return s

    def _getElementNameSelector(self, inputText, marker):
        m = marker.copy()
        t = ""

        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_":
                t += c
                m.p += 1
            else:
                break

        if len(t) == 0:
            return None

        marker.p = m.p

        s = MElementNameSelector(t)

        return s

    def _getProperties(self, inputText, marker):
        m = marker.copy()

        self._getWhiteSpace(inputText, m)

        c = cut(inputText, m.p)

        if c != "{":
            return None

        m.p += 1

        properties = []
        wasNone = False

        while wasNone == False:
            p = self._getProperty(inputText, m)

            if p == None:
                wasNone = True
            else:
                properties.append(p)

        self._getWhiteSpace(inputText, m)

        c = cut(inputText, m.p)

        if c != "}":
            return None

        m.p += 1

        marker.p = m.p

        return properties

    def _getProperty(self, inputText, marker):
        m = marker.copy()

        self._getWhiteSpace(inputText, m)
        name = self._getPropertyName(inputText, m)

        if name == None:
            return None

        self._getWhiteSpace(inputText, m)

        c = cut(inputText, m.p)

        if c != ":":
            return None

        m.p += 1

        value = self._getPropertyValue(inputText, m)

        if value == None:
            return None

        c = cut(inputText, m.p)

        if c != ";":
            return None

        m.p += 1

        marker.p = m.p

        p = MProperty(name.strip(), value)

        return p

    def _getPropertyName(self, inputText, marker):
        m = marker
        t = ""

        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-":
                t += c
                m.p += 1
            else:
                break

        if len(t) == 0:
            return None

        return t

    def _getPropertyValue(self, inputText, marker):
        lengthSet = self._getLengthSet(inputText, marker)

        if lengthSet != None:
            return lengthSet

        m = marker
        t = ""

        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c not in ";}{":
                t += c
                m.p += 1
            else:
                break

        if len(t) == 0:
            return None

        return t.strip()

    def _getLengthSet(self, inputText, marker):
        m = marker.copy()

        lengths = []
        wasNone = False

        while wasNone == False:
            self._getWhiteSpace(inputText, m)

            length = self._getLength(inputText, m)

            if length != None:
                lengths.append(length)
            else:
                wasNone = True

        if len(lengths) == 0:
            return None

        marker.p = m.p

        lengthSet = MLengthSet()

        lengthSet.lengths = lengths

        return lengthSet

    def _getLength(self, inputText, marker):
        m = marker.copy()

        number = self._getNumber(inputText, m)

        if number == None:
            return None

        self._getWhiteSpace(inputText, m)

        unit = self._getLengthUnit(inputText, m)

        if unit == None:
            return None

        marker.p = m.p

        length = MLength()

        length.number = number
        length.unit = unit

        return length

    def _getNumber(self, inputText, marker):
        m = marker
        t = ""
        q = 0

        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in "0123456789":
                t += c
                m.p += 1
            elif c == "." and q == 0:
                t += c
                q += 1
                m.p += 1
            else:
                break

        if len(t) == 0:
            return None

        if t == ".":
            return None

        number = MNumber(t)

        return number

    def _getLengthUnit(self, inputText, marker):
        m = marker

        for lu in self.lengthUnits:
            if m.p <= len(inputText) - len(lu):
                c = cut(inputText, m.p, len(lu))

                if c == lu:
                    lengthUnit = MLengthUnit(c)
                    m.p += len(c)

                    return lengthUnit

        return None

    def _getWhiteSpace(self, inputText, marker):
        m = marker
        t = ""

        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c in " \t\n":
                t += c
                m.p += 1
            else:
                break

        if len(t) == 0:
            return None

        return t


def importMorpheDocument(document):
    importer = MImporter()

    return importer.importDocument(document)


def importMorpheProperties(properties):
    importer = MImporter()

    return importer._getProperties(properties, MMarker())
