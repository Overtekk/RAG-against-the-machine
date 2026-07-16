# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  index.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/03 09:27:09 by roandrie        #+#    #+#               #
#  Updated: 2026/07/16 21:16:23 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import json
import os
import bm25s
import Stemmer
from tqdm import tqdm
from .utils import load_files
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

    # - Save the chunks -
    _saving_chunks(metadatas_list, texts_list, data_directory)

    # - Build the index -
    _build_index(metadatas_list, texts_list, data_directory)


def _saving_chunks(
    metadatas_list: list[MinimalSource],
    texts_list: list[str],
    data_directory: dict[str, str]) -> None:
    print_rule()
    print("Saving raw chunks dataset...")

    # Create the structure of the json
    chunks_dataset: list[dict[str, str]] = []
    for metadata, raw_text in zip(metadatas_list, texts_list):
        chunks_dataset.append({
            "file_path": metadata["file_path"],
            "first_character_index": metadata["first_character_index"],
            "last_character_index": metadata["last_character_index"],
            "content": raw_text
        })

    # Saving the structure in a json file
    chunks_file_path = os.path.join(data_directory['chunk_dir'],
                                    'chunks_db.json')

    with open(chunks_file_path, 'w', encoding='utf-8') as f:
        json.dump(chunks_dataset, f, ensure_ascii=False, indent=4)

    print_log(f"Chunks database saved under '{chunks_file_path}'")

def _build_index(
    metadatas_list: list[MinimalSource],
    texts_list: list[str],
    data_directory: dict[str, str]) -> None:
    # Create a stemmer (get the root of multiples same words)
    stemmer = Stemmer.Stemmer('english')

    # - Constructing the index -
    print_rule()
    # Create the BM25 model
    retriever = bm25s.BM25()
    # Tokenize the corpus and only keep the ids
    tokens = bm25s.tokenize(
        texts_list, stopwords='en', stemmer=stemmer, show_progress=True,
        leave=True
    )
    # Index the corpus
    retriever.index(tokens, show_progress=True, leave_progress=True)
    # Save the array and the corpus
    retriever.save(
        data_directory['bm25_dir'], corpus=metadatas_list, show_progress=True)

    print_rule()
    print_log(f"BM25 index saved in '{data_directory['bm25_dir']}'.")
