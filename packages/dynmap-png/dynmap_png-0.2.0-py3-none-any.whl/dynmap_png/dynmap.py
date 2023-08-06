import json
import requests


# Class that defines a Dynmap configuration
class DynmapConfiguration:
  # Constructor
  def __init__(self, **kwargs):
    self.worlds = [DynmapWorld(self, **world_kwargs) for world_kwargs in kwargs.get('worlds', [])]

  # Parse the configuration from JSON URL
  @classmethod
  def parse_url(cls, url):
    response = requests.get(url)
    return cls(**response.json())


# Class that defines a Dynmap world
class DynmapWorld:
  # Constructor
  def __init__(self, configuration, **kwargs):
    self.configuration = configuration

    self.name = kwargs.get('name', '')
    self.title = kwargs.get('title', '')
    self.maps = [DynmapMap(configuration, self, **map_kwargs) for map_kwargs in kwargs.get('maps', [])]


# Class that defines a Dynmap map
class DynmapMap:
  # Constructor
  def __init__(self, configuration, world, **kwargs):
    self.configuration = configuration
    self.world = world

    self.name = kwargs.get('name', '')
    self.title = kwargs.get('title', '')
    self.perspective = kwargs.get('perspective', '')
    self.prefix = kwargs.get('prefix', '')
    self.image_format = kwargs.get('image-format', '')
