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
from templateprocessor.dv import (
    DeploymentView,
    Node,
    Partition,
    DeploymentFunction,
    Device,
    Connection,
    Message,
)


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
            id="func_1",
            comment="No Comment",
            name="TestFunction",
            is_type=False,
            language=Language.C,
        )

        # Add a provided interface
        pi = ProvidedInterface(
            id="pi_1",
            name="test_pi",
            comment="No Comment",
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
            comment="No Comment",
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

    @staticmethod
    def create_sample_deployment_view() -> DeploymentView:
        """Create a sample DeploymentView for testing."""
        dv = DeploymentView(
            version="1.2",
            ui_file="test_deployment.ui.xml",
            creator_hash="test_creator",
            modifier_hash="test_modifier",
        )

        # Create first node (x86 Linux)
        node1 = Node(
            id="n1",
            name="x86 Linux C++_1",
            type="ocarina_processors_x86::x86.generic_linux",
            node_label="Node_1",
            namespace="ocarina_processors_x86",
            requirement_ids=["r20", "r21"],
        )

        # Add partition to node1
        partition1 = Partition(
            id="p1",
            name="test_partition_1",
        )

        # Add functions to partition
        func1 = DeploymentFunction(
            id="f1",
            name="TestFunction",
            path="/test/path/function1",
        )
        partition1.functions.append(func1)
        node1.partitions.append(partition1)

        # Add device to node1
        device1 = Device(
            id="d1",
            name="uart0",
            requires_bus_access="UART",
            port="uart0",
            asn1file="test.asn",
            asn1type="TestType",
            asn1module="TestModule",
            namespace="test_namespace",
            extends="BaseDevice",
            impl_extends="BaseImpl",
            bus_namespace="uart_namespace",
        )
        node1.devices.append(device1)

        # Create second node (ARM RTEMS)
        node2 = Node(
            id="n2",
            name="SAM V71 RTEMS N7S_1",
            type="ocarina_processors_arm::samv71.rtems",
            node_label="Node_2",
            namespace="ocarina_processors_arm",
        )

        # Add partition to node2
        partition2 = Partition(
            id="p2",
            name="test_partition_2",
        )

        func2 = DeploymentFunction(
            id="f2",
            name="SensorFunction",
            path="/test/path/function2",
        )
        partition2.functions.append(func2)
        node2.partitions.append(partition2)

        # Add nodes to deployment view
        dv.nodes.append(node1)
        dv.nodes.append(node2)

        # Create connection between nodes
        connection = Connection(
            id="c1",
            name="UartLink",
            from_node="n1",
            from_port="uart0",
            to_bus="UART",
            to_node="n2",
            to_port="uart0",
        )

        # Add messages to connection
        msg1 = Message(
            id="m1",
            name="DataMessage",
            from_function="TestFunction",
            from_interface="test_pi",
            to_function="SensorFunction",
            to_interface="sensor_ri",
        )
        connection.messages.append(msg1)

        dv.connections.append(connection)

        return dv

    def test_instantiator_initialization(self):
        """Test TemplateInstantiator initialization."""
        iv = self.create_sample_interface_view()
        dv = self.create_sample_deployment_view()
        so_types = self.create_sample_system_object_types()

        instantiator = TemplateInstantiator(iv, dv, so_types, {})

        assert instantiator.interface_view == iv
        assert instantiator.system_object_types == so_types
        assert len(instantiator.system_object_types) == 2

    def test_instantiate_simple_template(self):
        """Test instantiating a simple template."""
        iv = self.create_sample_interface_view()
        dv = self.create_sample_deployment_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, dv, so_types, {})

        template = "Hello World!"

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)

        assert result == "Hello World!"

    def test_instantiate_template_with_interface_view(self):
        """Test instantiating a template that uses Interface View."""
        iv = self.create_sample_interface_view()
        dv = self.create_sample_deployment_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, dv, so_types, {})

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
        dv = self.create_sample_deployment_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, dv, so_types, {})

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
        dv = self.create_sample_deployment_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, dv, so_types, {})

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
        dv = self.create_sample_deployment_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, dv, so_types, {})

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
        dv = self.create_sample_deployment_view()

        so_types = {}

        instantiator = TemplateInstantiator(iv, dv, so_types, {})

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
        dv = self.create_sample_deployment_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, dv, so_types, {})

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

    def test_instantiate_template_with_deployment_view(self):
        """Test instantiating a template that uses Deployment View."""
        iv = self.create_sample_interface_view()
        dv = self.create_sample_deployment_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, dv, so_types, {})

        template = """Deployment View version: ${deployment_view.version}
UI file: ${deployment_view.ui_file}
Number of nodes: ${len(deployment_view.nodes)}
Number of connections: ${len(deployment_view.connections)}"""

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)

        assert "Deployment View version: 1.2" in result
        assert "UI file: test_deployment.ui.xml" in result
        assert "Number of nodes: 2" in result
        assert "Number of connections: 1" in result

    def test_instantiate_template_with_deployment_nodes(self):
        """Test instantiating a template that accesses Deployment View nodes."""
        iv = self.create_sample_interface_view()
        dv = self.create_sample_deployment_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, dv, so_types, {})

        template = """% for node in deployment_view.nodes:
Node: ${node.name}
Type: ${node.type}
Label: ${node.node_label}
Namespace: ${node.namespace}
Partitions: ${len(node.partitions)}
Devices: ${len(node.devices)}
% endfor"""

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)

        assert "Node: x86 Linux C++_1" in result
        assert "Type: ocarina_processors_x86::x86.generic_linux" in result
        assert "Node: SAM V71 RTEMS N7S_1" in result
        assert "Type: ocarina_processors_arm::samv71.rtems" in result
        assert "Partitions: 1" in result
        assert "Devices: 1" in result

    def test_instantiate_template_with_partitions_and_functions(self):
        """Test instantiating a template that accesses partitions and deployed functions."""
        iv = self.create_sample_interface_view()
        dv = self.create_sample_deployment_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, dv, so_types, {})

        template = """% for node in deployment_view.nodes:
${node.name}
% for partition in node.partitions:
Partition: ${partition.name}
% for func in partition.functions:
- Function: ${func.name} (${func.id})
  Path: ${func.path}
% endfor
% endfor
% endfor"""

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)

        assert "x86 Linux C++_1" in result
        assert "Partition: test_partition_1" in result
        assert "- Function: TestFunction (f1)" in result
        assert "Path: /test/path/function1" in result
        assert "SAM V71 RTEMS N7S_1" in result
        assert "Partition: test_partition_2" in result
        assert "- Function: SensorFunction (f2)" in result
        assert "Path: /test/path/function2" in result

    def test_instantiate_template_with_devices(self):
        """Test instantiating a template that accesses node devices."""
        iv = self.create_sample_interface_view()
        dv = self.create_sample_deployment_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, dv, so_types, {})

        template = """% for node in deployment_view.nodes:
% if node.devices:
Node: ${node.name}
% for device in node.devices:
  Device: ${device.name}
  - Port: ${device.port}
  - Bus: ${device.requires_bus_access}
  - ASN1 Type: ${device.asn1type}
% endfor
% endif
% endfor"""

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)

        assert "Node: x86 Linux C++_1" in result
        assert "Device: uart0" in result
        assert "- Port: uart0" in result
        assert "- Bus: UART" in result
        assert "- ASN1 Type: TestType" in result

    def test_instantiate_template_with_connections(self):
        """Test instantiating a template that accesses connections and messages."""
        iv = self.create_sample_interface_view()
        dv = self.create_sample_deployment_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, dv, so_types, {})

        template = """% for conn in deployment_view.connections:
Connection: ${conn.name}
  From: ${conn.from_node}:${conn.from_port}
  To: ${conn.to_node}:${conn.to_port}
  Bus: ${conn.to_bus}
  Messages: ${len(conn.messages)}
% for msg in conn.messages:
    - ${msg.name}: ${msg.from_function}.${msg.from_interface} -> ${msg.to_function}.${msg.to_interface}
% endfor
% endfor"""

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)

        assert "Connection: UartLink" in result
        assert "From: n1:uart0" in result
        assert "To: n2:uart0" in result
        assert "Bus: UART" in result
        assert "Messages: 1" in result
        assert (
            "- DataMessage: TestFunction.test_pi -> SensorFunction.sensor_ri" in result
        )

    def test_instantiate_template_with_node_requirements(self):
        """Test instantiating a template that accesses node requirement IDs."""
        iv = self.create_sample_interface_view()
        dv = self.create_sample_deployment_view()
        so_types = self.create_sample_system_object_types()
        instantiator = TemplateInstantiator(iv, dv, so_types, {})

        template = """% for node in deployment_view.nodes:
Node: ${node.name}
% if node.requirement_ids:
  Requirements: ${', '.join(node.requirement_ids)}
% else:
  Requirements: None
% endif
% endfor"""

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)

        assert "Node: x86 Linux C++_1" in result
        assert "Requirements: r20, r21" in result
        assert "Node: SAM V71 RTEMS N7S_1" in result
        assert "Requirements: None" in result

    def test_instantiate_template_with_values(self):
        """Test instantiating a template that uses provided values."""
        iv = self.create_sample_interface_view()
        dv = self.create_sample_deployment_view()
        so_types = self.create_sample_system_object_types()

        values = {
            "project_name": "MyProject",
            "version": "2.1.0",
            "author": "Test Author",
            "description": "Test project description",
        }

        instantiator = TemplateInstantiator(iv, dv, so_types, values)

        template = """Project: ${values['project_name']}
Version: ${values['version']}
Author: ${values['author']}
Description: ${values['description']}"""

        with tempfile.TemporaryDirectory() as tmpdir:
            result = instantiator.instantiate(template, tmpdir)

        assert "Project: MyProject" in result
        assert "Version: 2.1.0" in result
        assert "Author: Test Author" in result
        assert "Description: Test project description" in result
