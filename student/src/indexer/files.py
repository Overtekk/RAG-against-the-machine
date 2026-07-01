# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  files.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/01 11:18:23 by roandrie        #+#    #+#               #
#  Updated: 2026/07/01 13:27:38 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import zipfile

from student.src.utils import print_log, print_rule


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
