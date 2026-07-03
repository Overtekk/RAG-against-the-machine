# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  files.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/01 11:18:23 by roandrie        #+#    #+#               #
#  Updated: 2026/07/03 11:47:28 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import zipfile
import os

from student.src.utils import print_log, print_rule


IGNORED_PATH = [
    '__pycache__', '.git'
]


def extract_archive(zip_path: str) -> None:
    print_rule()
    print_log("📁 Extracting ...")

    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall()
            print_log("✅ Zip extracted.", color='green')

    except zipfile.BadZipFile:
        raise ValueError("Error when extracting ZIP file.")

    except PermissionError as e:
        raise ValueError(e)


def load_files(vLLM_path: str) -> list[tuple[str, str]]:
    files_list: list[tuple[str, str]] = []

    for (root, dirs, filesname) in os.walk(
        vLLM_path, topdown=True, onerror=True, followlinks=False):
        # Ignore path
        dirs[:] = [d for d in dirs if d not in IGNORED_PATH]

        for file in filesname:
            files_list.append(dirs, file)

    return files_list
