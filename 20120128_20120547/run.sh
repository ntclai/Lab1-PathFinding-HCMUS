#!/bin/sh
sudo apt-get install python3-pygame
sudo apt-get install python3-opencv

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

cd "$parent_path"

cd source

python3 main.py
