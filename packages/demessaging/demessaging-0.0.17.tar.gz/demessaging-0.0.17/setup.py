import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
version = '0.0.17'

setup(
    name='demessaging',
    version=version,
    description='python module wrapper for the data analytics software framework DASF',
    long_description=README,
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    packages=['demessaging'],
    author='Daniel Eggert',
    author_email='eggi@gfz-potsdam.de',
    keywords=['dasf', 'digital-earth', 'pulsar', 'gfz', 'helmholtz', 'hzg', 'hgf', 'rcp'],
    url='https://git.geomar.de/digital-earth/dasf/dasf-messaging-python',
    download_url='https://git.geomar.de/digital-earth/dasf/dasf-messaging-python/-/archive/v'
                 + version + '/dasf-messaging-python-v' + version + '.tar.gz',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'websocket_client',
        'netcdf4',
        'xarray',
        'numpy',
        'deprogressapi'
    ],
    setup_requires=[
        'wheel'
    ]
)
