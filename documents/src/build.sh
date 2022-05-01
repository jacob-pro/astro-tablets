#!/bin/bash

for i in ./*.md
do :
    echo "Converting: ${i}"
    pandoc -t markdown_strict --filter pandoc-citeproc --bibliography=bibliography.bib --csl=ieee.csl -o ../$i $i
done
