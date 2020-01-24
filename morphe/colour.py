

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

    def __str__(self):
        return "#{0}{1}{2}{3}".format(format(self.r, "02X"),
                                      format(self.g, "02X"),
                                      format(self.b, "02X"),
                                      format(self.a, "02X"))


class MRGBColour(MRGBAColour):
    """
    Represents an RGB colour.
    """

    def __init__(self, r=0, g=0, b=0):
        super(MRGBColour, self).__init__(r, g, b)

    def __str__(self):
        return "#{0}{1}{2}{3}".format(format(self.r, "02X"),
                                      format(self.g, "02X"),
                                      format(self.b, "02X"))


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