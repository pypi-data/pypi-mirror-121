class dotdict(dict):
    """dot notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, d):
        for k, v in d.items():
            if isinstance(v, dict):
                d[k] = dotdict(v)
        super().__init__(d)
