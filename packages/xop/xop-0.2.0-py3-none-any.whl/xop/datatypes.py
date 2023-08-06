from dataclasses import dataclass
from typing import BinaryIO, List, NamedTuple

from lxml import etree

"""Note that representing an XML Infoset by `etree._ElementTree` is
formally inadequate, but suffices pragmatically for now.
"""

XmlInfoset = etree._ElementTree
XopInfoset = XmlInfoset
XmlDocument = str
XopDocument = XmlDocument


class BinaryContent(NamedTuple):
    content_id: str
    content_type: str
    data: BinaryIO


@dataclass
class XopPackage:
    """XOP Package."""

    xop_infoset: XopInfoset
    optimized_content: List[BinaryContent]

    @property
    def xop_document(self):
        return etree.tostring(self.xop_infoset, encoding=str)
