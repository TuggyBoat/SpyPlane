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
    description='PTN Faction Spy Plane',
    long_description=long_description,
    author='PTN Time Wasting Team',
    url='',
    install_requires=[
        'discord@git+https://github.com/Rapptz/discord.py#334ef1d7facce9dbfba2a6924bf57fc59bc827b5',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'spyplane=ptn.spyplane.spy:run',
        ],
    },
    keyword='PTN',
    project_urls={
        "Source": "https://github.com/PilotsTradeNetwork/SpyPlane",
    },
    python_required='>=3.9',
)
