from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='GreekRomanUtils',
  version='1.0.0',
  author='PKALab',
  author_email='kpalab@pkotlyarov.ru',
  description='The module converts Arabic numerals to Greek and Roman numbers',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/PavelKotDRM/GreekRomanNumerical',
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: Apache Software License'
  ],
  keywords='python,greek,roman',
  project_urls={
    'Documentation': 'https://github.com/PavelKotDRM/GreekRomanNumerical'
  },
  python_requires='>=3.7'
)