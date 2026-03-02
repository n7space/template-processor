#!/bin/bash

cd demo-project
mkdir -p ../output

# Generate MD E2E documentation
template-processor --verbosity info \
    --iv interfaceview.xml \
    -o ../output \
    -t ../e2e-demo.tmplt

# Generate DOCX version
template-processor --verbosity info \
    --iv interfaceview.xml \
    -o ../output \
    -t ../e2e-demo.tmplt \
    -p md2docx
