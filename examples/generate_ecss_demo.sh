#!/bin/bash
mkdir -p output
template-processor --verbosity info --value TARGET=ASW --iv demo-project/interfaceview.xml --dv demo-project/deploymentview.dv.xml -o output -t ../data/ecss-template/ecss-e-st-40c_6_requirement_traceability.tmplt
pandoc --pdf-engine=pdfroff --output=output/ecss-e-st-40c_6_requirement_traceability.pdf output/ecss-e-st-40c_6_requirement_traceability.md
template-processor --verbosity info --value TARGET=ASW --iv demo-project/interfaceview.xml --dv demo-project/deploymentview.dv.xml -o output -t ../data/ecss-template/ecss-e-st-40c_5_4_aspects_of_each_component.tmplt
pandoc --pdf-engine=pdfroff --output=output/ecss-e-st-40c_5_4_aspects_of_each_component.pdf output/ecss-e-st-40c_5_4_aspects_of_each_component.md
template-processor --verbosity info --value TARGET=ASW --iv demo-project/interfaceview.xml --dv demo-project/deploymentview.dv.xml -o output -t ../data/ecss-template/ecss-e-st-40c_4_2_software_dynamic_architecture.tmplt
pandoc --pdf-engine=pdfroff --output=output/ecss-e-st-40c_4_2_software_dynamic_architecture.pdf output/ecss-e-st-40c_4_2_software_dynamic_architecture.md
template-processor --verbosity info --value TARGET=ASW --iv demo-project/interfaceview.xml --dv demo-project/deploymentview.dv.xml -o output -t ../data/ecss-template/ecss-e-st-40c_5_5_internal_interface_design.tmplt
pandoc --pdf-engine=pdfroff --output=output/ecss-e-st-40c_5_5_internal_interface_design.pdf output/ecss-e-st-40c_5_5_internal_interface_design.md
template-processor --verbosity info --value TARGET=ASW --iv demo-project/interfaceview.xml --dv demo-project/deploymentview.dv.xml -o output -t ../data/ecss-template/ecss-e-st-40c_4_4_interfaces_context.tmplt
pandoc --pdf-engine=pdfroff --output=output/ecss-e-st-40c_4_4_interfaces_context.pdf output/ecss-e-st-40c_4_4_interfaces_context.md