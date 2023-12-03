import setuptools
from insight_cli.config import config


setuptools.setup(
    name="insight-cli",
    version=config.INSIGHT_VERSION,
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["insight = insight_cli:main"],
    },
    install_requires=[
        "pip>=23.3.1",
        "requests==2.31.0",
    ],
    python_requires=">=3.12.0",
)
