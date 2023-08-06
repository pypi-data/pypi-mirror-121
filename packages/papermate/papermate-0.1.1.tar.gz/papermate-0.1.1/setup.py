import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name='papermate',
    version='0.1.1',
    description="A Python package to help researchers and academics write papers using Markdown",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MartinHeroux/papermate",
    author="Martin Héroux",
    author_email="heroux.martin@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    packages=['papermate'],
    entry_points={'console_scripts' : ['papermate = papermate.papermate:main']}
    )

