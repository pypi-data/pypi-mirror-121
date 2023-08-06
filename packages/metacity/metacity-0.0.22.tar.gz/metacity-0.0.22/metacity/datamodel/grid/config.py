import numpy as np
from metacity.filesystem import grid as fs
from metacity.filesystem.file import read_json, write_json


class RegularGridConfig:
    def __init__(self, grid):
        self.bbox = np.array([0, 0, 0])
        self.tile_size = 1000

        self.oid_to_id = {}
        self.id_to_oid = {}
        self.resolution = np.array([0, 0])
        self.id_counter = 0
        self.grid = grid

        try:
            path = fs.grid_config(self.grid.dir)
            self.deserialize(read_json(path))
        except Exception:
            pass

    def id_for_oid(self, oid):
        if oid not in self.oid_to_id:
            self.oid_to_id[oid] = self.id_counter
            self.id_to_oid[self.id_counter] = oid
            self.id_counter += 1
        return self.oid_to_id[oid]

    @property
    def shift(self):
        return self.bbox[0]

    def x_tile_base(self, x):
        return self.shift[0] + x * self.tile_size

    def y_tile_base(self, y):
        return self.shift[1] + y * self.tile_size

    def x_tile_top(self, x):
        return self.shift[0] + (x + 1) * self.tile_size

    def y_tile_top(self, y):
        return self.shift[1] + (y + 1) * self.tile_size

    def serialize(self):
        return {
            'oid_to_id': self.oid_to_id,
            'id_to_oid': self.id_to_oid,
            'id_counter': self.id_counter,
            'resolution': self.resolution.tolist(),
            'bbox': self.bbox.tolist(),
            'tile_size': self.tile_size
        }

    def deserialize(self, data):
        self.oid_to_id = data['oid_to_id']
        self.id_to_oid = data['id_to_oid']
        self.id_counter = data['id_counter']
        self.resolution = np.array(data['resolution'])
        self.bbox = np.array(data['bbox'])
        self.tile_size = data['tile_size']

    def export(self):
        path = fs.grid_config(self.grid.dir)
        write_json(path, self.serialize())
