import inspect


class Handler:
    @staticmethod
    def _raise_for_invalid_params(params):
        if not isinstance(params, list):
            raise TypeError("params must be a list")

        for param in params:
            if "type" not in param:
                raise KeyError("type key required")

            if "name" not in param:
                raise KeyError("name key required")

    @staticmethod
    def _raise_for_invalid_function(function):
        if not inspect.isfunction(function):
            raise TypeError("function must be a function")

    @staticmethod
    def _raise_for_params_function_mismatch(params, function):
        if len(params) != len(inspect.signature(function).parameters):
            raise ValueError(
                "The number of params don't match the number of function parameters"
            )

    def __init__(self, params, function):
        Handler._raise_for_invalid_params(params)
        Handler._raise_for_invalid_function(function)
        Handler._raise_for_params_function_mismatch(params, function)

        self._params = params
        self._function = function

    def __call__(self, *args, **kwargs):
        return self._function(*args, **kwargs)

    @property
    def has_params(self) -> bool:
        return len(self._params) != 0

    @property
    def num_params(self) -> int:
        return len(self._params)

    @property
    def params(self) -> list[dict]:
        return self._params.copy()

    @property
    def param_names(self):
        return [param["name"] for param in self._params]

    @property
    def param_types(self):
        return [param["type"] for param in self._params]
