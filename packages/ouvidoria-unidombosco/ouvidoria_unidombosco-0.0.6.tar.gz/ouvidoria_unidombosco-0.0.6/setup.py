from distutils.core import setup
import os

OS_SEPARATOR = os.path.sep

version = '0.0.6'
name = 'ouvidoria_unidombosco'
url = f'https://github.com/SamuelJansen/{name}/'

setup(
    name = name,
    packages = [
        name,
        f'{name}{OS_SEPARATOR}api',
        f'{name}{OS_SEPARATOR}api{OS_SEPARATOR}resource',
        f'{name}{OS_SEPARATOR}api{OS_SEPARATOR}src',
    ],
    package_data = {
        '': ['*.yml']
    },
    version = version,
    license = 'MIT',
    description = 'Unidombosco ouvidoria package',
    author = 'Samuel Jansen',
    author_email = 'samuel.jansenn@gmail.com',
    url = url,
    download_url = f'{url}archive/v{version}.tar.gz',
    keywords = ['goodbye indiference'],
    install_requires = [
        'globals<=0.3.4',
        'selenium==3.141.0',
        'webdriver_manager==3.2.1'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9'
    ]
)
