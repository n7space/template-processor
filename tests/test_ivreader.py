"""
Tests for IVReader class
"""

import pytest
from pathlib import Path
from templateprocessor.ivreader import IVReader
from templateprocessor.iv import (
    InterfaceView,
    Function,
    Language,
    Encoding,
    InterfaceKind,
)


class TestIVReader:
    """Test cases for IVReader class."""

    # Assuming the data directory is at the workspace root
    @staticmethod
    def get_test_data_file(filename: str) -> Path:
        """Get the path to a test data file."""
        return Path(__file__).parent.parent / "data" / filename

    def test_read_simple_iv_xml(self):
        """Test reading the simple.iv.xml file."""
        # Prepare
        reader = IVReader()
        iv_file = self.get_test_data_file("simple.iv.xml")
        assert iv_file.exists()

        # Read
        iv = reader.read(iv_file)

        # Verify basic attributes
        assert isinstance(iv, InterfaceView)
        assert iv.version == "1.3"
        assert iv.asn1file == "simple.acn"
        assert iv.uiFile == "interfaceview.ui.xml"

        # Verify functions were parsed
        assert len(iv.functions) > 0

        # Check specific function names
        function_names = [f.name for f in iv.functions]
        assert "host" in function_names
        assert "master" in function_names
        assert "slave" in function_names
        assert "Worker" in function_names
        assert "WorkerType" in function_names

    def test_read_nested_functions(self):
        """Test reading nested functions in the simple.iv.xml file."""
        # Prepare
        reader = IVReader()
        iv_file = self.get_test_data_file("simple.iv.xml")
        assert iv_file.exists()

        # Read
        iv = reader.read(iv_file)

        # Verify basic attributes
        assert isinstance(iv, InterfaceView)
        assert iv.version == "1.3"
        assert iv.asn1file == "simple.acn"
        assert iv.uiFile == "interfaceview.ui.xml"

        # Verify functions were parsed
        assert len(iv.functions) > 0

        # Check specific function names
        host = next((f for f in iv.functions if f.name == "host"), None)
        function_names = [f.name for f in host.nested_functions]
        assert "child1" in function_names
        assert "child2" in function_names

    def test_read_functions_details(self):
        """Test that function details are correctly parsed."""
        # Prepare
        reader = IVReader()
        iv_file = self.get_test_data_file("simple.iv.xml")
        assert iv_file.exists()

        # Read
        iv = reader.read(iv_file)

        # Find the 'host' function
        host = next((f for f in iv.functions if f.name == "host"), None)
        assert host is not None
        assert host.language == Language.SDL
        assert host.is_type == False

        # Check interfaces
        assert len(host.provided_interfaces) > 0
        assert len(host.required_interfaces) > 0

        # Check specific provided interface
        child1_pi = next(
            (pi for pi in host.provided_interfaces if pi.name == "child1_if"), None
        )
        assert child1_pi is not None
        assert child1_pi.kind == InterfaceKind.SPORADIC
        assert len(child1_pi.input_parameters) == 1
        assert child1_pi.input_parameters[0].name == "p1"
        assert child1_pi.input_parameters[0].type == "T-Int32"
        assert child1_pi.input_parameters[0].encoding == Encoding.NATIVE

    def test_read_connections(self):
        """Test that connections are correctly parsed."""
        # Prepare
        reader = IVReader()
        iv_file = self.get_test_data_file("simple.iv.xml")
        assert iv_file.exists()

        # Read
        iv = reader.read(iv_file)

        # Verify connections were parsed
        assert len(iv.connections) > 0

        # Check a specific connection
        connection = next(
            (
                c
                for c in iv.connections
                if c.id == "{0ed63357-7a9b-40f0-8392-27844d53ef6b}"
            ),
            None,
        )
        assert connection.source is not None
        assert connection.target is not None
        assert connection.source.function_name == "master"
        assert connection.target.function_name == "host"

    def test_read_worker_type_function(self):
        """Test parsing function type and instance."""
        # Prepare
        reader = IVReader()
        iv_file = self.get_test_data_file("simple.iv.xml")
        assert iv_file.exists()

        # Read
        iv = reader.read(iv_file)

        # Find WorkerType (function type)
        worker_type = next((f for f in iv.functions if f.name == "WorkerType"), None)
        assert worker_type is not None
        assert worker_type.is_type == True
        assert worker_type.type_language == Language.SDL

        # Find Worker (instance of WorkerType)
        worker = next((f for f in iv.functions if f.name == "Worker"), None)
        assert worker is not None
        assert worker.instance_of == "WorkerType"
        assert worker.is_type == False

    def test_read_interface_with_multiple_parameters(self):
        """Test parsing interface with multiple input parameters."""
        # Prepare
        reader = IVReader()
        iv_file = self.get_test_data_file("simple.iv.xml")
        assert iv_file.exists()

        # Read
        iv = reader.read(iv_file)

        # Find master function
        master = next((f for f in iv.functions if f.name == "master"), None)
        assert master is not None

        # Find unprotected RI with multiple parameters
        unprotected_ri = next(
            (ri for ri in master.required_interfaces if ri.name == "unprotected"), None
        )
        assert unprotected_ri is not None
        assert len(unprotected_ri.input_parameters) == 3

        # Verify different encodings
        assert unprotected_ri.input_parameters[0].name == "p1"
        assert unprotected_ri.input_parameters[0].type == "T-Int32"
        assert unprotected_ri.input_parameters[0].encoding == Encoding.NATIVE
        assert unprotected_ri.input_parameters[1].name == "p2"
        assert unprotected_ri.input_parameters[1].type == "T-Int32"
        assert unprotected_ri.input_parameters[1].encoding == Encoding.UPER
        assert unprotected_ri.input_parameters[2].name == "p3"
        assert unprotected_ri.input_parameters[2].type == "T-Int32"
        assert unprotected_ri.input_parameters[2].encoding == Encoding.ACN

    def test_read_output_parameters(self):
        """Test parsing interface with output parameters."""
        # Prepare
        reader = IVReader()
        iv_file = self.get_test_data_file("simple.iv.xml")
        assert iv_file.exists()

        # Read
        iv = reader.read(iv_file)

        # Find slave function
        slave = next((f for f in iv.functions if f.name == "slave"), None)
        assert slave is not None

        # Find protected_if PI with output parameter
        protected_pi = next(
            (pi for pi in slave.provided_interfaces if pi.name == "protected_if"), None
        )
        assert protected_pi is not None
        assert len(protected_pi.input_parameters) == 1
        assert len(protected_pi.output_parameters) == 1
        assert protected_pi.output_parameters[0].name == "p2"
        assert protected_pi.output_parameters[0].encoding == Encoding.UPER

    def test_read_layers_and_comments(self):
        """Test parsing layers and comments."""
        # Prepare
        reader = IVReader()
        iv_file = self.get_test_data_file("simple.iv.xml")
        assert iv_file.exists()

        # Read
        iv = reader.read(iv_file)

        # Verify layers
        assert len(iv.layers) > 0
        default_layer = next((l for l in iv.layers if l.name == "default"), None)
        assert default_layer is not None
        assert default_layer.is_visible == True

        # Verify comments
        assert len(iv.comments) > 0

    def test_read_string(self):
        """Test reading from XML string."""
        reader = IVReader()

        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<InterfaceView version="1.0" asn1file="test.acn" UiFile="test.ui.xml" modifierHash="abc123">
    <Function id="{test-id}" name="test_func" is_type="NO" language="C" default_implementation="default" 
              fixed_system_element="NO" required_system_element="NO" instances_min="1" instances_max="1" startup_priority="1">
    </Function>
    <Layer name="default" is_visible="true"/>
</InterfaceView>"""

        iv = reader.read_string(xml_content)

        assert iv.version == "1.0"
        assert iv.asn1file == "test.acn"
        assert len(iv.functions) == 1
        assert iv.functions[0].name == "test_func"
        assert len(iv.layers) == 1

    def test_read_requirements(self):
        """Test parsing interface with requirement IDs."""
        # Prepare
        reader = IVReader()
        iv_file = self.get_test_data_file("requirements.iv.xml")
        assert iv_file.exists()

        # Read
        iv = reader.read(iv_file)

        # Find Function_1 function
        function1 = next((f for f in iv.functions if f.name == "Function_1"), None)
        assert function1 is not None

        assert len(function1.requirement_ids) == 2
        assert "r1" in function1.requirement_ids
        assert "r2" in function1.requirement_ids

        # Find Function_2 function
        function2 = next((f for f in iv.functions if f.name == "Function_2"), None)
        assert function2 is not None

        # Find do_smth interface
        do_smth = next(
            (pi for pi in function2.provided_interfaces if pi.name == "do_smth"), None
        )
        assert do_smth is not None
        assert len(do_smth.requirement_ids) == 1
        assert "r5" in do_smth.requirement_ids
