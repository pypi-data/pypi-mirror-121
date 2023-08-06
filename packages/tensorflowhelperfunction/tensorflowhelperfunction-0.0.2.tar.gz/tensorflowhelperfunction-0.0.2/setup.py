from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='tensorflowhelperfunction',
  version='0.0.2',
  description='helper function used in tensorflow',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='abbas kareem',
  author_email='kareemabbas106@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='helperfunctions', 
  packages=find_packages(),
  install_requires=[''] 
)