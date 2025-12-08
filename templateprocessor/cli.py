"""
Command Line Interface for Template Processor
"""

import logging
import argparse
import os
from pathlib import Path
import sys
from templateprocessor import __version__
from templateprocessor.iv import InterfaceView
from templateprocessor.templateinstantiator import TemplateInstantiator
from templateprocessor.ivreader import IVReader
from templateprocessor.soreader import SOReader


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
        "-s",
        "--sos",
        help="Input System Objects provided as CSV files (each as a separate argument)",
        metavar="FILE",
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
        choices=["none", "md2docx"],
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


def main():
    """Main entry point for the Template Processor CLI."""

    args = parse_arguments()
    logging_level = get_log_level(args.verbosity)
    logging.basicConfig(level=logging_level)

    logging.info("Template Processor")
    logging.debug(f"Interface View: {args.iv}")
    logging.debug(f"System Objects: {args.sos}")
    logging.debug(f"Templates: {args.template}")
    logging.debug(f"Output Directory: {args.output}")

    logging.info(f"Reading Interface View from {args.iv}")
    iv = IVReader().read(args.iv) if args.iv else InterfaceView()
    sots = {}
    so_reader = SOReader()
    for sot_file in args.sos:
        logging.info(f"Reading System Objects from {sot_file}")
        name = Path(sot_file).stem
        logging.debug(f"-SOT name: {name}")
        sos = so_reader.read(sot_file)
        sots[name] = sos

    instantiator = TemplateInstantiator(iv, sots)

    for template_file in args.template:
        logging.info(f"Processing template {template_file}")
        name = Path(template_file).stem
        logging.debug(f"Base name: {name}")
        logging.debug(f"Reading template {template_file}")
        with open(template_file, "r") as f:
            template = f.read()
        logging.debug(f"Instantiating template:\n {template}")
        instantiated_template = instantiator.instantiate(template, "")
        logging.debug(f"Instantiation:\n {instantiated_template}")
        output = Path(args.output) / f"{name}.md"
        logging.debug(f"Saving to {output}")
        with open(output, "w") as f:
            f.write(instantiated_template)

    return 0


if __name__ == "__main__":
    sys.exit(main())
