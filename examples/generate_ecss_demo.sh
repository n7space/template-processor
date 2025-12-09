#!/bin/bash
mkdir -p output
template-processor --verbosity info --iv demo-project/interfaceview.xml --dv demo-project/deploymentview.dv.xml -o output -t ../data/ecss-template/ecss-e-st-40c_6_requirement_traceability.tmplt
pandoc --pdf-engine=pdfroff --output=output/ecss-e-st-40c_6_requirement_traceability.pdf output/ecss-e-st-40c_6_requirement_traceability.md
template-processor --verbosity info --iv demo-project/interfaceview.xml --dv demo-project/deploymentview.dv.xml -o output -t ../data/ecss-template/ecss-e-st-40c_5_4_aspects_of_each_component.tmplt
pandoc --pdf-engine=pdfroff --output=output/ecss-e-st-40c_5_4_aspects_of_each_component.pdf output/ecss-e-st-40c_5_4_aspects_of_each_component.md
