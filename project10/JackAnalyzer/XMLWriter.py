from xml.etree.ElementTree import Element, SubElement, ElementTree, indent

class XMLWriter:
    def __init__(self, output_filename, root_name):
        self.output_filename = output_filename
        self.root_element = Element(root_name)
        self.sub_root_table = [self.root_element]

    def write(self, key, value):
        assert(self.sub_root_table)
        SubElement(self.sub_root_table[-1], key).text = value

    def write_sub_root(self, key):
        element = SubElement(self.sub_root_table[-1], key)
        element.text = "\n"

        self.sub_root_table.append(element)

    def end_sub_root(self):
        self.sub_root_table.pop()

    def write_end(self):
        indent(self.root_element)
        result_tree = ElementTree(self.root_element)
        result_tree.write(self.output_filename + '.xml')