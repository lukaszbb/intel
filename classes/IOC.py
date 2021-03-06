#!/usr/bin/env python

"""Parse OpenIOC Files. Return a Dictionary With It's Properties."""

import sys  # Interact with the interpreter.

# Library for processing XML and HTML.
try:
    import lxml
    from lxml import etree

except ImportError:
    sys.exit(
        """\n
        You're Missing the LXML Module. Go here:
        http://lxml.de/installation.html\n
        """
    )


__program__ = "IOC.py"
__author__ = "Johnny C. Wachter"
__copyright__ = "Copyright (C) 2014 Johnny C. Wachter"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Johnny C. Wachter"
__contact__ = "wachter.johnny@gmail.com"
__status__ = "Development"


class IOC(object):

    """Parse IOC Files. Return a Dictionary With It's Properties."""

    def __init__(self, ioc_path, schema_path):
        """Instantiate the Class."""

        self.ioc_path = ioc_path
        self.schema_path = schema_path

    def valid_ioc(self):
        """Return if IOC is Valid."""

        ioc_path = self.ioc_path
        schema_path = self.schema_path

        # Validate XML file with an XSD file.
        parser = etree.XMLParser(dtd_validation=True)

        try:
            with open(schema_path) as schema_file:
                schema_data = etree.parse(schema_file)

            schema = etree.XMLSchema(schema_data)

        except:
            sys.exit("Could Not Parse XSD File: %s" % schema_path)

        try:
            with open(ioc_path) as ioc_file:
                ioc_data = etree.parse(ioc_file)

        except:
            sys.exit("Could Not Parse IOC File: %s" % ioc_path)

        if schema.validate(ioc_data):

            tree = etree.parse(ioc_path)  # Parse XML.

            root = tree.getroot()  # Get the entire document (root).

        return root

    def parse_ioc(self):
        """Parse IOC Files. Return a Dictionary With It's Properties."""

        root = self.valid_ioc()

        namespace = "{http://schemas.mandiant.com/2010/ioc}"  # Because...

        # Dictionary to house extracted data from IOC file.
        ioc = {
            'metadata': {
                'ioc_id': '',
                'last_modified': '',
                'short_description': '',
                'description': '',
                'keywords': '',
                'author': '',
                'created': ''
            },

            'definition': []  # Populated later. Store multiple IndicatorItems.
        }

        # Iterate the document and extract neccessary information.
        for xml_tag in root.iter("*"):

            # Increases readability and keeps lines a little bit shorter.
            attribute = xml_tag.attrib

            if xml_tag.tag == namespace + 'ioc':

                ioc['metadata']['ioc_id'] = attribute['id']
                ioc['metadata']['last_modified'] = attribute['last-modified']

            elif xml_tag.tag == namespace + 'short_description':

                ioc['metadata']['short_description'] = xml_tag.text

            elif xml_tag.tag == namespace + 'description':

                ioc['metadata']['description'] = xml_tag.text

            elif xml_tag.tag == namespace + 'keywords':

                ioc['metadata']['keywords'] = xml_tag.text

            elif xml_tag.tag == namespace + 'authored_by':

                ioc['metadata']['author'] = xml_tag.text

            elif xml_tag.tag == namespace + 'authored_date':

                ioc['metadata']['created'] = xml_tag.text

            elif xml_tag.tag == namespace + 'IndicatorItem':

                indicator_item = {
                    'indicator_item_id': '',
                    'condition': '',
                    'category': '',
                    'subcategory': '',
                    'type': '',
                    'indicator': ''
                }

                attrib_child1 = xml_tag[0].attrib
                attrib_child2 = xml_tag[1].attrib
                text_child2 = xml_tag[1].text

                indicator_item['indicator_item_id'] = attribute['id']
                indicator_item['condition'] = attribute['condition']
                indicator_item['category'] = attrib_child1['document']
                indicator_item['subcategory'] = attrib_child1['search']
                indicator_item['type'] = attrib_child2['type']
                indicator_item['indicator'] = text_child2

                ioc['definition'].append(indicator_item)

        return ioc
