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

pip install dist/insight_cli-0.0.0-py3-none-any.whl --force-reinstall

read -p "Press Enter to exit"
