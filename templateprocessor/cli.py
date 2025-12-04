"""
Command Line Interface for Template Processor
"""

import argparse
import sys
from templateprocessor import __version__


def main():
    """Main entry point for the Template Processor CLI."""
    parser = argparse.ArgumentParser(
        description="Template Processor - Template processing engine for TASTE Document Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"template-processor {__version__}"
    )

    parser.add_argument(
        "-i",
        "--input",
        help="Input data file (e.g., TASTE Interface View data)",
        metavar="FILE",
    )

    parser.add_argument(
        "-t", "--template", help="Template file to process", metavar="FILE"
    )

    parser.add_argument(
        "-o", "--output", help="Output file for processed template", metavar="FILE"
    )

    args = parser.parse_args()

    print("Template Processor - Not yet implemented")
    print(f"Version: {__version__}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
