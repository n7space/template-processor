#!/bin/bash
mkdir -p output
# List of template names
templates=(
    "ecss-e-st-40c_4_1_software_static_architecture"
    "ecss-e-st-40c_4_2_software_dynamic_architecture"
    "ecss-e-st-40c_4_4_interfaces_context"
    "ecss-e-st-40c_5_2_overall_architecture"
    "ecss-e-st-40c_5_3_software_components_design"
    "ecss-e-st-40c_5_4_aspects_of_each_component"
    "ecss-e-st-40c_5_5_internal_interface_design"
    "ecss-e-st-40c_6_requirement_traceability"
)

# Loop through templates
for template in "${templates[@]}"; do
    template-processor --verbosity info --value TARGET=ASW --iv demo-project/interfaceview.xml --dv demo-project/deploymentview.dv.xml -o output -t ../data/ecss-template/${template}.tmplt
    template-processor --verbosity info --value TARGET=ASW --iv demo-project/interfaceview.xml --dv demo-project/deploymentview.dv.xml -o output -t ../data/ecss-template/${template}.tmplt -p md2docx
    template-processor --verbosity info --value TARGET=ASW --iv demo-project/interfaceview.xml --dv demo-project/deploymentview.dv.xml -o output -t ../data/ecss-template/${template}.tmplt -p md2html
    pandoc --pdf-engine=pdfroff --output=output/${template}.pdf output/${template}.md
done