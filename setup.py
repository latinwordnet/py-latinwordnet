from setuptools import setup, find_packages


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

requirements = [
    'requests>=2.22.0',
]


setup(
    name='latinwordnet',
    version='0.1.3',
    packages=find_packages(),
    url='https://latinwordnet.exeter.ac.uk',
    license='GNU General Public License v3.0',
    author='William Michael Short',
    author_email='w.short@exeter.ac.uk',
    description='A light-weight Python wrapper for the Latin WordNet 2.0 API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    test_suite='tests'
)
