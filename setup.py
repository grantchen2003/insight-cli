from setuptools import setup, find_packages

setup(
    name="insight-cli",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "certifi==2023.11.17",
        "charset-normalizer==3.3.2",
        "idna==3.4",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "urllib3==2.1.0",
    ],
    entry_points={
        "console_scripts": ["insight = src:insight_cli"],
    },
)
