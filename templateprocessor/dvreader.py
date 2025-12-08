"""
TASTE Deployment View XML Reader.

This module provides functionality to parse TASTE Deployment View XML files
and construct DeploymentView data model instances.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union

from templateprocessor.dv import (
    DeploymentView,
    Node,
    Partition,
    DeploymentFunction,
    Device,
    Connection,
    Message,
)


class DVReader:
    """
    Reader for TASTE Deployment View XML files.

    Parses XML files conforming to the TASTE Deployment View schema and
    constructs corresponding DeploymentView objects.

    Example:
        reader = DVReader()
        deployment_view = reader.read("deploymentview.dv.xml")
    """

    def read(self, file_path: Union[str, Path]) -> DeploymentView:
        """
        Read and parse a TASTE Deployment View XML file.

        Args:
            file_path: Path to the DV XML file

        Returns:
            DeploymentView object populated with parsed data

        Raises:
            FileNotFoundError: If the file does not exist
            xml.etree.ElementTree.ParseError: If XML is malformed
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Deployment View file not found: {file_path}")

        tree = ET.parse(file_path)
        root = tree.getroot()

        return self._parse_deployment_view(root)

    def read_string(self, xml_content: str) -> DeploymentView:
        """
        Read and parse TASTE Deployment View XML from a string.

        Args:
            xml_content: XML content as string

        Returns:
            DeploymentView object populated with parsed data

        Raises:
            xml.etree.ElementTree.ParseError: If XML is malformed
        """
        root = ET.fromstring(xml_content)
        return self._parse_deployment_view(root)

    def _parse_deployment_view(self, root: ET.Element) -> DeploymentView:
        """Parse the root DeploymentView element."""
        dv = DeploymentView(
            version=root.get("version", ""),
            ui_file=root.get("UiFile", ""),
            creator_hash=root.get("creatorHash", ""),
            modifier_hash=root.get("modifierHash", ""),
        )

        # Parse all Node elements
        for node_elem in root.findall("Node"):
            node = self._parse_node(node_elem)
            dv.nodes.append(node)

        # Parse all Connection elements
        for conn_elem in root.findall("Connection"):
            connection = self._parse_connection(conn_elem)
            dv.connections.append(connection)

        return dv

    def _parse_node(self, elem: ET.Element) -> Node:
        """Parse a Node element."""
        # Parse requirement_ids if present
        requirement_ids = []
        req_ids_str = elem.get("requirement_ids", "")
        if req_ids_str:
            requirement_ids = [
                rid.strip() for rid in req_ids_str.split(",") if rid.strip()
            ]

        node = Node(
            id=elem.get("id", ""),
            name=elem.get("name", ""),
            type=elem.get("type", ""),
            node_label=elem.get("node_label", ""),
            namespace=elem.get("namespace", ""),
            requirement_ids=requirement_ids,
        )

        # Parse partitions
        for partition_elem in elem.findall("Partition"):
            partition = self._parse_partition(partition_elem)
            node.partitions.append(partition)

        # Parse devices
        for device_elem in elem.findall("Device"):
            device = self._parse_device(device_elem)
            node.devices.append(device)

        return node

    def _parse_partition(self, elem: ET.Element) -> Partition:
        """Parse a Partition element."""
        partition = Partition(
            id=elem.get("id", ""),
            name=elem.get("name", ""),
        )

        # Parse functions
        for func_elem in elem.findall("Function"):
            function = self._parse_deployment_function(func_elem)
            partition.functions.append(function)

        return partition

    def _parse_deployment_function(self, elem: ET.Element) -> DeploymentFunction:
        """Parse a Function element within a Partition."""
        return DeploymentFunction(
            id=elem.get("id", ""),
            name=elem.get("name", ""),
            path=elem.get("path", ""),
        )

    def _parse_device(self, elem: ET.Element) -> Device:
        """Parse a Device element."""
        # Parse requirement_ids if present
        requirement_ids = []
        req_ids_str = elem.get("requirement_ids", "")
        if req_ids_str:
            requirement_ids = [
                rid.strip() for rid in req_ids_str.split(",") if rid.strip()
            ]

        return Device(
            id=elem.get("id", ""),
            name=elem.get("name", ""),
            requires_bus_access=elem.get("requires_bus_access", ""),
            port=elem.get("port", ""),
            asn1file=elem.get("asn1file", ""),
            asn1type=elem.get("asn1type", ""),
            asn1module=elem.get("asn1module", ""),
            namespace=elem.get("namespace", ""),
            extends=elem.get("extends", ""),
            impl_extends=elem.get("impl_extends", ""),
            bus_namespace=elem.get("bus_namespace", ""),
            requirement_ids=requirement_ids,
        )

    def _parse_connection(self, elem: ET.Element) -> Connection:
        """Parse a Connection element."""
        connection = Connection(
            id=elem.get("id", ""),
            name=elem.get("name", ""),
            from_node=elem.get("from_node", ""),
            from_port=elem.get("from_port", ""),
            to_bus=elem.get("to_bus", ""),
            to_node=elem.get("to_node", ""),
            to_port=elem.get("to_port", ""),
        )

        # Parse messages
        for msg_elem in elem.findall("Message"):
            message = self._parse_message(msg_elem)
            connection.messages.append(message)

        return connection

    def _parse_message(self, elem: ET.Element) -> Message:
        """Parse a Message element."""
        return Message(
            id=elem.get("id", ""),
            name=elem.get("name", ""),
            from_function=elem.get("from_function", ""),
            from_interface=elem.get("from_interface", ""),
            to_function=elem.get("to_function", ""),
            to_interface=elem.get("to_interface", ""),
        )
