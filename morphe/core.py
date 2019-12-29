

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

    def _getProperty(inputText, marker):
        m = marker.copy()

        self._getWhiteSpace(inputText, m)
        name = self._getPropertyName(inputText, m)

        if name == None:
            return None

        self._getWhiteSpace(inputText, m)

        c = cut(inputText, m.p)

        if c != ":":
            return None

        value = self._getPropertyValue(inputText, m)

        if value == None:
            return None

        c = cut(inputText, m.p)

        if c != ";":
            return None

        p = MProperty(name, value)

        return p

    def _getPropertyValue(inputText, marker):
        m = marker
        t = ""

        while m.p < len(inputText):
            c = cut(inputText, m.p)

            if c not in ";\{\}":
                t += c
                m.p += 1
            else:
                break

        if len(t) == 0:
            return None

        return t

    def _getPropertyName(inputText, marker):
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

    def _getWhiteSpace(inputText, marker):
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
