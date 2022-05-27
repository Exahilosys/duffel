import setuptools

with open('README.md') as file:
    readme = file.read()

name = 'duffel'

version = '3.4.3'

author = 'Exahilosys'

url = 'https://github.com/{0}/{1}'.format(author, name)

setuptools.setup(
    name = name,
    python_requires = '>=3.5',
    version = version,
    url = url,
    packages = setuptools.find_packages(),
    license = 'MIT',
    description = 'Minimal Python Api Wrapper for Duffel',
    long_description = readme
)
