from setuptools import setup, find_packages

setup(
    name='geolib',
    version='0.0.1',
    description='geo lib',
    url='https://github.com/ivanpastukhov/geof.git',
    author='Ivan Pastukhov',
    author_email='ivanpastukhoff@gmail.com',
    license='unlicense',
    packages=['geolib', 'geolib.features', 'geolib.vizualization', 'geolib.tools'],
    zip_safe=False
)