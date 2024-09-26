from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension(
            name="Single_Threaded_Coincidence_Finder",  # as it would be imported
            # may include packages/namespaces separated by `.`
            sources=[
                "./src/FindCoincidences.cpp"
            ],  # all sources are compiled into a single binary file
        ),
    ]
)
