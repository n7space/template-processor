"""
TASTE Deployment View (DV) data model classes.

This module provides Python classes that reflect the schema/structure of
TASTE Deployment View XML files, allowing for parsing, manipulation, and
generation of DV data.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DeploymentFunction:
    """Function deployed to a partition."""

    id: str
    name: str
    path: str


@dataclass
class Partition:
    """
    Partition within a node.

    A partition represents an execution context that can host one or more
    functions (software components).
    """

    id: str
    name: str
    functions: List[DeploymentFunction] = field(default_factory=list)


@dataclass
class Device:
    """
    Hardware device attached to a node.

    Devices represent connection hardpoints (e.g., UART, TCP/UDP ports) that
    provide bus access for communication.
    """

    id: str
    name: str
    requires_bus_access: str
    port: str
    asn1file: str
    asn1type: str
    asn1module: str
    namespace: str
    extends: str
    impl_extends: str
    bus_namespace: str
    requirement_ids: List[str] = field(default_factory=list)


@dataclass
class Node:
    """
    Deployment node (processor/platform).

    A node represents a physical or virtual hardware platform that can host
    partitions and devices. Examples include embedded processors, Linux systems,
    or other execution platforms.
    """

    id: str
    name: str
    type: str
    node_label: str
    namespace: str
    partitions: List[Partition] = field(default_factory=list)
    devices: List[Device] = field(default_factory=list)
    requirement_ids: List[str] = field(default_factory=list)


@dataclass
class Message:
    """
    Message routed through a connection.

    Represents data flow from one function's interface to another function's
    interface over a physical connection.
    """

    id: str
    name: str
    from_function: str
    from_interface: str
    to_function: str
    to_interface: str


@dataclass
class Connection:
    """
    Physical connection between nodes.

    Represents a communication link between devices on different nodes,
    potentially through a bus. Contains the messages that are routed
    through this connection.
    """

    id: str
    name: str
    from_node: str
    from_port: str
    to_bus: str
    to_node: str
    to_port: str
    messages: List[Message] = field(default_factory=list)


@dataclass
class DeploymentView:
    """
    Root element representing a TASTE Deployment View.

    This is the main data structure that contains all nodes, connections,
    and other elements that define how a TASTE system is deployed to
    physical/virtual hardware.
    """

    version: str = ""
    ui_file: str = ""
    creator_hash: str = ""
    modifier_hash: str = ""
    nodes: List[Node] = field(default_factory=list)
    connections: List[Connection] = field(default_factory=list)
