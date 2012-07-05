import json
json.encoder.FLOAT_REPR = lambda o: format(o, '.25g')

class Serializable(object):
    """An object that can be serialized to a JSON file"""

    def dict(self):
        """Serialize object to dictionary

        Should be overridden by derived classes
        """
        return {}

    @classmethod
    def from_dict(cls, j, **kwargs):
        """Deserialize object from dictionary

        Should be overridden by derived classes
        """
        return cls()

    def dump(self, fp):
        """Serialize object to file

        :param fp: A .write()-supporting file-like object
        """
        return json.dump(self.dict(), fp, indent=2)

    @classmethod
    def load(cls, fp):
        """Deserialize object from file

        :param fp: A .read()-supporting file-like object
        """
        return cls.from_dict(json.load(fp))

    def dumps(self):
        """Serialize object to string

        :param fp: A .write()-supporting file-like object
        """
        return json.dumps(self.dict(), indent=2)

    @classmethod
    def loads(cls, s):
        """Deserialize object from string

        :param str s: string encoding the object
        """
        return cls.from_dict(json.loads(s))


def py_to_dict(d):
    return {k: v.dict() for k, v in d.items()}

def dict_to_py(cls, j, **kwargs):
    return {str(k): cls.from_dict(v, **kwargs) for k, v in j.items()}
