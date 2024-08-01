#!/bin/bash

# run insight-cli unittests

cd ..

python -m unittest discover -s tests -p "test_*.py"
