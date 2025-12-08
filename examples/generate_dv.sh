#!/bin/bash
mkdir -p output
template-processor --verbosity info --dv ../data/deploymentview.dv.xml -o output -t dv.tmplt
pandoc --pdf-engine=pdfroff --output=output/dv.pdf output/dv.md