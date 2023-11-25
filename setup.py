import setuptools, yaml


with open("insight.yaml", "r") as file:
    config = yaml.safe_load(file)


setuptools.setup(
    name="insight-cli",
    version=config["version"],
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["insight = src:insight_cli"]},
    install_requires=[
        "requests==2.31.0",
        "PyYAML==6.0.1",
    ],
)
