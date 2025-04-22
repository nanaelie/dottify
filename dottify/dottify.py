class Dottify:
    def __init__(self, dic:dict):
        super(Dottify, self).__init__()
        for key, value in dic.items():
            if isinstance(value, dict):
                setattr(self, key, Dottify(value))
            else:
                setattr(self, key, value)
                
    def __repr__(self):
        return self.to_dict().__repr__()
        
    def to_dict(self):
        res = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Dottify):
                res[key] = value.to_dict()
            else:
                res[key] = value
        return res
