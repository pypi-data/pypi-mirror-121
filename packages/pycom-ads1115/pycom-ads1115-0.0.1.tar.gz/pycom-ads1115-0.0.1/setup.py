import setuptools
from distutils.core import setup

with open('README.md', 'r') as f:
    long_description = f.read()

pkg_info = {}
with open('src/ADS1115/_version.py', 'r') as f:
    exec(f.read(), pkg_info)

setup(
    name="pycom-ads1115",
    version=pkg_info['__version__'],
    description="Pycom ADS1115 library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="snebot",
    author_email="snebot@bitgrup.com",
    url="https://github.com/snebot-bg/pycom-ads1115",
    keywords=[],
    classifiers=[],
    package_dir={ "": "src" },
    packages=setuptools.find_packages(where="src")
)
