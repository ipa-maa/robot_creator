# %%
from dm_control import mjcf
from dm_control import viewer
from dm_control import mujoco

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


class Robot(object):
    def __init__(self, name):
        self.mjcf_model = mjcf.RootElement(model=name)

        self.base = self.mjcf_model.worldbody.add('body', name='base')
        base = Cylinder(r=0.2, l=0.3, color='red')
        self.base.add('geom',
                      name='base',
                      type=base.type,
                      pos=[0, 0, 0 + base.m_l],
                      size=base.size,
                      rgba=base.rgba)

        shoulder_link = Capsule(r=0.15, l=0.8)
        self.shoulder_link = self.base.add('body', name='shoulder_link')
        self.shoulder_link.add('joint',
                               name='robot:joint1',
                               type='hinge',
                               pos=[0, base.r, base.l + shoulder_link.m_l],
                               axis=[0, 0, 1])
        self.shoulder_link.add('geom',
                               name='shoulder_link',
                               type=shoulder_link.type,
                               pos=[0, base.r, base.l + shoulder_link.m_l],
                               size=shoulder_link.size,
                               rgba=shoulder_link.rgba)

        upper_arm_link = Capsule(r=0.15, l=0.6)
        self.upper_arm_link = self.shoulder_link.add('body', name='upper_arm_link')
        self.upper_arm_link.add('geom',
                                name='upper_arm_link',
                                type=upper_arm_link.type,
                                pos=[0, 0, base.l + shoulder_link.l + upper_arm_link.m_l],
                                size=upper_arm_link.size,
                                rgba=upper_arm_link.rgba)
        self.upper_arm_link.add('joint',
                                name='robot:joint2',
                                type='hinge',
                                pos=[0, 0, base.l + shoulder_link.l],
                                axis=[0, 1, 0])

        # print(self.upper_arm_link.geom[0].pos[2])

        forearm_link = Capsule(r=0.15, l=0.2)
        self.forearm_link = self.upper_arm_link.add('body', name='forearm_link')
        self.forearm_link.add('geom',
                              name='forearm_link',
                              type=forearm_link.type,
                              pos=[0, .15, base.l + shoulder_link.l + upper_arm_link.l + forearm_link.m_l],
                              size=forearm_link.size)
        self.forearm_link.add('joint',
                              name='robot:joint3',
                              type='hinge',
                              pos=[0, .15, base.l + shoulder_link.l + upper_arm_link.l],
                              axis=[0, 1, 0])

    def save_model(self, filename):
        with open(filename, 'w') as f:
            f.write(self.mjcf_model.to_xml_string())


robot = Robot(name='robot')

robot.save_model('robot.xml')

# physics = mjcf.Physics.from_mjcf_model(body.mjcf_model)