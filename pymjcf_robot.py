# %%
from dm_control import mjcf
from pymjcf_utils import Box, Cylinder, Capsule

# ur5 dimensions https://www.zacobria.com/temp/ur5_dimensions.jpg
# ur10 dimensions https://ars.els-cdn.com/content/image/1-s2.0-S0957415818300369-gr3.jpg
class Robot(object):
    def __init__(self, name):
        self.mjcf_model = mjcf.RootElement(model=name)

        base = Cylinder(r=0.1, l=0.181, color='red')
        shoulder_link = Cylinder(r=0.075, l=0.613)
        upper_arm_link = Cylinder(r=0.075, l=0.571)
        forearm_link = Cylinder(r=0.05, l=0.120)
        wrist_link = Cylinder(r=0.05, l=0.117)

        self.base = self.mjcf_model.worldbody.add('body', name='base')
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

        self.shoulder_link = self.base.add('body', name='shoulder_link')
        self.shoulder_link.add('geom',
                               name='shoulder_link',
                               type=shoulder_link.type,
                               pos=[0, 0.176, base.l + shoulder_link.m_l],
                               size=shoulder_link.size,
                               rgba=shoulder_link.rgba)
        self.shoulder_link.add('joint',
                               name='robot:joint1',
                               type='hinge',
                               pos=[0, 0.176, base.l],
                               axis=[0, 1, 0])

        self.upper_arm_link = self.shoulder_link.add('body', name='upper_arm_link')
        self.upper_arm_link.add('geom',
                                name='upper_arm_link',
                                type=upper_arm_link.type,
                                pos=[0, 0.176 - 0.137, base.l + shoulder_link.l + upper_arm_link.m_l],
                                size=upper_arm_link.size,
                                rgba=upper_arm_link.rgba)
        self.upper_arm_link.add('joint',
                                name='robot:joint2',
                                type='hinge',
                                pos=[0, 0.176 - 0.137, base.l + shoulder_link.l],
                                axis=[0, 1, 0])

        self.forearm_link = self.upper_arm_link.add('body', name='forearm_link')
        self.forearm_link.add('geom',
                              name='forearm_link',
                              type=forearm_link.type,
                              pos=[0, 0.176 - 0.137 + 0.135, base.l + shoulder_link.l + upper_arm_link.l + forearm_link.m_l],
                              size=forearm_link.size)
        self.forearm_link.add('joint',
                              name='robot:joint3',
                              type='hinge',
                              pos=[0, 0.176 - 0.137 + 0.135, base.l + shoulder_link.l + upper_arm_link.l],
                              axis=[0, 1, 0])

        self.wrist_link = self.forearm_link.add('body', name='wrist_link')
        self.wrist_link.add('geom',
                            name='wrist_link',
                            type=wrist_link.type,
                            quat=[-1, 1, 0, 0],
                            pos=[0, 0.176 - 0.137 + 0.135 + 0.117, base.l + shoulder_link.l + upper_arm_link.l + forearm_link.l + wrist_link.m_l],
                            size=wrist_link.size)
        self.wrist_link.add('joint',
                            name='robot:joint4',
                            type='hinge',
                            pos=[0, 0.176 - 0.137 + 0.135, base.l + shoulder_link.l + upper_arm_link.l + forearm_link.l])

        gripper = Gripper()
        self.wrist_link_site = self.wrist_link.add('site',
                                                   name='wrist_link_site',
                                                   quat=[-1, 1, 0, 0],
                                                   pos=[0, 0.176 - 0.137 + 0.135 + 0.117117 + wrist_link.m_l + gripper.box_base.m_lz, base.l + shoulder_link.l + upper_arm_link.l + forearm_link.l + wrist_link.r])

        self.gripper = self.wrist_link_site.attach(gripper.mjcf_model)

    def save_model(self, filename):
        with open(filename, 'w') as f:
            f.write(self.mjcf_model.to_xml_string())


class Gripper(object):
    def __init__(self, name='gripper'):
        self.mjcf_model = mjcf.RootElement(model=name)

        base = Box(lx=0.15, ly=0.05, lz=0.05, color='yellow')
        finger = Box(lx=0.1, ly=0.05, lz=0.01, color='yellow')

        self.box_base = base
        self.box_finger = finger

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
                             name='joint_left',
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
                              name='joint_right',
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
