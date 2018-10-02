import json
import yaml
import copy
import pprint

class CFGObj:

  def __init__(self, *args, **kwargs):
    self.__dict__ = dict()
    if isinstance(kwargs, dict):
      self.__dict__.update(copy.deepcopy(kwargs))
    for key, value in self.__dict__.items():
      if isinstance(value, dict):
        self.__dict__[key] = self.__class__(**value)
  @classmethod
  def from_json_file(cls, filepath):
    with open(filepath) as json_file:
      values = json.loads(json_file.read())
      output = cls(**values)
    return output
  
  @classmethod
  def from_yaml_file(cls, filepath):
    with open(filepath) as yaml_file:
      values = yaml.load(yaml_file.read())
      output = cls(**values)
    return output

  @classmethod
  def from_json_str(cls, json_str):
    values = json.loads(json_str)
    output = cls(**values)
    return output

  @classmethod
  def from_dict(cls, dictionary):
    return cls(**dictionary)
  
  def to_json_str(self) -> str :
    return json.dumps(self.__dict__, indent=2)

  def to_json_file(self, filepath) -> None:
    with open(filepath, "w+") as output_file:
      json.dump(self.__dict__, output_file, indent=2)
    return

  def to_dict(self) -> dict:
    dict_copy = copy.deepcopy(self.__dict__)
    for key, value in dict_copy.items():
      if isinstance(value, self.__class__):
        dict_copy[key] = value.to_dict()
    return dict_copy

  def __str__(self):
    return str(self.to_dict())

if __name__ == "__main__":
  import __main__
  __main__.main()