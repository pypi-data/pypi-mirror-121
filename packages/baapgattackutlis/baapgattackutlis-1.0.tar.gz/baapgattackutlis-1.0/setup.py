from setuptools import setup, find_packages
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='baapgattackutlis',
  version='1.0',
  description='Fuck you',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ansh Dadwal',
  author_email='anshdadwal298@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='utlis', 
  packages=find_packages(),
  install_requires=['requests','tqdm'] 
)
