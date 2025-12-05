"""
Template Instantiator.

This module is responsible for instantiating Mako templates using the provided data.
"""

from templateprocessor.iv import InterfaceView
from templateprocessor.so import SystemObjectType, SystemObject
from typing import List
from mako.template import Template


class TemplateInstantiator:
    """
    Instantiator of Mako templates
    """

    system_object_types: List[SystemObjectType] = list()
    interface_view: InterfaceView

    def __init__(
        self, interface_view: InterfaceView, system_object_types: List[SystemObjectType]
    ):
        self.system_object_types = system_object_types
        self.interface_view = interface_view

    def instantiate(self, template: str, context_directory: str) -> str:
        mako_template = Template(text=template, module_directory=context_directory)

        context = {
            "system_object_types": self.system_object_types,
            "interface_view": self.interface_view,
        }

        instantiated_text = str(mako_template.render(**context))
        return instantiated_text
