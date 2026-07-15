# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  chunker.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/03 14:37:38 by roandrie        #+#    #+#               #
#  Updated: 2026/07/15 14:22:04 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from src.model import MinimalSource
from src.utils import check_file_extension, print_log


class ChunkerEngine():
    def __init__(self, chunk_size: int) -> None:
        self._chunk_size: int = chunk_size

    def process(
        self, file_path: str, content: str) -> list[tuple[MinimalSource, str]]:
        if check_file_extension(file_path, '.md'):
            return self._chunk_md_file(file_path, content)

        elif check_file_extension(file_path, '.py'):
            return self._chunk_py_file(file_path, content)

        else:
            print_log(f"Unkown file extension for {file_path}.", 'red')

    # :-----------------:
    #   PRIVATE METHODS
    # :-----------------:

    def _chunk_py_file(
        self, file_path: str, content: str) -> list[tuple[MinimalSource, str]]:
        python_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=self._chunk_size,
            chunk_overlap=0
        )

        return self._split_text(python_splitter, file_path, content)

    def _chunk_md_file(
        self, file_path: str, content: str) -> list[tuple[MinimalSource, str]]:
        # Split the text based on the chunk size. Keep all seperators
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._chunk_size,
            chunk_overlap=0,
            keep_separator=True
        )

        return self._split_text(text_splitter, file_path, content)

    def _split_text(
        self,
        text_splitter: RecursiveCharacterTextSplitter,
        file_path: str, content: str) -> list[tuple[MinimalSource, str]]:
        # Create the index and the list
        index: int = 0
        chunked_txt: list[tuple[MinimalSource, str]] = []

        # Split the text into small chunks
        for sub_txt in text_splitter.split_text(content):
            # Find the first index of the chunk
            sub_first_index = content.find(sub_txt, index)
            # Find the last index of the chunk
            sub_last_index = sub_first_index + len(sub_txt)
            # Update the index
            index = sub_last_index

            # Add the chunk to the list as MinimalSource
            chunked_txt.append((MinimalSource(
                file_path=file_path,
                first_character_index=sub_first_index,
                last_character_index=sub_last_index), sub_txt)
            )

        return chunked_txt

