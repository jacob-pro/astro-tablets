#!/bin/bash
for i in ./*.md
do :
    pandoc -t markdown_strict --filter pandoc-citeproc --bibliography=bibliography.bib --csl=ieee.csl -o ../$i $i
done
