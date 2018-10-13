import json, yaml

class obj(object):

  native_types = (str, int, float, type(None))
  array_types = (list, tuple)

  def __init__(self, *args, **kwargs):
    if len(args) > 0:
      raise ValueError("Bare arrays cannot be entered into the object.")
    self.__dict__ = dict()
    if isinstance(kwargs, dict):
      self.__dict__.update(kwargs)
    for key, value in self.__dict__.items():
      if isinstance(value, dict):
        self.__dict__[key] = self.from_dict(value)
      if isinstance(value, self.array_types):
        self.__dict__[key] = self.from_array(value)
      
  @classmethod
  def from_json_file(cls, filepath):
    """
    Returns a obj created from JSON-formatted file.
    """
    with open(filepath) as json_file:
      values = json.loads(json_file.read())
      output = cls.from_dict_or_array(values)
    return output
  
  @classmethod
  def from_yaml_file(cls, filepath):
    """
    Returns a obj created from YAML-formatted file.
    """
    with open(filepath) as yaml_file:
      values = yaml.safe_load(yaml_file)
      output = cls.from_dict_or_array(values)
    return output

  @classmethod
  def from_json_str(cls, json_str):
    """
    Returns a obj created from JSON-formatted string.
    """
    values = json.loads(json_str)
    output = cls.from_dict_or_array(values)
    return output

  @classmethod
  def from_dict(cls, dictionary):
    """
    Returns an array of obj from a python dict object.
    """
    if isinstance(dictionary, dict):
      return cls(**dictionary)
    else:
      raise ValueError("obj.from_dict() called with non-dict object: {0}.".format(dictionary.__class__))
  
  @classmethod
  def from_array(cls, array):
    """
    Returns an array of obj/native type from an list or a tuple
    """
    if isinstance(array, cls.array_types):
      items = list()
      for item in array:
        items.append(cls.from_generic_value(item))
      return items
    else:
      raise ValueError("obj.from_array() called with non-array object: {0}.".format(array.__class__))

  @classmethod
  def from_generic_value(cls, value, strict_mode = False):
    """
    Returns a obj/native type from any Python object that either 
    1) is a native type, 
    2) is a dict or list, or
    3) has a __dict__ value defined.
    """
    if isinstance(value, cls.native_types):
      return value
    elif isinstance(value, (dict, *cls.array_types)):
      return cls.from_dict_or_array(value)
    elif strict_mode:
      if hasattr(value, "__dict__"):
        return cls.from_dict(value.__dict__)
      else:
        raise ValueError("Unknown value type in `from_generic_value(...): {0} : {1}`.".format(value.__class__, str(value)))
    else:
      return value

  @classmethod
  def from_dict_or_array(cls, obj):
    """
    Returns a obj or list of obj/native types from a Python dict or list object
    """
    if isinstance(obj, dict):
      return cls.from_dict(obj)
    elif isinstance(obj, cls.array_types):
      return cls.from_array(obj)
    else:
      raise ValueError("Unknown value type in `from_dict_or_array(...): {0} : {1}`.".format(obj.__class__, str(obj)))
  
  def to_json_str(self) -> str :
    """
    Returns a JSON-formatted string with the data from the obj
    """
    return json.dumps(self.to_dict(), indent=2)

  def to_json_file(self, filepath) -> None:
    """
    Writes a JSON-formatted at `filepath` with the data from the obj
    """
    with open(filepath, "w+") as output_file:
      json.dump(self.to_dict(), output_file, indent=2)
    return

  def to_yaml_file(self, filepath) -> None:
    """
    Writes a YAML-formatted at `filepath` with the data from the obj
    """
    with open(filepath, "w+") as output_file:
      yaml.dump(self.to_dict(), output_file)
    return

  def to_dict(self, root = None, safe_mode = True) -> dict:
    """
    Returns a dict with the data from the obj
    """
    dict_copy = self.__dict__.copy()
    if root is None:
      root = [self]
    else:
      if safe_mode:
        root.append(self)
    try:
      for key, value in dict_copy.items():
        if isinstance(value, self.__class__) and value not in root:
          dict_copy[key] = value.to_dict(root = root)
        elif isinstance(value, self.array_types):
          dict_copy[key] = self.array_to_array_dict(value)
    except RecursionError:
      pass
    return dict_copy

  def __str__(self):
    return str(self.to_dict())

  @classmethod
  def array_to_array_dict(cls, array):
    if not isinstance(array, cls.array_types):
      raise TypeError("This method ")
    output = list()
    for item in array:
      if isinstance(item, cls):
        output.append(item.to_dict())
      elif isinstance(item, cls.array_types):
        output.append(cls.array_to_array_dict(item))
      else:
        output.append(item)
    return output

  @classmethod
  def toString(cls, obj):
    """Returns a string object describing the object or class, as a dict/list combo"""
    if isinstance(obj, cls):
      return str(obj.to_dict())
    if isinstance(obj, cls.array_types):
      output = list()
      for item in obj:
        output.append(cls.toString(item))
      return str(output)
    raise TypeError("obj.toString called on non-array, non-obj object: {0} :: {1} ".format(type(obj), str(obj)))
  
  def extend(self, other):
    """Extends self with properties from other (dict or obj)"""
    if isinstance(other, type(self)):
      for key, value in other.__dict__.values():
        self.__dict__[key] = value
    elif isinstance(other, dict):
      for key, value in other.values():
        self.__dict__[key] = self.from_generic_value(value)
    else:
      raise TypeError("obj.extend called on non-dict, non-obj object : {0} :: {1} ".format(type(other), str(other)))

  def __getattr__(self, name):
    try:
      return self.__dict__[name]
    except KeyError:
      return None
  
  def __setattr__(self, name, value):
    if name == "__dict__": # have to protect the family jewels
      if isinstance(value, dict):
        object.__setattr__(self, name, value)
      else:
        raise TypeError("Cannot assign non-dict value to obj.__dict__")
    elif isinstance(value, dict):
      self.__dict__[name] = type(self).from_dict(value)
    else:
      self.__dict__[name] = value
  
  def __getitem__(self, name):
    try:
      return self.__dict__[name]
    except KeyError:
      return None

if __name__ == "__main__":
  import __main__
  __main__.main()