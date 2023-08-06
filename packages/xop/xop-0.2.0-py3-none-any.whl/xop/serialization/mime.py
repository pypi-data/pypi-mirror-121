from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from typing import Optional

from ..datatypes import BinaryContent, XopPackage


def _serialize_xop_binary_content_to_mime(binary_content: BinaryContent) -> MIMEBase:
    mime_type, mime_subtype = binary_content.content_type.split("/")

    mime_binary_part = MIMEBase(mime_type, mime_subtype)
    mime_binary_part.add_header("Content-Transfer-Encoding", "binary")
    mime_binary_part.add_header("Content-ID", f"<{binary_content.content_id}>")

    mime_binary_part.set_payload(binary_content.data.read())

    return mime_binary_part


def _serialize_xop_document_to_mime(xop_document: str, cid: str) -> MIMEApplication:
    mime_root_part = MIMEApplication(
        xop_document,
        "xop+xml",
        encoders.encode_7or8bit,
        type="text/xml",
        charset="utf-8",
    )
    mime_root_part.add_header("Content-ID", f"<{cid}>")

    return mime_root_part


def serialize_to_mime(
    xop_pkg: XopPackage, xop_doc_cid: Optional[str] = "<xop-document>"
) -> MIMEMultipart:
    mime_multipart_message = MIMEMultipart(
        "related",
        boundary="MIME_boundary",
        type="application/xop+xml",
        start=xop_doc_cid,
        start_info="text/xml",
    )

    mime_root_part = _serialize_xop_document_to_mime(xop_pkg.xop_document, xop_doc_cid)
    mime_multipart_message.attach(mime_root_part)

    for binary_content in xop_pkg.optimized_content:
        mime_binary_content_part = _serialize_xop_binary_content_to_mime(binary_content)
        mime_multipart_message.attach(mime_binary_content_part)

    return mime_multipart_message
