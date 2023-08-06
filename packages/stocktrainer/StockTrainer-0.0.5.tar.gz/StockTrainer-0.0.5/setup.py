from setuptools import setup, find_packages
import os
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.5'
DESCRIPTION = 'Stock environment for training machine learning agents'

# Setting up
setup(
    name="StockTrainer",
    version=VERSION,
    author="Daniel Prakah-Asante",
    author_email="doprakah@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
     keywords = ['USEFULL', 'STOCKS','MACHINE LEARNING', 'AI', 'ARTIFICAL INTELLIGENCE' ],   
  install_requires=[           
          'pandas',
          'numpy',
          'datetime',
          'pandas_datareader'
      ],
        classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',    
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ]
)
