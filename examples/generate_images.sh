#!/bin/bash
mkdir -p output

template-processor --verbosity info  -t images.tmplt -o output -p md2docx
