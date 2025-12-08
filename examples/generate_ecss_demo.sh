#!/bin/bash
mkdir -p output
template-processor --verbosity info --iv ../data/requirements.iv.xml -o output -t ../data/ecss-template/ecss-e-st-40c_6_requirement_traceability.tmplt
pandoc --pdf-engine=pdfroff --output=output/ecss-e-st-40c_6_requirement_traceability.pdf output/ecss-e-st-40c_6_requirement_traceability.md
