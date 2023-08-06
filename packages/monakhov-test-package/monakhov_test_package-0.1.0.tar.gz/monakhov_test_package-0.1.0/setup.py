from setuptools import setup

setup(
    name='monakhov_test_package',
    version='0.1.0',
    description='A example Python package',
    author='Daniil Monakhov',
    author_email='d.monakhov1@gmail.com',
    packages=['monakhov_test_package'],
    install_requires=['numpy',
                      'typing'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)