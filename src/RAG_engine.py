# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  RAG_engine.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/29 14:12:52 by roandrie        #+#    #+#               #
#  Updated: 2026/07/15 11:47:23 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pathlib
from src.utils import (
    is_folder_exist, is_file_exist, can_read_file, can_write_to_file,
    print_log
)
from src.config import Config
from src.indexer import files, indexer


LIST_DIRECTORY: dict[str, str] = {
    'index_dir': Config.INDEX_DIRECTORY,
    'bm25_dir': Config.INDEX_BM25_DIRECTORY,
    'chunk_dir': Config.INDEX_CHUNKS_DIRECTORY
}


class RAGEngine():

    def index(self, max_chunk_size: int = 2000) -> None:
        # - SECURITY -
        if max_chunk_size <= 0:
            raise ValueError("Chunk size need to be superior than 0.")

        vLLM_directory: str = Config.DEFAULT_VLLM_DIRECTORY

        # - SECURITY -
        # If vLLM zip or folder do not exist. Stop the program here.
        if not is_file_exist(Config.VLLM_ZIP):
            if not is_folder_exist(vLLM_directory):
                raise ValueError(
                    "vLLM zip or folder not found. Download it first and then"
                    "re-run the program.")

        # If folder not found, extract the archive. Otherwise, use the existing
        # folder.
        elif not is_folder_exist(vLLM_directory):
            files.extract_archive(Config.VLLM_ZIP)
        else:
            if not can_read_file(vLLM_directory):
                raise ValueError(
                    f"Error while trying to open {vLLM_directory}")

        # Check that folders doesn't exist. If not, create them.
        for dir in LIST_DIRECTORY.values():
            _check_path(dir, True)

        # Launch the indexer
        print_log(
            f"Starting the indexing with chunk size of {max_chunk_size}\n",
            'yellow')
        indexer(vLLM_directory, max_chunk_size, LIST_DIRECTORY)

        print_log(
            "Ingestion complete! Indices saved under "
            f"'{Config.INDEX_DIRECTORY}'"
        )

    def search(self,k: int = 10,) -> None:
        pass

    def search_dataset (
        self,
        dataset_path: str = Config.DEFAULT_DATASET_PATH,
        k: int = 10,
        save_directory: str = Config.DEFAULT_SAVE_DIRECTORY
    ) -> None:
        # Check paths
        _check_path(dataset_path)
        _check_path(save_directory, True)

    def answer(self, prompt: str, k: int = 10) -> None:
        pass

    def answer_dataset(
        self,
        student_search_results_path: str = (
            Config.DEFAULT_STUDENT_SEARCH_RESULTS_PATH),
        save_directory: str = Config.DEFAULT_SAVE_DIRECTORY
    ) -> None:
        # Check paths
        _check_path(student_search_results_path)
        _check_path(save_directory, True)

    def evaluate_student_search_results(
        self,
        student_answer_path: str = Config.DEFAULT_STUDENT_ANSWER_PATH,
        dataset_path: str = Config.DEFAULT_DATASET_PATH,
        k: int = 10,
        max_context_lenght: int = 2000
    ) -> None:
        # Check paths
        _check_path(student_answer_path)
        _check_path(dataset_path)


# :--------------------:
#   PRIVATES FUNCTIONS
# :--------------------:


def _check_path(raw_path: str, is_directory: bool = False) -> None:
    """Path checker for a file or a folder.

    Take the raw path of transform it to a 'Path' object. Create the folders
    parents if they do not exist, then the file or the path. If one of these
    already exist, check for the permission.

    Args:
        raw_path (str): raw path of the folder or file.
        is_directory (bool, optional): If is a folder. Defaults to False.

    Raises:
        ValueError: If an error occurred with permissions.
    """
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
