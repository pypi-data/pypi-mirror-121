from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='lyrah_classinstance',
  version='0.0.1',
  description='A class instance',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Yorushika Lyrah',
  author_email='lyrahprivacy@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Class', 
  packages=find_packages(),
  install_requires=[''] 
)