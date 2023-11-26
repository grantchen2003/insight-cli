#!/bin/bash

cd ..

python -m unittest discover -s tests -p "test_*.py"

read -p "Press Enter to exit"
