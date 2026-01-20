"""
Command Line Interface for Template Processor
"""

import logging
import argparse
from pathlib import Path
import sys
from templateprocessor import __version__
from templateprocessor.iv import InterfaceView
from templateprocessor.dv import DeploymentView
from templateprocessor.templateinstantiator import TemplateInstantiator
from templateprocessor.ivreader import IVReader
from templateprocessor.soreader import SOReader
from templateprocessor.dvreader import DVReader
from templateprocessor.so import SystemObjectType
from templateprocessor.postprocessor import (
    PostprocessorType,
    Md2docxPostprocessor,
    Md2HtmlPostprocessor,
    PassthroughPostprocessor,
    Postprocessor,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Template Processor - Template processing engine for TASTE Document Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"template-processor {__version__}"
    )

    parser.add_argument(
        "-i",
        "--iv",
        help="Input Interface View",
        metavar="FILE",
    )

    parser.add_argument(
        "-d",
        "--dv",
        help="Input Deployment View",
        metavar="FILE",
    )

    parser.add_argument(
        "-s",
        "--system-objects",
        help="Input System Objects provided as CSV files (each as a separate argument)",
        metavar="FILE",
        action="append",
    )

    parser.add_argument(
        "-v",
        "--value",
        help="Input values (formatted as name=value pair, e.g., target=ASW)",
        action="append",
    )

    parser.add_argument(
        "-t",
        "--template",
        help="Template file to process (each as a separate argument)",
        metavar="FILE",
        action="append",
    )

    parser.add_argument(
        "-m",
        "--module-directory",
        help="Module directory for Mako templating engine",
        metavar="FILE",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output directory for processed templates",
        metavar="DIR",
        required=True,
    )

    parser.add_argument(
        "--verbosity",
        choices=["info", "debug", "warning", "error"],
        default="warning",
        help="Logging verbosity",
    )

    parser.add_argument(
        "-p",
        "--postprocess",
        choices=["none", "md2docx", "md2html"],
        help="Output postprocessing",
        default="none",
    )

    return parser.parse_args()


def get_log_level(level_str: str) -> int:
    log_levels = {
        "info": logging.INFO,
        "debug": logging.DEBUG,
        "warning": logging.WARNING,
        "error": logging.ERROR,
    }

    return log_levels.get(level_str.lower(), logging.WARNING)


def get_postprocessor_type(type_str: str) -> PostprocessorType:
    types = {
        PostprocessorType.NONE.value: PostprocessorType.NONE,
        PostprocessorType.MD2DOCX.value: PostprocessorType.MD2DOCX,
        PostprocessorType.MD2HTML.value: PostprocessorType.MD2HTML,
    }

    return types.get(type_str.lower(), PostprocessorType.NONE)


def get_values_dictionary(values: list[str]) -> dict[str, str]:
    if not values or not isinstance(values, list):
        return {}
    result = {}
    for pair in values:
        if pair.count("=") != 1:
            raise ValueError(
                f"Pair [{pair}] contains incorrect number of name/value separators (=)"
            )
        split = pair.split("=")
        name = split[0].strip()
        value = split[1].strip()
        if len(name) == 0:
            raise ValueError(f"Name in [{pair}] is empty")
        # value can be empty
        result[name] = value
    return result


def read_sots(file_names: list[str]) -> dict[str, SystemObjectType]:
    sots = {}
    so_reader = SOReader()
    for sot_file in file_names:
        try:
            logging.info(f"Reading System Objects from {sot_file}")
            name = Path(sot_file).stem
            logging.debug(f"-SOT name: {name}")
            sos = so_reader.read(sot_file)
            sots[name] = sos
        except Exception as e:
            logging.error(f"Could not read System Objects from {sot_file}")
    return sots


def instantiate(
    instantiator: TemplateInstantiator,
    postprocessor: Postprocessor,
    template_file: str,
    module_directory: str,
    postprocessor_type: PostprocessorType,
    output_directory: str,
):
    try:
        logging.info(f"Processing template {template_file}")
        name = Path(template_file).stem
        logging.debug(f"Base name: {name}")
        logging.debug(f"Reading template {template_file}")
        with open(template_file, "r") as f:
            template = f.read()
        logging.debug(f"Instantiating template:\n {template}")
        instantiated_template = instantiator.instantiate(template, module_directory)
        logging.debug(f"Instantiation:\n {instantiated_template}")
        output = str(Path(output_directory) / f"{name}")
        logging.debug(f"Postprocessing with {postprocessor_type}")
        # Base directory for postprocessing is the output directory
        postprocessor.process(
            postprocessor_type, instantiated_template, output, output_directory
        )
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
    except Exception as e:
        logging.error(f"Error processing template {template_file}: {e}")


def main():
    """Main entry point for the Template Processor CLI."""

    args = parse_arguments()
    logging_level = get_log_level(args.verbosity)
    logging.basicConfig(level=logging_level)
    postprocessor_type = get_postprocessor_type(args.postprocess)

    logging.info("Template Processor")
    logging.debug(f"Interface View: {args.iv}")
    logging.debug(f"Deployment View: {args.dv}")
    logging.debug(f"System Objects: {args.system_objects}")
    logging.debug(f"Values: {args.value}")
    logging.debug(f"Templates: {args.template}")
    logging.debug(f"Output Directory: {args.output}")
    logging.debug(f"Module directory: {args.module_directory}")
    logging.debug(f"Postprocessing: {postprocessor_type.value}")

    logging.info(f"Reading Interface View from {args.iv}")
    iv = IVReader().read(args.iv) if args.iv else InterfaceView()

    logging.info(f"Reading Deployment View from {args.dv}")
    dv = DVReader().read(args.dv) if args.dv else DeploymentView()

    logging.info(f"Reading provided System Objects")
    sots = read_sots(args.system_objects) if args.system_objects else {}

    logging.info(f"Parsing values from {args.value}")
    values = get_values_dictionary(args.value)

    logging.info(f"Instantiating the TemplateInstantiator")
    instantiator = TemplateInstantiator(iv, dv, sots, values, args.output)

    logging.info(f"Instantiating the Postprocessor")
    postprocessor = Postprocessor(
        {
            PostprocessorType.NONE: PassthroughPostprocessor(),
            PostprocessorType.MD2DOCX: Md2docxPostprocessor(),
            PostprocessorType.MD2HTML: Md2HtmlPostprocessor(),
        }
    )

    if args.template:
        logging.info(f"Instantiating templates")
        for template_file in args.template:
            instantiate(
                instantiator,
                postprocessor,
                template_file,
                args.module_directory,
                postprocessor_type,
                args.output,
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
