#!/bin/bash
[ -z "$1" ] && echo "ERROR: Pass in a png as argument" && exit 2

if [ -f "$1" ]
then
    echo "INFO: Running pngquant"
    pngquant --strip --speed 1 --nofs -v -o interim.png "$1"
    echo "INFO: Running pngcrush"
    pngcrush -brute -reduce interim.png "optim-$1"
    rm interim.png
else
    echo "ERROR: Not file"
fi
