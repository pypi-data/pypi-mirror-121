from setuptools import setup

install_requires = list(val.strip() for val in open('requirements.txt'))
tests_require = list(val.strip() for val in open('test_requirements.txt'))

setup(name='ha-somecomfort',
      version='0.6.2',
      description='A client for Honeywell\'s US-based cloud devices',
      author='Jeremy Drost',
      author_email='jeremy@benchmark-creative.com',
      url='http://github.com/jad889nb/somecomfort',
      packages=['somecomfort'],
      entry_points={
          'console_scripts': [
              'somecomfort = somecomfort.__main__:main'
          ]
      },
      install_requires=install_requires,
      tests_require=tests_require,
)
