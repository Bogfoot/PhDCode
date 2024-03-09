from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension(
            name="Coinc_Counter",  # as it would be imported
            # may include packages/namespaces separated by `.`
            sources=[
                "Coinc_Counter.c"
            ],  # all sources are compiled into a single binary file
        ),
    ]
)
