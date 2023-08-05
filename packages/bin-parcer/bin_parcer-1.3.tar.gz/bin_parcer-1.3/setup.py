from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(name='bin_parcer',
      version='1.3',
      description='a utility lib for parsing text bins',
      packages=['bin_parcer'],
      license='MPL-2.0 License',
      author = 'hiikion',
      long_description=long_description,
      url='https://github.com/hiikion/pastebinOmatic',
      install_requires=[ 
          'requests',
          'beautifulsoup4'
      ],
      zip_safe=False)
