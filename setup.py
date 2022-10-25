from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import setuptools

setuptools.setup(
    name="tensorboard_plugin_example",
    version="0.1.0",
    description="Sample Tensorboard plugin.",
    packages=["tensorboard_plugin_example"],
    package_data={"tensorboard_plugin_example": ["static/**"],},
    entry_points={
        "tensorboard_plugins": [
            "example_basic = tensorboard_plugin_example.plugin:ExamplePlugin",
        ],
    },
)

