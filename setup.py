
from setuptools import setup, find_packages

setup(
    name="spider-ctf",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-magic",
    ],
    entry_points={
        'console_scripts': [
            'spider=spider.cli.spider:main',
        ],
    },
)
