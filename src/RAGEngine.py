# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  RAGEngine.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/29 14:12:52 by roandrie        #+#    #+#               #
#  Updated: 2026/07/20 17:36:29 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pathlib import Path
from typing import Any
from src.utils import (
    is_folder_exist,
    is_file_exist,
    check_perm_can_read,
    check_perm_can_write,
    print_log,
    print_with_color,
    func_timer,
)
from src.config import PathConfig, RAGConfig, RAGError
from src.indexer import indexer, utils
from src.retriever import RetrieverEngine


LIST_DIRECTORY: dict[str, str] = {
    "vllm_dir": PathConfig.DEFAULT_VLLM_DIRECTORY,
    "index_dir": PathConfig.INDEX_DIRECTORY,
    "bm25_dir": PathConfig.INDEX_BM25_DIRECTORY,
    "chunk_dir": PathConfig.INDEX_CHUNKS_DIRECTORY,
}


class RAGEngine:
    @func_timer
    def index(self, max_chunk_size: int = 2000) -> None:
        # - SECURITY -
        try:
            _check_value_range(
                max_chunk_size,
                RAGConfig.MIN_CHUNK_SIZE,
                RAGConfig.MAX_CHUNK_SIZE,
                "max chunk size",
            )
        except RAGError as e:
            raise ValueError(e)

        vLLM_directory: str = PathConfig.DEFAULT_VLLM_DIRECTORY

        # - SECURITY -
        # If vLLM zip or folder do not exist. Stop the program here.
        if not is_file_exist(PathConfig.VLLM_ZIP):
            if not is_folder_exist(vLLM_directory):
                raise ValueError(
                    "vLLM zip or folder not found. Download it first and then"
                    "re-run the program."
                )

        # If folder not found, extract the archive. Otherwise, use the existing
        # folder.
        elif not is_folder_exist(vLLM_directory):
            utils.extract_archive(PathConfig.VLLM_ZIP)
        else:
            if not check_perm_can_read(vLLM_directory):
                raise ValueError(
                    f"Error while trying to open {vLLM_directory}"
                )

        # Check that folders doesn't exist. If not, create them.
        for dir in LIST_DIRECTORY.values():
            _check_path(dir, True)

        # Launch the indexer
        print_log(
            f"Starting the indexing with chunk size of {max_chunk_size}\n",
            "yellow",
        )
        nb_chunks = indexer(vLLM_directory, max_chunk_size, LIST_DIRECTORY)

        print_with_color(
            f"\nIngestion complete! Indexed {nb_chunks} chunks in "
            f"'{PathConfig.INDEX_CHUNKS_DIRECTORY}'.\nIndices saved under "
            f"'{PathConfig.INDEX_BM25_DIRECTORY}'",
            "green",
        )

    @func_timer
    def search(
        self,
        query: str,
        k: int = 10,
    ) -> None:
        # - SECURITY -
        try:
            _check_value_range(
                k,
                RAGConfig.MIN_K_CHUNKS,
                RAGConfig.MAX_K_CHUNKS,
                "number of results",
            )
        except RAGError as e:
            raise ValueError(e)
        if not query or not isinstance(query, str):
            raise ValueError("Please, provide a valid question.")

        # Init the retriever and retrieve the k best results
        try:
            retriever = RetrieverEngine(k, LIST_DIRECTORY)
            print_log(f"Searching the best {k} documents for '{query}'")
            result = retriever.retrieve(query)
        except RAGError as e:
            raise ValueError(e)

        print_log("✅ Done\n", "green")

        # Go throught the result and print the final results
        result_msg = ""
        for index in result:
            result_msg += (
                f"{index.file_path} [{index.first_character_index}:"
                f"{index.last_character_index}]\n"
            )
        print(result_msg)

    @func_timer
    def search_dataset(
        self,
        dataset_path: str = PathConfig.DEFAULT_DATASET_PATH,
        k: int = 10,
        save_directory: str = PathConfig.DEFAULT_SAVE_DIRECTORY,
    ) -> None:
        # - SECURITY -
        try:
            _check_value_range(
                k,
                RAGConfig.MIN_K_CHUNKS,
                RAGConfig.MAX_K_CHUNKS,
                "number of results",
            )
        except RAGError as e:
            raise ValueError(e)
        # Check path
        _check_path(save_directory, True)

        try:
            # Init the retriever
            retriever = RetrieverEngine(k, LIST_DIRECTORY)

            # Go throught the dataset path given
            path = Path(dataset_path)
            for file in (
                [path] if path.is_file() else list(path.rglob("*.json"))
            ):
                rag_dataset = retriever.create_dataset(file)
                if rag_dataset:
                    search_results = retriever.retrieve_dataset(rag_dataset)
                    retriever.save_retriever_result(
                        search_results, save_directory, file.name
                    )
        except RAGError as e:
            raise ValueError(e)

    @func_timer
    def answer(self, query: str, k: int = 10) -> None:
        pass

    @func_timer
    def answer_dataset(
        self,
        student_search_results_path: str = (
            PathConfig.DEFAULT_STUDENT_SEARCH_RESULTS_PATH
        ),
        save_directory: str = PathConfig.DEFAULT_SAVE_DIRECTORY,
    ) -> None:
        # Check paths
        _check_path(student_search_results_path)
        _check_path(save_directory, True)

    @func_timer
    def evaluate_student_search_results(
        self,
        student_answer_path: str = PathConfig.DEFAULT_STUDENT_ANSWER_PATH,
        dataset_path: str = PathConfig.DEFAULT_DATASET_PATH,
        k: int = 10,
        max_context_lenght: int = 2000,
    ) -> None:
        # Check paths
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
    path = Path(raw_path)

    # Create the folders if they do not exist
    if path.parent:
        path.parent.mkdir(parents=True, exist_ok=True)

    if is_directory:
        if not is_folder_exist(path):
            path.mkdir()
        else:
            if not check_perm_can_read(path) and not check_perm_can_write(
                path
            ):
                raise ValueError(f"Permission error for {path}")

    else:
        if not is_file_exist(path):
            path.touch()

        else:
            if not check_perm_can_read(path) and not check_perm_can_write(
                path
            ):
                raise ValueError(f"Permission error for {path}")


def _check_value_range(
    variable: Any, min: int, max: int, type_name: str
) -> None:
    """Check the range value of the variable.

    Args:
        variable (Any): variable to check.
        min (int): minimal value range.
        max (int): max value range.
        type_name (str): name of the variable (for clear error message).

    Raises:
        RAGError: if the variable is not a integer.
        RAGError: if the variable is outside range.
    """
    if not _check_if_int(variable):
        raise RAGError(f"Provide a valid number for {type_name}.")

    if not min < variable <= max:
        raise RAGError(
            f"Provide a {type_name} superior to {min} and inferior to {max}"
        )


def _check_if_int(variable: Any) -> bool:
    """Check if the provided value is of type int.

    Args:
        variable (Any): the variable to check.

    Returns:
        bool: False if not an int. True otherwise.
    """
    try:
        int(variable)
    except ValueError:
        return False
    return True
