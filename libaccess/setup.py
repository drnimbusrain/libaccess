from setuptools import setup

setup(name='libaccess',
      version='1.0',
      description='python plotting library for ACCESS modeling system',
      url='https://github.com/rdsaylor-noaa/libaccess',
      author='Rick Saylor',
      author_email='rdsaylor@gmail.com',
      packages=['libaccess'],
      install_requires=[
          'seaborn',
          'matplotlib',
          'numpy',
          'datetime',
      ],
      zip_safe=False)   

