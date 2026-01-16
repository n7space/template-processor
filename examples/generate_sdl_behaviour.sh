#!/bin/bash

cd sdl-project
mkdir -p ../output

# Generate MD behaviour documentation
template-processor --verbosity info \
    --value TARGET=ASW \
    --iv interfaceview.xml \
    --dv deploymentview.dv.xml \
    -o ../output \
    -t ../../data/ecss-template/ecss-e-st-40c_4_3_software_behaviour.tmplt

# Generate DOCX version
template-processor --verbosity info \
    --value TARGET=ASW \
    --iv interfaceview.xml \
    --dv deploymentview.dv.xml \
    -o ../output \
    -t ../../data/ecss-template/ecss-e-st-40c_4_3_software_behaviour.tmplt \
    -p md2docx

# Generate HTML version
template-processor --verbosity info \
    --value TARGET=ASW \
    --iv interfaceview.xml \
    --dv deploymentview.dv.xml \
    -o ../output \
    -t ../../data/ecss-template/ecss-e-st-40c_4_3_software_behaviour.tmplt \
    -p md2html
