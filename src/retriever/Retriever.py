# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Retriever.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/17 12:07:28 by roandrie        #+#    #+#               #
#  Updated: 2026/07/17 14:31:54 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any
import os
import bm25s
import json
from json import JSONDecodeError
from src import RAGError
from src.utils import print_log, print_rule, is_folder_exist, is_file_exist


class RetrieverEngine:
    def __init__(self, k: int, directories_list: dict[str, str]):
        self._k = k
        self.directories_list = directories_list
        self._load_database()

    def retrieve(self, query: str) -> list[dict[str, Any]]:
        # Tokenize the query
        query_token = bm25s.tokenize(query, show_progress=True, leave=False)

        # Retrieve the best match documents from the corpus
        indices, scores = self._retriever.retrieve(
            query_token,
            k=self._k,
            show_progress=True,
            leave_progress=False,
        )

        # Transform the ndarray into a single list
        top_k_indices = indices[0]
        top_k_scores = scores[0]

        # Add the content and score to the result of the retriever
        retrieve_chunk: list[dict[str, str]] = []
        for index, score in zip(top_k_indices, top_k_scores):
            # Find the correspond chunk in the database, copy its data
            try:
                chunk = self._chunks[index].copy()
            except IndexError:
                raise RAGError(
                    "Error while trying to find the index in the retriever. "
                    "Re-run the index command."
                )
            # Add the score
            chunk["score"] = float(score)
            # Add everything into the new dict
            retrieve_chunk.append(chunk)

        return retrieve_chunk

    # :-----------------:
    #   PRIVATE METHODS
    # :-----------------:

    def _load_database(self) -> None:
        # - SECURITY -
        chunk_db_file = os.path.join(
            self.directories_list["chunk_dir"], "chunks_db.json"
        )
        self._security_checker(chunk_db_file)

        # - Load the index folder with bm25 -
        print_rule("BM25 Database")
        print_log("Loading the BM25 database...")
        try:
            self._retriever = bm25s.BM25.load(
                self.directories_list["bm25_dir"], load_corpus=False
            )
        except FileNotFoundError as e:
            raise RAGError(f"{e}\nRe-run the index command.")
        print_log("✅ Done", "green")

        # - Load the chunks database -
        print_rule("Chunk Database")
        print_log("Loading the chunks database...")
        with open(chunk_db_file, "r") as f:
            try:
                self._chunks = json.load(f)
            except JSONDecodeError:
                raise RAGError("Error while trying to open 'chunk_db.json'")

        print_log("✅ Done", "green")
        print_rule()

    def _security_checker(self, chunk_db_file: str) -> None:
        # - BM25 Directory -
        # Check that the BM25 directory exist.
        if not is_folder_exist(self.directories_list["bm25_dir"]):
            raise RAGError(
                "BM25 indexing directory doesn't exist. Cannot launch the "
                "retriever.\nRun the index command first."
            )
        # Check that is not empty
        if len(os.listdir(self.directories_list["bm25_dir"])) == 0:
            raise RAGError("Cannot retrieve. The BM25 folder is empty.")

        # - Chunks Directory -
        # Check that the database exist
        if not is_file_exist(chunk_db_file):
            raise RAGError(
                "Chunk database doesn't exist.\nRun the index command first."
            )
        # Check that the file is not empty
        if os.path.getsize(chunk_db_file) == 0:
            raise RAGError("Chunk database is empty. Is everything ok?")
