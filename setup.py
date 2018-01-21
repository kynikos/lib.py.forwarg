from setuptools import setup

setup(
    name='forwarg',
    version='1.0.0',
    description=('Parse and forward command-line arguments.'),
    long_description=("Drop-in replacement for Python's argparse module, used "
                      "to parse command-line arguments. forwarg is designed "
                      "to make it easier to forward the arguments to another "
                      "command, allowing to manipulate them through special "
                      "objects. forwarg implements the same API as argparse, "
                      "but it has been written from scratch."),
    url='https://github.com/kynikos/lib.py.forwarg',
    author='Dario Giovannetti',
    author_email='dev@dariogiovannetti.net',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: System :: Shells',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # noqa
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='commandline parser',
    py_modules=["forwarg"],
)
