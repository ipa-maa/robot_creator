COLORS = {"RED": (1., 0., 0., 0.3),
          "GREEN": (0., 1., 0., 0.3),
          "BLUE": (0., 0., 1., 0.3),
          "CYAN": (0., 1., 1., 0.3),
          "MAGENTA": (1., 0., 1., 0.3),
          "YELLOW": (1., 1., 0., 0.3)}


class Box:
    def __init__(self, lx: float, ly: float, lz: float, color: str = ''):
        self.lx = lx
        self.ly = ly
        self.lz = lz
        self.m_lz = lz / 2
        self.m_ly = ly / 2
        self.m_lx = lx / 2
        if color.upper() in COLORS.keys():
            self.rgba = COLORS[color.upper()]
        else:
            self.rgba = [1, 1, 1, 0.3]
        self.type = 'box'
        self.size = [self.m_lx, self.m_ly, self.m_lz]


class Cylinder:
    def __init__(self, r: float, l: float, color: str = ''):
        self.r = r
        self.l = l
        self.m_l = l/2
        if color.upper() in COLORS.keys():
            self.rgba = COLORS[color.upper()]
        else:
            self.rgba = [1, 1, 1, 0.3]
        self.type = 'cylinder'
        self.size = [self.r, self.m_l]


class Capsule(Cylinder):
    def __init__(self, r: float, l: float, color: str = ''):
        super().__init__(r=r, l=l, color=color)
        self.type = 'capsule'
