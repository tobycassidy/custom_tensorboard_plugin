package(default_visibility = ["//tensorboard:internal"])

licenses(["notice"])

sh_test(
    name = "smoke_test",
    size = "large",
    timeout = "moderate",
    srcs = ["smoke_test.sh"],
    # Don't just `glob(["**"])` because `setup.py` creates artifacts
    # like wheels and a `tensorboard_plugin_example.egg-info` directory,
    # and we want to make sure that those don't interfere with the test.
    data = [
        "setup.py",
        "//tensorboard/pip_package",
    ] + glob([
        "tensorboard_plugin_example/*.py",
        "tensorboard_plugin_example/static/**",
    ]),
    tags = [
        "manual",  # https://github.com/tensorflow/tensorboard/issues/2987
    ],
)