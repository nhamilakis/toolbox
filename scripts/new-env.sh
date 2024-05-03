#!/bin/bash

echo "$(pip -V)"
echo "updating pip"
pip install --upgrade pip

echo "adding basic stuff"
pip install ipython
pip install rich
pip install pytest