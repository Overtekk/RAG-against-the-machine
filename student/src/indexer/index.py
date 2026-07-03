# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  index.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/03 09:27:09 by roandrie        #+#    #+#               #
#  Updated: 2026/07/03 11:37:57 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from .files import load_files


def indexer(
    vLLM_path: str, chunk_size: int, data_directory: dict[str, str]) -> None:

    loaded_files: list[tuple[str, str]] = load_files(vLLM_path)
    print(loaded_files)
