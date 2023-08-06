from setuptools import setup, find_packages

__VERSION = '1.0.0'

setup(name='log.client',
      version=__VERSION,
      description='log library for python',
      author='dugangandy@qq.com',
      packages=find_packages(),
      license='MIT',
      tests_require=['unittest2'],
      install_requires=['requests>=2.3.0'],
      classifiers=['Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'License :: OSI Approved :: MIT License'],
      url='https://github.com/dugangandy/log-client-python.git',
      )
