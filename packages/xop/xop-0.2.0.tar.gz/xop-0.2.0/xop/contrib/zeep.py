from lxml import etree
from zeep.transports import Transport


class MtomTransport(Transport):
    def post_xml(self, address, envelope, headers):
        # body, headers = soap.parse_soap_11_mtom(envelope, headers)
        message = etree.tostring(envelope)

        # return self.post(address, message, headers)
        pass
