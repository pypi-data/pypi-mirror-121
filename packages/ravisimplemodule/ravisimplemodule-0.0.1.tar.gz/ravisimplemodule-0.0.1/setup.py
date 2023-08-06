# from setuptools import setup ,find_packages

# classifiers=[
#     'Development Status :: 5 - Production/Stable',
#     'Intended Audience :: Education',
#     'Operating System :: Ubuntu :: Linux ::Microsoft::window ',
#     'license :: MIT License',
#     'Programming Language :: Python :: 3 '
# ]

# setup(
#     name='test-module',
#     version='0.0.1',
#     description="Short summary of modules",
#     Long_description=open("README.txt").read()+'\n\n'+open('CHANGELOG.txt').read(),
#     url='',
#     author='Ravi Sharma',
#     author_email='ravikr845430@gmail.com',
#     License='MIT',
#     classifiers=classifiers,
#     keywords='',
#     packages=find_packages(),
#     install_requires=['']
# )



from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.7'
]

setup(
  name='ravisimplemodule',
  version='0.0.1',
  description='A very basic calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Ravi Sharma',
  author_email='ravikr845430@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='calculator',
  packages=find_packages(),
  install_requires=['']
)