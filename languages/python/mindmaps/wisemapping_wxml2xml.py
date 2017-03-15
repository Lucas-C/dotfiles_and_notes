#!/usr/bin/python3

import xml.dom.minidom, sys

with open(sys.argv[1]) as xml_file:
    tree = xml.dom.minidom.parseString(xml_file.read())
xml_map = tree.getElementsByTagName('xml')[0].childNodes[0].wholeText
pretty_xml = xml.dom.minidom.parseString(xml_map).toprettyxml(indent='    ')
print(pretty_xml)

