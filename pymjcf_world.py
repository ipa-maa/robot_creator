
from dm_control import mjcf
from pymjcf_utils import Box


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


if __name__ == '__main__':
    w = World('world')
    w.save_model('world.xml')
