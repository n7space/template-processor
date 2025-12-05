"""
OPUS2 System Object CSV Reader.

This module provides functionality to parse CSV files containing System Object data
and construct SystemObjectType instances.
"""

import csv
from io import TextIOWrapper
from pathlib import Path
from typing import Union

from templateprocessor.so import SystemObject, SystemObjectType
from io import StringIO


class SOReader:
    """
    Reader for System Object CSV files.

    Parses semicolon-delimited CSV files and constructs corresponding
    SystemObjectType objects with property names from headers and
    SystemObject instances from data rows.

    Example:
        reader = SOReader()
        so_type = reader.read("events.csv")
        # Access property names
        print(so_type.property_names)  # ['ID', 'Name', 'Auxilary data', 'Severity']
        # Access instances
        for instance in so_type.instances:
            print(instance.values)
    """

    def read(
        self, file_path: Union[str, Path], delimiter: str = ";"
    ) -> SystemObjectType:
        """
        Read and parse a System Object CSV file.

        Args:
            file_path: Path to the CSV file
            delimiter: CSV delimiter character (default: ';')

        Returns:
            SystemObjectType object populated with parsed data

        Raises:
            FileNotFoundError: If the file does not exist
            csv.Error: If CSV parsing fails
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"System Object CSV file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as csvfile:
            return self._parse_csv(csvfile, delimiter)

    def read_string(self, csv_content: str, delimiter: str = ";") -> SystemObjectType:
        """
        Read and parse System Object CSV from a string.

        Args:
            csv_content: CSV content as string
            delimiter: CSV delimiter character (default: ';')

        Returns:
            SystemObjectType object populated with parsed data

        Raises:
            csv.Error: If CSV parsing fails
        """
        csvfile = StringIO(csv_content)
        return self._parse_csv(csvfile, delimiter)

    def _parse_csv(
        self, csvfile: Union[TextIOWrapper, StringIO], delimiter: str
    ) -> SystemObjectType:
        """
        Parse CSV content and construct SystemObjectType.

        Args:
            csvfile: File-like object containing CSV data
            delimiter: CSV delimiter character

        Returns:
            SystemObjectType with property names and instances populated
        """
        reader = csv.DictReader(csvfile, delimiter=delimiter)

        # Initialize SystemObjectType
        so_type = SystemObjectType()

        # Get property names from the CSV header
        if reader.fieldnames:
            so_type.property_names = list(reader.fieldnames)

        # Parse each row as a SystemObject instance
        for row in reader:
            system_object = SystemObject()
            # Populate values dictionary with all properties
            for key, value in row.items():
                if key is not None:  # Skip None keys
                    system_object.values[key] = value if value is not None else ""
            so_type.instances.append(system_object)

        return so_type
