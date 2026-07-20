# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/15 10:29:07 by roandrie        #+#    #+#               #
#  Updated: 2026/07/20 11:18:57 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum, IntEnum


class PathConfig(str, Enum):
    DEFAULT_DATASET_PATH = "data/datasets/"
    DEFAULT_SAVE_DIRECTORY = "data/output/search_results/"
    DEFAULT_STUDENT_SEARCH_RESULTS_PATH = (
        "data/output/search_results/dataset_docs_public.json"
    )
    DEFAULT_STUDENT_ANSWER_PATH = (
        "data/output/search_results/dataset_docs_public.json"
    )
    DEFAULT_VLLM_DIRECTORY = "data/raw/"
    VLLM_ZIP = "vllm-0.10.1.zip"
    INDEX_DIRECTORY = "data/processed/"
    INDEX_BM25_DIRECTORY = "data/processed/bm25_index"
    INDEX_CHUNKS_DIRECTORY = "data/processed/chunks"

    def __str__(self) -> str:
        return self.value


class RAGConfig(IntEnum):
    MIN_CHUNK_SIZE = 0
    MAX_CHUNK_SIZE = 2000
    MIN_K_CHUNKS = 0
    MAX_K_CHUNKS = 1000


class RAGError(Exception):
    """Custom class for RAGEngine related error."""

    pass
