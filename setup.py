from setuptools import setup

setup(
    name="in-memory-db",
    version="0.1",
    py_modules=["memdb"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        db=memdb:cli
    """,
)