#!/bin/bash
mkdir -p output
template-processor --verbosity info --system-objects ../data/events.csv -o output -t so_list.tmplt
pandoc --pdf-engine=pdfroff --output=output/so_list.pdf output/so_list.md
template-processor --verbosity info --system-objects ../data/events.csv -o output -t so_list.tmplt -p md2docx
