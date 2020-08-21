# %%
from dm_control import mjcf
from pymjcf_utils import Box
from pymjcf_robot import Robot


class World(object):
    def __init__(self, name):
        self.mjcf_model = mjcf.RootElement(model=name)

        floor = Box(lx=10, ly=10, lz=0.001, color='blue')
        table = Box(lx=2, ly=2, lz=1)

        self.floor = self.mjcf_model.worldbody.add('body', name='floor')
        self.floor.add('geom',
                       name='floor',
                       pos=[0, 0, 0],
                       type=floor.type,
                       size=floor.size,
                       rgba=floor.rgba)

        self.table = self.floor.add('body', name='table')
        self.table.add('geom',
                       name='table',
                       pos=[0, 0, table.m_lz],
                       type=table.type,
                       size=table.size,
                       rgba=[1, 1, 1, 1])

        self.asset = self.mjcf_model.asset.add('texture',
                                               name="skybox",
                                               type="skybox",
                                               builtin="gradient",
                                               rgb1=".4 .6 .8",
                                               rgb2="0 0 0",
                                               width="800",
                                               height="800",
                                               mark="random",
                                               markrgb="1 1 1")

    def save_model(self, filename):
        with open(filename, 'w') as f:
            f.write(self.mjcf_model.to_xml_string())


class RopeWorld(object):
    def __init__(self, name):
        self.mjcf_model = mjcf.RootElement(model=name)

        world = World('world')
        self.world_site = self.mjcf_model.worldbody.add('site', name='world')
        self.world_site.attach(world.mjcf_model)

        robot = Robot('ub10')
        self.robot_site = self.mjcf_model.worldbody.add('site',
                                                        name='ub10',
                                                        pos=[0, 0, 1.0])
        self.robot_site.attach(robot.mjcf_model)

        # self.rope_body = self.mjcf_model.worldbody.add('body', name='B0:rope', pos=[0, 0.5, 1])
        # self.rope_body.add('freejoint', name='rope_joint')
        # self.rope_composite = self.rope_body.add('composite',
        #                                          type="rope",
        #                                          count="21 1 1",
        #                                          spacing="0.04",
        #                                          offset="0 0 2")

        # self.rope_composite.add('joint',
        #                         kind="main",
        #                         damping="0.005")
        # self.rope_body.add('geom',
        #                    type="capsule",
        #                    size=".01 .015",
        #                    rgba=".8 .2 .1 1")

    def save_model(self, filename):
        with open(filename, 'w') as f:
            f.write(self.mjcf_model.to_xml_string())


# %%
if __name__ == '__main__':
    # w = World('world')
    # w.save_model('world.xml')
    rw = RopeWorld('rope_world')
    rw.save_model('rope_world.xml')
