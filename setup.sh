#!/bin/bash

# if you don't have pip3, then use whatever pip for your install of python 3.5+
pip3 install virtualenv
virtualenv
source bin/activate

# install requirements
pip install -r requirements.txt