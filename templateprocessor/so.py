"""
OPUS2 System Object (SO) data model classes.

This module provides Python classes that reflect the OPUS2 System Object data.
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class SystemObject:
    """System Object"""

    values: Dict[str, str] = field(default_factory=dict)


@dataclass
class SystemObjectType:
    """Definition of a System Object Type"""

    property_names: List[str] = field(default_factory=list)
    instances: List[SystemObject] = field(default_factory=list)
