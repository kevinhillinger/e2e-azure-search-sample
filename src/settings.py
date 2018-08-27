import os
import yaml
from datetime import datetime
from pathlib import Path

class Settings(object):
  def __init__(self):
    self.__values = {}

class SettingsProvider(object):
  def get_settings(self):
    settings_path = self.__get_settings_path()
    settings = Settings()

    with open(settings_path, 'r') as yaml_file:
      settings.__values = yaml.load(yaml_file)

    self.__load(target = settings, values = settings.__values)

    return settings

  def get_param_suffix(self):
    dt = datetime.now()
    suffix = "%i%i%i" % (dt.month, dt.minute, dt.second)
    return suffix

  def __load(self, target, values):
    for key in values:
      if type(values[key]) is dict:
        settings = Settings()
        setattr(target, key, settings)
        self.__load(target = settings, values = values[key])
      else:
        setattr(target, key, values[key])

  def __get_settings_path(self):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    config_path = current_path.parents[0] #go up a level to access config
    settings_path = config_path / 'config/config.yaml'

    return settings_path