# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  engine.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/29 14:12:52 by roandrie        #+#    #+#               #
#  Updated: 2026/07/03 11:54:53 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pathlib
from student.src.utils import (
    is_folder_exist, is_file_exist, can_read_file, can_write_to_file,
    print_log
)
from student.src.indexer import files, indexer


DEFAULT_DATASET_PATH : str = (
    'data/datasets/UnansweredQuestions/dataset_docs_public.json'
)
DEFAULT_STUDENT_ANSWER_PATH: str = (
    'data/output/search_results/dataset_docs_public.json'
)
DEFAULT_STUDENT_SEARCH_RESULTS_PATH: str = (
    'data/output/search_results/dataset_docs_public.json'
)

DEFAULT_SAVE_DIRECTORY: str = 'data/output/search_results'

DEFAULT_VLLM_DIRECTORY: str = 'vllm-0.10.1'
VLLM_ZIP: str = 'vllm-0.10.1.zip'

INDEX_DIRECTORY: str = 'data/processed/'
INDEX_BM25_DIRECTORY: str = 'data/processed/bm25_index'
INDEX_CHUNKS_DIRECTORY: str = 'data/processed/chunks'


class RAGEngine():

    def index(
        self,
        vLLM_directory: str = DEFAULT_VLLM_DIRECTORY,
        max_chunk_size: int = 2000
    ) -> None:
        # Check for the vLLM zip or directory
        if not is_file_exist(VLLM_ZIP):
            if not is_folder_exist(vLLM_directory):
                raise ValueError(
                    "vLLM zip or folder not found. Download it first and then"
                    "re-run the program.")

        elif not is_folder_exist(vLLM_directory):
            files.extract_archive(VLLM_ZIP)
        else:
            if not can_read_file(vLLM_directory):
                raise ValueError(
                    f"Error while trying to open {vLLM_directory}")

        # Check path for the processed data
        list_directory: dict[str, str] = {
            'index_dir': INDEX_DIRECTORY,
            'bm25_dir': INDEX_BM25_DIRECTORY,
            'chunk_dir': INDEX_CHUNKS_DIRECTORY
        }

        for dir in list_directory.values():
            _check_path(dir, True)

        indexer(vLLM_directory, max_chunk_size, list_directory)

        print_log(
            f"Ingestion complete! Indices saved under '{INDEX_DIRECTORY}'"
        )

    def answer(self, prompt: str, k: int = 10) -> None:
        pass

    def search_dataset(
        self,
        dataset_path: str = DEFAULT_DATASET_PATH,
        k: int = 10,
        save_directory: str = DEFAULT_SAVE_DIRECTORY
    ) -> None:
        # Check paths
        _check_path(dataset_path)
        _check_path(save_directory, True)

    def evaluate_student_search_results(
        self,
        student_answer_path: str = DEFAULT_STUDENT_ANSWER_PATH,
        dataset_path: str = DEFAULT_DATASET_PATH,
        k: int = 10,
        max_context_lenght: int = 2000
    ) -> None:
        # Check paths
        _check_path(student_answer_path)
        _check_path(dataset_path)

    def answer_dataset(
        self,
        student_search_results_path: str = DEFAULT_STUDENT_SEARCH_RESULTS_PATH,
        save_directory: str = DEFAULT_SAVE_DIRECTORY
    ) -> None:
        # Check paths
        _check_path(student_search_results_path)
        _check_path(save_directory, True)


# :--------------------:
#   PRIVATES FUNCTIONS
# :--------------------:


def _check_path(raw_path: str, is_directory: bool = False) -> None:
    path: pathlib.Path = pathlib.Path(raw_path)

    # Create the folders if they do not exist
    if path.parent:
        path.parent.mkdir(parents=True, exist_ok=True)

    if is_directory:
        if not is_folder_exist(path):
            path.mkdir()
        else:
            if not can_read_file(path) and not can_write_to_file(path):
                raise ValueError(f"Permission error for {path}")

    else:
        if not is_file_exist(path):
            path.touch()

        else:
            if not can_read_file(path) and not can_write_to_file(path):
                raise ValueError(f"Permission error for {path}")
