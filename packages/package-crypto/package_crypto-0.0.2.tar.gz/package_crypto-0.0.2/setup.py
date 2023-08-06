from setuptools import setup, find_packages
 
setup(
  name='package_crypto',
  version='0.0.2',
  description='This package is for getting all the paragraphs related to specific cryptocurrencies',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Taukenov Assylken',
  author_email='asylken02@gmail.com',
  license='MIT', 
  keywords='crypto parsing', 
  packages=find_packages(include=['package_crypto', 'package_crypto.*']),
  install_requires=["beautifulsoup4 == 4.10.0", "requests == 2.26.0"] 
)