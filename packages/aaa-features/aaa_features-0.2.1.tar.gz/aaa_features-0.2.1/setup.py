'''
Created on Sep 30, 2021

@author: wacero
'''

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='aaa_features',  
     version='0.2.1',
     packages=['aaa_features'] ,
     author="Marielle Malfante",
     author_email="marielle.malfante@gmail.com",
     description="Python code to calculate signal features. This code was extracted from https://github.com/malfante/AAA",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/awacero/aaa_features",
     install_requires = ['obspy>=1.1.0','python-speech-features>=0.6','sympy>=1.8'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: CeCILL-B Free Software License Agreement (CECILL-B)",
         "Operating System :: OS Independent",
     ],
 )
