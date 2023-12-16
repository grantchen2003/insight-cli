import setuptools
from insight_cli.config import config


def main():
    setuptools.setup(
        name="insight-cli",
        version=config.INSIGHT_VERSION,
        packages=setuptools.find_packages(),
        entry_points={
            "console_scripts": ["insight = insight_cli:main"],
        },
        install_requires=[
            "colorama==0.4.6",
            "requests==2.31.0",
        ],
        python_requires=">=3.10.0",
    )


if __name__ == "__main__":
    main()
