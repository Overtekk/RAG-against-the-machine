# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  index.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/03 09:27:09 by roandrie        #+#    #+#               #
#  Updated: 2026/07/03 14:30:29 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import bm25s
from tqdm import tqdm

from .files import load_files
from student.src.utils import print_log


def indexer(
    vLLM_path: str, chunk_size: int, data_directory: dict[str, str]) -> None:

    # Load all files
    print_log(f"Reading files in '{vLLM_path}'...")
    loaded_files: list[tuple[str, str]] = load_files(vLLM_path)
    print_log(f"{len(loaded_files)} files found!")

    # Chunking
    test = []
    for file_path, content in tqdm(loaded_files, desc='Chunking'):
        test.append(content)

    # Constructing the index
    print_log("Constructing the BM25S index...")
    retriever = bm25s.BM25(corpus=loaded_files)
    retriever.index(bm25s.tokenize(test, show_progress=True))

    retriever.save(data_directory['bm25_dir'])
    print_log(f"BM25 index saved in '{data_directory['bm25_dir']}'.")
