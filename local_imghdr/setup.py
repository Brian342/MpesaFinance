from setuptools import setup

setup(
    name="imghdr-fix",
    version="0.0.1",
    py_modules=["imghdr"],
    description="Small imghdr shim to provide imghdr.what for environments missing stdlib imghdr",
)
