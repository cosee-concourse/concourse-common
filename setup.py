from setuptools import setup

setup(name='concourse_common',
      version='0.3.0',
      description='Common utitilies for concourse resources',
      url='https://github.com/cosee-concourse/concourse-common.git',
      author='cosee',
      license='MIT',
      packages=['concourse_common'],
      zip_safe=False, install_requires=['jsonschema'])