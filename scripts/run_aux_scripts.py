#!/usr/bin/python3
import os

curr_dir = os.getcwd()
for root, _, files in os.walk("content"):
    for name in files:
        if name == "script.py":
            os.chdir(root)
            print("Executing script", root, name)
            exec(open(name).read()) # very unsafe, proceed with caution
            os.chdir(curr_dir)
