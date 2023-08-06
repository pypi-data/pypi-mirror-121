"""
Creates all zip files.
Manifest exists in folder, so creating combine archives.
"""

from __future__ import absolute_import, print_function

import os
import shutil


def create_all_zip(base_dir, out_dir, extension):
    """Creates zip for all folders.

    :param base_dir:
    :param out_dir: output directory
    :param extension: file extension for zip file
    :return:
    """

    if not os.path.exists(base_dir):
        raise IOError

    # only in base dir, otherwise use os.walk for recursive subdirectories
    for directory in [f for f in os.listdir(base_dir) if os.path.isdir(f)]:

        if "_te_" in directory or directory == ".":
            continue
        create_zip_from_folder(directory, out_dir=out_dir, extension=extension)


def create_zip_from_folder(directory, out_dir, extension):
    """

    :param directory:
    :return:
    """

    if not extension.startswith("."):
        extension = "." + extension
    zip_file = os.path.join(out_dir, os.path.basename(directory) + extension)
    print(directory, "->", zip_file)
    shutil.make_archive(
        zip_file, "zip", directory
    )  # creates archive with added .zip extension
    shutil.move(zip_file + ".zip", zip_file)

    print("-" * 80)


if __name__ == "__main__":
    print("*" * 80)
    print("Creating OMEX archives from folders")
    # TODO: infer the data types and create real omex

    print("*" * 80)
    create_all_zip(base_dir=".", out_dir=".", extension="omex")
