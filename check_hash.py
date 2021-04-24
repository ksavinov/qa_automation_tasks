# /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Checking files hash sums according with hashing algorithms (MD5/SHA1/SHA256)
"""
import os
import sys
import hashlib

# File stores data in format:
# file_01.bin md5 aaeab83fcc93cd3ab003fa8bfd8d8906
FILE_NAME = "hash_files_list.txt"
FILES_DATA = []


def handling_input_paths():
    """
    Checks 2 input arguments: input_file_path, hash_files_path
    input_file_path: path to FILE_NAME
    hash_files_path: path to directory where files to check are stored
    :return: input_file_path
    """
    try:
        path_arg1 = sys.argv[1]
        hash_files_path = sys.argv[2]
        path_arg1 = os.path.join(path_arg1, FILE_NAME)
        os.chdir(hash_files_path)
        return path_arg1
    except IndexError:
        print("Please, specify the following input arguments:\n path to hash_files_list.txt\n path to files to check")
        quit()
    except OSError:
        print("Wrong path to files to check: %s" % path_arg1)
        quit()


def add_hash_algorithms():
    """
    Calls constructors for md5, sha1, sha256
    :return: md5, sha1, sha256
    """
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    return md5, sha1, sha256


def parse_input_file(file_path):
    """
    Parses file where data is stored and adds data to the nested list.
    :param file_path: D:\working_directory\hash_files_list.txt
    :return: None
    """
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line == "\n":
                    continue
                FILES_DATA.append(line.split())
    except OSError:
        print("Wrong path to the input file: %s" % file_path)
        quit()


def get_digest_by_hashing_algorithm(algorithm, file_content):
    """
    Checks file's hash sum
    :param algorithm: md5 / sha1 / sha256
    :param file_content: file content
    :return: False (if unsupported hash algorithm) / file's real hash sum
    """
    if algorithm == "md5":
        md5_hash.update(file_content)
        return md5_hash.hexdigest()
    elif algorithm == "sha1":
        sha1_hash.update(file_content)
        return sha1_hash.hexdigest()
    elif algorithm == "sha256":
        sha256_hash.update(file_content)
        return sha256_hash.hexdigest()
    else:
        return False


def assert_checksum(real_checksum, input_file_checksum):
    """
    Checks file's checksum
    :param real_checksum: file's real checksum
    :param input_file_checksum: checksum from FILE_NAME
    :return: None
    """
    if real_checksum == input_file_checksum:
        print("OK")
    else:
        print("FAIL")


if __name__ == "__main__":
    input_file_path = handling_input_paths()
    parse_input_file(input_file_path)
    md5_hash, sha1_hash, sha256_hash = add_hash_algorithms()

    for file_data in FILES_DATA:
        try:
            a_file = open(file_data[0], "rb")
            print(file_data[0], end=" ")
        except OSError:
            print("{} NOT FOUND".format(file_data[0]))
            continue

        content = a_file.read()

        digest = get_digest_by_hashing_algorithm(file_data[1], content)
        if not digest:
            print("Unknown hashing algorithm!")
            continue

        assert_checksum(digest, file_data[2])
