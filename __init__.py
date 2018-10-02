import json
import yaml
import copy
import pprint

class CFGObj:

  def __init__(self, *args, **kwargs):
    if len(args) > 0:
      raise ValueError("Bare arrays cannot be entered into the CFGObject.")
    self.__dict__ = dict()
    if isinstance(kwargs, dict):
      self.__dict__.update(copy.deepcopy(kwargs))
    for key, value in self.__dict__.items():
      if isinstance(value, dict):
        self.__dict__[key] = self.__class__.from_dict(value)
      if isinstance(value, list):
        self.__dict__[key] = self.__class__.from_array(value)
      
  @classmethod
  def from_json_file(cls, filepath):
    with open(filepath) as json_file:
      values = json.loads(json_file.read())
      output = cls.from_dict_or_array(values)
    return output
  
  @classmethod
  def from_yaml_file(cls, filepath):
    with open(filepath) as yaml_file:
      values = yaml.load(yaml_file.read())
      output = cls.from_dict_or_array(values)
    return output

  @classmethod
  def from_json_str(cls, json_str):
    values = json.loads(json_str)
    output = cls.from_dict_or_array(values)
    return output

  @classmethod
  def from_dict(cls, dictionary):
    if isinstance(dictionary, dict):
      return cls(**dictionary)
    else:
      raise ValueError("CFGObj.from_dict() called with non-dict object.")
  
  @classmethod
  def from_array(cls, array):
    if isinstance(array, list) or isinstance(array, tuple):
      items = list()
      for item in array:
        items.append(cls.from_generic_value(item))
      return items
    else:
      raise ValueError("CFGObj.from_array() called with non-dict object.")

  @classmethod
  def from_generic_value(cls, value):
    if value.__class__ in (int, float, str):
      return value
    elif value.__class__ in (dict, list, tuple):
      return cls.from_dict_or_array(value)
    elif hasattr(value, "__dict__"):
      return cls.from_dict(value.__dict__)
    else:
      raise ValueError("Unknown value in `from_generic_value(...): {0} : {1}`. How did you get here?".format(str(value), value.__class__))

  @classmethod
  def from_dict_or_array(cls, obj):
    if isinstance(obj, dict):
      return cls.from_dict(obj)
    elif isinstance(obj, list) or isinstance(obj, tuple):
      return cls.from_array(obj)
    else: # if it's non-iterable, just extract values from its __dict__
      raise ValueError("Unknown value in `from_dict_or_array(...): {0} : {1}` How did you get here?".format(str(obj), obj.__class__))
  
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