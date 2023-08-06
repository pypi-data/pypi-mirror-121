import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="secretserverpy",
    version="0.0.1",
    description="Package to interact and automate against Secret Server REST API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/realpython/reader",
    author="Shawn Melton",
    author_email="shawn.melton@thycotic.com",
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 1 - Planning',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        "Natural Language :: English",
        "Topic :: Security",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    packages=["secretserverpy"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
    },
)
