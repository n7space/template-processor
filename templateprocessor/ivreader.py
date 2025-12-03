"""
TASTE Interface View XML Reader.

This module provides functionality to parse TASTE Interface View XML files
and construct InterfaceView data model instances.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union

from templateprocessor.iv import (
    InterfaceView,
    Function,
    FunctionInterface,
    ProvidedInterface,
    RequiredInterface,
    InterfaceParameter,
    InputParameter,
    OutputParameter,
    Implementation,
    Connection,
    ConnectionSource,
    ConnectionTarget,
    Comment,
    Layer,
    Property,
    Language,
    Encoding,
    InterfaceKind,
)


class IVReader:
    """
    Reader for TASTE Interface View XML files.

    Parses XML files conforming to the TASTE Interface View schema and
    constructs corresponding InterfaceView objects.

    Example:
        reader = IVReader()
        interface_view = reader.read("simple.iv.xml")
    """

    def read(self, file_path: Union[str, Path]) -> InterfaceView:
        """
        Read and parse a TASTE Interface View XML file.

        Args:
            file_path: Path to the IV XML file

        Returns:
            InterfaceView object populated with parsed data

        Raises:
            FileNotFoundError: If the file does not exist
            xml.etree.ElementTree.ParseError: If XML is malformed
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Interface View file not found: {file_path}")

        tree = ET.parse(file_path)
        root = tree.getroot()

        return self._parse_interface_view(root)

    def read_string(self, xml_content: str) -> InterfaceView:
        """
        Read and parse TASTE Interface View XML from a string.

        Args:
            xml_content: XML content as string

        Returns:
            InterfaceView object populated with parsed data

        Raises:
            xml.etree.ElementTree.ParseError: If XML is malformed
        """
        root = ET.fromstring(xml_content)
        return self._parse_interface_view(root)

    def _parse_interface_view(self, root: ET.Element) -> InterfaceView:
        """Parse the root InterfaceView element."""
        iv = InterfaceView(
            version=root.get("version", ""),
            asn1file=root.get("asn1file", ""),
            uiFile=root.get("UiFile", ""),
            modifierHash=root.get("modifierHash", ""),
        )

        # Parse all Function elements
        for func_elem in root.findall("Function"):
            function = self._parse_function(func_elem)
            iv.functions.append(function)

        # Parse all Connection elements
        for conn_elem in root.findall("Connection"):
            connection = self._parse_connection(conn_elem)
            iv.connections.append(connection)

        # Parse all Comment elements
        for comment_elem in root.findall("Comment"):
            comment = self._parse_comment(comment_elem)
            iv.comments.append(comment)

        # Parse all Layer elements
        for layer_elem in root.findall("Layer"):
            layer = self._parse_layer(layer_elem)
            iv.layers.append(layer)

        return iv

    def _parse_function(self, elem: ET.Element) -> Function:
        """Parse a Function element."""
        function = Function(
            id=elem.get("id", ""),
            name=elem.get("name", ""),
            is_type=elem.get("is_type", "NO") == "YES",
            language=Language(elem.get("language", ""))
            if elem.get("language")
            else None,
            default_implementation=elem.get("default_implementation", "default"),
            fixed_system_element=elem.get("fixed_system_element", "NO") == "YES",
            required_system_element=elem.get("required_system_element", "NO") == "YES",
            instances_min=int(elem.get("instances_min", "1")),
            instances_max=int(elem.get("instances_max", "1")),
            startup_priority=int(elem.get("startup_priority", "1")),
            instance_of=elem.get("instance_of"),
            type_language=Language(elem.get("type_language"))
            if elem.get("type_language")
            else None,
        )

        # Parse properties
        for prop_elem in elem.findall("Property"):
            prop = self._parse_property(prop_elem)
            function.properties.append(prop)

        # Parse provided interfaces
        for pi_elem in elem.findall("Provided_Interface"):
            pi = self._parse_provided_interface(pi_elem)
            function.provided_interfaces.append(pi)

        # Parse required interfaces
        for ri_elem in elem.findall("Required_Interface"):
            ri = self._parse_required_interface(ri_elem)
            function.required_interfaces.append(ri)

        # Parse implementations
        implementations_elem = elem.find("Implementations")
        if implementations_elem is not None:
            for impl_elem in implementations_elem.findall("Implementation"):
                impl = self._parse_implementation(impl_elem)
                function.implementations.append(impl)

        # Parse nested functions
        for nested_elem in elem.findall("Function"):
            nested_function = self._parse_function(nested_elem)
            function.nested_functions.append(nested_function)

        # Parse nested connections
        for nested_conn_elem in elem.findall("Connection"):
            nested_connection = self._parse_connection(nested_conn_elem)
            function.nested_connections.append(nested_connection)

        return function

    def _parse_interface(self, elem: ET.Element) -> FunctionInterface:
        """Parse an interface element."""
        iface = FunctionInterface(
            id=elem.get("id", ""),
            name=elem.get("name", ""),
            kind=InterfaceKind(elem.get("kind", "")),
            enable_multicast=elem.get("enable_multicast", "true") == "true",
            layer=elem.get("layer", "default"),
            required_system_element=elem.get("required_system_element", "NO") == "YES",
            is_simulink_interface=elem.get("is_simulink_interface", "false") == "true",
            simulink_full_interface_ref=elem.get("simulink_full_interface_ref", ""),
            wcet=int(elem.get("wcet", "0")),
            stack_size=int(elem.get("stack_size")) if elem.get("stack_size") else None,
            queue_size=int(elem.get("queue_size")) if elem.get("queue_size") else None,
            miat=int(elem.get("miat")) if elem.get("miat") else None,
            period=int(elem.get("period")) if elem.get("period") else None,
            dispatch_offset=int(elem.get("dispatch_offset"))
            if elem.get("dispatch_offset")
            else None,
            priority=int(elem.get("priority")) if elem.get("priority") else None,
        )

        # Parse input parameters
        for param_elem in elem.findall("Input_Parameter"):
            param = self._parse_input_parameter(param_elem)
            iface.input_parameters.append(param)

        # Parse output parameters
        for param_elem in elem.findall("Output_Parameter"):
            param = self._parse_output_parameter(param_elem)
            iface.output_parameters.append(param)

        # Parse properties
        for prop_elem in elem.findall("Property"):
            prop = self._parse_property(prop_elem)
            iface.properties.append(prop)

        return iface

    def _parse_provided_interface(self, elem: ET.Element) -> ProvidedInterface:
        """Parse a Provided_Interface element."""
        pi = ProvidedInterface(**vars(self._parse_interface(elem)))
        return pi

    def _parse_required_interface(self, elem: ET.Element) -> RequiredInterface:
        """Parse a Required_Interface element."""
        ri = RequiredInterface(**vars(self._parse_interface(elem)))
        return ri

    def _parse_parameter(self, elem: ET.Element) -> InterfaceParameter:
        """Parse an InterfaceParameter element."""
        return InterfaceParameter(
            name=elem.get("name", ""),
            type=elem.get("type", ""),
            encoding=Encoding(elem.get("encoding", "NATIVE")),
        )

    def _parse_input_parameter(self, elem: ET.Element) -> InputParameter:
        """Parse an Input_Parameter element."""
        return InputParameter(**vars(self._parse_parameter(elem)))

    def _parse_output_parameter(self, elem: ET.Element) -> OutputParameter:
        """Parse an Output_Parameter element."""
        return OutputParameter(**vars(self._parse_parameter(elem)))

    def _parse_implementation(self, elem: ET.Element) -> Implementation:
        """Parse an Implementation element."""
        return Implementation(
            name=elem.get("name", ""),
            language=Language(elem.get("language", "")),
        )

    def _parse_connection(self, elem: ET.Element) -> Connection:
        """Parse a Connection element."""
        connection = Connection(
            id=elem.get("id", ""),
            required_system_element=elem.get("required_system_element", "NO") == "YES",
            name=elem.get("name"),
        )

        # Parse source
        source_elem = elem.find("Source")
        if source_elem is not None:
            pi_name = source_elem.get("pi_name")
            ri_name = source_elem.get("ri_name")
            connection.source = ConnectionSource(
                iface_id=source_elem.get("iface_id", ""),
                function_name=source_elem.get("func_name", ""),
                iface_name=pi_name if pi_name is not None else ri_name,
            )

        # Parse target
        target_elem = elem.find("Target")
        if target_elem is not None:
            pi_name = target_elem.get("pi_name")
            ri_name = target_elem.get("ri_name")
            connection.target = ConnectionTarget(
                iface_id=target_elem.get("iface_id", ""),
                function_name=target_elem.get("func_name", ""),
                iface_name=pi_name if pi_name is not None else ri_name,
            )

        return connection

    def _parse_comment(self, elem: ET.Element) -> Comment:
        """Parse a Comment element."""
        return Comment(
            id=elem.get("id", ""),
            name=elem.get("name", ""),
            required_system_element=elem.get("required_system_element", "NO") == "YES",
        )

    def _parse_layer(self, elem: ET.Element) -> Layer:
        """Parse a Layer element."""
        return Layer(
            name=elem.get("name", ""),
            is_visible=elem.get("is_visible", "true") == "true",
        )

    def _parse_property(self, elem: ET.Element) -> Property:
        """Parse a Property element."""
        return Property(
            name=elem.get("name", ""),
            value=elem.get("value", ""),
        )
