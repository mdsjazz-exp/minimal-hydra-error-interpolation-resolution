"""
This is an example where Hydra fails to run when dictionary interpolation works on a resolved value
which does not return an allowed primitive type. However the issue would be solved if not for a copy-config-set-flag
routine at the beginning of hydra.utils.instantiate. See below for an example.
"""

from typing import Optional

import hydra
from omegaconf import DictConfig, OmegaConf

def resolve_tuple(*args):
    return tuple(args)

if not OmegaConf.has_resolver("as_tuple"):
    OmegaConf.register_new_resolver("as_tuple", resolve_tuple)


class TestClassLevel1:
    """A test class which may successfully instantiate if not for multiple interpolations of the my_values config"""
    def __init__(self, test_class_level_2: Optional[DictConfig] = None, my_values: Optional[DictConfig] = None):
        self.my_values = my_values
        self.test_class_level_2 = hydra.utils.instantiate(test_class_level_2)

    def __repr__(self) -> None:
        return f"""\n    Test Class Level 1:
            {self.my_values=},

            {self.test_class_level_2},
        """


class TestClassLevel2:
    """A test class which may successfully instantiate if not for multiple interpolations of the my_values config"""
    def __init__(self, my_values: Optional[DictConfig] = None):
        self.my_values = my_values

    def __repr__(self) -> None:
        return f"""\n    Test Class Level 2:
            {self.my_values=},
        
        """

def instantiate_and_print(config: DictConfig) -> None:
    my_test_class = hydra.utils.instantiate(config.test_class_level_1, _recursive_=False)
    print(my_test_class)


@hydra.main(config_path="configs", config_name="config.yaml")
def main(config: DictConfig):
    try:
        instantiate_and_print(config)
    except Exception as e:
        print(e)

    config._set_flag(flags="allow_objects", values=True)

    instantiate_and_print(config)


if __name__ == "__main__":
    main()  # pylint: disable=No value for argument 'config' in function call (no-value-for-parameter)
