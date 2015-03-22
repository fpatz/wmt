import argparse
import copy
import sys
from lxml import etree

SVG_PATH = etree.QName("{http://www.w3.org/2000/svg}path")
XLINK_HREF = etree.QName("{http://www.w3.org/1999/xlink}href")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    args = parser.parse_args()
    with open(args.infile) as infile:
        tree = etree.parse(infile)
    root = tree.getroot()
    root.insert(0, etree.XML("""
    <style>
    .clickable:hover {
      stroke: red;
      stroke-width: 24;
    }
    </style>
    """))
    found = tree.findall(SVG_PATH)
    for node in found:
        target = node.get("onclick")
        if target:
            inner = copy.copy(node)
            del inner.attrib["onclick"]
            inner.attrib["class"] = "clickable"
            node.tag = "a"
            for aname in node.attrib.keys():
                del node.attrib[aname]
            node.attrib[XLINK_HREF] = target
            node.attrib["target"] = "_top"
            node.append(inner)
    with open(args.outfile, "w") as outfile:
        tree.write(outfile, pretty_print=True)
    


if __name__ == "__main__":
    main()
