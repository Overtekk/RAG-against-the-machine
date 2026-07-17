# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  RAG_engine.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/29 14:12:52 by roandrie        #+#    #+#               #
#  Updated: 2026/07/17 10:29:42 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pathlib
from src.utils import (
    is_folder_exist, is_file_exist, check_perm_can_read, check_perm_can_write,
    print_log, print_with_color, func_timer
)
from src.config import PathConfig, RAGConfig
from src.indexer import indexer, utils


LIST_DIRECTORY: dict[str, str] = {
    'vllm_dir': PathConfig.DEFAULT_VLLM_DIRECTORY,
    'index_dir': PathConfig.INDEX_DIRECTORY,
    'bm25_dir': PathConfig.INDEX_BM25_DIRECTORY,
    'chunk_dir': PathConfig.INDEX_CHUNKS_DIRECTORY
}


class RAGEngine():

    @func_timer
    def index(self, max_chunk_size: int = 2000) -> None:
        # - SECURITY -
        if not (RAGConfig.MIN_CHUNK_SIZE <= max_chunk_size
                    < RAGConfig.MAX_CHUNK_SIZE):
            raise ValueError(
                f"Provide a chunk size superior to {RAGConfig.MIN_CHUNK_SIZE} "
                f"and inferior to {RAGConfig.MAX_CHUNK_SIZE}"
            )

        vLLM_directory: str = PathConfig.DEFAULT_VLLM_DIRECTORY

        # - SECURITY -
        # If vLLM zip or folder do not exist. Stop the program here.
        if not is_file_exist(PathConfig.VLLM_ZIP):
            if not is_folder_exist(vLLM_directory):
                raise ValueError(
                    "vLLM zip or folder not found. Download it first and then"
                    "re-run the program.")

        # If folder not found, extract the archive. Otherwise, use the existing
        # folder.
        elif not is_folder_exist(vLLM_directory):
            utils.extract_archive(PathConfig.VLLM_ZIP)
        else:
            if not check_perm_can_read(vLLM_directory):
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

        print_with_color(
            "\nIngestion complete! Indices saved under "
            f"'{PathConfig.INDEX_DIRECTORY}'", 'green'
        )

    def search(self, query: str, k: int = 10,) -> None:
        # - SECURITY -
        if not (RAGConfig.MIN_N_CHUNKS <= k < RAGConfig.MAX_N_CHUNKS):
            raise ValueError(
                "Provide a number of chunks to get above "
                f"{RAGConfig.MIN_N_CHUNKS} and below {RAGConfig.MAX_N_CHUNKS}."
            )
        if not query and not isinstance(query, str):
            raise ValueError("Please, provide a valid question.")
        print(query)

    def search_dataset (
        self,
        dataset_path: str = PathConfig.DEFAULT_DATASET_PATH,
        k: int = 10,
        save_directory: str = PathConfig.DEFAULT_SAVE_DIRECTORY
    ) -> None:
        # Check paths
        _check_path(dataset_path)
        _check_path(save_directory, True)

    def answer(self, query: str, k: int = 10) -> None:
        pass

    def answer_dataset(
        self,
        student_search_results_path: str = (
            PathConfig.DEFAULT_STUDENT_SEARCH_RESULTS_PATH),
        save_directory: str = PathConfig.DEFAULT_SAVE_DIRECTORY
    ) -> None:
        # Check paths
        _check_path(student_search_results_path)
        _check_path(save_directory, True)

    def evaluate_student_search_results(
        self,
        student_answer_path: str = PathConfig.DEFAULT_STUDENT_ANSWER_PATH,
        dataset_path: str = PathConfig.DEFAULT_DATASET_PATH,
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
            if (not check_perm_can_read(path) and
                    not check_perm_can_write(path)):
                raise ValueError(f"Permission error for {path}")

    else:
        if not is_file_exist(path):
            path.touch()

        else:
            if (not check_perm_can_read(path) and
                    not check_perm_can_write(path)):
                raise ValueError(f"Permission error for {path}")
