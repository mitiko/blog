#!/usr/bin/bash

echo 'You just got hacked!'

for i in 'Stealing cookies...' 'Fornicating with your mother...' 'Mining crypto...' 'Downloading pictures of kittens...'; do
    echo -e '\n<div>' >> index.md
    curl -s http://metaphorpsum.com/sentences/4 >> index.md
    echo -e '\n</div>' >> index.md
    echo $i
done
