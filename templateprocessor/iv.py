"""
TASTE Interface View (IV) data model classes.

This module provides Python classes that reflect the schema/structure of
TASTE Interface View XML files, allowing for parsing, manipulation, and
generation of IV data.
"""

from dataclasses import dataclass, field, fields
from typing import List, Optional, Literal
from enum import Enum


class InterfaceKind(str, Enum):
    """Types of interfaces in TASTE."""

    SPORADIC = "Sporadic"
    CYCLIC = "Cyclic"
    PROTECTED = "Protected"
    UNPROTECTED = "Unprotected"


class Encoding(str, Enum):
    """Parameter encoding types."""

    NATIVE = "NATIVE"
    UPER = "UPER"
    ACN = "ACN"


class Language(str, Enum):
    """Programming languages supported in TASTE."""

    SDL = "SDL"
    C = "C"
    ADA = "Ada"
    CPP = "C++"
    SIMULINK = "Simulink"
    QGenc = "QGenc"


@dataclass
class Property:
    """Generic property/attribute with name-value pair."""

    name: str
    value: str


@dataclass
class InterfaceParameter:
    """Parameter for an interface."""

    name: str
    type: str
    encoding: Encoding = Encoding.NATIVE


@dataclass
class InputParameter(InterfaceParameter):
    """Input parameter for an interface."""

    pass


@dataclass
class OutputParameter(InterfaceParameter):
    """Output parameter for an interface."""

    pass


@dataclass
class FunctionInterface:
    """Function interface."""

    id: str
    name: str
    kind: InterfaceKind
    enable_multicast: bool = True
    layer: str = "default"
    required_system_element: bool = False
    is_simulink_interface: bool = False
    simulink_full_interface_ref: str = ""
    wcet: int = 0
    stack_size: Optional[int] = None
    queue_size: Optional[int] = None
    miat: Optional[int] = None
    period: Optional[int] = None
    dispatch_offset: Optional[int] = None
    priority: Optional[int] = None
    input_parameters: List[InputParameter] = field(default_factory=list)
    output_parameters: List[OutputParameter] = field(default_factory=list)
    properties: List[Property] = field(default_factory=list)


@dataclass
class ProvidedInterface(FunctionInterface):
    """Provided interface - implemented by a function"""

    pass


@dataclass
class RequiredInterface(FunctionInterface):
    """Required interface - required by a function"""

    pass


@dataclass
class Implementation:
    """Function implementation details."""

    name: str
    language: Language


@dataclass
class Function:
    """TASTE Function - a software component in the system."""

    id: str
    name: str
    is_type: bool
    language: Language
    default_implementation: str = "default"
    fixed_system_element: bool = False
    required_system_element: bool = False
    instances_min: int = 1
    instances_max: int = 1
    startup_priority: int = 1
    instance_of: Optional[str] = None  # For instances of function types
    type_language: Optional[Language] = None  # For function types
    provided_interfaces: List[ProvidedInterface] = field(default_factory=list)
    required_interfaces: List[RequiredInterface] = field(default_factory=list)
    implementations: List[Implementation] = field(default_factory=list)
    properties: List[Property] = field(default_factory=list)
    nested_functions: List["Function"] = field(default_factory=list)
    nested_connections: List["Connection"] = field(default_factory=list)


@dataclass
class ConnectionEndpoint:
    """Connection endpoint."""

    iface_id: str
    function_name: str
    iface_name: str


@dataclass
class ConnectionSource(ConnectionEndpoint):
    """Source endpoint of a connection."""

    pass


@dataclass
class ConnectionTarget(ConnectionEndpoint):
    """Target endpoint of a connection."""

    pass


@dataclass
class Connection:
    """Connection between two interfaces."""

    id: str
    required_system_element: bool = False
    name: str = None
    source: ConnectionSource = None
    target: ConnectionTarget = None


@dataclass
class Comment:
    """Comment/annotation in the interface view."""

    id: str
    name: str
    required_system_element: bool = False


@dataclass
class Layer:
    """Visual layer for organizing the interface view."""

    name: str
    is_visible: bool = True


@dataclass
class InterfaceView:
    """
    Root element representing a TASTE Interface View.

    This is the main data structure that contains all functions, connections,
    and other elements that define a TASTE system's interface architecture.
    """

    version: str
    asn1file: str
    UiFile: str
    modifierHash: str
    functions: List[Function] = field(default_factory=list)
    connections: List[Connection] = field(default_factory=list)
    comments: List[Comment] = field(default_factory=list)
    layers: List[Layer] = field(default_factory=list)
