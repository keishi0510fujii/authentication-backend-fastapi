class AttrDict(dict):
    """Dict that can get attribute by dot, and doesn't raise KeyError"""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return None
