""" 
python setup.py sdist bdist_wheel

twine upload dist/*
"""

from setuptools import setup


# move setup to other files for security issues
if __name__ == "__main__":
    setup()
