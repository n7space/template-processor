"""
Template Instantiator.

This module is responsible for instantiating Mako templates using the provided data.
"""

from templateprocessor.iv import InterfaceView
from templateprocessor.dv import DeploymentView
from templateprocessor.so import SystemObjectType, SystemObject
from typing import List, Dict
from mako.template import Template


class TemplateInstantiator:
    """
    Instantiator of Mako templates
    """

    system_object_types: Dict[str, SystemObjectType] = dict()
    values: Dict[str, str] = dict()
    interface_view: InterfaceView
    deployment_view: DeploymentView

    def __init__(
        self,
        interface_view: InterfaceView,
        deployment_view: DeploymentView,
        system_object_types: Dict[str, SystemObjectType],
        values: Dict[str, str],
    ):
        self.system_object_types = system_object_types
        self.interface_view = interface_view
        self.deployment_view = deployment_view
        self.values = values

    def instantiate(self, template: str, context_directory: str) -> str:
        mako_template = Template(text=template, module_directory=context_directory)

        context = {
            "system_object_types": self.system_object_types,
            "interface_view": self.interface_view,
            "deployment_view": self.deployment_view,
            "values": self.values,
        }

        instantiated_text = str(mako_template.render(**context))
        return instantiated_text
