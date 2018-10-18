from lxml import etree
from os import path, system
from argparse import ArgumentParser

__authors__ = 'Nikolay Zaytsev, Artsiom Rachytski'

def create_or_get_xml(filename):
    filename_xml = filename.replace(".yang", ".xml")
    if not path.isfile(filename):
        return
    if path.isfile(filename_xml):
        print ('XML file aready exists, reading...',filename_xml)
    else:
        system("pyang -f yin {} > {}".format(filename, filename_xml))
    return filename_xml


def get_leafs(leaf_name, xml_file):
    try:
        with open(xml_file) as fl:
            xml_string = fl.read()
    except IOError:
        print("Can't open location %s" % xml_file)
        exit(44)
        return

    root = etree.XML(xml_string)
    tree = etree.ElementTree(root)

    # Get "None" namespace from root element of the tree. All children live in this ns
    # Using EXLT regex requires its own namespace as defined
    #
    ns = root.nsmap[None]
    regexp_ns = "http://exslt.org/regular-expressions"

    nss = {'ns': ns,
           're': regexp_ns
           }

    # Looking for elements in the tree by regex (e. g. element should contain specified name)
    #
    leafs = tree.xpath('.//ns:leaf[re:test(@name, "%s")]' % leaf_name, namespaces=nss)
    containers = tree.xpath('.//ns:container[re:test(@name, "%s")]' % leaf_name, namespaces=nss)
    groupings = tree.xpath('.//ns:grouping[re:test(@name, "%s")]' % leaf_name, namespaces=nss)

    elements = leafs + containers + groupings

    pseudopath = {}
    opt_num = 1

    # Get all parents iteratively bottom-up to determine full path
    #
    for e in elements:
        _pseudopath = []
        while e.getparent() is not None:
            _pseudopath.append(e.attrib['name'])
            e = e.getparent()
        pseudopath['opt%i' % opt_num] = '.'.join(reversed(_pseudopath))
        opt_num += 1

    return pseudopath.values()


def prettyprint(_items):
    print
    print('=' * 80)
    for key in _items:
        print(key)
    print('=' * 80)
    print


def parse_include_files(filename_yang, file_list):
    try:
        filename_xml = create_or_get_xml(filename_yang)
        XMLDoc = etree.parse(open(filename_xml))
        root = XMLDoc.getroot()
    except:
        print ('Please copy {} to your directory'.format(filename_yang))
        return
    for included_file in root:
        if 'include' in included_file.tag:
            file_yang = included_file.attrib['module'] + '.yang'
            parse_include_files(file_yang, file_list)
    file_list.append(filename_xml)
    return reversed(file_list)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("yang_model",
                        help="Include yang model to search in")
    parser.add_argument("variable",
                        help="Variable to look up")
    args = parser.parse_args()

    leaf_name = args.variable
    yang_file = args.yang_model
    file_lists = parse_include_files(yang_file, [])
    possible_values = []
    for xml_file in file_lists:
        print ('parsing {}'.format(xml_file))
        pseudopath = get_leafs(leaf_name, xml_file)
        possible_values += pseudopath
    prettyprint(possible_values)
