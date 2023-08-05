# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dolus']
install_requires = \
['click-help-colors>=0.9.1,<0.10.0',
 'click>=8.0.1,<9.0.0',
 'numpy>=1.21.2,<2.0.0',
 'opencv-python>=4.5.3,<5.0.0',
 'pafy>=0.5.5,<0.6.0',
 'pyvirtualcam>=0.8.0,<0.9.0',
 'requests>=2.26.0,<3.0.0',
 'youtube_dl>=2021.6.6,<2022.0.0']

entry_points = \
{'console_scripts': ['dolus = dolus:main']}

setup_kwargs = {
    'name': 'dolus',
    'version': '0.1.1',
    'description': 'A command-line interface to put effects on your virtual camera(OBS/Unity/v4l2loopback)',
    'long_description': '# dolus\nA command-line interface to put effects on your virtual camera(OBS/Unity/v4l2loopback)\n\n\n\n# Prerequisites\n\n## Windows/MacOS\n\nPython 3.7 or higher \n\nOBS 26 or Higher\n\n## Linux \n\nPython 3.7 or higher \n\nv4l2loopback\n\n# Installation\n\n## Windows\n\n```pip install dolus```\n\n## Mac/Linux\n\n```pip3 install dolus```\n\n\n# Usage\n\nType dolus in the terminal/powershell\n\nIt should look like this:-\n\n![image](https://user-images.githubusercontent.com/77975448/134615846-797d222f-7c60-4c33-bacc-1b65d7f35f6d.png)\n\nThen type dolus effectname\n\n![image](https://user-images.githubusercontent.com/77975448/134615915-c10c3e4c-26a8-48f9-bd9e-2fadbc5e0fab.png)\n\nThe ytvid function takes an argument for youtube video in a string\n\n![image](https://user-images.githubusercontent.com/77975448/134616051-01e0a458-d9b2-43a6-9cd0-60388e5a1c7f.png)\n\nTo use it in video calling platforms, change your camera to the virual camera, which is OBS Virtual camera in my case\n\n![image](https://user-images.githubusercontent.com/77975448/134616113-29d7197c-73d4-401d-a35d-d6a2c6cd81dd.png)\n\n\n\n\n',
    'author': 'Avanindra Chakraborty',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AvanindraC/dolus',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
