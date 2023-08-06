from pathlib import Path
from setuptools import setup, find_packages

# The directory containing this file
HERE = Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='jsonclasses-orm',
      version='2.8.1',
      description='Definitions for JSONClasses ORM integration implementation.',
      long_description=README,
      long_description_content_type="text/markdown",
      author='Fillmula Inc.',
      author_email='victor.teo@fillmula.com',
      license='MIT',
      packages=find_packages(exclude=("tests")),
      package_data={'jsonclasses_orm': ['py.typed']},
      zip_safe=False,
      url='https://github.com/fillmula/jsonclasses-orm',
      include_package_data=True,
      python_requires='>=3.9',
      install_requires=['qsparser>=1.0.1,<2.0.0'])
