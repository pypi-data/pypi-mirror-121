from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name='fastluks',
    version='0.0.3',
    description='LUKS storage encryption.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['fastluks'],
    url='https://github.com/dacolombo/fast-luks-py',
    author='Daniele Colombo',
    author_email='daniele.colombo39@gmail.com',
    license='',
    install_requires = [
        'zc.lockfile',
        'requests',
        'urllib3',
    ]
)
