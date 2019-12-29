

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