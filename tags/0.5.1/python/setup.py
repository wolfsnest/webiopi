import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup, Extension, find_packages

classifiers = ['Development Status :: 3 - Alpha',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.6',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: Home Automation',
               'Topic :: System :: Hardware']

setup(name             = 'WebIOPi',
      version          = '0.5.1',
      author           = 'Eric PTAK',
      author_email     = 'trouch@trouch.com',
      description      = 'A package to control Raspberry Pi GPIO from the web',
      long_description = open('../doc/README').read(),
      license          = 'MIT',
      keywords         = 'RaspberryPi GPIO Python REST',
      url              = 'http://code.google.com/p/webiopi/',
      classifiers      = classifiers,
      py_modules       = ["webiopi"],
      ext_modules      = [Extension('_webiopi.GPIO', ['native/bridge.c', 'native/gpio.c', 'native/cpuinfo.c'])],
      )
