"""
Tests for DVReader class
"""

import pytest
from pathlib import Path
from templateprocessor.dvreader import DVReader
from templateprocessor.dv import (
    DeploymentView,
    Node,
    Partition,
    DeploymentFunction,
    Device,
    Connection,
    Message,
)


class TestDVReader:
    """Test cases for DVReader class."""

    # Assuming the data directory is at the workspace root
    @staticmethod
    def get_test_data_file(filename: str) -> Path:
        """Get the path to a test data file."""
        return Path(__file__).parent.parent / "data" / filename

    def test_read_deploymentview_xml(self):
        """Test reading the deploymentview.dv.xml file."""
        # Prepare
        reader = DVReader()
        dv_file = self.get_test_data_file("deploymentview.dv.xml")
        assert dv_file.exists()

        # Read
        dv = reader.read(dv_file)

        # Verify basic attributes
        assert isinstance(dv, DeploymentView)
        assert dv.version == "1.2"
        assert dv.ui_file == "deploymentview.ui.xml"
        assert dv.creator_hash == "383508e"
        assert dv.modifier_hash == "383508e"

        # Verify nodes were parsed
        assert len(dv.nodes) == 2

    def test_read_nodes(self):
        """Test that nodes are correctly parsed."""
        # Prepare
        reader = DVReader()
        dv_file = self.get_test_data_file("deploymentview.dv.xml")
        assert dv_file.exists()

        # Read
        dv = reader.read(dv_file)

        # Check node names
        node_names = [n.name for n in dv.nodes]
        assert "SAM V71 RTEMS N7S_1" in node_names
        assert "x86 Linux C++_1" in node_names

        # Find the SAM V71 node
        sam_node = next((n for n in dv.nodes if n.name == "SAM V71 RTEMS N7S_1"), None)
        assert sam_node is not None
        assert sam_node.type == "ocarina_processors_arm::samv71.rtems"
        assert sam_node.node_label == "Node_2"
        assert sam_node.namespace == "ocarina_processors_arm"

        # Find the x86 Linux node
        linux_node = next((n for n in dv.nodes if n.name == "x86 Linux C++_1"), None)
        assert linux_node is not None
        assert linux_node.type == "ocarina_processors_x86::x86.generic_linux"
        assert linux_node.node_label == "Node_1"
        assert linux_node.namespace == "ocarina_processors_x86"

    def test_read_node_requirement_ids(self):
        """Test parsing node requirement IDs."""
        # Prepare
        reader = DVReader()
        dv_file = self.get_test_data_file("deploymentview.dv.xml")
        assert dv_file.exists()

        # Read
        dv = reader.read(dv_file)

        # Find the x86 Linux node with requirement_ids
        linux_node = next((n for n in dv.nodes if n.name == "x86 Linux C++_1"), None)
        assert linux_node is not None
        assert len(linux_node.requirement_ids) == 2
        assert "r20" in linux_node.requirement_ids
        assert "r21" in linux_node.requirement_ids

        # SAM node should have no requirement_ids
        sam_node = next((n for n in dv.nodes if n.name == "SAM V71 RTEMS N7S_1"), None)
        assert sam_node is not None
        assert len(sam_node.requirement_ids) == 0

    def test_read_partitions(self):
        """Test that partitions are correctly parsed."""
        # Prepare
        reader = DVReader()
        dv_file = self.get_test_data_file("deploymentview.dv.xml")
        assert dv_file.exists()

        # Read
        dv = reader.read(dv_file)

        # Find the SAM V71 node
        sam_node = next((n for n in dv.nodes if n.name == "SAM V71 RTEMS N7S_1"), None)
        assert sam_node is not None

        # Verify partitions
        assert len(sam_node.partitions) == 1
        partition = sam_node.partitions[0]
        assert partition.name == "ASW"
        assert partition.id == "{6d924f84-5366-47d0-8a89-56a2614f6813}"

    def test_read_partition_functions(self):
        """Test that partition functions are correctly parsed."""
        # Prepare
        reader = DVReader()
        dv_file = self.get_test_data_file("deploymentview.dv.xml")
        assert dv_file.exists()

        # Read
        dv = reader.read(dv_file)

        # Find the SAM V71 node
        sam_node = next((n for n in dv.nodes if n.name == "SAM V71 RTEMS N7S_1"), None)
        assert sam_node is not None

        # Get the ASW partition
        partition = sam_node.partitions[0]
        assert len(partition.functions) == 2

        # Check function names
        func_names = [f.name for f in partition.functions]
        assert "Frontend" in func_names
        assert "Backend" in func_names

        # Check function details
        frontend = next((f for f in partition.functions if f.name == "Frontend"), None)
        assert frontend is not None
        assert frontend.path == "Frontend"
        assert frontend.id == "{81aa583e-d1d0-47bb-ae8b-de3323dac654}"

    def test_read_devices(self):
        """Test that devices are correctly parsed."""
        # Prepare
        reader = DVReader()
        dv_file = self.get_test_data_file("deploymentview.dv.xml")
        assert dv_file.exists()

        # Read
        dv = reader.read(dv_file)

        # Find the SAM V71 node
        sam_node = next((n for n in dv.nodes if n.name == "SAM V71 RTEMS N7S_1"), None)
        assert sam_node is not None

        # Verify devices
        assert len(sam_node.devices) == 5

        # Check device names
        device_names = [d.name for d in sam_node.devices]
        assert "uart0" in device_names
        assert "uart1" in device_names
        assert "uart2" in device_names

        # Check specific device details
        uart0 = next((d for d in sam_node.devices if d.name == "uart0"), None)
        assert uart0 is not None
        assert uart0.port == "uart0"
        assert uart0.requires_bus_access == "ocarina_buses::serial.ccsds"
        assert uart0.namespace == "ocarina_drivers"
        assert uart0.extends == "ocarina_drivers::serial_ccsds"
        assert uart0.impl_extends == "ocarina_drivers::serial_ccsds.samv71_rtems"
        assert uart0.asn1type == "Serial-SamV71-Rtems-Conf-T"
        assert uart0.asn1module == "SAMV71-RTEMS-SERIAL-DRIVER"

    def test_read_device_requirement_ids(self):
        """Test parsing device requirement IDs."""
        # Prepare
        reader = DVReader()
        dv_file = self.get_test_data_file("deploymentview.dv.xml")
        assert dv_file.exists()

        # Read
        dv = reader.read(dv_file)

        # Find the SAM V71 node
        sam_node = next((n for n in dv.nodes if n.name == "SAM V71 RTEMS N7S_1"), None)
        assert sam_node is not None

        # Find uart0 device with requirement_ids
        uart0 = next((d for d in sam_node.devices if d.name == "uart0"), None)
        assert uart0 is not None
        assert len(uart0.requirement_ids) == 1
        assert "r10" in uart0.requirement_ids

        # Other devices should have no requirement_ids
        uart1 = next((d for d in sam_node.devices if d.name == "uart1"), None)
        assert uart1 is not None
        assert len(uart1.requirement_ids) == 0

    def test_read_connections(self):
        """Test that connections are correctly parsed."""
        # Prepare
        reader = DVReader()
        dv_file = self.get_test_data_file("deploymentview.dv.xml")
        assert dv_file.exists()

        # Read
        dv = reader.read(dv_file)

        # Verify connections were parsed
        assert len(dv.connections) == 1

        # Check connection details
        connection = dv.connections[0]
        assert connection.name == "Connection_1"
        assert connection.from_node == "x86 Linux C++_1"
        assert connection.from_port == "uart0"
        assert connection.to_bus == "ocarina_buses::serial.ccsds"
        assert connection.to_node == "SAM V71 RTEMS N7S_1"
        assert connection.to_port == "uart0"

    def test_read_messages(self):
        """Test that messages in connections are correctly parsed."""
        # Prepare
        reader = DVReader()
        dv_file = self.get_test_data_file("deploymentview.dv.xml")
        assert dv_file.exists()

        # Read
        dv = reader.read(dv_file)

        # Get the connection
        connection = dv.connections[0]

        # Verify messages
        assert len(connection.messages) == 2

        # Check message details
        msg_names = [m.name for m in connection.messages]
        assert "Message_1" in msg_names
        assert "Message_2" in msg_names

        # Check Message_1 details
        msg1 = next((m for m in connection.messages if m.name == "Message_1"), None)
        assert msg1 is not None
        assert msg1.from_function == "EGSE"
        assert msg1.from_interface == "tc"
        assert msg1.to_function == "Frontend"
        assert msg1.to_interface == "tc"

        # Check Message_2 details
        msg2 = next((m for m in connection.messages if m.name == "Message_2"), None)
        assert msg2 is not None
        assert msg2.from_function == "Frontend"
        assert msg2.from_interface == "tm"
        assert msg2.to_function == "EGSE"
        assert msg2.to_interface == "tm"

    def test_read_string(self):
        """Test reading from XML string."""
        reader = DVReader()

        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<DeploymentView version="1.0" UiFile="test.ui.xml" creatorHash="abc" modifierHash="def">
    <Node id="{test-id}" name="test_node" type="test_type" node_label="TestNode" namespace="test_ns">
        <Partition id="{part-id}" name="test_partition">
            <Function id="{func-id}" name="test_func" path="test/path"/>
        </Partition>
    </Node>
</DeploymentView>"""

        dv = reader.read_string(xml_content)

        assert dv.version == "1.0"
        assert dv.ui_file == "test.ui.xml"
        assert len(dv.nodes) == 1
        assert dv.nodes[0].name == "test_node"
        assert len(dv.nodes[0].partitions) == 1
        assert dv.nodes[0].partitions[0].name == "test_partition"

    def test_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent files."""
        reader = DVReader()

        with pytest.raises(FileNotFoundError):
            reader.read("nonexistent_file.dv.xml")
