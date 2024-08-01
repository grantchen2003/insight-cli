import setuptools
from insight_cli.config import config


def get_readme() -> str:
    with open("README.md", "r") as file:
        return file.read()


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
        long_description=get_readme(),
        long_description_content_type="text/markdown"
    )


if __name__ == "__main__":
    main()
