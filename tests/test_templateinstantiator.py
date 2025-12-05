"""
Tests for TemplateInstantiator class
"""

import pytest
import tempfile
from pathlib import Path
from typing import Dict, List
from templateprocessor.templateinstantiator import TemplateInstantiator
from templateprocessor.iv import (
    InterfaceView,
    Function,
    Language,
    ProvidedInterface,
    RequiredInterface,
    InterfaceKind,
    InputParameter,
    OutputParameter,
    Encoding,
)
from templateprocessor.so import SystemObjectType, SystemObject


class TestTemplateInstantiator:
    """Test cases for TemplateInstantiator class."""

    @staticmethod
    def create_sample_interface_view() -> InterfaceView:
        """Create a sample InterfaceView for testing."""
        iv = InterfaceView(
            version="1.3",
            asn1file="test.acn",
            uiFile="test.ui.xml",
            modifierHash="test_hash",
        )

        # Create a sample function
        func = Function(
            id="func_1", name="TestFunction", is_type=False, language=Language.C
        )

        # Add a provided interface
        pi = ProvidedInterface(
            id="pi_1",
            name="test_pi",
            kind=InterfaceKind.SPORADIC,
        )
        pi.input_parameters = [
            InputParameter(name="input1", type="MyInt", encoding=Encoding.NATIVE)
        ]
        func.provided_interfaces = [pi]

        # Add a required interface
        ri = RequiredInterface(
            id="ri_1",
            name="test_ri",
            kind=InterfaceKind.CYCLIC,
        )
        ri.output_parameters = [
            OutputParameter(name="output1", type="MyFloat", encoding=Encoding.UPER)
        ]
        func.required_interfaces = [ri]

        iv.functions = [func]
        return iv

    @staticmethod
    def create_sample_system_object_types() -> Dict[str, SystemObjectType]:
        """Create sample SystemObjectTypes for testing."""
        # Create events system object type
        events = SystemObjectType()
        events.property_names = ["ID", "Name", "Severity"]

        event1 = SystemObject()
        event1.values = {"ID": "1", "Name": "Error Event", "Severity": "high"}
        event2 = SystemObject()
        event2.values = {"ID": "2", "Name": "Info Event", "Severity": "low"}

        events.instances = [event1, event2]

        # Create parameters system object type
        params = SystemObjectType()
        params.property_names = ["ID", "Name", "Default"]

        param1 = SystemObject()
        param1.values = {"ID": "1", "Name": "Timeout", "Default": "100"}
        param2 = SystemObject()
        param2.values = {"ID": "2", "Name": "MaxRetries", "Default": "3"}

        params.instances = [param1, param2]

        sots = dict()
        sots["events"] = events
        sots["params"] = params

        return sots

    def test_instantiator_initialization(self):
        """Test TemplateInstantiator initialization."""
        iv = self.create_sample_interface_view()
        so_types = self.create_sample_system_object_types()

        instantiator = TemplateInstantiator(iv, so_types)

        assert instantiator.interface_view == iv
        assert instantiator.system_object_types == so_types
        assert len(instantiator.system_object_types) == 2

    def test_instantiate_simple_template(self):
        """Test instantiating a simple template."""
        iv = self.create_sample_interface_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, so_types)

        template = "Hello World!"

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)

        assert result == "Hello World!"

    def test_instantiate_template_with_interface_view(self):
        """Test instantiating a template that uses Interface View."""
        iv = self.create_sample_interface_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, so_types)

        template = """Interface View version: ${interface_view.version}
ASN1 file: ${interface_view.asn1file}
Number of functions: ${len(interface_view.functions)}"""

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)

        assert "Interface View version: 1.3" in result
        assert "ASN1 file: test.acn" in result
        assert "Number of functions: 1" in result

    def test_instantiate_template_with_function_details(self):
        """Test instantiating a template that accesses Function details."""
        iv = self.create_sample_interface_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, so_types)

        template = """% for func in interface_view.functions:
Function: ${func.name}
Language: ${func.language.value}
Provided Interfaces: ${len(func.provided_interfaces)}
Required Interfaces: ${len(func.required_interfaces)}
% endfor"""

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)

        assert "Function: TestFunction" in result
        assert "Language: C" in result
        assert "Provided Interfaces: 1" in result
        assert "Required Interfaces: 1" in result

    def test_instantiate_template_with_system_object_types(self):
        """Test instantiating a template that uses System Object Types."""
        iv = self.create_sample_interface_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, so_types)

        template = """Number of System Object Types: ${len(system_object_types)}
% for name, so_type in system_object_types.items():
  [${name}] Properties: ${', '.join(so_type.property_names)}
  [${name}] Instances: ${len(so_type.instances)}
% endfor"""

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)

        assert "Number of System Object Types: 2" in result
        assert "[events] Properties: ID, Name, Severity" in result
        assert "[params] Properties: ID, Name, Default" in result
        assert "Instances: 2" in result

    def test_instantiate_template_with_system_object_instances(self):
        """Test instantiating a template that accesses System Object Type instances."""
        iv = self.create_sample_interface_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, so_types)

        template = """% for name, so_type in system_object_types.items():
[${name}]
% for instance in so_type.instances:
% if 'Name' in instance.values:
 - ID: ${instance.values['ID']} - ${instance.values['Name']}
% endif
% endfor
% endfor"""

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)
        assert (
            """[events]
 - ID: 1 - Error Event
 - ID: 2 - Info Event
[params]
 - ID: 1 - Timeout
 - ID: 2 - MaxRetries
"""
            == result
        )

    def test_instantiate_template_with_empty_data(self):
        """Test instantiating a template with empty Interface View and no System Objects."""
        iv = InterfaceView(version="1.0", asn1file="", uiFile="", modifierHash="")

        so_types = {}

        instantiator = TemplateInstantiator(iv, so_types)

        template = """Version: ${interface_view.version}
Functions: ${len(interface_view.functions)}
System Object Types: ${len(system_object_types)}"""

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)

        assert "Version: 1.0" in result
        assert "Functions: 0" in result
        assert "System Object Types: 0" in result

    def test_instantiate_template_with_python_expressions(self):
        """Test instantiating a template with Python expressions."""
        iv = self.create_sample_interface_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, so_types)

        template = """<%
total_interfaces = sum(len(f.provided_interfaces) + len(f.required_interfaces) for f in interface_view.functions)
total_instances = sum(len(so.instances) for so in system_object_types.values())
%>
Total Interfaces: ${total_interfaces}
Total System Object Instances: ${total_instances}"""

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)

        assert "Total Interfaces: 2" in result
        assert "Total System Object Instances: 4" in result
