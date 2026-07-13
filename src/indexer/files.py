# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  files.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/01 11:18:23 by roandrie        #+#    #+#               #
#  Updated: 2026/07/13 12:50:11 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import zipfile
import os

from src.utils import print_log, print_rule, check_file_extension


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
            if (check_file_extension(file, '.py') or
                    check_file_extension(file, '.md')):

                # Construct the filepath
                filepath: str = os.path.join(root, file)

                # Open the file
                try:
                    with open(filepath, encoding='utf-8') as f:
                        # Add the filepath and file content
                        files_list.append((filepath, f.read()))

                except PermissionError:
                    print_log(f"Permission error for file: {file}.", 'red')
                except Exception as e:
                    print_log(
                        f"Error while trying to open file: {file} with error "
                        f"{e}", 'red')

    return files_list
