# Template Processor

## General

Template Processor (TP), created as a part of "Model-Based Execution Platform for Space Applications" project (contract 4000146882/24/NL/KK) financed by the European Space Agency.

TP is a template processing engine developed for TASTE Document Generator. Its main function is to consume the provided inputs (e.g., TASTE Interface View data), instantiate templates and translate them into format that can be integrated deliverable documents. Base requirements are provided in MBEP-N7S-EP-SRS, while the overall design is documented in MBEP-N7S-EP-SDD.

## Installation

This project uses Python. The recommended way to install dependencies is via the provided Makefile which exposes a convenient `make install` target.

Prerequisites:
- Python 3.10+ (or a compatible system Python)

## Configuration

None

## Running

The Template Processor can be run from the command line. The application name is `template-processor` which exposes the following arguments. Run the built-in help to see the same list:

```bash
template-processor --help
```

Key command-line arguments:

- `-i, --iv` : Input Interface View file (XML)
- `-d, --dv` : Input Deployment View file (XML)
- `-s, --system-objects` : One or more CSV files describing System Object Types (can be supplied multiple times)
- `-v, --value` : One or more name=value pairs to provide template values (e.g., `-v TARGET=ASW`)
- `-t, --template` : One or more template files to process (Mako templates). This argument can be provided multiple times.
- `-m, --module-directory` : Module directory for Mako to use for compiled template modules (optional)
- `-o, --output` : Output directory for processed templates (required)
- `--verbosity` : Logging verbosity (choices `info`, `debug`, `warning`, `error`, default `warning`)
- `-p, --postprocess` : Postprocessing option (choices `none`, `md2docx`, `md2html`; default `none`)

Example usage:

```bash
# instantiate a template and postprocess to DOCX
template-processor \\
	-i examples/demo-project/interfaceview.xml \\
	-d examples/demo-project/deploymentview.dv.xml \\
	-s data/parameters.csv \\
	-v TARGET=ASW \\
	-t data/ecss-template/ecss-e-st-40c_4_1_software_static_architecture.tmplt \\
	-o output \\
	-p md2docx
```

Notes:
- The `-o/--output` directory will be used for writing generated files; templates may also copy or move generated assets (images) into that directory if supported by the template.
- When using `md2docx` postprocessing, image paths inside the generated Markdown should be resolvable from the working directory or the output directory so images are embedded correctly in the produced DOCX.

## Frequently Asked Questions (FAQ)

None

## Troubleshooting

None
