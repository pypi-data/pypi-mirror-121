import setuptools
reqs = ['requests>=2.26.0',
        'termcolor']
version = '2.0'

setuptools.setup(
    name='utils-S',
    version=version,
    author="Sal Faris",
    description="Utility functions",
    packages=setuptools.find_packages(),
    license='MIT',
    author_email='salmanfaris2005@hotmail.com',
    url='https://github.com/The-Sal/utils/',
    download_url='https://github.com/The-Sal/utils/archive/refs/tags/v{}.tar.gz'.format(version),
    install_requires=reqs
)