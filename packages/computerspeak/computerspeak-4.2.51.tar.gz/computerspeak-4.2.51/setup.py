from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "Readme.md").read_text()


setup(name='computerspeak',
    summary='This module helps the user make computer speak anything in a male or female voice',
    version='4.2.51',
    author='Pratyush Jha',
    author_email='pratyush.jha299@gmail.com',
    install_requires='pyttsx3',
    description='This Module Helps A User To Use Computer Audio To Make The Computer Speak AnyThing You Want',
    long_description = long_description,
    long_description_content_type='text/markdown',
    license="License.txt",
    packages=['speak']
)
