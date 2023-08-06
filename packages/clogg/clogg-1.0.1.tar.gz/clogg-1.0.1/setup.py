from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='clogg',
      version='1.0.1',
      description='A simple python module for fast and efficient logging',
      url='https://github.com/ChecksumDev/clogpy',
      author='ChecksumDev',
      author_email='collierdevs@tuta.io',
      license='GPLv3',
      long_description=long_description,
      long_description_content_type="text/markdown",
      package_dir={"": "src"},
      packages=find_packages(where="src"),
      zip_safe=False,
      python_requires=">=3.6")
