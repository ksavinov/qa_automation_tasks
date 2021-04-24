# /usr/bin/python3
# -*- coding: utf-8 -*-
""" Copy files according with config file """
import os
import shutil
import xml.etree.ElementTree as ET

CONFIG_FILE = "config.xml"


def copy_files(config: str):
    """
    Copies files
    :param config: (str) config file in xml-format. For every three only these fields are available:
            source_path, destination_path, file_name
    :return: None
    """
    if config[-4:].lower() != ".xml":
        print("Wrong config file format!\nScript supports only xml-like files")
        return
    tree = ET.parse(config)
    root = tree.getroot()
    for child in root:
        try:
            src_path = os.path.join(child.attrib["source_path"], child.attrib["file_name"])
            dst_path = child.attrib["destination_path"]
            if not os.path.exists(dst_path):
                os.makedirs(dst_path, exist_ok=True)
            shutil.copy(src_path, dst_path)
        except KeyError as e:
            print("Wrong field in the confih file: {}".format(e))
            print("Script only supports these fields:\n-source_path\n-file_name\n-destination_path", end="\n\n")
            continue
        except OSError:
            print("Source path does not exist: {}".format(src_path), end="\n\n")
            continue


if __name__ == "__main__":
    copy_files(CONFIG_FILE)
