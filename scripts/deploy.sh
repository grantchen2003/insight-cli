#!/bin/bash

# automate deployment of insight-cli to PyPI

cd ..

python -m pip install setuptools wheel twine

directories=("build" "dist" "insight_cli.egg-info")

for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        rm -r "$dir"
        echo "Directory $dir removed."
    else
        echo "Directory $dir doesn't exist, skipping."
    fi
done

python setup.py sdist bdist_wheel

whl_file=$(find dist -type f -name "*.whl" -print -quit)

if [ -n "$whl_file" ]; then
    pip install "$whl_file" --force-reinstall
    echo "Installed $whl_file."
else
    echo "No .whl file found in the dist directory."
fi
