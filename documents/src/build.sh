#!/bin/bash
# pip install jinja2 j2cli
set -e

for i in ./*.md
do :
    echo "Converting: ${i}"
    text=$(j2 $i --filters filters.py)
    echo "${text}" | pandoc -t markdown_strict --filter pandoc-citeproc --bibliography=bibliography.bib --csl=ieee.csl -o ../$i
done
