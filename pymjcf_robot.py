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
        self.base.add('joint',
                      name='robot:joint0',
                      type='hinge',
                      pos=[0, 0, 0 + base.m_l],
                      axis=[0, 0, 1])
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
                               pos=[0, base.r, base.l],
                               axis=[0, 1, 0])
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


class Gripper:
    def __init__(self, name='gripper'):
        self.mjcf_model = mjcf.RootElement(model=name)

        base = Box(lx=0.15, ly=0.05, lz=0.05, color='yellow')
        finger = Box(lx=0.1, ly=0.05, lz=0.01, color='yellow')

        self.base = self.mjcf_model.worldbody.add('body', name='base')
        self.base.add('geom',
                      name='base',
                      type=base.type,
                      pos=[0, 0, 0],
                      size=base.size,
                      rgba=base.rgba)

        self.finger_left = self.base.add('body', name='finger_left')
        self.finger_left.add('geom',
                             name='finger_left',
                             type=finger.type,
                             quat=[1, 0, -1, 0],
                             pos=[base.m_lx * (2/3), 0, base.m_lz + finger.m_lx],
                             size=finger.size,
                             rgba=finger.rgba)
        self.finger_left.add('joint',
                             name='gripper:joint_left',
                             type='slide',
                             pos=[0, 0, base.m_lz],
                             axis=[1, 0, 0],
                             limited='True',
                             range=[-base.m_lx * (2/3) + finger.m_lz, 0.],
                             damping=1)

        self.finger_right = self.base.add('body', name='finger_right')
        self.finger_right.add('geom',
                              name='finger_right',
                              type=finger.type,
                              quat=[1, 0, 1, 0],
                              pos=[- base.m_lx * (2/3), 0, base.m_lz + finger.m_lx],
                              size=finger.size,
                              rgba=finger.rgba)
        self.finger_right.add('joint',
                              name='gripper:joint_right',
                              type='slide',
                              pos=[0, 0, base.m_lz],
                              axis=[1, 0, 0],                            
                              limited='True',
                              range=[0., base.m_lx * (2/3) - finger.m_lz],
                              damping=1)

    def save_model(self, filename):
        with open(filename, 'w') as f:
            f.write(self.mjcf_model.to_xml_string())


robot = Robot(name='robot')
gripper = Gripper(name='gripper')

robot.save_model('robot.xml')
gripper.save_model('gripper.xml')
# physics = mjcf.Physics.from_mjcf_model(body.mjcf_model)
