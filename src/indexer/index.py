# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  index.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/03 09:27:09 by roandrie        #+#    #+#               #
#  Updated: 2026/07/15 10:25:12 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import bm25s
from tqdm import tqdm

from .files import load_files
from .chunker import ChunkerEngine
from src.utils import print_log, print_rule
from src.model import MinimalSource


def indexer(
    vLLM_path: str, chunk_size: int, data_directory: dict[str, str]) -> None:

    # - Load all files -
    print_log(f"Reading files in '{vLLM_path}'...")
    loaded_files: list[tuple[str, str]] = load_files(vLLM_path)
    print_log(f"{len(loaded_files)} files found!\n")
    print_rule()

    # - Chunking -
    # Init the chunker class with the chunk size
    the_chunker = ChunkerEngine(chunk_size)

    metadatas_list: list[MinimalSource] = []
    texts_list: list[str] = []

    # Go throught all files and, if the file is not empty, add the
    # MinimalSource to the metadata list, and the content is the texts list.
    # The metadata will be the corpus.
    for file_path, content in tqdm(loaded_files, desc='Chunking'):
        chunked_file = the_chunker.process(file_path, content)

        if chunked_file:
            for metadata, raw_text in chunked_file:
                # Note: transform the metadata into dict because bm25 doesn't
                # like object other than str, dict and list.
                metadatas_list.append(metadata.model_dump())
                texts_list.append(raw_text)

    # - Constructing the index -
    print_rule()
    retriever = bm25s.BM25(corpus=metadatas_list)
    tokens = bm25s.tokenize(texts_list, show_progress=True, leave=True)
    retriever.index(tokens)
    retriever.save(data_directory['bm25_dir'])

    print_rule()
    print_log(f"BM25 index saved in '{data_directory['bm25_dir']}'.")
