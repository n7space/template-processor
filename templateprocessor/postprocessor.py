"""
Postprocessor.

This module is responsible for postprocessing the instantiated text into the target format.
"""

from enum import Enum
from templateprocessor import md2docx
from abc import ABC, abstractmethod
from typing import Dict
import markdown2


class PostprocessorType(Enum):
    NONE = "none"
    MD2HTML = "md2html"
    HTML2DOCX = "html2docx"
    MD2DOCX = "md2docx"


class AbstractPostprocessor(ABC):

    @abstractmethod
    def process(self, text: str, base_file_name: str) -> None:
        """
        Process the input text and write to output file.

        Args:
            text: Input text string to process
            base_file_name: Path to output file, without extension
        """
        pass


class Md2docxPostprocessor(AbstractPostprocessor):

    def process(self, text: str, base_file_name: str) -> None:
        output_file_name = f"{base_file_name}.docx"
        md2docx.markdown_to_word_file(text, output_file_name)


class Md2HtmlPostprocessor(AbstractPostprocessor):

    def process(self, text: str, base_file_name: str) -> None:
        output_file_name = f"{base_file_name}.html"
        html_content = markdown2.markdown(text, extras=["tables", "wiki-tables"])
        with open(output_file_name, "w") as f:
            f.write(html_content)


class PassthroughPostprocessor(AbstractPostprocessor):

    def process(self, text: str, base_file_name: str) -> None:
        output_file_name = f"{base_file_name}.md"
        with open(output_file_name, "w") as f:
            f.write(text)


class Postprocessor:
    registry: Dict[PostprocessorType, AbstractPostprocessor]

    def __init__(self, registry: Dict[PostprocessorType, AbstractPostprocessor]):
        self.registry = registry

    def process(self, postprocessor_type: PostprocessorType, text: str, base_file_name: str) -> None:
        """
        Process the input text and write to output file based on processor type.

        Args:
            postprocessor_type: Desired postprocessor type
            text: Input text string to process
            base_file_name: Path to output file, without extension
        """
        if not postprocessor_type in self.registry.keys():
            raise ValueError(f"Not supported postprocessor {postprocessor_type.value}")
        self.registry[postprocessor_type].process(text, base_file_name)
