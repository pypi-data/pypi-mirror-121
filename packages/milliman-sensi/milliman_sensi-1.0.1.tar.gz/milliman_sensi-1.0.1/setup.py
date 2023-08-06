from setuptools import setup


# specify requirements of your package here
REQUIREMENTS = ['pandas', 'objectpath']

# some more details
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    ]

# calling the setup function
setup(name='milliman_sensi',
      version='1.0.1',
      description='A parser and modifier of the configuration in Milliman-CHESS',
      long_description="""A parser and modifier of CHESS's configuration
Use it to get parse configuration from sensi_config.csv and sensi_param.csv and apply them to the new tables""",
      url='https://dev.azure.com/millimanparis/CHESS-Sensitivity-Manager',
      author='Quincy HSEIH',
      author_email='quincy.hsieh@milliman.com',
      license='MIT',
      packages=['milliman_sensi'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='parse apply configuration CHESS'
      )
