

class MColour(object):
    """
    A base class for all Morph colour objects.
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
        return "#{:02X}{:02X}{:02X}{:02X}".format(self.r, self.g, self.b, self.a)


class MRGBColour(MRGBAColour):
    """
    Represents an RGB colour.
    """

    def __init__(self, r=0, g=0, b=0):
        super(MRGBColour, self).__init__(r, g, b)

    def __str__(self):
        return "#{:02X}{:02X}{:02X}".format(self.r, self.g, self.b)


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

    def __str__(self):
        return "hsla({0}, {1}, {2}, {3})".format(self.h, self.s, self.l, self.a)


class MHSLColour(MHSLAColour):
    """
    Represents a HSL colour.
    """

    def __init__(self, h=0, s=0, l=0):
        super(MHSLColour, self).__init__(h, s, l)

    def __str__(self):
        return "hsl({0}, {1}, {2})".format(self.h, self.s, self.l)


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

    def __str__(self):
        return "cmyk({0}, {1}, {2}, {3})".format(self.c, self.m, self.y, self.k)


class MNamedColour(MColour):
    """
    Represents a named colour.
    """

    def __init__(self, name):
        self.name = name
        self.rgbaColour = None
        self.hslaColour = None
        self.cmykColour = None

    def __str__(self):
        return self.name


namedHTMLColours = {"Pink": ["#FFC0CB"],
                    "LightPink": ["#FFB6C1"],
                    "HotPink": ["#FF69B4"],
                    "DeepPink": ["#FF1493"],
                    "PaleVioletRed": ["#DB7093"],
                    "MediumVioletRed": ["#C71585"],
                    "LightSalmon": ["#FFA07A"],
                    "Salmon": ["#FA8072"],
                    "DarkSalmon": ["#E9967A"],
                    "LightCoral": ["#F08080"],
                    "IndianRed": ["#CD5C5C"],
                    "Crimson": ["#DC143C"],
                    "Firebrick": ["#B22222"],
                    "DarkRed": ["#8B0000"],
                    "Red": ["#FF0000"],
                    "OrangeRed": ["#FF4500"],
                    "Tomato": ["#FF6347"],
                    "Coral": ["#FF7F50"],
                    "DarkOrange": ["#FF8C00"],
                    "Orange": ["#FFA500"],
                    "Yellow": ["#FFFF00"],
                    "LightYellow": ["#FFFFE0"],
                    "LemonChiffon": ["#FFFACD"],
                    "LightGoldenrodYellow": ["#FAFAD2"],
                    "PapayaWhip": ["#FFEFD5"],
                    "Moccasin": ["#FFE4B5"],
                    "PeachPuff": ["#FFDAB9"],
                    "PaleGoldenrod": ["#EEE8AA"],
                    "Khaki": ["#F0E68C"],
                    "DarkKhaki": ["#BDB76B"],
                    "Gold": ["#FFD700"],
                    "Cornsilk": ["#FFF8DC"],
                    "BlanchedAlmond": ["#FFEBCD"],
                    "Bisque": ["#FFE4C4"],
                    "NavajoWhite": ["#FFDEAD"],
                    "Wheat": ["#F5DEB3"],
                    "Burlywood": ["#DEB887"],
                    "Tan": ["#D2B48C"],
                    "RosyBrown": ["#BC8F8F"],
                    "SandyBrown": ["#F4A460"],
                    "Goldenrod": ["#DAA520"],
                    "DarkGoldenrod": ["#B8860B"],
                    "Peru": ["#CD853F"],
                    "Chocolate": ["#D2691E"],
                    "SaddleBrown": ["#8B4513"],
                    "Sienna": ["#A0522D"],
                    "Brown": ["#A52A2A"],
                    "Maroon": ["#800000"],
                    "DarkOliveGreen": ["#556B2F"],
                    "Olive": ["#808000"],
                    "OliveDrab": ["#6B8E23"],
                    "YellowGreen": ["#9ACD32"],
                    "LimeGreen": ["#32CD32"],
                    "Lime": ["#00FF00"],
                    "LawnGreen": ["#7CFC00"],
                    "Chartreuse": ["#7FFF00"],
                    "GreenYellow": ["#ADFF2F"],
                    "SpringGreen": ["#00FF7F"],
                    "MediumSpringGreen": ["#00FA9A"],
                    "LightGreen": ["#90EE90"],
                    "PaleGreen": ["#98FB98"],
                    "DarkSeaGreen": ["#8FBC8F"],
                    "MediumAquamarine": ["#66CDAA"],
                    "MediumSeaGreen": ["#3CB371"],
                    "SeaGreen": ["#2E8B57"],
                    "ForestGreen": ["#228B22"],
                    "Green": ["#008000"],
                    "DarkGreen": ["#006400"],
                    "Aqua": ["#00FFFF"],
                    "Cyan": ["#00FFFF"],
                    "LightCyan": ["#E0FFFF"],
                    "PaleTurquoise": ["#AFEEEE"],
                    "Aquamarine": ["#7FFFD4"],
                    "Turquoise": ["#40E0D0"],
                    "MediumTurquoise": ["#48D1CC"],
                    "DarkTurquoise": ["#00CED1"],
                    "LightSeaGreen": ["#20B2AA"],
                    "CadetBlue": ["#5F9EA0"],
                    "DarkCyan": ["#008B8B"],
                    "Teal": ["#008080"],
                    "LightSteelBlue": ["#B0C4DE"],
                    "PowderBlue": ["#B0E0E6"],
                    "LightBlue": ["#ADD8E6"],
                    "SkyBlue": ["#87CEEB"],
                    "LightSkyBlue": ["#87CEFA"],
                    "DeepSkyBlue": ["#00BFFF"],
                    "DodgerBlue": ["#1E90FF"],
                    "CornflowerBlue": ["#6495ED"],
                    "SteelBlue": ["#4682B4"],
                    "RoyalBlue": ["#4169E1"],
                    "Blue": ["#0000FF"],
                    "MediumBlue": ["#0000CD"],
                    "DarkBlue": ["#00008B"],
                    "Navy": ["#000080"],
                    "MidnightBlue": ["#191970"],
                    "Lavender": ["#E6E6FA"],
                    "Thistle": ["#D8BFD8"],
                    "Plum": ["#DDA0DD"],
                    "Violet": ["#EE82EE"],
                    "Orchid": ["#DA70D6"],
                    "Fuchsia": ["#FF00FF"],
                    "Magenta": ["#FF00FF"],
                    "MediumOrchid": ["#BA55D3"],
                    "MediumPurple": ["#9370DB"],
                    "BlueViolet": ["#8A2BE2"],
                    "DarkViolet": ["#9400D3"],
                    "DarkOrchid": ["#9932CC"],
                    "DarkMagenta": ["#8B008B"],
                    "Purple": ["#800080"],
                    "Indigo": ["#4B0082"],
                    "DarkSlateBlue": ["#483D8B"],
                    "SlateBlue": ["#6A5ACD"],
                    "MediumSlateBlue": ["#7B68EE"],
                    "White": ["#FFFFFF"],
                    "Snow": ["#FFFAFA"],
                    "Honeydew": ["#F0FFF0"],
                    "MintCream": ["#F5FFFA"],
                    "Azure": ["#F0FFFF"],
                    "AliceBlue": ["#F0F8FF"],
                    "GhostWhite": ["#F8F8FF"],
                    "WhiteSmoke": ["#F5F5F5"],
                    "Seashell": ["#FFF5EE"],
                    "Beige": ["#F5F5DC"],
                    "OldLace": ["#FDF5E6"],
                    "FloralWhite": ["#FFFAF0"],
                    "Ivory": ["#FFFFF0"],
                    "AntiqueWhite": ["#FAEBD7"],
                    "Linen": ["#FAF0E6"],
                    "LavenderBlush": ["#FFF0F5"],
                    "MistyRose": ["#FFE4E1"],
                    "Gainsboro": ["#DCDCDC"],
                    "LightGray": ["#D3D3D3"],
                    "Silver": ["#C0C0C0"],
                    "DarkGray": ["#A9A9A9"],
                    "Gray": ["#808080"],
                    "DimGray": ["#696969"],
                    "LightSlateGray": ["#778899"],
                    "SlateGray": ["#708090"],
                    "DarkSlateGray": ["#2F4F4F"],
                    "Black": ["#000000"]
                    }

namedColours = {}

for c in namedHTMLColours:
    name = c.lower()
    hd = namedHTMLColours[c][0]

    r = int(hd[1:3], 16)
    g = int(hd[3:5], 16)
    b = int(hd[5:7], 16)

    rgbaColour = MRGBAColour(r, g, b)

    namedColour = MNamedColour(name)
    namedColour.rgbaColour = rgbaColour

    namedColours[name] = namedColour
