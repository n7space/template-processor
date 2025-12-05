#!/bin/bash
mkdir -p output
template-processor --verbosity info --sos ../data/events.csv -o output -t so_list.tmplt