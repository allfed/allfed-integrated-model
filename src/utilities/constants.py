class ScenarioConstants:
    def __init__(self):
        self._consts = {}

    def define(self, name, value):
        if name in self._consts:
            raise ValueError(f"Constant '{name}' is already defined.")
        self._consts[name] = value

    def __getattr__(self, name):
        if name in self._consts:
            return self._consts[name]
        raise AttributeError(f"Constant '{name}' is not defined.")


class FixedConstants:
    def __init__(self):
        self._consts = {}

    def define(self, name, value):
        if name in self._consts:
            raise ValueError(f"Constant '{name}' is already defined.")
        self._consts[name] = value

    def __getattr__(self, name):
        if name in self._consts:
            return self._consts[name]
        raise AttributeError(f"Constant '{name}' is not defined.")


class MonthlyConstants:
    def __init__(self):
        self._consts = {}

    def define(self, name, value):
        if name in self._consts:
            raise ValueError(f"Monthly constant '{name}' is already defined.")
        self._consts[name] = value

    def __getattr__(self, name):
        if name in self._consts:
            return self._consts[name]
        raise AttributeError(f"Monthly constant '{name}' is not defined.")
