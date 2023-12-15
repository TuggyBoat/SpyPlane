import io
import os
from pathlib import Path
from importlib import util

from setuptools import setup

NAMESPACE = 'ptn'
COMPONENT = 'spyplane'

here = Path().absolute()

# Bunch of things to allow us to dynamically load the metadata file in order to read the version number.
# This is really overkill but it is better code than opening, streaming and parsing the file ourselves.

metadata_name = f'{NAMESPACE}.{COMPONENT}._metadata'
spec = util.spec_from_file_location(metadata_name, os.path.join(here, NAMESPACE, COMPONENT, '_metadata.py'))
metadata = util.module_from_spec(spec)
spec.loader.exec_module(metadata)

# load up the description field
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=f'{NAMESPACE}.{COMPONENT}',
    version=metadata.__version__,
    packages=[
        'ptn.spyplane', # core
        'ptn.spyplane.botcommands', # user interactions
        'ptn.spyplane.database', # database
        'ptn.spyplane.modules', # modules for various functions
        'ptn.spyplane.classes'
        ],
    description='Pilots Trade Network Faction Support Bot',
    long_description=long_description,
    author='Thomas Kirtley',
    url='',
    install_requires=[
        'aiohttp==3.9.0',
        'aiosignal==1.3.1',
        'async-timeout==4.0.3',
        'attrs==23.1.0',
        'bidict==0.22.1',
        'cachetools==5.3.2',
        'certifi==2023.11.17',
        'charset-normalizer==3.3.2',
        'DateTime==4.3',
        'discord.py==2.3.2',
        'frozenlist==1.4.0',
        'google-auth==2.25.2',
        'google-auth-oauthlib==1.1.0',
        'gspread==5.12.2',
        'h11==0.14.0',
        'idna==3.4',
        'multidict==6.0.4',
        'numpy==1.26.2',
        'oauthlib==3.2.2',
        'pandas==2.1.4',
        'pyasn1==0.5.1',
        'pyasn1-modules==0.3.0',
        'python-dateutil==2.8.2',
        'python-dotenv==0.15.0',
        'python-engineio==4.8.0',
        'python-socketio==5.10.0',
        'pytz==2023.3.post1',
        'requests==2.31.0',
        'requests-oauthlib==1.3.1',
        'rsa==4.9',
        'simple-websocket==1.0.0',
        'six==1.16.0',
        'tzdata==2023.3',
        'urllib3==2.1.0',
        'wsproto==1.2.0',
        'yarl==1.9.3',
        'zope.interface==6.1'
    ],
    entry_points={
        'console_scripts': [
            'spyplane=ptn.spyplane.application:run',
        ],
    },
    license='None',
    keyword='PTN',
    project_urls={
        "Source": "https://github.com/PilotsTradeNetwork/spyplane",
    },
    python_required='>=3.9',
)
