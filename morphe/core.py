

class MProperty(object):
    def __init__(self, name="", value=""):

        self.name = name
        self.value = value


class MElementNameSelector(object):
    def __init__(self, elementName=""):

        self.elementName = elementName


class MClassSelector(object):
    def __init__(self, className=""):

        self.className = className


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
        pp = "".join(["\t" + self.exportProperty(p) +
                      "\n" for p in styleRule.properties])
        t = ss + " {\n" + pp + "}\n\n"
        return t

    def exportSelector(self, selector):
        if isinstance(selector, MElementNameSelector):
            return selector.elementName
        if isinstance(selector, MClassSelector):
            return "." + selector.className

    def exportProperty(self, p):
        return p.name.strip() + ": " + p.value.strip() + ";"


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

        p = MProperty(name.strip(), value.strip())

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

        return t

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
