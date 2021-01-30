from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='packcircles',
    version='0.11',
    description='A pure Python implementation of a circle packing algorithm',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mhtchan/packcircles',
    author='mhtchan',
    author_email='mhtchan@outlook.com',
    license='MIT',
    packages=['packcircles'],
    install_requires=['pyllist >= 0.3'])
