#!/bin/bash
mkdir -p output
template-processor --verbosity info --iv ../data/requirements.iv.xml -o output -t requirements.tmplt
pandoc --pdf-engine=pdfroff --output=output/requirements.pdf output/requirements.md