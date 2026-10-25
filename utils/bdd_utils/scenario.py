import inspect
import os

import pytest_bdd


def scenario(scenario_name):
    def scenario_wrap(func):
        module = inspect.getmodule(func)
        if module is None or not hasattr(module, "__file__"):
            raise RuntimeError("Cannot determine the module file for the test function.")
        module_path = os.path.abspath(module.__file__)
        feature_path = module_path.replace("steps_def", "features").replace("_test.py", ".feature")
        if not os.path.exists(feature_path):
            raise FileNotFoundError(f"Feature file not found: {feature_path}")
        scenario_func = pytest_bdd.scenario(feature_path, scenario_name)(func)
        return scenario_func

    return scenario_wrap
